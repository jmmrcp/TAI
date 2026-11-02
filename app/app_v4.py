#!/usr/bin/env python3
"""
app_v4.py — TAI Oposición (Streamlit)
Adaptado a la nueva estructura de BD y con un rediseño de interfaz CLI/Terminal completo.
"""
import html
import json
import os
import random
import re
import sqlite3
import unicodedata
from datetime import date, datetime, timedelta
from pathlib import Path

import streamlit as st

# ============================================================
# CONFIGURACIÓN
# ============================================================

ROOT = Path.home() / "oposicion"
DB_PATH = Path(os.environ.get("OPOSICION_DB", ROOT / "oposicion.db"))

INTERVALOS_HUMANOS = [1, 2, 3, 5, 7, 10, 14, 21, 30, 45, 60, 90, 120, 180, 270, 365]
FACTORES = {
    "otra_vez": (0.0, -0.20),
    "dificil":  (1.2, -0.15),
    "bien":     (2.5,  0.00),
    "facil":    (3.5, +0.15),
}
EASE_MIN = 1.3
EASE_MAX = 3.0

PAGINAS = ["./HOY", "./PRACTICAR", "./TEMARIO", "./MATERIAL", "./PROGRESO"]
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

st.set_page_config(
    page_title="TAI_OS v4",
    page_icon="💻",
    layout="centered",
    initial_sidebar_state="collapsed",
)

CSS_TERMINAL = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600;700&display=swap');

:root {
    --bg: #09090b;
    --surface: #121214;
    --border: #27272a;
    --text: #a1a1aa;
    --text-bright: #f4f4f5;
    --accent: #10b981; 
    --accent-hover: #059669;
    --accent-dim: rgba(16, 185, 129, 0.1);
    --ok: #10b981;
    --bad: #ef4444;
    --warn: #eab308;
    --font: 'Fira Code', monospace;
}

html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: var(--bg) !important; color: var(--text-bright);
    font-family: var(--font) !important;
}

* { font-family: var(--font) !important; }
h1, h2, h3, h4 { color: var(--accent) !important; font-weight: 700 !important; text-transform: uppercase; }
h1 { border-bottom: 1px dashed var(--border); padding-bottom: 0.5rem; margin-bottom: 1.5rem !important; }
hr { border-color: var(--border) !important; }

[data-testid="stSidebar"], [data-testid="stHeader"], [data-testid="collapsedControl"] { display: none !important; }
.block-container { padding-top: 1.5rem !important; max-width: 850px; }

/* Top Nav as Radio */
[data-testid="stRadio"] > div[role="radiogroup"] {
    display: flex; flex-wrap: wrap; gap: 0; background: var(--bg); border: 1px solid var(--border);
    margin-bottom: 1.5rem;
}
[data-testid="stRadio"] label {
    padding: 0.6rem 1rem; cursor: pointer; border-right: 1px solid var(--border);
    flex: 1; text-align: center; background: transparent; transition: all 0.1s;
}
[data-testid="stRadio"] label:last-child { border-right: none; }
[data-testid="stRadio"] div[data-baseweb="radio"] > div:first-child { display: none; }
[data-testid="stRadio"] label:hover { background: var(--surface); }
[data-testid="stRadio"] label:has(input:checked) {
    background: var(--surface); border-bottom: 2px solid var(--accent);
}
[data-testid="stRadio"] label:has(input:checked) p { color: var(--accent) !important; font-weight: 700; }

.header-logo {
    font-size: 1.2rem; font-weight: 700; color: var(--accent);
    margin-bottom: 1rem; text-shadow: 0 0 5px var(--accent-dim);
}

.card {
    background: var(--surface); border: 1px solid var(--border); padding: 1.2rem; margin-bottom: 1rem;
    position: relative; border-left: 2px solid var(--accent);
}
.card::before {
    content: "[ SYS_OBJ ]"; position: absolute; top: -0.6rem; left: 1rem;
    background: var(--bg); padding: 0 0.5rem; color: var(--text); font-size: 0.75rem;
}

.stat {
    background: var(--surface); border: 1px solid var(--border); padding: 1rem; text-align: center;
    border-top: 2px solid var(--accent);
}
.stat .v { font-size: 1.8rem; color: var(--text-bright); font-weight: 700; }
.stat .v.ok { color: var(--ok); }
.stat .l { font-size: 0.75rem; color: var(--text); margin-top: 0.2rem; text-transform: uppercase; }

.pbar { height: 4px; background: var(--border); width: 100%; margin: 0.5rem 0; }
.pbar > div { height: 100%; background: var(--accent); transition: width 0.3s; }
.sbar { display: flex; height: 6px; background: var(--border); width: 100%; margin: 0.5rem 0; }
.sbar span { height: 100%; }

table.tabla { width: 100%; border-collapse: collapse; border: 1px solid var(--border); font-size: 0.85rem; margin-bottom: 1rem; }
table.tabla th { background: var(--surface); color: var(--accent); text-align: left; padding: 0.6rem; border: 1px solid var(--border); text-transform: uppercase; }
table.tabla td { padding: 0.6rem; border: 1px solid var(--border); color: var(--text-bright); }

