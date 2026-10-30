#!/usr/bin/env python3
"""
generar_simulacro.py — Genera tests de práctica según BOE 2025.

Modos:
    global        Simulacro completo (80 test + 20 supuesto)
    solo-test     Solo la primera parte (80 preguntas)
    solo-supuesto Solo la segunda parte (20 preguntas de un supuesto)
    bloque        N preguntas de un bloque
    tema          N preguntas de un tema
    concepto      N preguntas de un concepto
    simular-nota  Verificar la fórmula de cálculo sin generar test

Uso:
    python generar_simulacro.py --tipo global --root ~/oposicion
    python generar_simulacro.py --tipo solo-test --root ~/oposicion
    python generar_simulacro.py --tipo simular-nota \
        --aciertos-test 55 --errores-test 10 \
        --aciertos-sup 15 --errores-sup 3
"""

import argparse
import json
import random
import sqlite3
import sys
from datetime import date, datetime
from pathlib import Path

# ============================================================
# CONSTANTES BOE 2025
# ============================================================

# Distribución típica del test general (80 preguntas)
CUOTAS_GLOBAL = {
    "bloque-i":   {"n": 25},  # 31 %
    "bloque-ii":  {"n": 12},  # 15 %
    "bloque-iii": {"n": 22},  # 28 %
    "bloque-iv":  {"n": 21},  # 26 %
}

# Valores por defecto (mínimo legal BOE)
PD_MIN_TEST = 24.0  # 30 % de 80
PD_MIN_SUP = 6.0    # 30 % de 20
PD_MAX_TEST = 80.0
PD_MAX_SUP = 20.0
CAL_MIN_APROBADO = 25.0
CAL_MAX = 50.0

# Dificultad
DIFICULTAD_PESO = {
    "baja":  0.30,
    "media": 0.50,
    "alta":  0.20,
}


def conectar(db_path: Path) -> sqlite3.Connection:
    if not db_path.exists():
        print(f"[error] No existe la BD: {db_path}")
        sys.exit(1)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def hoy_iso() -> str:
    return date.today().isoformat()


def timestamp_id() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


# ============================================================
# CÁLCULO DE CALIFICACIÓN (BOE 2025)
# ============================================================

def calcular_calificacion_boe2025(
    aciertos_test: int,
    errores_test: int,
    aciertos_sup: int | None,
    errores_sup: int | None,
    pd_min_test: float = PD_MIN_TEST,
    pd_min_sup: float = PD_MIN_SUP,
) -> dict:
    """
    Calcula la calificación según BOE 22/12/2025 (Núm. 306).

    Doble corte eliminatorio:
    - Si PD_test < pd_min_test → SUSPENDIDO, segunda NO evaluada
    - Si PD_sup < pd_min_sup → SUSPENDIDO (solo con cal_test)
    - Si ambas OK → cal_total = cal_test + cal_sup
    """
    # ============ PRIMERA PARTE ============
    pd_test = aciertos_test - (errores_test / 3)

    if pd_test < pd_min_test:
        return {
            "pd_test": round(pd_test, 2),
            "pd_sup": None,
            "cal_test": 0.0,
            "cal_sup": 0.0,
            "cal_total": 0.0,
            "aprobado": False,
            "motivo": f"No supera la 1ª parte (PD₁={pd_test:.2f} < {pd_min_test:.1f})",
            "segunda_evaluada": False,
        }

    cal_test = CAL_MIN_APROBADO + (
        (pd_test - pd_min_test) * (CAL_MAX - CAL_MIN_APROBADO)
        / (PD_MAX_TEST - pd_min_test)
    )
    cal_test = min(cal_test, CAL_MAX)

    # Si no se proporciona el supuesto, devolver solo el test
    if aciertos_sup is None or errores_sup is None:
        return {
            "pd_test": round(pd_test, 2),
            "pd_sup": None,
            "cal_test": round(cal_test, 2),
            "cal_sup": None,
            "cal_total": round(cal_test, 2),
            "aprobado": cal_test >= CAL_MIN_APROBADO,
            "motivo": "Solo se evaluó la primera parte",
            "segunda_evaluada": False,
        }

    # ============ SEGUNDA PARTE ============
    pd_sup = aciertos_sup - (errores_sup / 3)

    if pd_sup < pd_min_sup:
        return {
            "pd_test": round(pd_test, 2),
            "pd_sup": round(pd_sup, 2),
            "cal_test": round(cal_test, 2),
            "cal_sup": 0.0,
            "cal_total": round(cal_test, 2),
            "aprobado": False,
            "motivo": f"No supera la 2ª parte (PD₂={pd_sup:.2f} < {pd_min_sup:.1f})",
            "segunda_evaluada": True,
        }

    cal_sup = CAL_MIN_APROBADO + (
        (pd_sup - pd_min_sup) * (CAL_MAX - CAL_MIN_APROBADO)
        / (PD_MAX_SUP - pd_min_sup)
    )
    cal_sup = min(cal_sup, CAL_MAX)

    # ============ TOTAL ============
    cal_total = cal_test + cal_sup

    return {
        "pd_test": round(pd_test, 2),
        "pd_sup": round(pd_sup, 2),
        "cal_test": round(cal_test, 2),
        "cal_sup": round(cal_sup, 2),
        "cal_total": round(cal_total, 2),
        "aprobado": True,
        "motivo": "Supera ambas partes",
        "segunda_evaluada": True,
    }


