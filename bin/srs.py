#!/usr/bin/env python3
"""
srs.py — Sistema de repaso espaciado (curva del olvido) para TAI Oposición.

Uso:
    python srs.py reconciliar --root ~/oposicion
    python srs.py hoy --root ~/oposicion
    python srs.py responder test:tema-01:p-00123 bien --root ~/oposicion
    python srs.py estado tema-01-la-constitucion --root ~/oposicion
    python srs.py bloque bloque-iii --root ~/oposicion

Subcomandos:
    reconciliar   Sincroniza srs_items con el contenido (nuevos + huérfanos)
    hoy           Muestra qué toca repasar hoy, agrupado por concepto/bloque
    responder     Registra una respuesta (otra_vez | dificil | bien | facil)
    estado        Muestra el estado de un tema concreto
    bloque        Muestra el estado de un bloque completo
    problemáticos Lista los ítems leech (veces_fallada >= 8)
    historial     Muestra el historial de un ítem
"""

import argparse
import json
import sqlite3
import sys
from datetime import date, timedelta
from pathlib import Path

# ============================================================
# CONSTANTES
# ============================================================

# Tabla de intervalos "humanos" (redondeo hacia arriba)
INTERVALOS_HUMANOS = [
    1, 2, 3, 5, 7, 10, 14, 21, 30, 45, 60, 90, 120, 180, 270, 365,
]

# (factor_intervalo, delta_ease)
FACTORES = {
    "otra_vez": (0.0, -0.20),
    "dificil":  (1.2, -0.15),
    "bien":     (2.5,  0.00),
    "facil":    (3.5, +0.15),
}

EASE_MIN = 1.3
EASE_MAX = 3.0
EASE_INICIAL = 2.5

ORDEN_ESTADOS = ["sin-empezar", "por-aprender", "en-progreso", "dominado"]
LEECH_UMBRAL = 8
HISTORIAL_MAX = 20

ESTADOS_COLOR = {
    "sin-empezar": "⬜",
    "por-aprender": "🟥",
    "en-progreso": "🟨",
    "dominado": "🟩",
}


# ============================================================
# UTILIDADES
# ============================================================

def conectar(db_path: Path) -> sqlite3.Connection:
    """Abre conexión con pragmas óptimos."""
    if not db_path.exists():
        print(f"[error] No existe la BD: {db_path}")
        print(f"        Ejecuta primero: python bin/db.py init")
        sys.exit(1)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


def hoy_iso() -> str:
    return date.today().isoformat()


def redondear_intervalo(dias_raw: float) -> int:
    """Redondea al siguiente intervalo humano >= dias_raw."""
    if dias_raw < 1:
        return 1
    for v in INTERVALOS_HUMANOS:
        if v >= dias_raw:
            return v
    return INTERVALOS_HUMANOS[-1]


def calcular_estado(intervalo: int, respuesta: str) -> str:
    """Determina el estado según el intervalo y la respuesta."""
    if respuesta == "otra_vez":
        return "por-aprender"
    if intervalo < 3:
        return "por-aprender"
    if intervalo < 21:
        return "en-progreso"
    return "dominado"


def peor_estado(estados: list[str]) -> str:
    """Devuelve el peor estado de una lista (según ORDEN_ESTADOS)."""
    return min(estados, key=lambda e: ORDEN_ESTADOS.index(e))


def formatear_dias(dias: int) -> str:
    """Formatea días a lenguaje natural."""
    if dias == 0:
        return "hoy"
    if dias == 1:
        return "mañana"
    if dias < 7:
        return f"en {dias} días"
    if dias == 7:
        return "en 1 semana"
    if dias < 30:
        return f"en {dias // 7} semanas"
    if dias == 30:
        return "en 1 mes"
    if dias < 365:
        return f"en {dias // 30} meses"
    return f"en {dias // 365} año(s)"


# ============================================================
# RECONCILIACIÓN: srs_items ↔ contenido
# ============================================================

