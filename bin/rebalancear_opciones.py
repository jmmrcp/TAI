#!/usr/bin/env python3
"""
rebalancear_opciones.py — Corrige el sesgo de opciones SOLO en las preguntas
generadas automáticamente por el LLM (Fase 0), NO en las de exámenes oficiales.

Criterio por defecto:
  - Rebalancear: origen IS NULL o origen = 'ingesta-inicial' o 'ampliacion' o 'manual'
  - Excluir:     origen = 'examen-oficial' o preguntas vinculadas a examen_preguntas

Uso:
    python rebalancear_opciones.py --root ~/oposicion --dry-run
    python rebalancear_opciones.py --root ~/oposicion --tema tema-01-...
    python rebalancear_opciones.py --root ~/oposicion --incluir-examenes
"""
import argparse
import json
import random
import sqlite3
import sys
from pathlib import Path


def conectar(db_path: Path) -> sqlite3.Connection:
    if not db_path.exists():
        print(f"[error] No existe la BD: {db_path}")
        sys.exit(1)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def construir_filtro(args) -> tuple[str, list]:
    """
    Devuelve (where_sql, params) para seleccionar solo las preguntas
    que DEBEN rebalancearse (excluyendo las de exámenes oficiales).
    """
    condiciones = ["p.verificado = 1"]
    params = []

    if args.tema:
        condiciones.append("p.tema_id = ?")
        params.append(args.tema)

    if not args.incluir_examenes:
        condiciones.append("""
            p.id NOT IN (
                SELECT pregunta_id FROM examen_preguntas
            )
        """)
        condiciones.append("p.id NOT LIKE 'pendiente-supuesto-%'")
        condiciones.append("""
            COALESCE(p.origen, 'manual') NOT IN ('examen-oficial')
        """)

    where_sql = " AND ".join(condiciones)
    return where_sql, params


def rebalancear_pregunta(opciones: list, correcta_idx: int) -> tuple[list, int]:
    """Baraja opciones preservando la correcta."""
    if not opciones or correcta_idx < 0 or correcta_idx >= len(opciones):
        raise ValueError(f"Índice inválido: {correcta_idx} para {len(opciones)} opciones")

    pares = [(op, i == correcta_idx) for i, op in enumerate(opciones)]
    random.shuffle(pares)

    nuevas_opciones = [p[0] for p in pares]
    nuevo_idx = next(i for i, p in enumerate(pares) if p[1])

    return nuevas_opciones, nuevo_idx


def mostrar_distribucion(conn: sqlite3.Connection, where_sql: str, params: list, titulo: str):
    """Muestra la distribución de respuestas correctas."""
    print(f"[rebalancear] {titulo}:")
    cur = conn.execute(f"""
        SELECT p.correcta, COUNT(*) AS n
        FROM preguntas p
        WHERE {where_sql}
        GROUP BY p.correcta
        ORDER BY p.correcta
    """, params)
    dist = {r["correcta"]: r["n"] for r in cur.fetchall()}
    total = sum(dist.values())

    if total == 0:
        print("  (no hay preguntas con este filtro)")
        return

    for idx in range(4):
        n = dist.get(idx, 0)
        letra = "abcd"[idx]
        pct = (n * 100 / total) if total > 0 else 0
        barra = "█" * int(pct / 5)
        print(f"  {letra}: {n:4d} ({pct:5.1f}%) {barra}")
    print(f"  Total: {total}")


def detectar_duplicados(conn: sqlite3.Connection, where_sql: str, params: list) -> list:
    """Encuentra grupos de preguntas con la misma respuesta correcta y concepto similar."""
    cur = conn.execute(f"""
        SELECT p.id, p.enunciado, p.opciones, p.correcta, p.concepto_id
        FROM preguntas p
        WHERE {where_sql}
        ORDER BY p.concepto_id, p.id
    """, params)

    grupos = {}
    for row in cur.fetchall():
        opciones = json.loads(row["opciones"]) if row["opciones"] else []
        if not opciones or row["correcta"] >= len(opciones):
            continue
        respuesta = opciones[row["correcta"]].strip().lower()

        enunciado_norm = row["enunciado"].lower().strip()
        for prefijo in ["según el art.", "¿qué ", "el art.", "indique ", "señale "]:
            if enunciado_norm.startswith(prefijo):
                enunciado_norm = enunciado_norm[len(prefijo):]

        clave = (row["concepto_id"] or "sin-concepto", respuesta)
        grupos.setdefault(clave, []).append({
            "id": row["id"],
            "enunciado": row["enunciado"],
            "respuesta": opciones[row["correcta"]],
        })

    return [(k, v) for k, v in grupos.items() if len(v) > 1]