.stButton > button, [data-testid="stFormSubmitButton"] > button {
    background: var(--bg); border: 1px solid var(--border); color: var(--text-bright);
    border-radius: 0; text-transform: uppercase; font-weight: 700; transition: all 0.1s;
}
.stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover { 
    border-color: var(--accent); color: var(--accent); background: var(--accent-dim); 
}
.stButton > button[kind="primary"], [data-testid="stFormSubmitButton"] > button[kind="primaryFormSubmit"] {
    background: var(--accent-dim); border-color: var(--accent); color: var(--accent);
}
.stButton > button[kind="primary"]:hover, [data-testid="stFormSubmitButton"] > button[kind="primaryFormSubmit"]:hover {
    background: var(--accent); color: var(--bg) !important;
}
.stButton > button[kind="primary"]:hover p, [data-testid="stFormSubmitButton"] > button[kind="primaryFormSubmit"]:hover p {
    color: var(--bg) !important;
}

.opt {
    border: 1px solid var(--border); padding: 0.8rem; margin-bottom: 0.5rem; background: var(--surface);
    display: flex; gap: 0.8rem; cursor: pointer; transition: background 0.1s;
}
.opt .letter { color: var(--text); font-weight: 700; background: var(--bg); padding: 0 0.4rem; border: 1px solid var(--border); }
.opt.ok { border-color: var(--ok); background: rgba(16,185,129,0.05); }
.opt.ok .letter { color: var(--ok); border-color: var(--ok); }
.opt.bad { border-color: var(--bad); background: rgba(239,68,68,0.05); }
.opt.bad .letter { color: var(--bad); border-color: var(--bad); }
.opt.dim { opacity: 0.5; }

.q { font-size: 1.05rem; line-height: 1.5; margin-bottom: 0.5rem; font-weight: 700; }
.expl { border-left: 2px solid var(--text); padding-left: 1rem; margin-top: 1rem; color: var(--text); font-size: 0.9rem; }
.verdict { padding: 0.8rem; font-weight: 700; margin: 1rem 0; border: 1px solid; text-transform: uppercase; }
.verdict.ok { border-color: var(--ok); color: var(--ok); background: rgba(16,185,129,0.05); }
.verdict.bad { border-color: var(--bad); color: var(--bad); background: rgba(239,68,68,0.05); }
.blank { display:inline-block; min-width:2rem; text-align:center; border-bottom:2px solid var(--accent); color:var(--accent); font-weight:700; margin:0 0.2rem; }
.fill { display:inline-block; font-weight:700; padding:0 0.4rem; margin:0 0.2rem; border: 1px solid; }
.fill.ok { color: var(--ok); border-color: var(--ok); }
.fill.bad { color: var(--bad); border-color: var(--bad); }

