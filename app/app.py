#!/usr/bin/env python3
"""
app.py — App Q&A interactiva para TAI Oposición (Streamlit).

Arranque:
    cd /root/.dsh/oposicion
    pip install streamlit
    streamlit run app/app.py
"""
import json
import random
import re
import sqlite3
import unicodedata
from datetime import date, timedelta
from pathlib import Path

import streamlit as st

ROOT = Path("/root/.dsh/oposicion")
DB_PATH = ROOT / "oposicion.db"
TEMARIO_DIR = ROOT / "temario"

INTERVALOS_HUMANOS = [1, 2, 3, 5, 7, 10, 14, 21, 30, 45, 60, 90, 120, 180, 270, 365]
FACTORES = {
    "otra_vez": (0.0, -0.20),
    "dificil":  (1.2, -0.15),
    "bien":     (2.5,  0.00),
    "facil":    (3.5, +0.15),
}
EASE_MIN = 1.3
EASE_MAX = 3.0

st.set_page_config(
    page_title="TAI Oposición",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded",
)

@st.cache_resource
def get_conn():
    c = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    c.row_factory = sqlite3.Row
    return c


def redondear_intervalo(raw):
    if raw < 1:
        return 1
    for v in INTERVALOS_HUMANOS:
        if v >= raw:
            return v
    return INTERVALOS_HUMANOS[-1]


def calcular_estado(intervalo, respuesta):
    if respuesta == "otra_vez":
        return "por-aprender"
    if intervalo < 3:
        return "por-aprender"
    if intervalo < 21:
        return "en-progreso"
    return "dominado"


def actualizar_srs(item_key, respuesta):
    conn = get_conn()
    row = conn.execute(
        "SELECT ease, intervalo_dias FROM srs_items WHERE item_key = ?",
        (item_key,)
    ).fetchone()
    if not row:
        return None

    ease, intervalo = row["ease"], row["intervalo_dias"]
    factor, delta_ease = FACTORES[respuesta]
    nuevo_ease = max(EASE_MIN, min(EASE_MAX, ease + delta_ease))

    if respuesta == "otra_vez":
        nuevo_intervalo = 1
    else:
        base = intervalo if intervalo > 0 else 1
        nuevo_intervalo = redondear_intervalo(base * factor)

    nuevo_estado = calcular_estado(nuevo_intervalo, respuesta)
    nuevo_due = (date.today() + timedelta(days=nuevo_intervalo)).isoformat()

    conn.execute("""
        UPDATE srs_items SET
            ease = ?, intervalo_dias = ?, estado = ?, due = ?,
            ultima_respuesta = ?,
            veces_fallada = veces_fallada + ?,
            veces_acertada = veces_acertada + ?
        WHERE item_key = ?
    """, (
        nuevo_ease, nuevo_intervalo, nuevo_estado, nuevo_due,
        respuesta,
        1 if respuesta in ("otra_vez", "dificil") else 0,
        1 if respuesta in ("bien", "facil") else 0,
        item_key,
    ))
    conn.execute("""
        INSERT INTO srs_historial (item_key, fecha, respuesta, intervalo)
        VALUES (?, ?, ?, ?)
    """, (item_key, date.today().isoformat(), respuesta, nuevo_intervalo))
    conn.commit()
    return {"intervalo": nuevo_intervalo, "estado": nuevo_estado}


def cargar_items_srs_hoy(limite=30):
    conn = get_conn()
    filas = conn.execute("""
        SELECT
            s.item_key, s.tipo, s.tema_id, s.concepto_id, s.estado,
            p.id AS pregunta_id, p.enunciado, p.opciones, p.correcta,
            p.explicacion, p.referencia,
            f.id AS flashcard_id, f.modo, f.anverso, f.reverso,
            f.texto AS fc_texto, f.respuestas AS fc_respuestas
        FROM srs_items s
        LEFT JOIN preguntas p
            ON s.item_key = 'test:' || s.tema_id || ':' || p.id
        LEFT JOIN flashcards f
            ON s.item_key IN (
                'card:' || s.tema_id || ':' || f.id,
                'cloze:' || s.tema_id || ':' || f.id
            )
        WHERE s.due <= date('now') AND s.estado != 'dominado'
        ORDER BY RANDOM()
        LIMIT ?
    """, (limite,)).fetchall()

    items = []
    for f in filas:
        items.append(_fila_a_item(f))
    return items