def render_resultado_boe2025(
    resultado: dict,
    aciertos_t: int, errores_t: int,
    aciertos_s: int | None, errores_s: int | None,
) -> str:
    """Genera el informe en Markdown del simulacro."""
    lineas = []
    lineas.append("# Resultado del simulacro (BOE 2025)")
    lineas.append("")
    lineas.append(f"**Fecha**: {hoy_iso()}")
    lineas.append("")

    # --- Primera parte ---
    lineas.append("## Primera parte — Test general (80 preguntas)")
    lineas.append("")
    lineas.append("| Métrica | Valor |")
    lineas.append("|---|---|")
    lineas.append(f"| Aciertos | {aciertos_t} |")
    lineas.append(f"| Errores | {errores_t} |")
    lineas.append(f"| En blanco | {80 - aciertos_t - errores_t} |")
    lineas.append(f"| Puntuación directa | {resultado['pd_test']:.2f} / 80 |")
    lineas.append(f"| **Calificación** | **{resultado['cal_test']:.2f} / 50** |")
    lineas.append(f"| Mínimo para superar | 25 |")
    lineas.append("")

    if resultado["cal_test"] >= 25:
        lineas.append("✅ Primera parte **SUPERADA**")
    else:
        lineas.append("❌ Primera parte **NO superada**")
    lineas.append("")

    # --- Segunda parte ---
    if not resultado["segunda_evaluada"]:
        lineas.append("---")
        lineas.append("")
        lineas.append("## ⛔ Segunda parte NO EVALUADA")
        lineas.append("")
        lineas.append(f"**Motivo**: {resultado['motivo']}")
        lineas.append("")
        lineas.append("Según el BOE 2025, si no se supera la primera parte, "
                     "la segunda no se corrige.")
        return "\n".join(lineas)

    if aciertos_s is not None:
        lineas.append("---")
        lineas.append("")
        lineas.append("## Segunda parte — Supuesto práctico (20 preguntas)")
        lineas.append("")
        lineas.append("| Métrica | Valor |")
        lineas.append("|---|---|")
        lineas.append(f"| Aciertos | {aciertos_s} |")
        lineas.append(f"| Errores | {errores_s} |")
        lineas.append(f"| En blanco | {20 - aciertos_s - errores_s} |")
        lineas.append(f"| Puntuación directa | {resultado['pd_sup']:.2f} / 20 |")
        lineas.append(f"| **Calificación** | **{resultado['cal_sup']:.2f} / 50** |")
        lineas.append(f"| Mínimo para superar | 25 |")
        lineas.append("")

        if resultado["cal_sup"] >= 25:
            lineas.append("✅ Segunda parte **SUPERADA**")
        else:
            lineas.append("❌ Segunda parte **NO superada**")
        lineas.append("")

    # --- Resultado final ---
    lineas.append("---")
    lineas.append("")
    lineas.append("## Calificación final")
    lineas.append("")
    lineas.append(f"# {resultado['cal_total']:.2f} / 100")
    lineas.append("")

    if resultado["aprobado"]:
        lineas.append("## ✅ APROBADO")
    else:
        lineas.append("## ❌ SUSPENDIDO")
        lineas.append("")
        lineas.append(f"**Motivo**: {resultado['motivo']}")

    return "\n".join(lineas)


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
    excluir_ids = excluir_ids or set()

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
        if row["id"] in excluir_ids:
            continue
        candidatas.append({
            "id": row["id"],
            "enunciado": row["enunciado"],
            "opciones": json.loads(row["opciones"]) if row["opciones"] else [],
            "correcta": row["correcta"],
            "explicacion": row["explicacion"],
            "referencia": row["referencia"],
            "dificultad": row["dificultad"] or "media",
            "concepto_id": row["concepto_id"],
            "tema_id": row["tema_id"],
            "estado_srs": row["estado_srs"],
            "veces_fallada": row["veces_fallada"],
            "problematico": row["problematico"],
        })

    if not candidatas:
        return []

    # Priorización
    for c in candidatas:
        c["score"] = 0.0
        if priorizar_srs:
            if c["problematico"]:
                c["score"] += 10.0
            if c["estado_srs"] == "por-aprender":
                c["score"] += 5.0
            elif c["estado_srs"] == "en-progreso":
                c["score"] += 2.0
            elif c["estado_srs"] == "dominado":
                c["score"] -= 2.0
            c["score"] += c["veces_fallada"] * 0.5
        c["score"] += random.random()

    candidatas.sort(key=lambda x: x["score"], reverse=True)

    # Balanceo de dificultad
    n_baja = round(n * DIFICULTAD_PESO["baja"])
    n_media = round(n * DIFICULTAD_PESO["media"])
    n_alta = n - n_baja - n_media

    seleccionadas = []
    for diff, cuota in [("baja", n_baja), ("media", n_media), ("alta", n_alta)]:
        grupo = [c for c in candidatas if c["dificultad"] == diff]
        grupo_ord = sorted(grupo, key=lambda x: x["score"], reverse=True)
        seleccionadas.extend(grupo_ord[:cuota])

    ya_ids = {c["id"] for c in seleccionadas}
    if len(seleccionadas) < n:
        resto = [c for c in candidatas if c["id"] not in ya_ids]
        seleccionadas.extend(resto[:n - len(seleccionadas)])

    random.shuffle(seleccionadas)
    return seleccionadas[:n]


