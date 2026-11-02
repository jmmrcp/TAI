#!/usr/bin/env python3
"""
ingesta_examen.py — Importa exámenes oficiales con plantilla de respuestas.

Uso:
    python ingesta_examen.py --examen-json examen-2025.json \
        --respuestas respuestas-2025.json \
        --root ~/oposicion

Formato del JSON del examen (entrada):
{
  "id": "examen-tai-2025-modelo-a",
  "anio": 2025,
  "convocatoria": "2025",
  "modelo": "A",
  "tipo": "tai",
  "fecha": "2025-11-15",
  "total_teoricas": 80,
  "total_reserva": 20,
  "n_supuestos": 2,
  "preguntas_teoricas": [
    {
      "numero": 1,
      "enunciado": "...",
      "opciones": ["...", "...", "...", "..."],
      "concepto_id": "plazo-resolucion-3-meses",  (opcional)
      "tema_id": "tema-09-ley39"                   (opcional)
    }
  ],
  "preguntas_reserva": [...],
  "supuestos": [
    {
      "id": "supuesto-1",
      "titulo": "...",
      "bloque_id": "bloque-iii",
      "preguntas": [...]
    }
  ]
}

Formato del JSON de respuestas:
{
  "teoricas": {"1": "a", "2": "b", ...},
  "reserva": {"1": "c", "2": "d", ...},
  "supuestos": {
    "supuesto-1": {"1": "b", "2": "a", ...}
  }
}
"""

import argparse
import hashlib
import json
import sqlite3
import sys
import unicodedata
import re
from datetime import date
from pathlib import Path