def cargar_items_tema(tema_id, limite=30):
    conn = get_conn()
    filas = conn.execute("""
        SELECT
            p.id AS pregunta_id, p.enunciado, p.opciones, p.correcta,
            p.explicacion, p.referencia, p.tema_id, p.concepto_id
        FROM preguntas p
        WHERE p.tema_id = ?
          AND p.verificado = 1
        ORDER BY RANDOM()
        LIMIT ?
    """, (tema_id, limite)).fetchall()

    items = []
    for f in filas:
        items.append({
            "tipo": "test",
            "item_key": f"test:{f['tema_id']}:{f['pregunta_id']}",
            "tema_id": f["tema_id"],
            "concepto_id": f["concepto_id"],
            "enunciado": f["enunciado"],
            "opciones": _parse_json(f["opciones"], []),
            "correcta": f["correcta"],
            "explicacion": f["explicacion"],
            "referencia": f["referencia"],
        })
    return items


def cargar_items_flashcards(tema_id, limite=30):
    conn = get_conn()
    filas = conn.execute("""
        SELECT f.id, f.modo, f.anverso, f.reverso, f.texto,
               f.respuestas, f.tema_id, f.concepto_id
        FROM flashcards f
        WHERE f.tema_id = ?
        ORDER BY RANDOM()
        LIMIT ?
    """, (tema_id, limite)).fetchall()

    items = []
    for f in filas:
        items.append({
            "tipo": "cloze" if f["modo"] == "cloze" else "card",
            "item_key": f"{'cloze' if f['modo'] == 'cloze' else 'card'}:{f['tema_id']}:{f['id']}",
            "tema_id": f["tema_id"],
            "concepto_id": f["concepto_id"],
            "anverso": f["anverso"],
            "reverso": f["reverso"],
            "texto": f["texto"],
            "respuestas": _parse_json(f["respuestas"], []),
        })
    return items


def _fila_a_item(f):
    tipo = f["tipo"]
    if tipo == "test" and f["enunciado"]:
        return {
            "tipo": "test",
            "item_key": f["item_key"],
            "tema_id": f["tema_id"],
            "concepto_id": f["concepto_id"],
            "enunciado": f["enunciado"],
            "opciones": _parse_json(f["opciones"], []),
            "correcta": f["correcta"],
            "explicacion": f["explicacion"],
            "referencia": f["referencia"],
        }
    elif tipo == "card":
        return {
            "tipo": "card",
            "item_key": f["item_key"],
            "tema_id": f["tema_id"],
            "anverso": f["anverso"],
            "reverso": f["reverso"],
        }
    elif tipo == "cloze":
        return {
            "tipo": "cloze",
            "item_key": f["item_key"],
            "tema_id": f["tema_id"],
            "texto": f["fc_texto"],
            "respuestas": _parse_json(f["fc_respuestas"], []),
        }
    return None


def _parse_json(valor, default):
    if not valor:
        return default
    try:
        return json.loads(valor)
    except (json.JSONDecodeError, TypeError):
        return default