def cmd_rebalancear(args) -> int:
    root = Path(args.root).expanduser().resolve()
    conn = conectar(root / "oposicion.db")

    try:
        where_sql, params = construir_filtro(args)

        print(f"[rebalancear] Modo: {'INCLUYE exámenes' if args.incluir_examenes else 'EXCLUYE exámenes'}")
        if args.tema:
            print(f"[rebalancear] Tema: {args.tema}")
        print()

        mostrar_distribucion(conn, where_sql, params, "Distribución ANTES")
        print()

        cur = conn.execute("SELECT COUNT(*) FROM preguntas WHERE verificado = 1")
        total_global = cur.fetchone()[0]
        cur = conn.execute(f"SELECT COUNT(*) FROM preguntas p WHERE {where_sql}", params)
        total_filtrado = cur.fetchone()[0]
        print(f"[rebalancear] Total verificadas en BD: {total_global}")
        print(f"[rebalancear] A rebalancear: {total_filtrado}")
        print(f"[rebalancear] Excluidas (exámenes): {total_global - total_filtrado}")
        print()

        duplicados = detectar_duplicados(conn, where_sql, params)
        print(f"[rebalancear] Grupos duplicados detectados: {len(duplicados)}")
        for clave, grupo in duplicados[:5]:
            concepto, respuesta = clave
            print(f"  ⚠️  '{respuesta[:60]}'")
            for p in grupo:
                print(f"      - {p['id']}: {p['enunciado'][:70]}")
        if len(duplicados) > 5:
            print(f"  ... y {len(duplicados) - 5} grupos más")
        print()

        print("[rebalancear] Barajando opciones...")
        cur = conn.execute(f"""
            SELECT p.id, p.opciones, p.correcta
            FROM preguntas p
            WHERE {where_sql}
        """, params)

        actualizadas = 0
        errores = 0
        for row in cur.fetchall():
            try:
                opciones = json.loads(row["opciones"]) if row["opciones"] else []
                if len(opciones) < 2:
                    errores += 1
                    continue

                nuevas, nuevo_idx = rebalancear_pregunta(opciones, row["correcta"])

                if nuevo_idx != row["correcta"] or args.forzar:
                    if not args.dry_run:
                        conn.execute("""
                            UPDATE preguntas SET opciones = ?, correcta = ? WHERE id = ?
                        """, (
                            json.dumps(nuevas, ensure_ascii=False),
                            nuevo_idx,
                            row["id"],
                        ))
                    actualizadas += 1
            except Exception as e:
                errores += 1
                if args.verbose:
                    print(f"  [error] {row['id']}: {e}")

        if not args.dry_run:
            conn.commit()

        print(f"  Actualizadas: {actualizadas}")
        print(f"  Errores: {errores}")
        print()

        if not args.dry_run:
            mostrar_distribucion(conn, where_sql, params, "Distribución DESPUÉS")
            print()

            if duplicados:
                dup_file = root / "duplicados-tema-generado.json"
                with dup_file.open("w", encoding="utf-8") as f:
                    json.dump([
                        {"clave": list(k), "grupo": v}
                        for k, v in duplicados
                    ], f, ensure_ascii=False, indent=2)
                print(f"💡 Duplicados exportados a: {dup_file}")
                print("   Revisa manualmente y elimina los que sobren.")

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
        description="Rebalancea SOLO las preguntas generadas, respetando las de exámenes"
    )
    parser.add_argument("--root", default="~/oposicion")
    parser.add_argument("--tema", help="Solo este tema")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--forzar", action="store_true",
                        help="Re-barajar incluso si el índice no cambia")
    parser.add_argument("--incluir-examenes", action="store_true",
                        help="NO recomendado: también rebalancea las preguntas de exámenes oficiales")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()
    return cmd_rebalancear(args)


if __name__ == "__main__":
    sys.exit(main())