.stTextInput input { background: var(--surface) !important; color: var(--text-bright) !important; border: 1px solid var(--border) !important; border-radius: 0 !important; }
.stTextInput input:focus { border-color: var(--accent) !important; box-shadow: none !important; }
</style>
"""

JS_ATAJOS = """
<script>
(function () {
  try {
    var w = window.parent, d = w.document;
    if (w.__taiKeys) d.removeEventListener('keydown', w.__taiKeys, true);
    var h = function (e) {
      var t = (d.activeElement && d.activeElement.tagName || '').toLowerCase();
      if (t === 'input' || t === 'textarea' || e.ctrlKey || e.metaKey || e.altKey) return;
      var btns = Array.prototype.slice.call(d.querySelectorAll('button'));
      var txt = function (b) { return (b.innerText || '').trim(); };
      var k = e.key.toLowerCase(), target = null;
      var opts = btns.filter(function (b) { return /^[A-D]\)/.test(txt(b)); });
      if (opts.length && /^[a-d1-4]$/.test(k)) {
        var i = isNaN(parseInt(k)) ? k.charCodeAt(0) - 97 : parseInt(k) - 1;
        target = opts[i];
      }
      if (!target && /^[1-4]$/.test(k)) {
        var labels = ['Otra vez', 'Difícil', 'Bien', 'Fácil'];
        target = btns.filter(function (b) { return txt(b).indexOf(labels[parseInt(k) - 1]) >= 0; })[0];
      }
      if (!target && (k === 'enter' || k === ' ')) {
        target = btns.filter(function (b) { var s = txt(b); return s.indexOf('SIGUIENTE') >= 0 || s.indexOf('MOSTRAR') >= 0; })[0];
      }
      if (target && !target.disabled) { e.preventDefault(); target.click(); }
    };
    w.__taiKeys = h;
    d.addEventListener('keydown', h, true);
  } catch (err) {}
})();
</script>
"""

def inyectar_tema():
    st.markdown(CSS_TERMINAL, unsafe_allow_html=True)

# ============================================================
# HELPERS DE UI
# ============================================================

def esc(texto):
    return html.escape(str(texto if texto is not None else "")).replace("$", "&#36;").replace("\n", "<br>")

def embed_html(codigo, height):
    if hasattr(st, "iframe"):
        st.iframe(codigo, height=height)
    else:
        import streamlit.components.v1 as components
        components.html(codigo, height=height)

def stat_card(label, valor, clase=""):
    return f'<div class="stat {clase}"><div class="v {clase}">{esc(valor)}</div><div class="l">{esc(label)}</div></div>'

def barra_progreso(pct):
    pct = max(0, min(100, pct))
    return f'<div class="pbar"><div style="width:{pct:.1f}%"></div></div>'

def barra_estados(dom, prog, porap, nuevo):
    total = dom + prog + porap + nuevo
    if total == 0: return '<div class="sbar"></div>'
    def seg(n, c): return f'<span style="width:{n / total * 100:.2f}%;background:var(--{c})"></span>' if n else ""
    return f'<div class="sbar">{seg(dom, "ok")}{seg(prog, "accent")}{seg(porap, "warn")}{seg(nuevo, "border")}</div>'

def texto_intervalo(n):
    if n is None: return ""
    if n <= 1: return "mañana"
    if n < 30: return f"en {n} días"
    meses = round(n / 30)
    return f"en ~{meses} mes" + ("es" if meses != 1 else "")

def cabecera(titulo, sub=""):
    st.markdown(f"<h1>> {esc(titulo)}</h1>", unsafe_allow_html=True)
    if sub:
        st.markdown(f"<p style='color:var(--text)'>// {esc(sub)}</p>", unsafe_allow_html=True)

# ============================================================
# BASE DE DATOS
# ============================================================

@st.cache_resource
def get_conn():
    c = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    c.row_factory = sqlite3.Row
    return c

def consulta(sql, params=()):
    return get_conn().execute(sql, params).fetchall()

def hoy_iso():
    return date.today().isoformat()

def redondear_intervalo(raw):
    if raw < 1: return 1
    for v in INTERVALOS_HUMANOS:
        if v >= raw: return v
    return INTERVALOS_HUMANOS[-1]

def calcular_estado(intervalo, respuesta):
    if respuesta == "otra_vez": return "por-aprender"
    if intervalo < 3: return "por-aprender"
    if intervalo < 21: return "en-progreso"
    return "dominado"

def actualizar_srs(item_key, respuesta):
    conn = get_conn()
    row = conn.execute("SELECT ease, intervalo_dias FROM srs_items WHERE item_key = ?", (item_key,)).fetchone()
    if not row: return None

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
            ultima_respuesta = ?, veces_fallada = veces_fallada + ?,
            veces_acertada = veces_acertada + ?
        WHERE item_key = ?
    """, (
        nuevo_ease, nuevo_intervalo, nuevo_estado, nuevo_due, respuesta,
        1 if respuesta in ("otra_vez", "dificil") else 0,
        1 if respuesta in ("bien", "facil") else 0, item_key
    ))
    conn.execute("INSERT INTO srs_historial (item_key, fecha, respuesta, intervalo) VALUES (?, ?, ?, ?)", 
                 (item_key, hoy_iso(), respuesta, nuevo_intervalo))
    conn.commit()
    return {"intervalo": nuevo_intervalo, "estado": nuevo_estado}

# ============================================================
# CONSULTAS DE ESTADÍSTICAS
# ============================================================

def stats_globales():
    hoy = hoy_iso()
    r = consulta("""
        SELECT COUNT(*) AS n,
               COALESCE(SUM(estado = 'dominado'), 0) AS dom,
               COALESCE(SUM(estado = 'en-progreso'), 0) AS prog,
               COALESCE(SUM(estado = 'por-aprender'), 0) AS porap,
               COALESCE(SUM(estado = 'sin-empezar'), 0) AS nuevo,
               COALESCE(SUM(due <= ? AND estado != 'dominado'), 0) AS hoy,
               COALESCE(SUM(veces_acertada), 0) AS ac,
               COALESCE(SUM(veces_fallada), 0) AS fa
        FROM srs_items
    """, (hoy,))[0]
    s = dict(r)
    s["hechas_hoy"] = consulta("SELECT COUNT(*) FROM srs_historial WHERE fecha = ?", (hoy,))[0][0]
    resp = s["ac"] + s["fa"]
    s["precision"] = (s["ac"] / resp * 100) if resp else None
    s["racha"] = racha()
    return s

def racha():
    fechas = {r[0] for r in consulta("SELECT DISTINCT fecha FROM srs_historial")}
    d = date.today()
    if d.isoformat() not in fechas: d -= timedelta(days=1)
    n = 0
    while d.isoformat() in fechas:
        n += 1
        d -= timedelta(days=1)
    return n

def listar_bloques_temas():
    bloques = [dict(b) for b in consulta("SELECT * FROM bloques ORDER BY numero")]
    temas = consulta("""
        SELECT t.id, t.numero, t.titulo, t.bloque_id, t.estado_ingesta,
               COUNT(s.item_key) AS n_items,
               COALESCE(SUM(s.estado = 'dominado'), 0) AS n_dom,
               COALESCE(SUM(s.estado = 'en-progreso'), 0) AS n_prog,
               COALESCE(SUM(s.estado = 'por-aprender'), 0) AS n_porap,
               COALESCE(SUM(s.estado = 'sin-empezar'), 0) AS n_nuevo,
               COALESCE(SUM(s.due <= ? AND s.estado != 'dominado'), 0) AS n_hoy
        FROM temas t LEFT JOIN srs_items s ON s.tema_id = t.id
        GROUP BY t.id ORDER BY t.numero
    """, (hoy_iso(),))
    por_bloque = {}
    for t in temas: por_bloque.setdefault(t["bloque_id"], []).append(dict(t))
    for b in bloques: b["temas"] = por_bloque.get(b["id"], [])
    return bloques