def normalizar(texto):
    if not texto:
        return ""
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("ascii")
    texto = texto.lower()
    texto = re.sub(r"[^a-z0-9\s]", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


def validar_respuesta_cloze(entrada, respuestas_correctas):
    entrada_norm = normalizar(entrada)
    for correcta in respuestas_correctas:
        if normalizar(correcta) == entrada_norm:
            return True
    return False


@st.cache_data(ttl=60)
def listar_temas():
    conn = get_conn()
    filas = conn.execute("""
        SELECT t.id, t.numero, t.titulo, t.bloque_id, b.nombre AS bloque_nombre,
               COUNT(s.item_key) AS n_items,
               SUM(CASE WHEN s.estado = 'dominado' THEN 1 ELSE 0 END) AS n_dom,
               SUM(CASE WHEN s.due <= date('now') AND s.estado != 'dominado' THEN 1 ELSE 0 END) AS n_hoy
        FROM temas t
        JOIN bloques b ON b.id = t.bloque_id
        LEFT JOIN srs_items s ON s.tema_id = t.id
        WHERE t.estado_ingesta != 'pendiente'
        GROUP BY t.id
        ORDER BY t.numero
    """).fetchall()
    return [dict(f) for f in filas]


def render_pregunta_test(item, index, total):
    st.markdown(f"#### Pregunta {index + 1} de {total}")
    st.markdown(f"**{item['enunciado']}**")
    st.write("")

    opciones = item["opciones"]
    correcta = item["correcta"]
    ya_respondida = "respuesta_actual" in st.session_state

    respuesta_elegida = st.session_state.get("respuesta_actual")

    for i, opcion in enumerate(opciones):
        letra = chr(97 + i)

        if ya_respondida:
            if i == correcta:
                st.success(f"**{letra})** {opcion}  ✓")
            elif i == respuesta_elegida:
                st.error(f"**{letra})** {opcion}  ✗ (tu respuesta)")
            else:
                st.markdown(f"**{letra})** {opcion}")
        else:
            if st.button(f"{letra}) {opcion}", key=f"opt_{item['item_key']}_{i}",
                         use_container_width=True):
                st.session_state["respuesta_actual"] = i
                resultado = "bien" if i == correcta else "otra_vez"
                actualizar_srs(item["item_key"], resultado)
                st.rerun()

    if ya_respondida:
        st.divider()
        if respuesta_elegida == correcta:
            st.success("✅ **Correcto**")
        else:
            st.error("❌ **Incorrecto**")

        if item.get("explicacion"):
            st.markdown(f"**Explicación:** {item['explicacion']}")
        if item.get("referencia"):
            st.caption(f"📖 {item['referencia']}")

        if st.button("Siguiente →", type="primary",
                     use_container_width=True,
                     key=f"sig_{item['item_key']}"):
            _avanzar()


def render_card(item, index, total):
    st.markdown(f"#### Flashcard {index + 1} de {total}")
    st.markdown(f"**{item['anverso']}**")
    st.write("")

    if "mostrar_reverso" not in st.session_state:
        if st.button("Mostrar reverso", use_container_width=True):
            st.session_state["mostrar_reverso"] = True
            st.rerun()
    else:
        st.info(item["reverso"])
        st.write("")
        st.markdown("**¿Cómo lo recordaste?**")
        cols = st.columns(3)
        with cols[0]:
            if st.button("😞 Difícil", use_container_width=True):
                actualizar_srs(item["item_key"], "dificil")
                _avanzar()
        with cols[1]:
            if st.button("🙂 Bien", use_container_width=True):
                actualizar_srs(item["item_key"], "bien")
                _avanzar()
        with cols[2]:
            if st.button("😎 Fácil", use_container_width=True):
                actualizar_srs(item["item_key"], "facil")
                _avanzar()


def render_cloze(item, index, total):
    st.markdown(f"#### Rellenar huecos {index + 1} de {total}")

    texto = item["texto"]
    texto_visual = re.sub(r"\{\{c\d+::([^}]+)\}\}", r"**[___]**", texto)
    st.markdown(texto_visual)
    st.write("")

    entrada = st.text_input("Tu respuesta:", key=f"cloze_{item['item_key']}")

    cols = st.columns(2)
    with cols[0]:
        if st.button("Comprobar", type="primary", use_container_width=True):
            if validar_respuesta_cloze(entrada, item["respuestas"]):
                st.success(f"✅ Correcto: {', '.join(item['respuestas'])}")
                actualizar_srs(item["item_key"], "bien")
                st.session_state["cloze_ok"] = True
            else:
                st.error(f"❌ Incorrecto. Respuesta: {', '.join(item['respuestas'])}")
                actualizar_srs(item["item_key"], "otra_vez")
                st.session_state["cloze_ok"] = False
    with cols[1]:
        if st.session_state.get("cloze_ok") is not None:
            if st.button("Siguiente →", type="primary", use_container_width=True):
                st.session_state.pop("cloze_ok", None)
                _avanzar()


def _avanzar():
    st.session_state["index"] += 1
    st.session_state.pop("respuesta_actual", None)
    st.session_state.pop("mostrar_reverso", None)
    st.session_state.pop("cloze_ok", None)
    if st.session_state["index"] >= len(st.session_state["items"]):
        st.session_state["modo"] = "resumen"
    st.rerun()


def inicializar_sesion(items, modo):
    st.session_state["items"] = items
    st.session_state["index"] = 0
    st.session_state["aciertos"] = 0
    st.session_state["fallos"] = 0
    st.session_state["modo"] = modo
    st.session_state.pop("respuesta_actual", None)
    st.session_state.pop("mostrar_reverso", None)
    st.session_state.pop("cloze_ok", None)


def pantalla_inicio():
    st.title("🎓 TAI Oposición")

    temas = listar_temas()
    if not temas:
        st.warning("No hay temas ingestados. Ejecuta `make migrar` o la Fase 0 primero.")
        return

    total_items = sum(t["n_items"] or 0 for t in temas)
    total_hoy = sum(t["n_hoy"] or 0 for t in temas)

    col1, col2, col3 = st.columns(3)
    col1.metric("Temas", len(temas))
    col2.metric("Ítems totales", total_items)
    col3.metric("Para hoy", total_hoy)

    st.divider()

    st.subheader("¿Qué quieres hacer?")
    modo = st.radio(
        "Modo",
        [
            "🔄 Repaso SRS (lo que toca hoy)",
            "🎯 Práctica libre (del banco del tema)",
            "🎴 Flashcards (anverso/reverso + cloze)",
            "📊 Ver estado de temas",
        ],
        label_visibility="collapsed",
    )

    if modo == "📊 Ver estado de temas":
        pantalla_estado(temas)
        return

    tema_seleccionado = None
    if "Repaso SRS" not in modo:
        opciones = {f"Tema {t['numero']}: {t['titulo']}": t["id"] for t in temas}
        tema_label = st.selectbox("Tema", list(opciones.keys()))
        tema_seleccionado = opciones[tema_label]

    n_items = st.slider("Número de ítems", 5, 50, 20, 5)

    if st.button("▶️ Empezar", type="primary", use_container_width=True):
        if "Repaso SRS" in modo:
            items = cargar_items_srs_hoy(limite=n_items)
            modo_sesion = "repaso"
        elif "Práctica libre" in modo:
            items = cargar_items_tema(tema_seleccionado, limite=n_items)
            modo_sesion = "practica"
        elif "Flashcards" in modo:
            items = cargar_items_flashcards(tema_seleccionado, limite=n_items)
            modo_sesion = "flashcards"

        if not items:
            st.error("No hay ítems disponibles con esos filtros.")
            return

        inicializar_sesion(items, modo_sesion)
        st.rerun()


def pantalla_estado(temas):
    for t in temas:
        n_items = t["n_items"] or 0
        n_dom = t["n_dom"] or 0
        n_hoy = t["n_hoy"] or 0
        pct = (n_dom / n_items * 100) if n_items > 0 else 0

        with st.expander(f"Tema {t['numero']}: {t['titulo']}"):
            col1, col2, col3 = st.columns(3)
            col1.metric("Ítems", n_items)
            col2.metric("Dominados", f"{pct:.0f}%")
            col3.metric("Para hoy", n_hoy)
            st.progress(pct / 100)
            st.caption(f"Bloque: {t['bloque_nombre']}")


def pantalla_sesion():
    items = st.session_state["items"]
    index = st.session_state["index"]
    total = len(items)

    if index >= total:
        pantalla_resumen()
        return

    item = items[index]

    col1, col2 = st.columns([3, 1])
    with col1:
        st.progress((index + 1) / total)
    with col2:
        st.caption(f"{index + 1}/{total}")

    st.divider()

    tipo = item["tipo"]
    if tipo == "test":
        render_pregunta_test(item, index, total)
    elif tipo == "card":
        render_card(item, index, total)
    elif tipo == "cloze":
        render_cloze(item, index, total)


def pantalla_resumen():
    st.title("✅ Sesión completada")

    items = st.session_state["items"]
    total = len(items)

    st.metric("Ítems repasados", total)
    st.info("Los ítems se han registrado en el SRS. Vuelve mañana para los siguientes.")

    if st.button("🔙 Volver al inicio", type="primary", use_container_width=True):
        for key in ["items", "index", "modo", "aciertos", "fallos",
                    "respuesta_actual", "mostrar_reverso", "cloze_ok"]:
            st.session_state.pop(key, None)
        st.rerun()


def sidebar():
    st.sidebar.title("🎓 TAI")
    st.sidebar.markdown("Sistema de estudio")

    if "modo" in st.session_state and st.session_state["modo"] != "inicio":
        if st.sidebar.button("🏠 Volver al inicio", use_container_width=True):
            for key in ["items", "index", "modo", "respuesta_actual",
                        "mostrar_reverso", "cloze_ok"]:
                st.session_state.pop(key, None)
            st.rerun()

    st.sidebar.divider()
    st.sidebar.caption("Versión 0.1")
    st.sidebar.caption(f"BD: {DB_PATH.name}")


def main():
    sidebar()

    modo = st.session_state.get("modo")
    if modo is None or modo == "inicio":
        pantalla_inicio()
    elif modo == "resumen":
        pantalla_resumen()
    else:
        pantalla_sesion()


if __name__ == "__main__":
    main()
