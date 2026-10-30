#!/usr/bin/env python3
"""
generar_simulacro.py — Genera tests de práctica para TAI Oposición.

Tipos:
    global    80 preguntas con cuotas por bloque (réplica del examen real)
    bloque    N preguntas de un bloque concreto
    tema      N preguntas de un tema
    concepto  N preguntas del mismo concepto (refuerzo)

Uso:
    python generar_simulacro.py --tipo global --root ~/oposicion
    python generar_simulacro.py --tipo bloque --scope bloque-iii --n 25
    python generar_simulacro.py --tipo tema --scope tema-15-modelado-de-datos
    python generar_simulacro.py --tipo concepto --scope c-plazo-resolucion
"""

import argparse
import json
import random
import sqlite3
import sys
from datetime import date, datetime
from pathlib import Path

# ============================================================
# CUOTAS DEL SIMULACRO GLOBAL
# Réplica del examen real TAI (verificado con 2024/2025)
# ============================================================

# Cuotas basadas en el examen real TAI 2026 (80 preguntas):
#   Bloque I:  9 temas → ~25 preguntas (31%)
#   Bloque II: 5 temas → ~12 preguntas (15%)
#   Bloque III: 9 temas → ~22 preguntas (28%)
#   Bloque IV: 10 temas → ~21 preguntas (26%)
CUOTAS_GLOBAL = {
    "bloque-i":   {"n": 25},
    "bloque-ii":  {"n": 12},
    "bloque-iii": {"n": 22},
    "bloque-iv":  {"n": 21},
}

# Distribución de dificultad (30 % baja, 50 % media, 20 % alta)
DIFICULTAD_PESO = {
    "baja":  0.30,
    "media": 0.50,
    "alta":  0.20,
}


# ============================================================
# UTILIDADES
# ============================================================

def conectar(db_path: Path) -> sqlite3.Connection:
    if not db_path.exists():
        print(f"[error] No existe la BD: {db_path}")
        print(f"        Ejecuta primero: python bin/db.py init")
        sys.exit(1)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def hoy_iso() -> str:
    return date.today().isoformat()


def timestamp_id() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


# ============================================================
# SELECCIÓN DE PREGUNTAS
# ============================================================

def seleccionar_para_bloque(
    conn: sqlite3.Connection,
    bloque_id: str,
    n: int,
    excluir_ids: set[str] | None = None,
    priorizar_srs: bool = True,
) -> list[dict]:
    """
    Selecciona n preguntas de un bloque con priorización SRS + dificultad.
    """
    excluir_ids = excluir_ids or set()

    # 1. Preguntas candidatas del bloque
    cur = conn.execute("""
        SELECT
            p.id, p.enunciado, p.opciones, p.correcta, p.explicacion,
            p.referencia, p.dificultad, p.concepto_id, p.tema_id,
            COALESCE(s.estado, 'nuevo') AS estado_srs,
            COALESCE(s.veces_fallada, 0) AS veces_fallada,
            COALESCE(s.problematico, 0) AS problematico
        FROM preguntas p
        JOIN temas t ON t.id = p.tema_id
        LEFT JOIN srs_items s
            ON s.item_key = 'test:' || p.tema_id || ':' || p.id
        WHERE t.bloque_id = ?
          AND p.verificado = 1
    """, (bloque_id,))

    candidatas = []
    for row in cur.fetchall():
        if row[0] in excluir_ids:
            continue
        candidatas.append({
            "id": row[0],
            "enunciado": row[1],
            "opciones": json.loads(row[2]) if row[2] else [],
            "correcta": row[3],
            "explicacion": row[4],
            "referencia": row[5],
            "dificultad": row[6] or "media",
            "concepto_id": row[7],
            "tema_id": row[8],
            "estado_srs": row[9],
            "veces_fallada": row[10],
            "problematico": row[11],
        })

    if not candidatas:
        return []

    # 2. Aplicar priorización
    for c in candidatas:
        c["score"] = 0.0

        if priorizar_srs:
            # Refuerzo: ítems problemáticos y por-aprender primero
            if c["problematico"]:
                c["score"] += 10.0
            if c["estado_srs"] == "por-aprender":
                c["score"] += 5.0
            elif c["estado_srs"] == "en-progreso":
                c["score"] += 2.0
            elif c["estado_srs"] == "dominado":
                c["score"] -= 2.0
            # Factor de fallos (más fallos → más prioridad)
            c["score"] += c["veces_fallada"] * 0.5

        # Aleatoriedad para no repetir siempre las mismas
        c["score"] += random.random()

    # 3. Ordenar por score descendente
    candidatas.sort(key=lambda x: x["score"], reverse=True)

    # 4. Balanceo de dificultad (30/50/20)
    n_baja = round(n * DIFICULTAD_PESO["baja"])
    n_media = round(n * DIFICULTAD_PESO["media"])
    n_alta = n - n_baja - n_media

    seleccionadas = []
    for diff, cuota in [("baja", n_baja), ("media", n_media), ("alta", n_alta)]:
        grupo = [c for c in candidatas if c["dificultad"] == diff]
        grupo_ordenado = sorted(grupo, key=lambda x: x["score"], reverse=True)
        seleccionadas.extend(grupo_ordenado[:cuota])

    # 5. Completar si faltan (rellenar con el resto)
    ya_ids = {c["id"] for c in seleccionadas}
    if len(seleccionadas) < n:
        resto = [c for c in candidatas if c["id"] not in ya_ids]
        faltan = n - len(seleccionadas)
        seleccionadas.extend(resto[:faltan])

    # 6. Mezclar el orden final
    random.shuffle(seleccionadas)

    return seleccionadas[:n]