# ============================================================
# CARGA DE ÍTEMS
# ============================================================

def _parse_json(valor, default):
    if not valor: return default
    try: return json.loads(valor)
    except: return default

def _item_test(f, item_key=None):
    return {
        "tipo": "test", "item_key": item_key or f"test:{f['tema_id']}:{f['pregunta_id']}",
        "tema_id": f["tema_id"], "concepto_id": f["concepto_id"],
        "enunciado": f["enunciado"], "opciones": _parse_json(f["opciones"], []),
        "correcta": f["correcta"], "explicacion": f["explicacion"],
        "referencia": f["referencia"], "dificultad": f["dificultad"] if "dificultad" in f.keys() else None,
        "supuesto_contexto": f["supuesto_contexto"] if "supuesto_contexto" in f.keys() else None
    }

def _item_card(f, item_key):
    return {"tipo": "card", "item_key": item_key, "tema_id": f["tema_id"], "anverso": f["anverso"], "reverso": f["reverso"]}

def _item_cloze(f, item_key):
    return {"tipo": "cloze", "item_key": item_key, "tema_id": f["tema_id"], "texto": f["texto"], "respuestas": _parse_json(f["respuestas"], [])}

def _item_cuadro(valores, fuente, titulo, col_clave, col_resp, tema_id, item_key):
    v = _parse_json(valores, {})
    return {
        "tipo": "cuadro", "item_key": item_key, "tema_id": tema_id, "titulo": titulo,
        "clave_nombre": col_clave, "clave": v.get(col_clave, ""),
        "resp_nombre": col_resp, "respuesta": v.get(col_resp, ""), "fuente": fuente,
    }

def _fila_a_item(f):
    tipo = f["tipo"]
    if tipo == "test" and f["enunciado"]: return _item_test({**dict(f), "pregunta_id": None}, f["item_key"])
    if tipo == "card" and f["anverso"] is not None: return _item_card(f, f["item_key"])
    if tipo == "cloze" and f["fc_texto"]: return _item_cloze({"tema_id": f["tema_id"], "texto": f["fc_texto"], "respuestas": f["fc_respuestas"]}, f["item_key"])
    if tipo == "cuadro" and f["cf_valores"]: return _item_cuadro(f["cf_valores"], f["cf_fuente"], f["cu_titulo"], f["columna_clave"], f["columna_respuesta"], f["tema_id"], f["item_key"])
    return None

SQL_SRS = """
    SELECT s.item_key, s.tipo, s.tema_id, s.concepto_id, s.estado, s.veces_fallada, s.veces_acertada, s.ultima_respuesta,
           p.enunciado, p.opciones, p.correcta, p.explicacion, p.referencia, p.dificultad,
           f.anverso, f.reverso, f.texto AS fc_texto, f.respuestas AS fc_respuestas,
           cf.valores AS cf_valores, cf.fuente AS cf_fuente, cu.titulo AS cu_titulo, cu.columna_clave, cu.columna_respuesta
    FROM srs_items s
    LEFT JOIN preguntas p ON s.item_key = 'test:' || s.tema_id || ':' || p.id
    LEFT JOIN flashcards f ON s.item_key IN ('card:' || s.tema_id || ':' || f.id, 'cloze:' || s.tema_id || ':' || f.id)
    LEFT JOIN cuadro_filas cf ON s.item_key = 'cuadro:' || s.tema_id || ':' || cf.id
    LEFT JOIN cuadros cu ON cu.id = cf.cuadro_id
"""

def cargar_items_srs_hoy(limite=30):
    filas = consulta(SQL_SRS + " WHERE s.due <= ? AND s.estado != 'dominado' ORDER BY RANDOM() LIMIT ?", (hoy_iso(), limite))
    return [i for i in (_fila_a_item(f) for f in filas) if i]

def cargar_items_debiles(limite=30):
    filas = consulta(SQL_SRS + " WHERE s.veces_fallada > 0 OR s.ultima_respuesta IN ('otra_vez', 'dificil') ORDER BY s.veces_fallada DESC, RANDOM() LIMIT ?", (limite,))
    return [i for i in (_fila_a_item(f) for f in filas) if i]

def scope_sql(col, ambito):
    tipo, valor = ambito
    if tipo == "bloque": return f" AND {col} IN (SELECT id FROM temas WHERE bloque_id = ?)", [valor]
    if tipo == "tema": return f" AND {col} = ?", [valor]
    return "", []

def cargar_tests(ambito, dificultad, limite):
    sc, pr = scope_sql("p.tema_id", ambito)
    dif = " AND p.dificultad = ?" if dificultad else ""
    if dificultad: pr.append(dificultad)
    filas = consulta(f"""
        SELECT p.id AS pregunta_id, p.enunciado, p.opciones, p.correcta, p.explicacion,
               p.referencia, p.tema_id, p.concepto_id, p.dificultad
        FROM preguntas p WHERE p.verificado = 1 {sc} {dif} ORDER BY RANDOM() LIMIT ?
    """, pr + [limite])
    return [_item_test(f) for f in filas]