def recolectar_items_contenido(conn: sqlite3.Connection) -> dict[str, dict]:
    """
    Recorre preguntas, flashcards, cuadros y preguntas de supuestos.
    Devuelve {item_key: {tipo, tema_id, bloque_id, concepto_id}}.
    """
    items = {}

    # 1. Preguntas sueltas (banco)
    cur = conn.execute("""
        SELECT p.id, p.tema_id, t.bloque_id, p.concepto_id
        FROM preguntas p
        LEFT JOIN temas t ON t.id = p.tema_id
    """)
    for pid, tema_id, bloque_id, concepto_id in cur.fetchall():
        if not tema_id:
            continue
        key = f"test:{tema_id}:{pid}"
        items[key] = {
            "tipo": "test",
            "tema_id": tema_id,
            "bloque_id": bloque_id,
            "concepto_id": concepto_id,
        }

    # 2. Flashcards
    cur = conn.execute("""
        SELECT f.id, f.tema_id, t.bloque_id, f.concepto_id, f.modo
        FROM flashcards f
        LEFT JOIN temas t ON t.id = f.tema_id
    """)
    for fid, tema_id, bloque_id, concepto_id, modo in cur.fetchall():
        if not tema_id:
            continue
        prefijo = "cloze" if modo == "cloze" else "card"
        key = f"{prefijo}:{tema_id}:{fid}"
        items[key] = {
            "tipo": prefijo,
            "tema_id": tema_id,
            "bloque_id": bloque_id,
            "concepto_id": concepto_id,
        }

    # 3. Filas de cuadro (cada fila es evaluable)
    cur = conn.execute("""
        SELECT cf.id, c.tema_id, t.bloque_id
        FROM cuadro_filas cf
        JOIN cuadros c ON c.id = cf.cuadro_id
        LEFT JOIN temas t ON t.id = c.tema_id
    """)
    for fila_id, tema_id, bloque_id in cur.fetchall():
        if not tema_id:
            continue
        # Para el SRS, cada fila es un ítem del concepto que la fila referencia
        # (o del tema si no hay concepto específico)
        key = f"cuadro:{tema_id}:{fila_id}"
        items[key] = {
            "tipo": "cuadro",
            "tema_id": tema_id,
            "bloque_id": bloque_id,
            "concepto_id": None,  # se rellena en paso 3
        }

    # 4. Preguntas de supuestos (con bloque_id del supuesto)
    cur = conn.execute("""
        SELECT sp.pregunta_id, s.bloque_id, p.tema_id, p.concepto_id
        FROM supuesto_preguntas sp
        JOIN supuestos s ON s.id = sp.supuesto_id
        JOIN preguntas p ON p.id = sp.pregunta_id
    """)
    for pid, bloque_id, tema_id, concepto_id in cur.fetchall():
        # Las preguntas de supuesto tienen clave distinta: incluyen el supuesto
        # para no colisionar con la misma pregunta suelta.
        key = f"sup:{pid}"
        items[key] = {
            "tipo": "sup",
            "tema_id": tema_id,
            "bloque_id": bloque_id,
            "concepto_id": concepto_id,
        }

    return items