def seleccionar_para_tema(
    conn: sqlite3.Connection,
    tema_id: str,
    n: int,
    excluir_ids: set[str] | None = None,
) -> list[dict]:
    """Selecciona n preguntas de un tema."""
    cur = conn.execute(
        "SELECT bloque_id FROM temas WHERE id = ?", (tema_id,)
    )
    row = cur.fetchone()
    if not row:
        return []

    # Reutilizamos seleccionar_para_bloque y filtramos por tema
    bloque_id = row[0]
    todas = seleccionar_para_bloque(
        conn, bloque_id, n * 10, excluir_ids, priorizar_srs=True
    )
    del_tema = [p for p in todas if p["tema_id"] == tema_id]
    return del_tema[:n]


def seleccionar_para_concepto(
    conn: sqlite3.Connection,
    concepto_id: str,
    n: int,
) -> list[dict]:
    """Selecciona n preguntas del mismo concepto."""
    cur = conn.execute("""
        SELECT
            p.id, p.enunciado, p.opciones, p.correcta, p.explicacion,
            p.referencia, p.dificultad, p.concepto_id, p.tema_id
        FROM preguntas p
        WHERE p.concepto_id = ?
          AND p.verificado = 1
        ORDER BY RANDOM()
        LIMIT ?
    """, (concepto_id, n))

    return [
        {
            "id": row[0],
            "enunciado": row[1],
            "opciones": json.loads(row[2]) if row[2] else [],
            "correcta": row[3],
            "explicacion": row[4],
            "referencia": row[5],
            "dificultad": row[6] or "media",
            "concepto_id": row[7],
            "tema_id": row[8],
        }
        for row in cur.fetchall()
    ]


# ============================================================
# GENERACIÓN
# ============================================================

def generar_simulacro_global(
    conn: sqlite3.Connection, n_total: int = 80
) -> tuple[list[dict], dict]:
    """Genera un simulacro global con cuotas por bloque."""
    preguntas = []
    ids_usados = set()
    cuotas_aplicadas = {}

    for bloque_id, cuota in CUOTAS_GLOBAL.items():
        n_bloque = cuota["n"]
        p = seleccionar_para_bloque(conn, bloque_id, n_bloque, ids_usados)
        ids_usados.update(x["id"] for x in p)
        preguntas.extend(p)
        cuotas_aplicadas[bloque_id] = len(p)

    return preguntas, cuotas_aplicadas


def generar_simulacro_bloque(
    conn: sqlite3.Connection, bloque_id: str, n: int
) -> tuple[list[dict], dict]:
    preguntas = seleccionar_para_bloque(conn, bloque_id, n)
    return preguntas, {bloque_id: len(preguntas)}


# ============================================================
# GUARDAR
# ============================================================