def conectar(db_path: Path) -> sqlite3.Connection:
    if not db_path.exists():
        print(f"[error] No existe la BD: {db_path}")
        sys.exit(1)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def normalizar_texto(texto: str) -> str:
    if not texto:
        return ""
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("ascii")
    texto = texto.lower()
    texto = re.sub(r"[^a-z0-9\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


def sha256_exacto(*partes) -> str:
    texto = "||".join(str(p) for p in partes)
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def similitud_jaccard(a: str, b: str) -> float:
    tokens_a = set(normalizar_texto(a).split())
    tokens_b = set(normalizar_texto(b).split())
    if not tokens_a or not tokens_b:
        return 0.0
    return len(tokens_a & tokens_b) / len(tokens_a | tokens_b)


def buscar_pregunta_existente(
    conn: sqlite3.Connection,
    enunciado: str,
    opciones: list[str],
    concepto_id: str | None,
) -> tuple[str | None, str]:
    """
    Busca una pregunta en el banco.
    Devuelve (id_existente, motivo) o (None, 'pendiente').
    """
    # 1. Hash exacto
    h_exacto = sha256_exacto(enunciado, *opciones)
    cur = conn.execute(
        "SELECT id FROM preguntas WHERE hash_exacto = ?", (h_exacto,)
    )
    row = cur.fetchone()
    if row:
        return row[0], "exacta"

    # 2. Mismo concepto + similitud
    if concepto_id:
        cur = conn.execute("""
            SELECT id, enunciado FROM preguntas
            WHERE concepto_id = ?
        """, (concepto_id,))
        for pid, penun in cur.fetchall():
            if similitud_jaccard(enunciado, penun) > 0.85:
                return pid, "conceptual"

    # 3. Fallback: buscar por similitud global (solo si hay concepto_id)
    # Para no ralentizar demasiado, esto se omite

    return None, "pendiente"


LETRA_A_INDICE = {'a': 0, 'b': 1, 'c': 2, 'd': 3}


def importar_examen(conn: sqlite3.Connection, examen: dict,
                    respuestas: dict) -> dict:
    """Importa un examen completo a SQLite."""
    stats = {
        "examen_id": examen["id"],
        "preguntas_teoricas": 0,
        "preguntas_reserva": 0,
        "vinculadas": 0,
        "pendientes": 0,
        "supuestos": 0,
        "errores": [],
    }

    # 1. Insertar examen
    conn.execute("""
        INSERT OR REPLACE INTO examenes (
            id, anio, convocatoria, modelo, tipo, fecha,
            total_teoricas, total_reserva, n_supuestos, verificado
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        examen["id"],
        examen.get("anio"),
        examen.get("convocatoria"),
        examen.get("modelo"),
        examen.get("tipo", "tai"),
        examen.get("fecha"),
        examen.get("total_teoricas"),
        examen.get("total_reserva", 0),
        examen.get("n_supuestos", 0),
        1,
    ))

    # 2. Procesar preguntas teóricas
    for p in examen.get("preguntas_teoricas", []):
        numero = p["numero"]
        enunciado = p["enunciado"]
        opciones = p["opciones"]
        concepto_id = p.get("concepto_id")
        tema_id = p.get("tema_id")

        # Buscar en el banco
        pid, motivo = buscar_pregunta_existente(
            conn, enunciado, opciones, concepto_id
        )

        if not pid:
            # Crear huérfana
            pid = f"pendiente-{examen['id']}-t{numero:02d}"
            conn.execute("""
                INSERT OR IGNORE INTO preguntas (
                    id, tema_id, concepto_id, enunciado, opciones,
                    correcta, verificado, fecha_alta
                ) VALUES (?, ?, ?, ?, ?, 0, 0, ?)
            """, (
                pid, tema_id, concepto_id, enunciado,
                json.dumps(opciones, ensure_ascii=False),
                date.today().isoformat(),
            ))
            stats["pendientes"] += 1
        else:
            stats["vinculadas"] += 1

        # Vincular al examen
        respuesta = respuestas.get("teoricas", {}).get(str(numero))
        conn.execute("""
            INSERT OR REPLACE INTO examen_preguntas (
                examen_id, pregunta_id, seccion, numero, respuesta_oficial
            ) VALUES (?, ?, 'teorica', ?, ?)
        """, (examen["id"], pid, numero, respuesta))
        if respuesta in LETRA_A_INDICE:
            conn.execute("UPDATE preguntas SET correcta=? WHERE id=?", (LETRA_A_INDICE[respuesta], pid))
        elif respuesta == "anulada":
            conn.execute("UPDATE preguntas SET correcta=-1 WHERE id=?", (pid,))
        stats["preguntas_teoricas"] += 1

    # 3. Preguntas de reserva
    for p in examen.get("preguntas_reserva", []):
        numero = p["numero"]
        enunciado = p["enunciado"]
        opciones = p["opciones"]
        concepto_id = p.get("concepto_id")
        tema_id = p.get("tema_id")

        pid, motivo = buscar_pregunta_existente(
            conn, enunciado, opciones, concepto_id
        )

        if not pid:
            pid = f"pendiente-{examen['id']}-r{numero:02d}"
            conn.execute("""
                INSERT OR IGNORE INTO preguntas (
                    id, tema_id, concepto_id, enunciado, opciones,
                    correcta, verificado, fecha_alta
                ) VALUES (?, ?, ?, ?, ?, 0, 0, ?)
            """, (
                pid, tema_id, concepto_id, enunciado,
                json.dumps(opciones, ensure_ascii=False),
                date.today().isoformat(),
            ))
            stats["pendientes"] += 1
        else:
            stats["vinculadas"] += 1

        respuesta = respuestas.get("reserva", {}).get(str(numero))
        conn.execute("""
            INSERT OR REPLACE INTO examen_preguntas (
                examen_id, pregunta_id, seccion, numero, respuesta_oficial
            ) VALUES (?, ?, 'reserva', ?, ?)
        """, (examen["id"], pid, numero, respuesta))
        if respuesta in LETRA_A_INDICE:
            conn.execute("UPDATE preguntas SET correcta=? WHERE id=?", (LETRA_A_INDICE[respuesta], pid))
        elif respuesta == "anulada":
            conn.execute("UPDATE preguntas SET correcta=-1 WHERE id=?", (pid,))
        stats["preguntas_reserva"] += 1

    # 4. Supuestos
    for sup in examen.get("supuestos", []):
        sup_id = sup.get("id", f"sup-{examen['id']}-{sup.get('numero', 1)}")

        conn.execute("""
            INSERT OR REPLACE INTO supuestos (
                id, examen_id, bloque_id, numero, titulo, tipo,
                origen, contexto_texto, contexto_json, verificado
            ) VALUES (?, ?, ?, ?, ?, ?, 'real', ?, ?, 1)
        """, (
            sup_id,
            examen["id"],
            sup.get("bloque_id", "bloque-iii"),
            sup.get("numero", 1),
            sup.get("titulo", ""),
            sup.get("tipo", "mixto"),
            sup.get("contexto_texto", ""),
            json.dumps(sup.get("contexto_json", {}), ensure_ascii=False),
        ))

        # Preguntas del supuesto
        for p in sup.get("preguntas", []):
            numero = p["numero"]
            enunciado = p["enunciado"]
            opciones = p["opciones"]
            concepto_id = p.get("concepto_id")
            tema_id = p.get("tema_id")

            pid, motivo = buscar_pregunta_existente(
                conn, enunciado, opciones, concepto_id
            )

            if not pid:
                pid = f"pendiente-{sup_id}-p{numero:02d}"
                conn.execute("""
                    INSERT OR IGNORE INTO preguntas (
                        id, tema_id, concepto_id, enunciado, opciones,
                        correcta, verificado, fecha_alta
                    ) VALUES (?, ?, ?, ?, ?, 0, 0, ?)
                """, (
                    pid, tema_id, concepto_id, enunciado,
                    json.dumps(opciones, ensure_ascii=False),
                    date.today().isoformat(),
                ))
                stats["pendientes"] += 1
            else:
                stats["vinculadas"] += 1

            conn.execute("""
                INSERT OR REPLACE INTO supuesto_preguntas (
                    supuesto_id, pregunta_id, numero_en_supuesto, es_reserva
                ) VALUES (?, ?, ?, ?)
            """, (sup_id, pid, numero, int(p.get("es_reserva", False))))

            # Vincular tema
            if tema_id:
                conn.execute("""
                    INSERT OR IGNORE INTO supuesto_temas (
                        supuesto_id, tema_id, n_preguntas
                    ) VALUES (?, ?, 1)
                """, (sup_id, tema_id))

        stats["supuestos"] += 1

    return stats


def cmd_ingesta(args) -> int:
    root = Path(args.root).expanduser().resolve()
    conn = conectar(root / "oposicion.db")

    try:
        # Cargar JSON de examen
        examen_path = Path(args.examen_json).expanduser().resolve()
        if not examen_path.exists():
            print(f"[error] No existe el archivo: {examen_path}")
            return 1

        with examen_path.open(encoding="utf-8") as f:
            examen = json.load(f)

        # Cargar JSON de respuestas (si se proporciona)
        respuestas = {"teoricas": {}, "reserva": {}, "supuestos": {}}
        if args.respuestas:
            resp_path = Path(args.respuestas).expanduser().resolve()
            if resp_path.exists():
                with resp_path.open(encoding="utf-8") as f:
                    respuestas = json.load(f)

        print(f"[ingesta] Examen: {examen['id']}")
        print(f"[ingesta] Año: {examen.get('anio')}")
        print(f"[ingesta] Modo: {'CON respuestas' if args.respuestas else 'SIN respuestas'}")
        print()

        # Importar
        stats = importar_examen(conn, examen, respuestas)
        conn.commit()

        # Salida
        print("=" * 60)
        print("  INGESTA COMPLETADA")
        print("=" * 60)
        print(f"  Examen:              {stats['examen_id']}")
        print(f"  Preguntas teóricas:  {stats['preguntas_teoricas']}")
        print(f"  Preguntas reserva:   {stats['preguntas_reserva']}")
        print(f"  Vinculadas al banco: {stats['vinculadas']}")
        print(f"  Pendientes (huérf.): {stats['pendientes']}")
        print(f"  Supuestos:           {stats['supuestos']}")
        print("=" * 60)

        if stats["pendientes"] > 0:
            print()
            print(f"  ⚠️  {stats['pendientes']} preguntas marcadas como 'pendiente-*'")
            print(f"      Se resolverán automáticamente al ingestar los temas.")
            print(f"      Ver con: sqlite3 {root}/oposicion.db \\")
            print(f"        \"SELECT id FROM preguntas WHERE id LIKE 'pendiente-%';\"")

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
        description="Importar examen oficial a la BD"
    )
    parser.add_argument("--root", default="~/oposicion")
    parser.add_argument("--examen-json", required=True,
                        help="JSON del examen (estructura completa)")
    parser.add_argument("--respuestas",
                        help="JSON con las respuestas correctas")
    args = parser.parse_args()
    return cmd_ingesta(args)


if __name__ == "__main__":
    sys.exit(main())