def cmd_reconciliar(args) -> int:
    """Sincroniza srs_items con el contenido actual."""
    root = Path(args.root).expanduser().resolve()
    conn = conectar(root / "oposicion.db")

    try:
        print("[reconciliar] Leyendo contenido...")
        contenido = recolectar_items_contenido(conn)
        print(f"[reconciliar] Ítems en contenido: {len(contenido)}")

        # 1. Ítems ya en SRS
        cur = conn.execute("SELECT item_key FROM srs_items")
        existentes = {row[0] for row in cur.fetchall()}
        print(f"[reconciliar] Ítems ya en SRS:   {len(existentes)}")

        # 2. Añadir nuevos
        nuevos = 0
        hoy = hoy_iso()
        for key, info in contenido.items():
            if key in existentes:
                continue
            conn.execute("""
                INSERT INTO srs_items (
                    item_key, tipo, tema_id, bloque_id, concepto_id,
                    estado, ease, intervalo_dias, due
                ) VALUES (?, ?, ?, ?, ?, 'sin-empezar', ?, 0, ?)
            """, (
                key, info["tipo"], info["tema_id"], info["bloque_id"],
                info["concepto_id"], EASE_INICIAL, hoy,
            ))
            nuevos += 1

        # 3. Detectar huérfanos (en SRS pero no en contenido)
        huerfanos = existentes - set(contenido.keys())

        # 4. Cuadros no tienen concepto_id en el esquema; se deja NULL.

        conn.commit()

        # Resumen
        print()
        print("=" * 60)
        print("  RECONCILIACIÓN")
        print("=" * 60)
        print(f"  Ítems nuevos añadidos: {nuevos}")
        print(f"  Ítems huérfanos:       {len(huerfanos)}")
        if huerfanos and args.verbose:
            print("  Huérfanos (no se borran automáticamente):")
            for h in sorted(huerfanos)[:20]:
                print(f"    - {h}")
            if len(huerfanos) > 20:
                print(f"    ... y {len(huerfanos) - 20} más")

        # Estado general
        cur = conn.execute("SELECT COUNT(*) FROM srs_items")
        total = cur.fetchone()[0]
        print(f"  Total en SRS:          {total}")
        print("=" * 60)

        return 0

    except Exception as e:
        conn.rollback()
        print(f"[error] {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        conn.close()


# ============================================================
# HOY: qué toca repasar
# ============================================================

def cmd_hoy(args) -> int:
    """Muestra los ítems que vencen hoy, agrupados por concepto/bloque."""
    root = Path(args.root).expanduser().resolve()
    conn = conectar(root / "oposicion.db")

    try:
        hoy = hoy_iso()

        # Agrupar por (bloque, tema, concepto)
        cur = conn.execute("""
            SELECT
                COALESCE(bloque_id, 'sin-bloque') AS bloque,
                COALESCE(tema_id, 'sin-tema') AS tema,
                COALESCE(concepto_id, 'sin-concepto') AS concepto,
                COUNT(*) AS n_items,
                GROUP_CONCAT(estado) AS estados
            FROM srs_items
            WHERE due <= ?
              AND estado != 'dominado'
            GROUP BY bloque_id, tema_id, concepto_id
            ORDER BY bloque, tema, concepto
        """, (hoy,))

        filas = cur.fetchall()
        if not filas:
            print(f"[hoy] {hoy}")
            print()
            print("  ✅ Nada para repasar hoy. ¡Buen trabajo!")
            return 0

        # Agrupar por bloque y tema
        por_bloque = {}
        for bloque, tema, concepto, n_items, estados in filas:
            estados_lista = estados.split(",")
            peor = peor_estado(estados_lista)
            por_bloque.setdefault(bloque, {}).setdefault(tema, []).append({
                "concepto": concepto,
                "n_items": n_items,
                "peor_estado": peor,
            })

        # Cabecera
        print(f"[hoy] {hoy}")
        print()
        print("=" * 70)

        total_items = 0
        total_conceptos = 0

        for bloque, temas in por_bloque.items():
            # Cabecera bloque
            cur = conn.execute(
                "SELECT nombre FROM bloques WHERE id = ?", (bloque,)
            )
            row = cur.fetchone()
            nombre_bloque = row[0] if row else bloque

            n_items_bloque = sum(
                c["n_items"] for conceptos in temas.values() for c in conceptos
            )
            print(f"📚 {bloque}: {nombre_bloque}")
            print(f"   {n_items_bloque} ítems pendientes")
            print()

            for tema, conceptos in sorted(temas.items()):
                # Cabecera tema
                cur = conn.execute(
                    "SELECT numero, titulo FROM temas WHERE id = ?", (tema,)
                )
                row = cur.fetchone()
                if row:
                    num, titulo = row
                    print(f"  📖 Tema {num}: {titulo}")
                else:
                    print(f"  📖 {tema}")

                # Conceptos
                for c in conceptos:
                    emoji = ESTADOS_COLOR.get(c["peor_estado"], "⬜")
                    concepto_mostrar = c["concepto"]
                    if concepto_mostrar == "sin-concepto":
                        concepto_mostrar = "(conceptos varios)"
                    else:
                        # Truncar concepto_id para legibilidad
                        if len(concepto_mostrar) > 40:
                            concepto_mostrar = concepto_mostrar[:37] + "..."
                    print(f"    {emoji} {concepto_mostrar:42s} "
                          f"{c['n_items']} ítems   [{c['peor_estado']}]")
                    total_conceptos += 1
                    total_items += c["n_items"]

                print()

        print("=" * 70)
        print(f"  TOTAL: {total_items} ítems en {total_conceptos} conceptos")
        print("=" * 70)

        return 0

    finally:
        conn.close()


# ============================================================
# RESPONDER: actualizar un ítem
# ============================================================

def responder_item(conn: sqlite3.Connection, item_key: str, respuesta: str) -> dict:
    """Actualiza un ítem SRS según la respuesta y devuelve el nuevo estado."""
    cur = conn.execute(
        "SELECT ease, intervalo_dias, veces_fallada, veces_acertada FROM srs_items "
        "WHERE item_key = ?",
        (item_key,),
    )
    row = cur.fetchone()
    if not row:
        raise ValueError(f"Ítem no encontrado: {item_key}")

    ease_actual, intervalo_actual, fallos, aciertos = row
    factor, delta_ease = FACTORES[respuesta]

    # Actualizar ease
    nuevo_ease = max(EASE_MIN, min(EASE_MAX, ease_actual + delta_ease))

    # Calcular nuevo intervalo
    if respuesta == "otra_vez":
        nuevo_intervalo = 1
    else:
        base = intervalo_actual if intervalo_actual > 0 else 1
        nuevo_intervalo = redondear_intervalo(base * factor)

    # Calcular estado y due
    nuevo_estado = calcular_estado(nuevo_intervalo, respuesta)
    nuevo_due = (date.today() + timedelta(days=nuevo_intervalo)).isoformat()

    # Actualizar contadores
    nuevos_fallos = fallos + (1 if respuesta in ("otra_vez", "dificil") else 0)
    nuevos_aciertos = aciertos + (1 if respuesta in ("bien", "facil") else 0)
    problematico = 1 if nuevos_fallos >= LEECH_UMBRAL else 0

    # UPDATE
    conn.execute("""
        UPDATE srs_items SET
            ease = ?,
            intervalo_dias = ?,
            estado = ?,
            due = ?,
            ultima_respuesta = ?,
            veces_fallada = ?,
            veces_acertada = ?,
            problematico = ?
        WHERE item_key = ?
    """, (
        nuevo_ease, nuevo_intervalo, nuevo_estado, nuevo_due,
        respuesta, nuevos_fallos, nuevos_aciertos, problematico, item_key,
    ))

    # INSERT historial
    conn.execute("""
        INSERT INTO srs_historial (item_key, fecha, respuesta, intervalo)
        VALUES (?, ?, ?, ?)
    """, (item_key, hoy_iso(), respuesta, nuevo_intervalo))

    # Purgar historial (mantener solo HISTORIAL_MAX más recientes)
    conn.execute("""
        DELETE FROM srs_historial
        WHERE item_key = ?
          AND id NOT IN (
            SELECT id FROM srs_historial
            WHERE item_key = ?
            ORDER BY id DESC
            LIMIT ?
          )
    """, (item_key, item_key, HISTORIAL_MAX))

    return {
        "item_key": item_key,
        "respuesta": respuesta,
        "ease_anterior": ease_actual,
        "ease_nuevo": nuevo_ease,
        "intervalo_anterior": intervalo_actual,
        "intervalo_nuevo": nuevo_intervalo,
        "estado_nuevo": nuevo_estado,
        "due_nuevo": nuevo_due,
        "problematico": problematico,
    }


def cmd_responder(args) -> int:
    """Registra una respuesta a un ítem."""
    root = Path(args.root).expanduser().resolve()
    conn = conectar(root / "oposicion.db")

    try:
        resultado = responder_item(conn, args.item_key, args.respuesta)
        conn.commit()

        r = resultado
        print(f"[responder] {r['item_key']}")
        print(f"  respuesta:   {r['respuesta']}")
        print(f"  intervalo:   {r['intervalo_anterior']} → {r['intervalo_nuevo']} días "
              f"({formatear_dias(r['intervalo_nuevo'])})")
        print(f"  estado:      {r['estado_nuevo']}")
        print(f"  ease:        {r['ease_anterior']:.2f} → {r['ease_nuevo']:.2f}")
        print(f"  due:         {r['due_nuevo']}")

        if r["problematico"]:
            print()
            print("  ⚠️  Ítem problemático (8+ fallos). Considera reformular el enunciado.")

        return 0

    except ValueError as e:
        print(f"[error] {e}")
        return 1
    except Exception as e:
        conn.rollback()
        print(f"[error] {e}")
        return 1
    finally:
        conn.close()


# ============================================================
# ESTADO: ver estado de un tema
# ============================================================

def cmd_estado(args) -> int:
    """Muestra el estado SRS de un tema."""
    root = Path(args.root).expanduser().resolve()
    conn = conectar(root / "oposicion.db")

    try:
        tema_id = args.tema_id

        # Verificar que existe
        cur = conn.execute(
            "SELECT numero, titulo, estado_ingesta FROM temas WHERE id = ?",
            (tema_id,),
        )
        row = cur.fetchone()
        if not row:
            print(f"[error] No existe el tema: {tema_id}")
            return 1

        num, titulo, estado_ingesta = row

        print(f"[estado] Tema {num}: {titulo}")
        print(f"  Ingresado: {estado_ingesta}")
        print()

        # Estadísticas de SRS
        cur = conn.execute("""
            SELECT estado, COUNT(*) AS n
            FROM srs_items
            WHERE tema_id = ?
            GROUP BY estado
            ORDER BY CASE estado
                WHEN 'sin-empezar' THEN 1
                WHEN 'por-aprender' THEN 2
                WHEN 'en-progreso' THEN 3
                WHEN 'dominado' THEN 4
            END
        """, (tema_id,))

        estados = dict(cur.fetchall())
        total = sum(estados.values())

        print(f"  Total ítems: {total}")
        for estado in ORDEN_ESTADOS:
            n = estados.get(estado, 0)
            if n > 0 or estado == "dominado":
                emoji = ESTADOS_COLOR.get(estado, "⬜")
                pct = (n / total * 100) if total > 0 else 0
                barra = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
                print(f"    {emoji} {estado:14s} {n:4d} ({pct:5.1f}%) {barra}")

        # Próximos repasos
        cur = conn.execute("""
            SELECT due, COUNT(*) AS n
            FROM srs_items
            WHERE tema_id = ?
              AND estado != 'dominado'
              AND due > ?
            GROUP BY due
            ORDER BY due
            LIMIT 5
        """, (tema_id, hoy_iso()))
        proximos = cur.fetchall()
        if proximos:
            print()
            print("  Próximos repasos:")
            for due, n in proximos:
                print(f"    {due}: {n} ítems")

        # Problemáticos
        cur = conn.execute("""
            SELECT COUNT(*) FROM srs_items
            WHERE tema_id = ? AND problematico = 1
        """, (tema_id,))
        n_prob = cur.fetchone()[0]
        if n_prob > 0:
            print()
            print(f"  ⚠️  {n_prob} ítems problemáticos (leeches)")

        # Conceptos compartidos
        cur = conn.execute("""
            SELECT COUNT(DISTINCT ct.concepto_id)
            FROM concepto_temas ct
            WHERE ct.tema_id = ?
              AND ct.concepto_id IN (
                SELECT concepto_id FROM concepto_temas
                GROUP BY concepto_id HAVING COUNT(*) > 1
              )
        """, (tema_id,))
        n_shared = cur.fetchone()[0]
        if n_shared > 0:
            print(f"  🔗 {n_shared} conceptos compartidos con otros temas")

        return 0

    finally:
        conn.close()


# ============================================================
# BLOQUE: ver estado agregado de un bloque
# ============================================================

def cmd_bloque(args) -> int:
    """Muestra el estado SRS de un bloque completo."""
    root = Path(args.root).expanduser().resolve()
    conn = conectar(root / "oposicion.db")

    try:
        bloque_id = args.bloque_id

        cur = conn.execute(
            "SELECT nombre FROM bloques WHERE id = ?", (bloque_id,)
        )
        row = cur.fetchone()
        if not row:
            print(f"[error] No existe el bloque: {bloque_id}")
            return 1
        nombre_bloque = row[0]

        print(f"[bloque] {bloque_id}: {nombre_bloque}")
        print()

        # Temas del bloque con stats
        cur = conn.execute("""
            SELECT
                t.numero, t.titulo, t.estado_ingesta,
                COUNT(s.item_key) AS n_items,
                SUM(CASE WHEN s.estado = 'dominado' THEN 1 ELSE 0 END) AS n_dominados,
                SUM(CASE WHEN s.due <= ? AND s.estado != 'dominado' THEN 1 ELSE 0 END) AS n_para_hoy,
                SUM(CASE WHEN s.problematico = 1 THEN 1 ELSE 0 END) AS n_problematicos
            FROM temas t
            LEFT JOIN srs_items s ON s.tema_id = t.id
            WHERE t.bloque_id = ?
            GROUP BY t.id
            ORDER BY t.numero
        """, (hoy_iso(), bloque_id))

        print(f"  {'#':>3} {'Tema':50s} {'Estado':10s} {'Ítems':>6} {'Dom.':>5} {'Hoy':>4} {'Prob':>4}")
        print("  " + "-" * 85)

        total_items = 0
        total_dominados = 0
        total_para_hoy = 0

        for num, titulo, ingesta, n_items, n_dom, n_hoy, n_prob in cur.fetchall():
            n_items = n_items or 0
            n_dom = n_dom or 0
            n_hoy = n_hoy or 0
            n_prob = n_prob or 0
            total_items += n_items
            total_dominados += n_dom
            total_para_hoy += n_hoy
            titulo_corto = titulo[:48] if len(titulo) > 48 else titulo
            print(f"  {num:>3} {titulo_corto:50s} {ingesta:10s} "
                  f"{n_items:>6} {n_dom:>5} {n_hoy:>4} {n_prob:>4}")

        print("  " + "-" * 85)
        pct = (total_dominados / total_items * 100) if total_items > 0 else 0
        print(f"  {'':>3} {'TOTAL':50s} {'':10s} {total_items:>6} {total_dominados:>5} "
              f"{total_para_hoy:>4}")
        print(f"\n  Dominio del bloque: {pct:.1f}%")
        print(f"  Pendientes hoy:     {total_para_hoy} ítems")

        return 0

    finally:
        conn.close()


# ============================================================
# PROBLEMÁTICOS: listar leeches
# ============================================================

def cmd_problematicos(args) -> int:
    """Lista los ítems leech (veces_fallada >= 8)."""
    root = Path(args.root).expanduser().resolve()
    conn = conectar(root / "oposicion.db")

    try:
        cur = conn.execute("""
            SELECT
                s.item_key, s.tema_id, t.titulo,
                s.veces_fallada, s.veces_acertada,
                p.enunciado
            FROM srs_items s
            LEFT JOIN temas t ON t.id = s.tema_id
            LEFT JOIN preguntas p
                ON s.item_key = 'test:' || s.tema_id || ':' || p.id
            WHERE s.problematico = 1
            ORDER BY s.veces_fallada DESC, s.tema_id
        """)

        filas = cur.fetchall()
        if not filas:
            print("[problematicos] No hay ítems problemáticos. 👍")
            return 0

        print(f"[problematicos] {len(filas)} ítems con 8+ fallos")
        print()

        for item_key, tema_id, titulo, fallos, aciertos, enunciado in filas:
            print(f"⚠️  {item_key}")
            print(f"    Tema:       {titulo or tema_id}")
            print(f"    Fallos:     {fallos} ({aciertos} aciertos)")
            if enunciado:
                trunc = enunciado[:100] + "..." if len(enunciado) > 100 else enunciado
                print(f"    Enunciado:  {trunc}")
            print()

        return 0

    finally:
        conn.close()


# ============================================================
# HISTORIAL: ver historial de un ítem
# ============================================================

def cmd_historial(args) -> int:
    """Muestra el historial de un ítem."""
    root = Path(args.root).expanduser().resolve()
    conn = conectar(root / "oposicion.db")

    try:
        cur = conn.execute("""
            SELECT fecha, respuesta, intervalo
            FROM srs_historial
            WHERE item_key = ?
            ORDER BY id DESC
        """, (args.item_key,))

        filas = cur.fetchall()
        if not filas:
            print(f"[historial] Sin historial para: {args.item_key}")
            return 0

        print(f"[historial] {args.item_key}")
        print()
        print(f"  {'Fecha':12s} {'Respuesta':12s} {'Intervalo':>10s}")
        print("  " + "-" * 40)
        for fecha, respuesta, intervalo in filas:
            print(f"  {fecha:12s} {respuesta:12s} {intervalo:>10} días")

        return 0

    finally:
        conn.close()


# ============================================================
# MAIN
# ============================================================

def main() -> int:
    parser = argparse.ArgumentParser(
        description="SRS para TAI Oposición (SQLite)"
    )
    parser.add_argument("--root", default="~/oposicion",
                        help="Directorio raíz del proyecto")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # reconciliar
    p_rec = sub.add_parser("reconciliar",
                           help="Sincronizar srs_items con el contenido")
    p_rec.add_argument("--verbose", "-v", action="store_true")
    p_rec.set_defaults(func=cmd_reconciliar)

    # hoy
    p_hoy = sub.add_parser("hoy", help="Ver qué toca repasar hoy")
    p_hoy.set_defaults(func=cmd_hoy)

    # responder
    p_resp = sub.add_parser("responder", help="Registrar respuesta a un ítem")
    p_resp.add_argument("item_key", help="Clave del ítem (test:tema:p-id, etc.)")
    p_resp.add_argument("respuesta",
                        choices=list(FACTORES.keys()),
                        help="otra_vez | dificil | bien | facil")
    p_resp.set_defaults(func=cmd_responder)

    # estado
    p_est = sub.add_parser("estado", help="Ver estado de un tema")
    p_est.add_argument("tema_id")
    p_est.set_defaults(func=cmd_estado)

    # bloque
    p_blq = sub.add_parser("bloque", help="Ver estado de un bloque")
    p_blq.add_argument("bloque_id")
    p_blq.set_defaults(func=cmd_bloque)

    # problemáticos
    p_prob = sub.add_parser("problematicos",
                            help="Listar ítems leech")
    p_prob.set_defaults(func=cmd_problematicos)

    # historial
    p_hist = sub.add_parser("historial", help="Ver historial de un ítem")
    p_hist.add_argument("item_key")
    p_hist.set_defaults(func=cmd_historial)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())