def guardar_test(
    conn: sqlite3.Connection,
    test_id: str,
    tipo: str,
    scope: str | None,
    preguntas: list[dict],
    cuotas: dict,
    origen: str,
) -> None:
    """Guarda el test en la BD."""
    cuotas_json = json.dumps(cuotas, ensure_ascii=False)

    conn.execute("""
        INSERT INTO tests_practica (
            id, tipo, scope, fecha_generacion, n_preguntas, cuotas, origen
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        test_id, tipo, scope, hoy_iso(), len(preguntas), cuotas_json, origen,
    ))

    for i, p in enumerate(preguntas, 1):
        conn.execute("""
            INSERT INTO test_practica_preguntas (
                test_id, pregunta_id, numero
            ) VALUES (?, ?, ?)
        """, (test_id, p["id"], i))


def render_markdown(
    test_id: str, tipo: str, scope: str | None,
    preguntas: list[dict], cuotas: dict,
) -> str:
    """Renderiza el test en Markdown imprimible."""
    lineas = []

    # Cabecera
    lineas.append(f"# Simulacro TAI — {test_id}")
    lineas.append("")
    lineas.append(f"**Tipo:** {tipo}")
    if scope:
        lineas.append(f"**Scope:** {scope}")
    lineas.append(f"**Fecha:** {hoy_iso()}")
    lineas.append(f"**Preguntas:** {len(preguntas)}")
    lineas.append(f"**Distribución:** {json.dumps(cuotas, ensure_ascii=False)}")
    lineas.append("")
    lineas.append("**Instrucciones:** Marca la opción correcta en la plantilla de respuestas al final.")
    lineas.append("")
    lineas.append("---")
    lineas.append("")

    # Preguntas
    for i, p in enumerate(preguntas, 1):
        lineas.append(f"### Pregunta {i}")
        lineas.append("")
        lineas.append(p["enunciado"])
        lineas.append("")

        letras = ["a", "b", "c", "d"]
        for j, opcion in enumerate(p["opciones"]):
            letra = letras[j] if j < len(letras) else "?"
            lineas.append(f"- **{letra})** {opcion}")

        lineas.append("")

    # Plantilla de respuestas
    lineas.append("---")
    lineas.append("")
    lineas.append("## Plantilla de respuestas")
    lineas.append("")
    lineas.append("```")
    for i, p in enumerate(preguntas, 1):
        letra = letras[p["correcta"]] if p["correcta"] < 4 else "?"
        lineas.append(f"{i:>3}. {letra}")
    lineas.append("```")
    lineas.append("")

    # Referencias (al final, para autoevaluación)
    lineas.append("## Soluciones detalladas")
    lineas.append("")
    for i, p in enumerate(preguntas, 1):
        letra = letras[p["correcta"]] if p["correcta"] < 4 else "?"
        lineas.append(f"**{i}.** {letra}) {p['opciones'][p['correcta']]}")
        if p.get("explicacion"):
            lineas.append(f"  - *Explicación:* {p['explicacion']}")
        if p.get("referencia"):
            lineas.append(f"  - *Referencia:* {p['referencia']}")
        lineas.append("")

    return "\n".join(lineas)


# ============================================================
# COMANDO PRINCIPAL
# ============================================================

def cmd_generar(args) -> int:
    root = Path(args.root).expanduser().resolve()
    conn = conectar(root / "oposicion.db")

    try:
        test_id = f"test-{args.tipo}-{timestamp_id()}"

        # 1. Seleccionar preguntas según tipo
        if args.tipo == "global":
            preguntas, cuotas = generar_simulacro_global(conn, args.n or 80)

        elif args.tipo == "bloque":
            if not args.scope:
                print("[error] --scope requerido para tipo 'bloque'")
                return 1
            preguntas, cuotas = generar_simulacro_bloque(
                conn, args.scope, args.n or 25
            )

        elif args.tipo == "tema":
            if not args.scope:
                print("[error] --scope requerido para tipo 'tema'")
                return 1
            preguntas = seleccionar_para_tema(conn, args.scope, args.n or 15)
            cuotas = {args.scope: len(preguntas)}

        elif args.tipo == "concepto":
            if not args.scope:
                print("[error] --scope requerido para tipo 'concepto'")
                return 1
            preguntas = seleccionar_para_concepto(conn, args.scope, args.n or 5)
            cuotas = {args.scope: len(preguntas)}

        else:
            print(f"[error] Tipo no válido: {args.tipo}")
            return 1

        if not preguntas:
            print(f"[error] No hay preguntas verificadas disponibles")
            print(f"        Tipo: {args.tipo}")
            if args.scope:
                print(f"        Scope: {args.scope}")
            return 1

        # 2. Guardar en BD
        guardar_test(conn, test_id, args.tipo, args.scope,
                     preguntas, cuotas, args.origen)
        conn.commit()

        # 3. Renderizar Markdown
        output_dir = Path(args.output).expanduser().resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        md_path = output_dir / f"{test_id}.md"
        md_path.write_text(
            render_markdown(test_id, args.tipo, args.scope, preguntas, cuotas),
            encoding="utf-8",
        )

        # 4. Salida resumen
        print(f"[generar] ✅ Test generado: {test_id}")
        print(f"[generar] Tipo: {args.tipo}")
        if args.scope:
            print(f"[generar] Scope: {args.scope}")
        print(f"[generar] Preguntas: {len(preguntas)}")
        print(f"[generar] Distribución: {json.dumps(cuotas, ensure_ascii=False)}")
        print(f"[generar] Markdown: {md_path}")
        print()

        # Stats rápidas
        por_bloque = {}
        for p in preguntas:
            bloque = conn.execute(
                "SELECT bloque_id FROM temas WHERE id = ?",
                (p["tema_id"],)
            ).fetchone()
            if bloque:
                por_bloque[bloque[0]] = por_bloque.get(bloque[0], 0) + 1

        print("[generar] Composición real:")
        for bloque, n in sorted(por_bloque.items()):
            print(f"  {bloque}: {n} preguntas")

        return 0

    except Exception as e:
        conn.rollback()
        print(f"[error] {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        conn.close()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generar simulacros y tests de práctica"
    )
    parser.add_argument("--root", default="~/oposicion")
    parser.add_argument("--tipo", required=True,
                        choices=["global", "bloque", "tema", "concepto"])
    parser.add_argument("--scope",
                        help="bloque-iii, tema-15-..., c-concepto")
    parser.add_argument("--n", type=int,
                        help="Número de preguntas (default según tipo)")
    parser.add_argument("--output", default="~/oposicion/tests",
                        help="Carpeta para el Markdown")
    parser.add_argument("--origen", default="manual",
                        choices=["manual", "srs-sugerido", "simulacro"],
                        help="Origen del test")

    args = parser.parse_args()
    return cmd_generar(args)


if __name__ == "__main__":
    sys.exit(main())