def cargar_flashcards(ambito, limite):
    sc, pr = scope_sql("f.tema_id", ambito)
    filas = consulta(f"SELECT f.id, f.modo, f.anverso, f.reverso, f.texto, f.respuestas, f.tema_id FROM flashcards f WHERE 1 = 1 {sc} ORDER BY RANDOM() LIMIT ?", pr + [limite])
    return [_item_cloze(f, f"cloze:{f['tema_id']}:{f['id']}") if f["modo"] == "cloze" else _item_card(f, f"card:{f['tema_id']}:{f['id']}") for f in filas]

def cargar_cuadros(ambito, limite, cuadro_id=None):
    sc, pr = scope_sql("cu.tema_id", ambito)
    extra = " AND cu.id = ?" if cuadro_id else ""
    if cuadro_id: pr.append(cuadro_id)
    filas = consulta(f"""
        SELECT cf.id AS fila_id, cf.valores, cf.fuente, cu.titulo, cu.tema_id, cu.columna_clave, cu.columna_respuesta
        FROM cuadro_filas cf JOIN cuadros cu ON cu.id = cf.cuadro_id
        WHERE 1 = 1 {sc} {extra} ORDER BY RANDOM() LIMIT ?
    """, pr + [limite])
    return [_item_cuadro(f["valores"], f["fuente"], f["titulo"], f["columna_clave"], f["columna_respuesta"], f["tema_id"], f"cuadro:{f['tema_id']}:{f['fila_id']}") for f in filas]

def cargar_test_preparado(test_id):
    filas = consulta("""
        SELECT p.id AS pregunta_id, p.enunciado, p.opciones, p.correcta, p.explicacion, p.referencia, p.tema_id, p.concepto_id, p.dificultad
        FROM test_practica_preguntas tp JOIN preguntas p ON p.id = tp.pregunta_id WHERE tp.test_id = ? ORDER BY tp.numero
    """, (test_id,))
    return [_item_test(f) for f in filas]

def cargar_examen(examen_id):
    filas = consulta("""
        SELECT p.id AS pregunta_id, p.enunciado, p.opciones, p.correcta, p.explicacion, p.referencia, p.tema_id, p.concepto_id, p.dificultad
        FROM examen_preguntas ep JOIN preguntas p ON p.id = ep.pregunta_id
        WHERE ep.examen_id = ? ORDER BY ep.seccion, ep.numero
    """, (examen_id,))
    return [_item_test(f) for f in filas]

def cargar_supuesto(supuesto_id):
    sup = consulta("SELECT contexto_texto FROM supuestos WHERE id = ?", (supuesto_id,))
    ctx = sup[0]["contexto_texto"] if sup else None
    filas = consulta("""
        SELECT p.id AS pregunta_id, p.enunciado, p.opciones, p.correcta, p.explicacion, p.referencia, p.tema_id, p.concepto_id, p.dificultad
        FROM supuesto_preguntas sp JOIN preguntas p ON p.id = sp.pregunta_id
        WHERE sp.supuesto_id = ? ORDER BY sp.numero_en_supuesto
    """, (supuesto_id,))
    items = [_item_test(f) for f in filas]
    for it in items: it["supuesto_contexto"] = ctx
    return items

def contar_disponibles(tipo, ambito, dificultad):
    def n(sql, col, extra=()):
        sc, pr = scope_sql(col, ambito)
        return consulta(sql.format(sc=sc), list(pr) + list(extra))[0][0]
    tests = n("SELECT COUNT(*) FROM preguntas p WHERE p.verificado = 1 {sc}" + (" AND p.dificultad = ?" if dificultad else ""), "p.tema_id", [dificultad] if dificultad else [])
    flash = n("SELECT COUNT(*) FROM flashcards f WHERE 1 = 1 {sc}", "f.tema_id")
    cuad = n("SELECT COUNT(*) FROM cuadro_filas cf JOIN cuadros cu ON cu.id = cf.cuadro_id WHERE 1 = 1 {sc}", "cu.tema_id")
    return {"test": tests, "flash": flash, "cuadros": cuad, "mixto": tests + flash + cuad}.get(tipo, 0)

# ============================================================
# VALIDACIÓN Y CLOZE
# ============================================================

def normalizar(texto):
    if not texto: return ""
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", texto)).strip()

def validar_respuesta_cloze(entrada, respuestas_correctas):
    entrada_norm = normalizar(entrada)
    return any(normalizar(c) == entrada_norm for c in respuestas_correctas)

CLOZE_RE = re.compile(r"\{\{?c(\d+)::(.+?)\}\}?")
def partes_cloze(texto):
    partes, pos = [], 0
    for m in CLOZE_RE.finditer(texto or ""):
        if m.start() > pos: partes.append(("t", texto[pos:m.start()]))
        partes.append(("b", m.group(2)))
        pos = m.end()
    if pos < len(texto or ""): partes.append(("t", texto[pos:]))
    return partes

def respuestas_cloze(item):
    r = [p[1] for p in partes_cloze(item["texto"]) if p[0] == "b"]
    return r or list(item.get("respuestas") or [])

# ============================================================
# ESTADO DE SESIÓN
# ============================================================