# ============================================================
# GENERACIÓN
# ============================================================

def generar_test_general(conn, n: int = 80) -> tuple[list[dict], dict]:
    """Genera las 80 preguntas del test general con cuotas por bloque."""
    preguntas = []
    ids_usados = set()
    cuotas = {}

    for bloque_id, cuota in CUOTAS_GLOBAL.items():
        p = seleccionar_para_bloque(conn, bloque_id, cuota["n"], ids_usados)
        ids_usados.update(x["id"] for x in p)
        preguntas.extend(p)
        cuotas[bloque_id] = len(p)

    return preguntas, cuotas


def guardar_test(conn, test_id, tipo, scope, preguntas, cuotas, origen):
    conn.execute("""
        INSERT INTO tests_practica (
            id, tipo, scope, fecha_generacion, n_preguntas, cuotas, origen
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        test_id, tipo, scope, hoy_iso(), len(preguntas),
        json.dumps(cuotas, ensure_ascii=False), origen,
    ))

    for i, p in enumerate(preguntas, 1):
        conn.execute("""
            INSERT INTO test_practica_preguntas (
                test_id, pregunta_id, numero
            ) VALUES (?, ?, ?)
        """, (test_id, p["id"], i))


def render_test_markdown(test_id, tipo, scope, preguntas, cuotas):
    lineas = []
    lineas.append(f"# Simulacro TAI — {test_id}")
    lineas.append("")
    lineas.append(f"**Tipo:** {tipo}")
    if scope:
        lineas.append(f"**Scope:** {scope}")
    lineas.append(f"**Fecha:** {hoy_iso()}")
    lineas.append(f"**Preguntas:** {len(preguntas)}")
    lineas.append(f"**Distribución:** {json.dumps(cuotas, ensure_ascii=False)}")
    lineas.append("")
    lineas.append("---")
    lineas.append("")

    letras = ["a", "b", "c", "d"]
    for i, p in enumerate(preguntas, 1):
        lineas.append(f"### Pregunta {i}")
        lineas.append("")
        lineas.append(p["enunciado"])
        lineas.append("")
        for j, op in enumerate(p["opciones"]):
            lineas.append(f"- **{letras[j]})** {op}")
        lineas.append("")

    lineas.append("---")
    lineas.append("")
    lineas.append("## Plantilla de respuestas")
    lineas.append("")
    lineas.append("```")
    for i, p in enumerate(preguntas, 1):
        letra = letras[p["correcta"]] if p["correcta"] < 4 else "?"
        lineas.append(f"{i:>3}. {letra}")
    lineas.append("```")

    return "\n".join(lineas)


# ============================================================
# COMANDO simular-nota (verificación sin datos)
# ============================================================

def cmd_simular_nota(args) -> int:
    """Simula el cálculo de nota sin generar test."""
    resultado = calcular_calificacion_boe2025(
        aciertos_test=args.aciertos_test,
        errores_test=args.errores_test,
        aciertos_sup=args.aciertos_sup,
        errores_sup=args.errores_sup,
    )

    print(f"[simular-nota] Entrada:")
    print(f"  Test:     {args.aciertos_test} aciertos, {args.errores_test} errores")
    if args.aciertos_sup is not None:
        print(f"  Supuesto: {args.aciertos_sup} aciertos, {args.errores_sup} errores")
    print()

    informe = render_resultado_boe2025(
        resultado,
        args.aciertos_test, args.errores_test,
        args.aciertos_sup, args.errores_sup,
    )
    print(informe)

    return 0 if resultado["aprobado"] else 1


# ============================================================
# COMANDO PRINCIPAL
# ============================================================

def cmd_generar(args) -> int:
    root = Path(args.root).expanduser().resolve()
    conn = conectar(root / "oposicion.db")

    try:
        test_id = f"test-{args.tipo}-{timestamp_id()}"
        preguntas = []
        cuotas = {}
        tipo_real = args.tipo

        if args.tipo in ("global", "solo-test"):
            preguntas, cuotas = generar_test_general(conn, args.n or 80)

        elif args.tipo == "bloque":
            if not args.scope:
                print("[error] --scope requerido para tipo 'bloque'")
                return 1
            preguntas = seleccionar_para_bloque(conn, args.scope, args.n or 25)
            cuotas = {args.scope: len(preguntas)}

        elif args.tipo == "tema":
            if not args.scope:
                print("[error] --scope requerido para tipo 'tema'")
                return 1
            cur = conn.execute(
                "SELECT bloque_id FROM temas WHERE id = ?", (args.scope,)
            )
            row = cur.fetchone()
            if not row:
                print(f"[error] Tema no existe: {args.scope}")
                return 1
            todas = seleccionar_para_bloque(conn, row[0], (args.n or 15) * 10)
            preguntas = [p for p in todas if p["tema_id"] == args.scope][:args.n or 15]
            cuotas = {args.scope: len(preguntas)}

        elif args.tipo == "concepto":
            if not args.scope:
                print("[error] --scope requerido para tipo 'concepto'")
                return 1
            cur = conn.execute("""
                SELECT p.id, p.enunciado, p.opciones, p.correcta, p.explicacion,
                       p.referencia, p.dificultad, p.concepto_id, p.tema_id
                FROM preguntas p
                WHERE p.concepto_id = ? AND p.verificado = 1
                ORDER BY RANDOM() LIMIT ?
            """, (args.scope, args.n or 5))
            for row in cur.fetchall():
                preguntas.append({
                    "id": row["id"],
                    "enunciado": row["enunciado"],
                    "opciones": json.loads(row["opciones"]) if row["opciones"] else [],
                    "correcta": row["correcta"],
                    "explicacion": row["explicacion"],
                    "referencia": row["referencia"],
                    "dificultad": row["dificultad"] or "media",
                    "concepto_id": row["concepto_id"],
                    "tema_id": row["tema_id"],
                })
            cuotas = {args.scope: len(preguntas)}

        else:
            print(f"[error] Tipo no válido: {args.tipo}")
            return 1

        if not preguntas:
            print(f"[error] No hay preguntas verificadas disponibles")
            print(f"        Tipo: {args.tipo}")
            if args.scope:
                print(f"        Scope: {args.scope}")
            print()
            print("💡 Si tienes temas ingestados pero no verificados:")
            print("   sqlite3 oposicion.db \"UPDATE preguntas SET verificado=1;\"")
            return 1

        # Guardar en BD
        guardar_test(conn, test_id, tipo_real, args.scope,
                     preguntas, cuotas, args.origen)
        conn.commit()

        # Markdown
        output_dir = Path(args.output).expanduser().resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        md_path = output_dir / f"{test_id}.md"
        md_path.write_text(
            render_test_markdown(test_id, tipo_real, args.scope, preguntas, cuotas),
            encoding="utf-8",
        )

        print(f"[generar] ✅ Test generado: {test_id}")
        print(f"[generar] Tipo: {tipo_real}")
        print(f"[generar] Preguntas: {len(preguntas)}")
        print(f"[generar] Distribución: {json.dumps(cuotas, ensure_ascii=False)}")
        print(f"[generar] Markdown: {md_path}")

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
        description="Generar simulacros TAI según BOE 2025"
    )
    parser.add_argument("--root", default="~/oposicion")
    parser.add_argument("--tipo", required=True,
                        choices=["global", "solo-test", "solo-supuesto",
                                 "bloque", "tema", "concepto", "simular-nota"])
    parser.add_argument("--scope", help="bloque-iii, tema-15-..., c-concepto")
    parser.add_argument("--n", type=int)
    parser.add_argument("--output", default="~/oposicion/tests")
    parser.add_argument("--origen", default="manual")

    # Argumentos para simular-nota
    parser.add_argument("--aciertos-test", type=int, default=0)
    parser.add_argument("--errores-test", type=int, default=0)
    parser.add_argument("--aciertos-sup", type=int)
    parser.add_argument("--errores-sup", type=int)

    args = parser.parse_args()

    if args.tipo == "simular-nota":
        return cmd_simular_nota(args)
    return cmd_generar(args)


if __name__ == "__main__":
    sys.exit(main())