CLAVES_SESION = ["items", "index", "modo", "aciertos", "fallos", "errores", "titulo_sesion", "respuesta_actual", "mostrar_reverso", "cloze_res", "ultimo_intervalo"]

def limpiar_sesion():
    for k in CLAVES_SESION: st.session_state.pop(k, None)

def iniciar(items, titulo):
    items = [i for i in items if i]
    if not items: return False
    limpiar_sesion()
    st.session_state.update({"items": items, "index": 0, "aciertos": 0, "fallos": 0, "errores": [], "modo": "sesion", "titulo_sesion": titulo})
    return True

def responder(item, respuesta):
    res = actualizar_srs(item["item_key"], respuesta)
    if respuesta == "otra_vez": st.session_state["fallos"] = st.session_state.get("fallos", 0) + 1
    else: st.session_state["aciertos"] = st.session_state.get("aciertos", 0) + 1
    if respuesta in ("otra_vez", "dificil"):
        errores = st.session_state.setdefault("errores", [])
        if not any(e["item_key"] == item["item_key"] for e in errores): errores.append(item)
    st.session_state["ultimo_intervalo"] = res["intervalo"] if res else None
    return res

def _avanzar():
    st.session_state["index"] += 1
    for k in ("respuesta_actual", "mostrar_reverso", "cloze_res", "ultimo_intervalo"): st.session_state.pop(k, None)
    if st.session_state["index"] >= len(st.session_state["items"]): st.session_state["modo"] = "resumen"
    st.rerun()

def _terminar(): st.session_state["modo"] = "resumen"
def _ir_a(pagina, **estado): limpiar_sesion(); st.session_state["pagina"] = pagina; st.session_state.update(estado)
def _nav_cambiada(): limpiar_sesion()

# ============================================================
# WIDGETS DE ÍTEM
# ============================================================

def render_pregunta_test(item, index, total):
    if item.get("supuesto_contexto"):
        st.markdown(f'<div class="card accent" style="margin-bottom:0.5rem"><div class="q">CONTEXTO:</div><div class="expl" style="margin-top:0">{esc(item["supuesto_contexto"])}</div></div>', unsafe_allow_html=True)
        
    st.markdown(f'<div class="card"><div class="q">{esc(item["enunciado"])}</div></div>', unsafe_allow_html=True)
    ya = "respuesta_actual" in st.session_state
    elegida = st.session_state.get("respuesta_actual")

    for i, opcion in enumerate(item["opciones"]):
        letra = chr(65 + i)
        if ya:
            clase = "opt ok" if i == item["correcta"] else ("opt bad" if i == elegida else "opt dim")
            st.markdown(f'<div class="{clase}"><span class="letter">{letra}</span><span>{esc(opcion)}</span></div>', unsafe_allow_html=True)
        else:
            if st.button(f"{letra})  {opcion}", key=f"opt_{item['item_key']}_{i}", use_container_width=True):
                st.session_state["respuesta_actual"] = i
                responder(item, "bien" if i == item["correcta"] else "otra_vez")
                st.rerun()

    if ya:
        if elegida == item["correcta"]: st.markdown(f'<div class="verdict ok">✅ CORRECTO</div>', unsafe_allow_html=True)
        else: st.markdown(f'<div class="verdict bad">❌ INCORRECTO</div>', unsafe_allow_html=True)
        if item.get("explicacion") or item.get("referencia"):
            ref = f'<br>📖 {esc(item["referencia"])}' if item.get("referencia") else ""
            st.markdown(f'<div class="expl">{esc(item["explicacion"] or "")}{ref}</div>', unsafe_allow_html=True)
        if st.button("SIGUIENTE →", type="primary", use_container_width=True): _avanzar()

def render_card(item, index, total):
    frente = f'<div class="q">{esc(item["clave"])}</div><div class="expl">¿{esc(str(item.get("resp_nombre", "")).replace("_", " ").capitalize())}?</div>' if item["tipo"] == "cuadro" else f'<div class="q">{esc(item["anverso"])}</div>'
    dorso = f'<div class="q">{esc(item.get("respuesta", item.get("reverso", "")))}</div>' + (f'<div class="expl">📖 {esc(item["fuente"])}</div>' if item.get("fuente") else "")
    visible = "mostrar_reverso" in st.session_state
    
    st.markdown(f'<div class="card">{frente}' + (f'<hr>{dorso}' if visible else "") + "</div>", unsafe_allow_html=True)
    if not visible:
        if st.button("MOSTRAR REVERSO", type="primary", use_container_width=True): st.session_state["mostrar_reverso"] = True; st.rerun()
    else:
        cols = st.columns(4)
        for col, (lbl, k) in zip(cols, [("🔁 OTRA VEZ", "otra_vez"), ("😞 DIFÍCIL", "dificil"), ("🙂 BIEN", "bien"), ("😎 FÁCIL", "facil")]):
            with col:
                if st.button(lbl, key=f"rate_{k}", type="primary" if k == "bien" else "secondary", use_container_width=True):
                    responder(item, k); _avanzar()

def render_cloze(item, index, total):
    partes = partes_cloze(item["texto"]); respuestas = respuestas_cloze(item)
    res = st.session_state.get("cloze_res")
    if res is None:
        n_huecos, html_q = 0, ""
        for t, v in partes:
            if t == "t": html_q += esc(v)
            else: n_huecos += 1; html_q += f'<span class="blank">{n_huecos}</span>'
        st.markdown(f'<div class="card"><div class="q">{html_q or esc(item["texto"])}</div></div>', unsafe_allow_html=True)
        with st.form(f"form_{item['item_key']}", clear_on_submit=False):
            entradas = [st.text_input(f"HUECO {i+1}", key=f"cz_{i}") for i in range(len(respuestas))]
            if st.form_submit_button("COMPROBAR", type="primary", use_container_width=True):
                oks = [validar_respuesta_cloze(e, [r]) for e, r in zip(entradas, respuestas)]
                st.session_state["cloze_res"] = {"entradas": entradas, "oks": oks, "ok": all(oks)}
                st.rerun()
        return

    html_q, i = "", 0
    for t, v in partes:
        if t == "t": html_q += esc(v)
        else:
            ok = res["oks"][i]
            html_q += f'<span class="fill ok">{esc(v)}</span>' if ok else f'<span class="fill bad"><s>{esc(res["entradas"][i] or "—")}</s> {esc(v)}</span>'
            i += 1
    st.markdown(f'<div class="card"><div class="q">{html_q}</div></div>', unsafe_allow_html=True)

    if res["ok"]:
        st.markdown('<div class="verdict ok">✅ CORRECTO</div>', unsafe_allow_html=True)
        if st.button("SIGUIENTE →", type="primary", use_container_width=True): responder(item, "bien"); _avanzar()
    else:
        st.markdown('<div class="verdict bad">❌ REVISA TUS RESPUESTAS</div>', unsafe_allow_html=True)
        c1, c2 = st.columns([3, 2])
        if c1.button("SIGUIENTE →", type="primary", use_container_width=True): responder(item, "otra_vez"); _avanzar()
        if c2.button("✓ ERA CORRECTA", use_container_width=True): responder(item, "bien"); _avanzar()

# ============================================================
# PANTALLAS
# ============================================================

def pantalla_sesion():
    items = st.session_state["items"]; index = st.session_state["index"]; total = len(items)
    if index >= total: st.session_state["modo"] = "resumen"; st.rerun()
    st.markdown(f'<div class="header-logo">_> {esc(st.session_state.get("titulo_sesion", "SESION"))}</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([6, 1.3], vertical_alignment="center")
    with c1: st.markdown(f'{barra_progreso(index / total * 100)}', unsafe_allow_html=True)
    with c2: st.button("✕ ABORTAR", on_click=_terminar, use_container_width=True)
    
    item = items[index]
    if item["tipo"] == "test": render_pregunta_test(item, index, total)
    elif item["tipo"] in ("card", "cuadro"): render_card(item, index, total)
    elif item["tipo"] == "cloze": render_cloze(item, index, total)
    embed_html(JS_ATAJOS, 1)

def pantalla_resumen():
    cabecera("REPORTE DE SESION", "REGISTROS GUARDADOS")
    ss = st.session_state; total = len(ss.get("items", [])); aciertos, fallos = ss.get("aciertos", 0), ss.get("fallos", 0)
    c1, c2, c3 = st.columns(3)
    c1.markdown(stat_card("RESPONDIDAS", f"{aciertos+fallos}/{total}"), unsafe_allow_html=True)
    c2.markdown(stat_card("ACIERTOS", aciertos, "ok"), unsafe_allow_html=True)
    c3.markdown(stat_card("FALLOS", fallos), unsafe_allow_html=True)
    st.button("VOLVER AL INICIO", use_container_width=True, on_click=limpiar_sesion)

def pantalla_hoy():
    s = stats_globales()
    cabecera("HOY", date.today().isoformat())
    if s["hoy"] > 0:
        st.markdown(f'<div class="card accent"><div class="q">REPASOS PENDIENTES: {s["hoy"]}</div></div>', unsafe_allow_html=True)
        if st.button(f"▶ INICIAR REPASO (MAX 20)", type="primary", use_container_width=True):
            iniciar(cargar_items_srs_hoy(limite=20), "REPASO DIARIO"); st.rerun()
    else:
        st.markdown('<div class="card"><div class="q">TODO AL DIA. SISTEMA OPTIMIZADO.</div></div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.markdown(stat_card("RACHA", f"{s['racha']} D", "accent"), unsafe_allow_html=True)
    c2.markdown(stat_card("HECHAS HOY", s["hechas_hoy"]), unsafe_allow_html=True)
    c3.markdown(stat_card("PRECISION", f"{s['precision']:.0f}%" if s["precision"] else "—", "ok"), unsafe_allow_html=True)
    
    st.markdown("<br><h3>> ESTADO_POR_BLOQUES</h3>", unsafe_allow_html=True)
    for b in listar_bloques_temas():
        dom = sum(t["n_dom"] for t in b["temas"]); prog = sum(t["n_prog"] for t in b["temas"])
        porap = sum(t["n_porap"] for t in b["temas"]); nuevo = sum(t["n_nuevo"] for t in b["temas"])
        st.markdown(f'<div class="card" style="padding:0.8rem; margin-bottom:0.5rem"><b>BLOQUE {b["numero"]} · {esc(b["nombre"])}</b><br>{barra_estados(dom, prog, porap, nuevo)}</div>', unsafe_allow_html=True)

def pantalla_practicar():
    cabecera("ENTRENAMIENTO", "CONFIGURAR ENTORNO DE PRACTICA")
    TIPOS = {"test": "> TEST_OPOSICION", "flash": "> FLASHCARDS", "cuadros": "> DATA_TABLES", "mixto": "> MIXTO_ALEATORIO", "preparado": "> TESTS_GENERADOS", "examenes": "> EXAMENES_OFICIALES", "supuestos": "> SUPUESTOS_PRACTICOS", "debiles": "> PUNTOS_DEBILES"}
    tipo = st.radio("MODULO", list(TIPOS), format_func=TIPOS.get, horizontal=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if tipo == "examenes":
        examenes = consulta("SELECT * FROM examenes ORDER BY anio DESC, id DESC")
        if not examenes: st.info("NO DATA"); return
        mapa = {f"{e['anio']} - {e['tipo']} {e['modelo'] or ''}": e["id"] for e in examenes}
        sel = st.selectbox("TARGET EXAM", list(mapa))
        if st.button("▶ INICIAR EXAMEN", type="primary", use_container_width=True): iniciar(cargar_examen(mapa[sel]), f"EXAMEN: {sel}"); st.rerun()
    elif tipo == "supuestos":
        supuestos = consulta("SELECT * FROM supuestos ORDER BY id DESC")
        if not supuestos: st.info("NO DATA"); return
        mapa = {f"{s['titulo']} ({s['origen']})": s["id"] for s in supuestos}
        sel = st.selectbox("TARGET SUPUESTO", list(mapa))
        if st.button("▶ INICIAR SUPUESTO", type="primary", use_container_width=True): iniciar(cargar_supuesto(mapa[sel]), f"SUPUESTO: {sel}"); st.rerun()
    elif tipo == "preparado":
        tests = consulta("SELECT * FROM tests_practica ORDER BY id DESC")
        if not tests: st.info("NO DATA"); return
        mapa = {f"{t['tipo']} · {t['n_preguntas']} PREGUNTAS": t["id"] for t in tests}
        sel = st.selectbox("TARGET TEST", list(mapa))
        if st.button("▶ INICIAR TEST", type="primary", use_container_width=True): iniciar(cargar_test_preparado(mapa[sel]), "TEST PREPARADO"); st.rerun()
    elif tipo == "debiles":
        if st.button("▶ INICIAR PUNTOS DEBILES", type="primary", use_container_width=True): iniciar(cargar_items_debiles(20), "PUNTOS DEBILES"); st.rerun()
    else:
        ambitos = [("TODO EL TEMARIO", ("todo", None))] + [(f"B{b['numero']} - {b['nombre']}", ("bloque", b["id"])) for b in listar_bloques_temas() if sum(t["n_items"] for t in b["temas"])]
        ambitos += [(f"T{t['numero']} - {t['titulo']}", ("tema", t["id"])) for b in listar_bloques_temas() for t in b["temas"] if t["n_items"]]
        sel_a = st.selectbox("SCOPE", [a[0] for a in ambitos])
        ambito = dict(ambitos)[sel_a]
        if st.button("▶ INICIAR PRACTICA LIBRE (20 ITEMS)", type="primary", use_container_width=True):
            fns = {"test": lambda: cargar_tests(ambito, None, 20), "flash": lambda: cargar_flashcards(ambito, 20), "cuadros": lambda: cargar_cuadros(ambito, 20)}
            iniciar(fns.get(tipo, lambda: (cargar_tests(ambito, None, 10)+cargar_flashcards(ambito, 10))[:20])(), "PRACTICA LIBRE"); st.rerun()

def pantalla_temario(): cabecera("TEMARIO", "ESTRUCTURA DE DATOS"); st.info("Sistema de exploracion en desarrollo.")
def pantalla_material(): cabecera("MATERIAL", "RECURSOS COMPLEMENTARIOS"); st.info("Sistema de visualizacion en desarrollo.")
def pantalla_progreso(): cabecera("PROGRESO", "ANALISIS Y METRICAS"); st.info("Sistema de reportes en desarrollo.")

# ============================================================
# MAIN ROUTING
# ============================================================
def main():
    inyectar_tema()
    st.markdown('<div class="header-logo">_> TAI_OS // SISTEMA DE ESTUDIO v4.0</div>', unsafe_allow_html=True)
    
    modo = st.session_state.get("modo")
    if modo == "sesion": pantalla_sesion(); return
    if modo == "resumen": pantalla_resumen(); return

    st.session_state.setdefault("pagina", PAGINAS[0])
    p = st.radio("NAV", PAGINAS, horizontal=True, label_visibility="collapsed", key="nav_main", on_change=_nav_cambiada)
    st.session_state["pagina"] = p
    
    {PAGINAS[0]: pantalla_hoy, PAGINAS[1]: pantalla_practicar, PAGINAS[2]: pantalla_temario, PAGINAS[3]: pantalla_material, PAGINAS[4]: pantalla_progreso}[p]()

if __name__ == "__main__":
    main()
