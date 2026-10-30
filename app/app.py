#!/usr/bin/env python3
"""
app_v3.py — TAI Oposición (Streamlit). Rediseño de UX/UI con modo claro y oscuro.

Arranque:
    cd ~/oposicion
    streamlit run app/app.py

Requiere streamlit >= 1.40. La BD se busca en ~/oposicion/oposicion.db
(o en la ruta de la variable de entorno OPOSICION_DB).
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

<<<<<<< HEAD
# ============================================================
# CONFIGURACIÓN
# ============================================================
=======
ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "oposicion.db"
TEMARIO_DIR = ROOT / "temario"
>>>>>>> 3de9b13 (Hacer ROOT portable en app Streamlit)

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = Path(os.environ.get("OPOSICION_DB", ROOT / "oposicion.db"))

# Constantes SM-2 (duplicadas de srs.py)
INTERVALOS_HUMANOS = [1, 2, 3, 5, 7, 10, 14, 21, 30, 45, 60, 90, 120, 180, 270, 365]
FACTORES = {
    "otra_vez": (0.0, -0.20),
    "dificil":  (1.2, -0.15),
    "bien":     (2.5,  0.00),
    "facil":    (3.5, +0.15),
}
EASE_MIN = 1.3
EASE_MAX = 3.0

PAGINAS = ["🏠  Hoy", "🎯  Practicar", "📚  Temario", "🗂️  Material", "📈  Progreso"]
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

st.set_page_config(
    page_title="TAI Oposición",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ============================================================
# TEMA (CLARO / OSCURO)
# ============================================================

PALETAS = {
    "claro": {
        "bg": "#F5F6FA", "surface": "#FFFFFF", "surface2": "#EEF0F7",
        "text": "#1A1D2B", "muted": "#677089", "border": "#E1E4EE",
        "accent": "#4F46E5", "accent_hover": "#4338CA", "accent_soft": "#EEF0FF",
        "on_accent": "#FFFFFF",
        "ok": "#16A34A", "ok_bg": "#E8F7EE", "ok_text": "#15803D",
        "bad": "#DC2626", "bad_bg": "#FDECEC", "bad_text": "#B91C1C",
        "warn": "#D97706", "warn_bg": "#FEF3E2",
        "shadow": "0 1px 2px rgba(20,24,40,.05), 0 6px 18px rgba(20,24,40,.05)",
        "scheme": "light",
    },
    "oscuro": {
        "bg": "#0D1020", "surface": "#161A2D", "surface2": "#20253F",
        "text": "#E8EAF5", "muted": "#98A1BB", "border": "#2A3050",
        "accent": "#818CF8", "accent_hover": "#A5B0FF", "accent_soft": "#252A4D",
        "on_accent": "#0D1020",
        "ok": "#4ADE80", "ok_bg": "#12301F", "ok_text": "#4ADE80",
        "bad": "#F87171", "bad_bg": "#361719", "bad_text": "#F87171",
        "warn": "#FBBF24", "warn_bg": "#35290F",
        "shadow": "0 1px 2px rgba(0,0,0,.4), 0 8px 22px rgba(0,0,0,.35)",
        "scheme": "dark",
    },
}

CSS_BASE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ---------- Base ---------- */
html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: var(--bg) !important; color: var(--text); color-scheme: var(--scheme);
}
.stApp, .stApp p, .stApp label, .stApp li, .stApp button, .stApp input, .stApp textarea {
    font-family: "Inter", "Segoe UI", system-ui, -apple-system, sans-serif;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stDecoration"], [data-testid="stAppDeployButton"], footer { display: none !important; }
[data-testid="stElementContainer"]:has(> [data-testid="stMarkdown"] style),
[data-testid="stElementContainer"]:has(> [data-testid="stHtml"] style) { display: none; }
.block-container { padding-top: 4.2rem; padding-bottom: 5rem; max-width: 780px; }
.stApp h1, .stApp h2, .stApp h3, .stApp h4 { color: var(--text) !important; letter-spacing: -0.01em; }
.stApp p, .stApp li, .stMarkdown { color: var(--text); }
[data-testid="stCaptionContainer"], .stApp small { color: var(--muted) !important; }
hr { border-color: var(--border) !important; opacity: 1 !important; }
h3 { font-size: 1.15rem !important; font-weight: 700 !important; margin-top: .6rem !important; }

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] { background: var(--surface) !important; border-right: 1px solid var(--border); }
[data-testid="stSidebar"] * { color: var(--text); }
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * { color: var(--muted) !important; }
.brand { display:flex; align-items:center; gap:.7rem; margin: .2rem 0 1.1rem 0; }
.brand .logo { width: 40px; height: 40px; border-radius: 12px; display:flex; align-items:center;
    justify-content:center; font-size:1.25rem; background: linear-gradient(135deg, var(--accent), #A78BFA); }
.brand .name { font-weight: 800; font-size: 1.1rem; line-height: 1.1; }
.brand .sub { color: var(--muted); font-size: .78rem; }
.side-stats { display:flex; gap:.5rem; margin: 1rem 0 .4rem 0; }
.side-stats div { flex:1; background: var(--surface2); border-radius: 12px; padding: .55rem .7rem; }
.side-stats b { display:block; font-size: 1.15rem; }
.side-stats small { color: var(--muted) !important; font-size: .7rem; text-transform: uppercase; letter-spacing: .05em; }

/* Radios: ocultan el círculo y se ven como píldoras / tarjetas */
[class*="st-key-nav"] label[data-testid="stRadioOption"] > div > div:first-child,
[class*="st-key-pill_"] label[data-testid="stRadioOption"] > div > div:first-child,
[class*="st-key-tipo"] label[data-testid="stRadioOption"] > div > div:first-child,
[class*="st-key-nav"] [data-baseweb="radio"] > div:first-child,
[class*="st-key-pill_"] [data-baseweb="radio"] > div:first-child,
[class*="st-key-tipo"] [data-baseweb="radio"] > div:first-child { display: none; }
[class*="st-key-nav"] div[role="radiogroup"] { gap: .25rem; }
[class*="st-key-nav"] label { padding: .6rem .8rem; border-radius: 12px; width: 100%; cursor: pointer; transition: background .15s; }
[class*="st-key-nav"] label:hover { background: var(--surface2); }
[class*="st-key-nav"] label:has(input:checked) { background: var(--accent_soft); }
[class*="st-key-nav"] label:has(input:checked) p { color: var(--accent) !important; font-weight: 700; }
[class*="st-key-pill_"] div[role="radiogroup"] { gap: .4rem; flex-wrap: wrap; }
[class*="st-key-pill_"] label { padding: .35rem .95rem; border-radius: 999px; border: 1px solid var(--border);
    background: var(--surface); cursor: pointer; transition: all .15s; }
[class*="st-key-pill_"] label:hover { border-color: var(--accent); }
[class*="st-key-pill_"] label:has(input:checked) { background: var(--accent); border-color: var(--accent); }
[class*="st-key-pill_"] label:has(input:checked) p { color: var(--on_accent) !important; font-weight: 700; }
[class*="st-key-tipo"] div[role="radiogroup"] { display: grid !important; grid-template-columns: 1fr 1fr; gap: .55rem; }
[class*="st-key-tipo"] div[role="radiogroup"] { width: 100%; }
[class*="st-key-tipo"] div[role="radiogroup"] > div { width: 100%; }
@media (max-width: 640px) { [class*="st-key-tipo"] div[role="radiogroup"] { grid-template-columns: 1fr; } }
[class*="st-key-tipo"] label { padding: .8rem 1rem; border-radius: 14px; border: 1px solid var(--border);
    background: var(--surface); width: 100%; cursor: pointer; transition: all .15s; }
[class*="st-key-tipo"] label:hover { border-color: var(--accent); }
[class*="st-key-tipo"] label:has(input:checked) { border-color: var(--accent); background: var(--accent_soft); box-shadow: 0 0 0 1px var(--accent); }

/* ---------- Cabeceras de página ---------- */
.hero { margin-bottom: 1.2rem; }
.hero .eyebrow { color: var(--muted); font-size: .85rem; font-weight: 600; }
.hero .eyebrow::first-letter { text-transform: uppercase; }
.hero h1 { font-size: 2rem; margin: .1rem 0 .25rem 0; font-weight: 800; }
.hero p { color: var(--muted) !important; margin: 0; }

/* ---------- Tarjetas ---------- */
[class*="st-key-card_"], [class*="st-key-hero_"] {
    background: var(--surface); border: 1px solid var(--border); border-radius: 18px;
    padding: 1.2rem 1.3rem; box-shadow: var(--shadow); margin-bottom: .9rem;
}
[class*="st-key-hero_"] { border-left: 5px solid var(--accent); }
.big { font-size: 2.8rem; font-weight: 800; line-height: 1; color: var(--accent); }
.big small { font-size: 1rem; font-weight: 600; color: var(--muted) !important; margin-left: .4rem; }
.chips { display:flex; flex-wrap:wrap; gap:.4rem; margin: .7rem 0 .9rem 0; }
.chip { font-size: .78rem; font-weight: 600; padding: .22rem .65rem; border-radius: 999px;
    background: var(--surface2); color: var(--muted); }
.chip.dif-baja { background: var(--ok_bg); color: var(--ok_text); }
.chip.dif-media { background: var(--warn_bg); color: var(--warn); }
.chip.dif-alta { background: var(--bad_bg); color: var(--bad_text); }
.card { background: var(--surface); border: 1px solid var(--border); border-radius: 18px;
    padding: 1.4rem 1.5rem; box-shadow: var(--shadow); margin-bottom: 1rem; }
.card .tag { display:inline-block; font-size:.72rem; font-weight:700; letter-spacing:.06em; text-transform:uppercase;
    color: var(--accent); background: var(--accent_soft); padding: .2rem .65rem; border-radius: 999px; margin: 0 .4rem .8rem 0; }
.card .q { font-size: 1.2rem; font-weight: 650; line-height: 1.55; color: var(--text); }
.card .hint { color: var(--muted); margin-top: .5rem; }
.card .back { font-size: 1.05rem; line-height: 1.6; color: var(--text); }
.card .divider { height:1px; background: var(--border); margin: 1.1rem 0; }
.card .ref { color: var(--muted); font-size: .85rem; margin-top: .6rem; }
.blank { display:inline-block; min-width: 2.2rem; text-align:center; font-weight:700; color: var(--accent);
    background: var(--accent_soft); border-bottom: 2px solid var(--accent); border-radius: 6px 6px 0 0; padding: 0 .5rem; margin: 0 .15rem; }
.fill { display:inline-block; font-weight:700; padding: 0 .5rem; border-radius: 6px; margin: 0 .1rem; }
.fill.ok { background: var(--ok_bg); color: var(--ok_text); }
.fill.bad { background: var(--bad_bg); color: var(--bad_text); }
.fill s { opacity: .7; font-weight: 500; margin-right: .3rem; }

/* ---------- Estadísticas ---------- */
.stat { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: .95rem 1.05rem;
    box-shadow: var(--shadow); height: 100%; }
.stat .v { font-size: 1.65rem; font-weight: 800; color: var(--text); line-height: 1.1; }
.stat .l { font-size: .74rem; color: var(--muted); text-transform: uppercase; letter-spacing: .05em; margin-top: .3rem; }
.stat.accent .v { color: var(--accent); }
.stat.ok .v { color: var(--ok_text); }

/* ---------- Barras ---------- */
.pbar { height: 8px; background: var(--surface2); border-radius: 999px; overflow: hidden; }
.pbar > div { height: 100%; background: linear-gradient(90deg, var(--accent), #A78BFA); border-radius: 999px; transition: width .3s; }
.sbar { display:flex; height: 10px; border-radius: 999px; overflow:hidden; background: var(--surface2); }
.sbar span { display:block; height:100%; }
.legend { display:flex; flex-wrap:wrap; gap:.9rem; margin-top: .7rem; font-size: .8rem; color: var(--muted); }
.legend i { display:inline-block; width:.6rem; height:.6rem; border-radius:50%; margin-right:.35rem; }
.ptop { display:flex; align-items:center; gap:.8rem; }
.ptop .pbar { flex: 1; }
.ptop .n { color: var(--muted); font-size: .85rem; font-variant-numeric: tabular-nums; white-space: nowrap; }
.live { display:flex; gap:.4rem; margin: .5rem 0 1rem 0; }
.live .chip.ok { background: var(--ok_bg); color: var(--ok_text); }
.live .chip.bad { background: var(--bad_bg); color: var(--bad_text); }

/* ---------- Filas (temas, bloques) ---------- */
.row { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: .8rem 1rem; }
.row .t { font-weight: 650; line-height: 1.35; }
.row .m { color: var(--muted); font-size: .8rem; margin: .15rem 0 .5rem 0; }
.row.muted { opacity: .65; }
.bloque { display:flex; align-items:baseline; gap:.6rem; margin: 1.6rem 0 .6rem 0; }
.bloque .n { font-weight: 800; color: var(--accent); }
.bloque .t { font-weight: 700; font-size: 1.05rem; }
.bloque .d { color: var(--muted); font-size: .82rem; }

/* ---------- Opciones del test ---------- */
.opt { display:flex; gap:.75rem; align-items:flex-start; padding: .8rem 1rem; margin-bottom:.5rem;
    border: 1px solid var(--border); border-radius: 14px; background: var(--surface); color: var(--text); line-height: 1.45; }
.opt .letter { flex: 0 0 auto; width: 1.8rem; height: 1.8rem; border-radius: 9px; display:flex; align-items:center;
    justify-content:center; font-weight:700; font-size:.85rem; background: var(--surface2); color: var(--muted); }
.opt.ok { background: var(--ok_bg); border-color: var(--ok); }
.opt.ok .letter { background: var(--ok); color: var(--bg); }
.opt.bad { background: var(--bad_bg); border-color: var(--bad); }
.opt.bad .letter { background: var(--bad); color: var(--bg); }
.opt .note { margin-left:auto; font-size:.76rem; font-weight:700; white-space:nowrap; }
.opt.ok .note { color: var(--ok_text); }
.opt.bad .note { color: var(--bad_text); }
.opt.dim { opacity: .55; }
.verdict { border-radius: 14px; padding: .8rem 1rem; font-weight: 700; margin: .9rem 0 .7rem 0; }
.verdict small { font-weight: 500; opacity: .85; margin-left: .5rem; }
.verdict.ok { background: var(--ok_bg); color: var(--ok_text); }
.verdict.bad { background: var(--bad_bg); color: var(--bad_text); }
.expl { background: var(--surface); border: 1px solid var(--border); border-left: 4px solid var(--accent);
    border-radius: 14px; padding: .9rem 1.1rem; color: var(--text); line-height: 1.55; margin-bottom: .8rem; }
.expl .ref { color: var(--muted); font-size: .85rem; margin-top: .5rem; }
.keys { color: var(--muted); font-size: .78rem; text-align:center; margin-top: 1rem; }
.keys kbd { background: var(--surface2); border: 1px solid var(--border); border-radius: 5px; padding: 0 .4rem; font-size: .75rem; }

/* ---------- Resumen ---------- */
.ring { --p: 0; width: 132px; height: 132px; border-radius: 50%; margin: 0 auto 1rem auto; display:grid; place-items:center;
    background: conic-gradient(var(--ok) calc(var(--p) * 1%), var(--surface2) 0); }
.ring div { width: 100px; height: 100px; border-radius: 50%; background: var(--bg); display:grid; place-items:center;
    font-size: 1.7rem; font-weight: 800; color: var(--text); }
.center { text-align:center; }

/* ---------- Gráfico de actividad ---------- */
.spark { display:flex; align-items:flex-end; gap:.35rem; height: 130px; }
.spark .c { flex:1; display:flex; flex-direction:column; align-items:center; justify-content:flex-end; height:100%; gap:.3rem; }
.spark .b { width:100%; border-radius: 6px 6px 2px 2px; background: linear-gradient(180deg, var(--accent), #A78BFA); min-height: 3px; }
.spark .b.zero { background: var(--surface2); }
.spark span { font-size:.68rem; color: var(--muted); }

/* ---------- Tablas (cuadros) ---------- */
table.tabla { width:100%; border-collapse: separate; border-spacing: 0; border: 1px solid var(--border);
    border-radius: 14px; overflow:hidden; background: var(--surface); font-size: .92rem; }
table.tabla th { text-align:left; background: var(--surface2); color: var(--muted); font-size:.74rem;
    text-transform: uppercase; letter-spacing:.05em; padding: .6rem .9rem; }
table.tabla td { padding: .6rem .9rem; border-top: 1px solid var(--border); color: var(--text); }
table.tabla td.f { color: var(--muted); font-size: .82rem; white-space: nowrap; }

/* ---------- Botones ---------- */
.stButton > button, [data-testid="stFormSubmitButton"] > button {
    border-radius: 12px; border: 1px solid var(--border); background: var(--surface); color: var(--text);
    padding: .6rem 1rem; font-weight: 600; transition: all .15s ease; box-shadow: none; }
.stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
    border-color: var(--accent); color: var(--accent); background: var(--accent_soft); }
.stButton > button:focus:not(:active) { border-color: var(--accent); color: var(--accent); }
.stButton > button p, [data-testid="stFormSubmitButton"] > button p { color: inherit !important; }
.stButton > button[kind="primary"], [data-testid="stFormSubmitButton"] > button[kind="primaryFormSubmit"] {
    background: var(--accent); color: var(--on_accent); border-color: var(--accent); }
.stButton > button[kind="primary"]:hover, [data-testid="stFormSubmitButton"] > button[kind="primaryFormSubmit"]:hover {
    background: var(--accent_hover); border-color: var(--accent_hover); color: var(--on_accent); }
.stButton > button:disabled { opacity: .5; }
[class*="st-key-opt_"] button { justify-content: flex-start; text-align: left; padding: .8rem 1rem; }
[class*="st-key-opt_"] button p { text-align: left; }
[class*="st-key-salir"] button { border-color: transparent; background: transparent; color: var(--muted); }

/* ---------- Inputs ---------- */
.stTextInput input, [data-baseweb="select"] > div, [data-baseweb="input"] {
    background: var(--surface) !important; color: var(--text) !important;
    border-color: var(--border) !important; border-radius: 12px !important; }
[data-baseweb="select"] svg { fill: var(--muted); }
[data-baseweb="popover"] *, ul[role="listbox"] { background: var(--surface) !important; color: var(--text) !important; }
li[role="option"]:hover, li[aria-selected="true"] { background: var(--accent_soft) !important; }
.stTextInput input:focus { border-color: var(--accent) !important; box-shadow: 0 0 0 1px var(--accent) !important; }
[data-testid="stSlider"] [role="slider"] { background: var(--accent) !important; }
[data-testid="stForm"] { border: none !important; padding: 0 !important; background: transparent !important; }
[data-testid="stCheckbox"] label p { color: var(--text) !important; }
[data-testid="stCheckbox"] label:has(input:checked) > div:nth-of-type(1) { background: var(--accent) !important; }

/* ---------- Pestañas / expanders / alertas ---------- */
[data-baseweb="tab-list"] { gap: .4rem; border-bottom: 1px solid var(--border); }
[data-baseweb="tab"] { background: transparent !important; }
[data-baseweb="tab"] p { color: var(--muted) !important; font-weight: 600; }
[data-baseweb="tab"][aria-selected="true"] p { color: var(--accent) !important; }
[data-baseweb="tab-highlight"], .react-aria-SelectionIndicator { background: var(--accent) !important; }
[data-testid="stTab"][aria-selected="true"], [data-testid="stTab"][aria-selected="true"] p { color: var(--accent) !important; }
[data-testid="stSlider"] [role="group"] { filter: hue-rotate(243deg) saturate(.8); }
[data-baseweb="tab-border"] { background: transparent !important; }
[data-testid="stExpander"] { background: var(--surface); border: 1px solid var(--border) !important; border-radius: 14px; box-shadow: none; }
[data-testid="stExpander"] summary, [data-testid="stExpander"] summary * { color: var(--text) !important; }
[data-testid="stAlert"] { border-radius: 14px; border: 1px solid var(--border); background: var(--surface); }
[data-testid="stAlert"] * { color: var(--text) !important; }
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
      var opts = btns.filter(function (b) { return /^[A-D]\\)/.test(txt(b)); });
      if (opts.length && /^[a-d1-4]$/.test(k)) {
        var i = isNaN(parseInt(k)) ? k.charCodeAt(0) - 97 : parseInt(k) - 1;
        target = opts[i];
      }
      if (!target && /^[1-4]$/.test(k)) {
        var labels = ['Otra vez', 'Difícil', 'Bien', 'Fácil'];
        target = btns.filter(function (b) { return txt(b).indexOf(labels[parseInt(k) - 1]) >= 0; })[0];
      }
      if (!target && (k === 'enter' || k === ' ')) {
        target = btns.filter(function (b) { var s = txt(b); return s.indexOf('Siguiente') >= 0 || s.indexOf('Mostrar reverso') >= 0; })[0];
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
    tema = "oscuro" if st.session_state.get("oscuro") else "claro"
    p = PALETAS[tema]
    variables = ":root{" + "".join(f"--{k}:{v};" for k, v in p.items()) + "}"
    st.markdown(CSS_BASE.replace("<style>", "<style>" + variables, 1), unsafe_allow_html=True)


# ============================================================
# HELPERS DE UI
# ============================================================

def esc(texto):
    """Escapa HTML (y el $ de LaTeX) conservando saltos de línea."""
    return html.escape(str(texto if texto is not None else "")).replace("$", "&#36;").replace("\n", "<br>")


def embed_html(codigo, height):
    """Incrusta HTML con JS (st.iframe en Streamlit reciente, components.html en versiones antiguas)."""
    if hasattr(st, "iframe"):
        st.iframe(codigo, height=height)
    else:
        import streamlit.components.v1 as components
        components.html(codigo, height=height)


def card(key):
    """Contenedor con aspecto de tarjeta (usa la clave para el estilo)."""
    try:
        return st.container(key=key)
    except TypeError:
        return st.container(border=True)


def stat_card(label, valor, clase=""):
    return f'<div class="stat {clase}"><div class="v">{esc(valor)}</div><div class="l">{esc(label)}</div></div>'


def barra_progreso(pct):
    pct = max(0, min(100, pct))
    return f'<div class="pbar"><div style="width:{pct:.1f}%"></div></div>'


def barra_estados(dom, prog, porap, nuevo):
    total = dom + prog + porap + nuevo
    if total == 0:
        return '<div class="sbar"></div>'

    def seg(n, c):
        return f'<span style="width:{n / total * 100:.2f}%;background:var(--{c})"></span>' if n else ""

    return f'<div class="sbar">{seg(dom, "ok")}{seg(prog, "accent")}{seg(porap, "warn")}{seg(nuevo, "border")}</div>'


def leyenda(dom, prog, porap, nuevo):
    def it(c, n, t):
        return f'<span><i style="background:var(--{c})"></i>{n} {t}</span>'

    return ('<div class="legend">' + it("ok", dom, "dominados") + it("accent", prog, "en progreso")
            + it("warn", porap, "por aprender") + it("border", nuevo, "sin empezar") + "</div>")


def texto_intervalo(n):
    if n is None:
        return ""
    if n <= 1:
        return "mañana"
    if n < 30:
        return f"en {n} días"
    meses = round(n / 30)
    return f"en ~{meses} mes" + ("es" if meses != 1 else "")


def fecha_larga(d):
    return f"{DIAS[d.weekday()]}, {d.day} de {MESES[d.month - 1]}"


def saludo():
    h = datetime.now().hour
    return "Buenos días" if h < 14 else ("Buenas tardes" if h < 21 else "Buenas noches")


def cabecera(titulo, sub="", eyebrow=""):
    eb = f'<div class="eyebrow">{esc(eyebrow)}</div>' if eyebrow else ""
    sb = f"<p>{esc(sub)}</p>" if sub else ""
    st.markdown(f'<div class="hero">{eb}<h1>{esc(titulo)}</h1>{sb}</div>', unsafe_allow_html=True)


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
    """Actualiza un ítem del SRS. Devuelve dict con el resultado."""
    conn = get_conn()
    row = conn.execute(
        "SELECT ease, intervalo_dias FROM srs_items WHERE item_key = ?", (item_key,)
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
    """, (item_key, hoy_iso(), respuesta, nuevo_intervalo))
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
    if d.isoformat() not in fechas:
        d -= timedelta(days=1)
    n = 0
    while d.isoformat() in fechas:
        n += 1
        d -= timedelta(days=1)
    return n


def actividad(dias=14):
    cuentas = {r[0]: r[1] for r in consulta(
        "SELECT fecha, COUNT(*) FROM srs_historial GROUP BY fecha")}
    hoy = date.today()
    return [((hoy - timedelta(days=i)), cuentas.get((hoy - timedelta(days=i)).isoformat(), 0))
            for i in range(dias - 1, -1, -1)]


def pendientes_por_tipo():
    filas = consulta("""
        SELECT tipo, COUNT(*) AS n FROM srs_items
        WHERE due <= ? AND estado != 'dominado' GROUP BY tipo
    """, (hoy_iso(),))
    return {f["tipo"]: f["n"] for f in filas}


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
    for t in temas:
        por_bloque.setdefault(t["bloque_id"], []).append(dict(t))
    for b in bloques:
        b["temas"] = por_bloque.get(b["id"], [])
    return bloques


def romano(n):
    return {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI"}.get(n, str(n))


# ============================================================
# CARGA DE ÍTEMS
# ============================================================

def _parse_json(valor, default):
    if not valor:
        return default
    try:
        return json.loads(valor)
    except (json.JSONDecodeError, TypeError):
        return default


def _item_test(f, item_key=None):
    return {
        "tipo": "test",
        "item_key": item_key or f"test:{f['tema_id']}:{f['pregunta_id']}",
        "tema_id": f["tema_id"],
        "concepto_id": f["concepto_id"],
        "enunciado": f["enunciado"],
        "opciones": _parse_json(f["opciones"], []),
        "correcta": f["correcta"],
        "explicacion": f["explicacion"],
        "referencia": f["referencia"],
        "dificultad": f["dificultad"] if "dificultad" in f.keys() else None,
    }


def _item_card(f, item_key):
    return {"tipo": "card", "item_key": item_key, "tema_id": f["tema_id"],
            "anverso": f["anverso"], "reverso": f["reverso"]}


def _item_cloze(f, item_key):
    return {"tipo": "cloze", "item_key": item_key, "tema_id": f["tema_id"],
            "texto": f["texto"], "respuestas": _parse_json(f["respuestas"], [])}


def _item_cuadro(valores, fuente, titulo, col_clave, col_resp, tema_id, item_key):
    v = _parse_json(valores, {})
    return {
        "tipo": "cuadro", "item_key": item_key, "tema_id": tema_id, "titulo": titulo,
        "clave_nombre": col_clave, "clave": v.get(col_clave, ""),
        "resp_nombre": col_resp, "respuesta": v.get(col_resp, ""), "fuente": fuente,
    }


def _fila_a_item(f):
    """Convierte una fila de la consulta del SRS a un dict de ítem."""
    tipo = f["tipo"]
    if tipo == "test" and f["enunciado"]:
        return _item_test({**dict(f), "pregunta_id": None}, f["item_key"])
    if tipo == "card" and f["anverso"] is not None:
        return _item_card(f, f["item_key"])
    if tipo == "cloze" and f["fc_texto"]:
        return _item_cloze({"tema_id": f["tema_id"], "texto": f["fc_texto"],
                            "respuestas": f["fc_respuestas"]}, f["item_key"])
    if tipo == "cuadro" and f["cf_valores"]:
        return _item_cuadro(f["cf_valores"], f["cf_fuente"], f["cu_titulo"],
                            f["columna_clave"], f["columna_respuesta"], f["tema_id"], f["item_key"])
    return None


SQL_SRS = """
    SELECT s.item_key, s.tipo, s.tema_id, s.concepto_id, s.estado,
           s.veces_fallada, s.veces_acertada, s.ultima_respuesta,
           p.enunciado, p.opciones, p.correcta, p.explicacion, p.referencia, p.dificultad,
           f.anverso, f.reverso, f.texto AS fc_texto, f.respuestas AS fc_respuestas,
           cf.valores AS cf_valores, cf.fuente AS cf_fuente,
           cu.titulo AS cu_titulo, cu.columna_clave, cu.columna_respuesta
    FROM srs_items s
    LEFT JOIN preguntas p ON s.item_key = 'test:' || s.tema_id || ':' || p.id
    LEFT JOIN flashcards f ON s.item_key IN ('card:' || s.tema_id || ':' || f.id,
                                             'cloze:' || s.tema_id || ':' || f.id)
    LEFT JOIN cuadro_filas cf ON s.item_key = 'cuadro:' || s.tema_id || ':' || cf.id
    LEFT JOIN cuadros cu ON cu.id = cf.cuadro_id
"""


def cargar_items_srs_hoy(limite=30):
    filas = consulta(SQL_SRS + """
        WHERE s.due <= ? AND s.estado != 'dominado' ORDER BY RANDOM() LIMIT ?
    """, (hoy_iso(), limite))
    return [i for i in (_fila_a_item(f) for f in filas) if i]


def cargar_items_debiles(limite=30):
    filas = consulta(SQL_SRS + """
        WHERE s.veces_fallada > 0 OR s.ultima_respuesta IN ('otra_vez', 'dificil')
        ORDER BY s.veces_fallada DESC, RANDOM() LIMIT ?
    """, (limite,))
    return [i for i in (_fila_a_item(f) for f in filas) if i]


def scope_sql(col, ambito):
    """Filtro SQL por ámbito: ('todo', None) | ('bloque', id) | ('tema', id)."""
    tipo, valor = ambito
    if tipo == "bloque":
        return f" AND {col} IN (SELECT id FROM temas WHERE bloque_id = ?)", [valor]
    if tipo == "tema":
        return f" AND {col} = ?", [valor]
    return "", []


def cargar_tests(ambito, dificultad, limite):
    sc, pr = scope_sql("p.tema_id", ambito)
    dif = ""
    if dificultad:
        dif = " AND p.dificultad = ?"
        pr.append(dificultad)
    filas = consulta(f"""
        SELECT p.id AS pregunta_id, p.enunciado, p.opciones, p.correcta, p.explicacion,
               p.referencia, p.tema_id, p.concepto_id, p.dificultad
        FROM preguntas p WHERE p.verificado = 1 {sc} {dif}
        ORDER BY RANDOM() LIMIT ?
    """, pr + [limite])
    return [_item_test(f) for f in filas]


def cargar_flashcards(ambito, limite):
    sc, pr = scope_sql("f.tema_id", ambito)
    filas = consulta(f"""
        SELECT f.id, f.modo, f.anverso, f.reverso, f.texto, f.respuestas, f.tema_id
        FROM flashcards f WHERE 1 = 1 {sc} ORDER BY RANDOM() LIMIT ?
    """, pr + [limite])
    items = []
    for f in filas:
        if f["modo"] == "cloze":
            items.append(_item_cloze(f, f"cloze:{f['tema_id']}:{f['id']}"))
        else:
            items.append(_item_card(f, f"card:{f['tema_id']}:{f['id']}"))
    return items


def cargar_cuadros(ambito, limite, cuadro_id=None):
    sc, pr = scope_sql("cu.tema_id", ambito)
    extra = ""
    if cuadro_id:
        extra = " AND cu.id = ?"
        pr.append(cuadro_id)
    filas = consulta(f"""
        SELECT cf.id AS fila_id, cf.valores, cf.fuente, cu.titulo, cu.tema_id,
               cu.columna_clave, cu.columna_respuesta
        FROM cuadro_filas cf JOIN cuadros cu ON cu.id = cf.cuadro_id
        WHERE 1 = 1 {sc} {extra} ORDER BY RANDOM() LIMIT ?
    """, pr + [limite])
    return [_item_cuadro(f["valores"], f["fuente"], f["titulo"], f["columna_clave"],
                         f["columna_respuesta"], f["tema_id"],
                         f"cuadro:{f['tema_id']}:{f['fila_id']}") for f in filas]


def cargar_test_preparado(test_id):
    filas = consulta("""
        SELECT p.id AS pregunta_id, p.enunciado, p.opciones, p.correcta, p.explicacion,
               p.referencia, p.tema_id, p.concepto_id, p.dificultad
        FROM test_practica_preguntas tp JOIN preguntas p ON p.id = tp.pregunta_id
        WHERE tp.test_id = ? ORDER BY tp.numero
    """, (test_id,))
    return [_item_test(f) for f in filas]


def contar_disponibles(tipo, ambito, dificultad):
    def n(sql, col, extra=()):
        sc, pr = scope_sql(col, ambito)
        return consulta(sql.format(sc=sc), list(pr) + list(extra))[0][0]

    tests = n("SELECT COUNT(*) FROM preguntas p WHERE p.verificado = 1 {sc}"
              + (" AND p.dificultad = ?" if dificultad else ""), "p.tema_id",
              [dificultad] if dificultad else [])
    flash = n("SELECT COUNT(*) FROM flashcards f WHERE 1 = 1 {sc}", "f.tema_id")
    cuad = n("SELECT COUNT(*) FROM cuadro_filas cf JOIN cuadros cu ON cu.id = cf.cuadro_id "
             "WHERE 1 = 1 {sc}", "cu.tema_id")
    return {"test": tests, "flash": flash, "cuadros": cuad, "mixto": tests + flash + cuad}.get(tipo, 0)


# ============================================================
# VALIDACIÓN Y CLOZE
# ============================================================

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
    return any(normalizar(c) == entrada_norm for c in respuestas_correctas)


# Admite {c1::texto} y {{c1::texto}}
CLOZE_RE = re.compile(r"\{\{?c(\d+)::(.+?)\}\}?")


def partes_cloze(texto):
    """Devuelve [("t", texto) | ("b", respuesta)] preservando el orden."""
    partes, pos = [], 0
    for m in CLOZE_RE.finditer(texto or ""):
        if m.start() > pos:
            partes.append(("t", texto[pos:m.start()]))
        partes.append(("b", m.group(2)))
        pos = m.end()
    if pos < len(texto or ""):
        partes.append(("t", texto[pos:]))
    return partes


def respuestas_cloze(item):
    r = [p[1] for p in partes_cloze(item["texto"]) if p[0] == "b"]
    return r or list(item.get("respuestas") or [])


# ============================================================
# ESTADO DE SESIÓN
# ============================================================

CLAVES_SESION = ["items", "index", "modo", "aciertos", "fallos", "errores", "titulo_sesion",
                 "respuesta_actual", "mostrar_reverso", "cloze_res", "ultimo_intervalo"]


def limpiar_sesion():
    for k in CLAVES_SESION:
        st.session_state.pop(k, None)


def iniciar(items, titulo):
    items = [i for i in items if i]
    if not items:
        return False
    limpiar_sesion()
    st.session_state.update({
        "items": items, "index": 0, "aciertos": 0, "fallos": 0, "errores": [],
        "modo": "sesion", "titulo_sesion": titulo,
    })
    return True


def responder(item, respuesta):
    """Registra la respuesta en el SRS y en los contadores de la sesión."""
    res = actualizar_srs(item["item_key"], respuesta)
    if respuesta == "otra_vez":
        st.session_state["fallos"] = st.session_state.get("fallos", 0) + 1
    else:
        st.session_state["aciertos"] = st.session_state.get("aciertos", 0) + 1
    if respuesta in ("otra_vez", "dificil"):
        errores = st.session_state.setdefault("errores", [])
        if not any(e["item_key"] == item["item_key"] for e in errores):
            errores.append(item)
    st.session_state["ultimo_intervalo"] = res["intervalo"] if res else None
    return res


def _avanzar():
    st.session_state["index"] += 1
    for k in ("respuesta_actual", "mostrar_reverso", "cloze_res", "ultimo_intervalo"):
        st.session_state.pop(k, None)
    if st.session_state["index"] >= len(st.session_state["items"]):
        st.session_state["modo"] = "resumen"
    st.rerun()


def _salir():
    limpiar_sesion()


def _terminar():
    st.session_state["modo"] = "resumen"


def _ir_a(pagina, **estado):
    """Callback: cambia de página (y fija otros valores de widgets)."""
    limpiar_sesion()
    st.session_state["pagina"] = pagina
    st.session_state.update(estado)


def _nav_cambiada():
    limpiar_sesion()


# ============================================================
# WIDGETS DE ÍTEM
# ============================================================

def render_pregunta_test(item, index, total):
    dif = item.get("dificultad")
    chip_dif = f'<span class="tag" style="background:var(--surface2);color:var(--muted)">{esc(dif)}</span>' if dif else ""
    st.markdown(
        f'<div class="card"><div><span class="tag">Test</span>{chip_dif}</div>'
        f'<div class="q">{esc(item["enunciado"])}</div></div>',
        unsafe_allow_html=True,
    )

    opciones = item["opciones"]
    correcta = item["correcta"]
    ya = "respuesta_actual" in st.session_state
    elegida = st.session_state.get("respuesta_actual")

    for i, opcion in enumerate(opciones):
        letra = chr(65 + i)
        if ya:
            if i == correcta:
                clase, nota = "opt ok", "Correcta"
            elif i == elegida:
                clase, nota = "opt bad", "Tu respuesta"
            else:
                clase, nota = "opt dim", ""
            nota_html = f'<span class="note">{nota}</span>' if nota else ""
            st.markdown(
                f'<div class="{clase}"><span class="letter">{letra}</span>'
                f'<span>{esc(opcion)}</span>{nota_html}</div>', unsafe_allow_html=True)
        else:
            if st.button(f"{letra})  {opcion}", key=f"opt_{item['item_key']}_{i}", use_container_width=True):
                st.session_state["respuesta_actual"] = i
                responder(item, "bien" if i == correcta else "otra_vez")
                st.rerun()

    if ya:
        prox = texto_intervalo(st.session_state.get("ultimo_intervalo"))
        sub = f"<small>Lo volverás a ver {prox}</small>" if prox else ""
        if elegida == correcta:
            st.markdown(f'<div class="verdict ok">✅ ¡Correcto!{sub}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="verdict bad">❌ Incorrecto{sub}</div>', unsafe_allow_html=True)

        if item.get("explicacion") or item.get("referencia"):
            ref = f'<div class="ref">📖 {esc(item["referencia"])}</div>' if item.get("referencia") else ""
            expl = esc(item["explicacion"]) if item.get("explicacion") else ""
            st.markdown(f'<div class="expl">{expl}{ref}</div>', unsafe_allow_html=True)

        if st.button("Siguiente →", type="primary", use_container_width=True, key=f"sig_{item['item_key']}"):
            _avanzar()


def _frente_dorso(item):
    """HTML de la cara y del reverso de una flashcard o cuadro."""
    if item["tipo"] == "cuadro":
        pista = str(item["resp_nombre"]).replace("_", " ").capitalize()
        frente = (f'<div class="q">{esc(item["clave"])}</div>'
                  f'<div class="hint">¿{esc(pista)}?</div>')
        ref = f'<div class="ref">📖 {esc(item["fuente"])}</div>' if item.get("fuente") else ""
        dorso = f'<div class="back"><b>{esc(item["respuesta"])}</b></div>{ref}'
        etiqueta = f"Cuadro · {item['titulo']}"
    else:
        frente = f'<div class="q">{esc(item["anverso"])}</div>'
        dorso = f'<div class="back">{esc(item["reverso"])}</div>'
        etiqueta = "Flashcard"
    return etiqueta, frente, dorso


def render_card(item, index, total):
    etiqueta, frente, dorso = _frente_dorso(item)
    visible = "mostrar_reverso" in st.session_state
    st.markdown(
        f'<div class="card"><div><span class="tag">{esc(etiqueta)}</span></div>{frente}'
        + (f'<div class="divider"></div>{dorso}' if visible else "") + "</div>",
        unsafe_allow_html=True,
    )

    if not visible:
        if st.button("Mostrar reverso", type="primary", use_container_width=True,
                     key=f"rev_{item['item_key']}"):
            st.session_state["mostrar_reverso"] = True
            st.rerun()
    else:
        st.caption("¿Cómo lo recordaste?")
        cols = st.columns(4)
        opciones = [("🔁 Otra vez", "otra_vez"), ("😞 Difícil", "dificil"),
                    ("🙂 Bien", "bien"), ("😎 Fácil", "facil")]
        for col, (etiqueta_b, clave) in zip(cols, opciones):
            with col:
                if st.button(etiqueta_b, key=f"rate_{clave}_{item['item_key']}",
                             type="primary" if clave == "bien" else "secondary",
                             use_container_width=True):
                    responder(item, clave)
                    _avanzar()


def render_cloze(item, index, total):
    partes = partes_cloze(item["texto"])
    respuestas = respuestas_cloze(item)
    res = st.session_state.get("cloze_res")

    if res is None:
        n_huecos, html_q = 0, ""
        for tipo, valor in partes:
            if tipo == "t":
                html_q += esc(valor)
            else:
                n_huecos += 1
                html_q += f'<span class="blank">{n_huecos}</span>'
        if not n_huecos:
            html_q = esc(item["texto"])
        st.markdown(
            f'<div class="card"><div><span class="tag">Rellenar huecos</span></div>'
            f'<div class="q">{html_q}</div></div>', unsafe_allow_html=True)

        with st.form(f"form_{item['item_key']}", clear_on_submit=False):
            entradas = []
            for i in range(len(respuestas)):
                etiqueta = "Tu respuesta" if len(respuestas) == 1 else f"Hueco {i + 1}"
                entradas.append(st.text_input(etiqueta, key=f"cz_{item['item_key']}_{i}",
                                              placeholder="Escribe lo que falta…"))
            if st.form_submit_button("Comprobar", type="primary", use_container_width=True):
                oks = [validar_respuesta_cloze(e, [r]) for e, r in zip(entradas, respuestas)]
                st.session_state["cloze_res"] = {"entradas": entradas, "oks": oks, "ok": all(oks)}
                st.rerun()
        return

    # Resultado: el texto con los huecos rellenos
    html_q, i = "", 0
    for tipo, valor in partes:
        if tipo == "t":
            html_q += esc(valor)
        else:
            ok = res["oks"][i]
            if ok:
                html_q += f'<span class="fill ok">{esc(valor)}</span>'
            else:
                usado = res["entradas"][i] or "—"
                html_q += f'<span class="fill bad"><s>{esc(usado)}</s>{esc(valor)}</span>'
            i += 1
    if i == 0:
        html_q = esc(item["texto"]) + "<br>" + "".join(
            f'<span class="fill {"ok" if ok else "bad"}">{esc(r)}</span> ' for ok, r in zip(res["oks"], respuestas))
    st.markdown(
        f'<div class="card"><div><span class="tag">Rellenar huecos</span></div>'
        f'<div class="q">{html_q}</div></div>', unsafe_allow_html=True)

    if res["ok"]:
        st.markdown('<div class="verdict ok">✅ ¡Correcto!</div>', unsafe_allow_html=True)
        if st.button("Siguiente →", type="primary", use_container_width=True, key=f"sigc_{item['item_key']}"):
            responder(item, "bien")
            _avanzar()
    else:
        st.markdown('<div class="verdict bad">❌ Revisa las respuestas marcadas<small>'
                    '¿Era correcta la tuya? Puedes validarla.</small></div>', unsafe_allow_html=True)
        c1, c2 = st.columns([3, 2])
        with c1:
            if st.button("Siguiente →", type="primary", use_container_width=True, key=f"sigc_{item['item_key']}"):
                responder(item, "otra_vez")
                _avanzar()
        with c2:
            if st.button("✓ Era correcta", use_container_width=True, key=f"valc_{item['item_key']}"):
                responder(item, "bien")
                _avanzar()


# ============================================================
# PANTALLAS: SESIÓN Y RESUMEN
# ============================================================

def pantalla_sesion():
    items = st.session_state["items"]
    index = st.session_state["index"]
    total = len(items)
    if index >= total:
        st.session_state["modo"] = "resumen"
        st.rerun()
    item = items[index]

    c1, c2 = st.columns([6, 1.3], vertical_alignment="center")
    with c1:
        st.markdown(f'<div class="ptop">{barra_progreso(index / total * 100)}'
                    f'<span class="n">{index + 1} / {total}</span></div>', unsafe_allow_html=True)
    with c2:
        st.button("✕ Salir", key="salir_sesion", on_click=_terminar, use_container_width=True)

    st.markdown(
        f'<div class="live"><span class="chip ok">✓ {st.session_state.get("aciertos", 0)}</span>'
        f'<span class="chip bad">✗ {st.session_state.get("fallos", 0)}</span>'
        f'<span class="chip">{esc(st.session_state.get("titulo_sesion", ""))}</span></div>',
        unsafe_allow_html=True)

    tipo = item["tipo"]
    if tipo == "test":
        render_pregunta_test(item, index, total)
    elif tipo in ("card", "cuadro"):
        render_card(item, index, total)
    elif tipo == "cloze":
        render_cloze(item, index, total)

    st.markdown('<div class="keys"><kbd>A</kbd>–<kbd>D</kbd> o <kbd>1</kbd>–<kbd>4</kbd> para responder · '
                '<kbd>Intro</kbd> para continuar</div>', unsafe_allow_html=True)
    embed_html(JS_ATAJOS, 1)


def resumen_item(item):
    """(pregunta, respuesta) en texto plano para repasar los fallos."""
    t = item["tipo"]
    if t == "test":
        op = item["opciones"]
        return item["enunciado"], op[item["correcta"]] if item["correcta"] < len(op) else ""
    if t == "card":
        return item["anverso"], item["reverso"]
    if t == "cuadro":
        return f"{item['titulo']}: {item['clave']}", item["respuesta"]
    if t == "cloze":
        q = "".join(v if k == "t" else "____" for k, v in partes_cloze(item["texto"])) or item["texto"]
        return q, " · ".join(respuestas_cloze(item))
    return "", ""


def pantalla_resumen():
    ss = st.session_state
    total = len(ss.get("items", []))
    aciertos, fallos = ss.get("aciertos", 0), ss.get("fallos", 0)
    respondidos = aciertos + fallos
    pct = round(aciertos / respondidos * 100) if respondidos else 0
    errores = ss.get("errores", [])

    cabecera("Sesión completada" if respondidos >= total else "Sesión terminada",
             "Tus respuestas ya están registradas en el repaso espaciado.", "Resumen")

    with card("card_resumen"):
        st.markdown(f'<div class="ring" style="--p:{pct}"><div>{pct if respondidos else "—"}{"%" if respondidos else ""}</div></div>'
                    f'<div class="center" style="color:var(--muted)">precisión de la sesión</div>',
                    unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.markdown(stat_card("Respondidas", f"{respondidos}/{total}"), unsafe_allow_html=True)
    c2.markdown(stat_card("Aciertos", aciertos, "ok"), unsafe_allow_html=True)
    c3.markdown(stat_card("Fallos", fallos), unsafe_allow_html=True)
    st.write("")

    if errores:
        st.markdown(f"### A repasar ({len(errores)})")
        for e in errores:
            q, a = resumen_item(e)
            st.markdown(f'<div class="row" style="margin-bottom:.5rem"><div class="t">{esc(q)}</div>'
                        f'<div class="m" style="margin:.35rem 0 0 0">✔ {esc(a)}</div></div>', unsafe_allow_html=True)
        st.write("")
        if st.button(f"🔁  Repasar estos {len(errores)} ahora", type="primary", use_container_width=True,
                     key="repasar_errores"):
            iniciar(list(errores), "Repaso de fallos")
            st.rerun()

    st.button("Volver al inicio", use_container_width=True, key="volver_inicio", on_click=_salir)


# ============================================================
# PÁGINA: HOY
# ============================================================

def pantalla_hoy():
    s = stats_globales()
    cabecera(f"{saludo()} 👋", "Esto es lo que toca hoy.", fecha_larga(date.today()))

    with card("hero_hoy"):
        if s["hoy"] > 0:
            tipos = pendientes_por_tipo()
            etiquetas = {"test": "📝 tests", "card": "🎴 flashcards", "cloze": "✏️ huecos", "cuadro": "🗂️ cuadros"}
            chips = "".join(f'<span class="chip">{etiquetas.get(t, t)} · {n}</span>' for t, n in tipos.items())
            st.markdown(f'<div class="big">{s["hoy"]}<small>ítems para repasar hoy</small></div>'
                        f'<div class="chips">{chips}</div>', unsafe_allow_html=True)
            st.caption("Tamaño de la sesión")
            n = st.radio("Tamaño", [10, 20, 30, 50], index=1, horizontal=True,
                         label_visibility="collapsed", key="pill_n_rep")
            n_real = min(n, s["hoy"])
            if st.button(f"▶  Empezar repaso · {n_real} ítems", type="primary",
                         use_container_width=True, key="go_repaso"):
                if iniciar(cargar_items_srs_hoy(limite=n), "Repaso de hoy"):
                    st.rerun()
                else:
                    st.warning("No hay ítems disponibles ahora mismo.")
        else:
            st.markdown('<div class="big" style="font-size:2rem">🎉 Todo al día</div>'
                        '<div class="chips"><span class="chip">No quedan repasos pendientes hoy</span></div>',
                        unsafe_allow_html=True)
            st.button("🎯  Practicar algo más", type="primary", use_container_width=True, key="go_practicar_extra",
                      on_click=_ir_a, args=(PAGINAS[1],))

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(stat_card("Racha", f"🔥 {s['racha']}", "accent" if s["racha"] else ""), unsafe_allow_html=True)
    c2.markdown(stat_card("Hechas hoy", s["hechas_hoy"]), unsafe_allow_html=True)
    dom_pct = round(s["dom"] / s["n"] * 100) if s["n"] else 0
    c3.markdown(stat_card("Dominado", f"{dom_pct}%"), unsafe_allow_html=True)
    prec = f"{s['precision']:.0f}%" if s["precision"] is not None else "—"
    c4.markdown(stat_card("Precisión", prec, "ok"), unsafe_allow_html=True)
    st.write("")

    with card("card_estado"):
        st.markdown("**Tu progreso global**")
        st.markdown(barra_estados(s["dom"], s["prog"], s["porap"], s["nuevo"])
                    + leyenda(s["dom"], s["prog"], s["porap"], s["nuevo"]), unsafe_allow_html=True)

    st.markdown("### Por bloque")
    for b in listar_bloques_temas():
        n = sum(t["n_items"] for t in b["temas"])
        dom = sum(t["n_dom"] for t in b["temas"])
        prog = sum(t["n_prog"] for t in b["temas"])
        porap = sum(t["n_porap"] for t in b["temas"])
        nuevo = sum(t["n_nuevo"] for t in b["temas"])
        listos = sum(1 for t in b["temas"] if t["estado_ingesta"] != "pendiente")
        meta = f"{listos} de {len(b['temas'])} temas con contenido" + (f" · {n} ítems" if n else "")
        st.markdown(
            f'<div class="row {"" if n else "muted"}" style="margin-bottom:.5rem">'
            f'<div class="t">Bloque {romano(b["numero"])} · {esc(b["nombre"])}</div>'
            f'<div class="m">{esc(meta)}</div>{barra_estados(dom, prog, porap, nuevo)}</div>',
            unsafe_allow_html=True)


# ============================================================
# PÁGINA: PRACTICAR
# ============================================================

TIPOS_PRACTICA = {
    "test": "📝  Test · preguntas tipo oposición (A–D)",
    "flash": "🎴  Flashcards · anverso/reverso y huecos",
    "cuadros": "🗂️  Cuadros · plazos, mayorías, composiciones",
    "mixto": "🔀  Mixto · un poco de todo",
    "preparado": "📋  Tests preparados · simulacros ya generados",
    "debiles": "🎯  Puntos débiles · lo que más fallas",
}


def opciones_ambito():
    """Lista de (etiqueta, ambito) con contenido disponible."""
    opciones = [("Todo el temario", ("todo", None))]
    for b in listar_bloques_temas():
        if any(t["n_items"] for t in b["temas"]):
            opciones.append((f"Bloque {romano(b['numero'])} · {b['nombre']}", ("bloque", b["id"])))
    for b in listar_bloques_temas():
        for t in b["temas"]:
            if t["n_items"]:
                opciones.append((f"Tema {t['numero']}: {t['titulo']}", ("tema", t["id"])))
    return opciones


def pantalla_practicar():
    cabecera("Practicar", "Elige qué quieres entrenar y cuánto.", "Práctica libre")

    tipo = st.radio("Tipo", list(TIPOS_PRACTICA), format_func=TIPOS_PRACTICA.get,
                    key="tipo_practica", label_visibility="collapsed")
    st.write("")

    ambitos = opciones_ambito()
    etiquetas = [a[0] for a in ambitos]
    if st.session_state.get("prac_ambito") not in etiquetas:
        st.session_state["prac_ambito"] = etiquetas[0]

    items_fn, titulo, disponibles = None, "", 0
    with card("card_lanzador"):
        ambito, dificultad = ("todo", None), None
        if tipo == "preparado":
            tests = consulta("SELECT * FROM tests_practica ORDER BY fecha_generacion DESC, id DESC")
            if not tests:
                st.info("Todavía no hay tests preparados.")
                return
            mapa = {f"{t['tipo'].capitalize()} · {t['fecha_generacion']} · {t['n_preguntas']} preguntas": t["id"]
                    for t in tests}
            sel = st.selectbox("Test", list(mapa))
            test_id = mapa[sel]
            disponibles = consulta("SELECT COUNT(*) FROM test_practica_preguntas WHERE test_id = ?", (test_id,))[0][0]
            items_fn = lambda n: cargar_test_preparado(test_id)
            titulo = "Test preparado"
        elif tipo == "debiles":
            disponibles = consulta("""SELECT COUNT(*) FROM srs_items
                WHERE veces_fallada > 0 OR ultima_respuesta IN ('otra_vez', 'dificil')""")[0][0]
            items_fn = lambda n: cargar_items_debiles(n)
            titulo = "Puntos débiles"
            st.caption("Ítems que has fallado o marcado como difíciles, los más fallados primero.")
        else:
            etiqueta_a = st.selectbox("Ámbito", etiquetas, key="prac_ambito")
            ambito = dict(ambitos)[etiqueta_a]
            if tipo in ("test", "mixto"):
                st.caption("Dificultad")
                d = st.radio("Dificultad", ["Todas", "Baja", "Media", "Alta"], horizontal=True,
                             label_visibility="collapsed", key="pill_dificultad")
                dificultad = None if d == "Todas" else d.lower()
            disponibles = contar_disponibles(tipo, ambito, dificultad)
            titulo = {"test": "Test", "flash": "Flashcards", "cuadros": "Cuadros", "mixto": "Mixto"}[tipo]

            def items_fn(n, tipo=tipo, ambito=ambito, dificultad=dificultad):
                if tipo == "test":
                    return cargar_tests(ambito, dificultad, n)
                if tipo == "flash":
                    return cargar_flashcards(ambito, n)
                if tipo == "cuadros":
                    return cargar_cuadros(ambito, n)
                mezcla = (cargar_tests(ambito, dificultad, n) + cargar_flashcards(ambito, n)
                          + cargar_cuadros(ambito, n))
                random.shuffle(mezcla)
                return mezcla[:n]

        if disponibles == 0:
            st.warning("No hay ítems con esos filtros.")
            return

        if tipo == "preparado":
            n = disponibles
            st.caption(f"{disponibles} preguntas en este test, en el orden original.")
        else:
            tope = min(50, disponibles)
            if tope > 5:
                n = st.slider("Número de ítems", 5, tope, min(20, tope), 5)
            else:
                n = tope
            st.caption(f"{disponibles} ítems disponibles.")

        if st.button(f"▶  Empezar · {n} ítems", type="primary", use_container_width=True, key="go_practica"):
            if iniciar(items_fn(n), titulo):
                st.rerun()
            st.warning("No hay ítems con esos filtros.")


# ============================================================
# PÁGINA: TEMARIO
# ============================================================

def pantalla_temario():
    cabecera("Temario", "Tu progreso tema a tema.", "Programa")
    for b in listar_bloques_temas():
        st.markdown(
            f'<div class="bloque"><span class="n">{romano(b["numero"])}</span>'
            f'<span class="t">{esc(b["nombre"])}</span></div>'
            f'<div class="d" style="color:var(--muted);font-size:.82rem;margin:-.4rem 0 .7rem 0">{esc(b["descripcion"] or "")}</div>',
            unsafe_allow_html=True)
        pendientes = []
        for t in b["temas"]:
            if t["n_items"] == 0:
                pendientes.append(t)
                continue
            pct = round(t["n_dom"] / t["n_items"] * 100)
            c1, c2 = st.columns([5, 1.5], vertical_alignment="center")
            with c1:
                st.markdown(
                    f'<div class="row"><div class="t">Tema {t["numero"]} · {esc(t["titulo"])}</div>'
                    f'<div class="m">{t["n_items"]} ítems · {pct}% dominado · {t["n_hoy"]} para hoy</div>'
                    f'{barra_estados(t["n_dom"], t["n_prog"], t["n_porap"], t["n_nuevo"])}</div>',
                    unsafe_allow_html=True)
            with c2:
                st.button("Practicar", key=f"prac_{t['id']}", use_container_width=True,
                          on_click=_ir_a, args=(PAGINAS[1],),
                          kwargs={"tipo_practica": "mixto",
                                  "prac_ambito": f"Tema {t['numero']}: {t['titulo']}"})
        if pendientes:
            with st.expander(f"Temas pendientes de incorporar ({len(pendientes)})"):
                for t in pendientes:
                    st.markdown(f'<div class="m" style="color:var(--muted);padding:.15rem 0">'
                                f'Tema {t["numero"]} · {esc(t["titulo"])}</div>', unsafe_allow_html=True)


# ============================================================
# PÁGINA: MATERIAL (cuadros y esquemas)
# ============================================================

def html_mermaid(codigo, oscuro):
    p = PALETAS["oscuro" if oscuro else "claro"]
    tema = "dark" if oscuro else "neutral"
    return f"""
    <body style="margin:0;background:{p['surface']};color:{p['text']};font-family:Inter,system-ui,sans-serif">
    <pre class="mermaid" style="background:{p['surface']}">{html.escape(codigo)}</pre>
    <script type="module">
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
      mermaid.initialize({{startOnLoad: true, theme: '{tema}'}});
    </script></body>"""


def pantalla_material():
    cabecera("Material", "Cuadros de datos y esquemas para estudiar con calma.", "Estudio")
    tab_c, tab_e = st.tabs(["🗂️ Cuadros", "🧠 Esquemas"])

    with tab_c:
        cuadros = consulta("""SELECT cu.*, t.numero AS tema_numero FROM cuadros cu
                              LEFT JOIN temas t ON t.id = cu.tema_id ORDER BY cu.tema_id, cu.id""")
        if not cuadros:
            st.info("No hay cuadros todavía.")
        for cu in cuadros:
            cols = _parse_json(cu["columnas"], [])
            filas = consulta("SELECT * FROM cuadro_filas WHERE cuadro_id = ? ORDER BY id", (cu["id"],))
            cab = "".join(f"<th>{esc(str(c).replace('_', ' '))}</th>" for c in cols) + "<th>Fuente</th>"
            cuerpo = ""
            for f in filas:
                v = _parse_json(f["valores"], {})
                cuerpo += "<tr>" + "".join(f"<td>{esc(v.get(c, ''))}</td>" for c in cols) \
                          + f'<td class="f">{esc(f["fuente"] or "")}</td></tr>'
            st.markdown(f"### {cu['titulo']}")
            st.markdown(f'<table class="tabla"><thead><tr>{cab}</tr></thead><tbody>{cuerpo}</tbody></table>',
                        unsafe_allow_html=True)
            st.write("")
            if st.button(f"Memorizar este cuadro ({len(filas)} filas)", key=f"mem_{cu['id']}"):
                if iniciar(cargar_cuadros(("todo", None), 50, cuadro_id=cu["id"]), cu["titulo"]):
                    st.rerun()

    with tab_e:
        esquemas = consulta("""SELECT e.*, t.titulo AS tema_titulo FROM esquemas e
                               LEFT JOIN temas t ON t.id = e.tema_id ORDER BY e.id""")
        if not esquemas:
            st.info("No hay esquemas todavía.")
        for e in esquemas:
            st.markdown(f"### {e['tema_titulo'] or e['id']}")
            if e["formato"] in ("mindmap", "mermaid", "flowchart", "graph"):
                embed_html(html_mermaid(e["contenido"], bool(st.session_state.get("oscuro"))), 520)
            else:
                st.markdown(e["contenido"])
            with st.expander("Ver código fuente"):
                st.code(e["contenido"], language="text")


# ============================================================
# PÁGINA: PROGRESO
# ============================================================

def pantalla_progreso():
    s = stats_globales()
    cabecera("Progreso", "Constancia, precisión y puntos débiles.", "Seguimiento")

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(stat_card("Racha", f"🔥 {s['racha']}", "accent" if s["racha"] else ""), unsafe_allow_html=True)
    c2.markdown(stat_card("Ítems", s["n"]), unsafe_allow_html=True)
    c3.markdown(stat_card("Dominados", s["dom"], "ok"), unsafe_allow_html=True)
    prec = f"{s['precision']:.0f}%" if s["precision"] is not None else "—"
    c4.markdown(stat_card("Precisión", prec), unsafe_allow_html=True)
    st.write("")

    datos = actividad(14)
    mx = max((n for _, n in datos), default=0) or 1
    barras = "".join(
        f'<div class="c" title="{n} respuestas"><div class="b {"zero" if n == 0 else ""}" '
        f'style="height:{max(n / mx * 100, 2):.0f}%"></div><span>{d.day}</span></div>' for d, n in datos)
    with card("card_actividad"):
        st.markdown(f"**Actividad · últimos 14 días** &nbsp; <span style='color:var(--muted)'>"
                    f"{sum(n for _, n in datos)} respuestas</span>", unsafe_allow_html=True)
        st.markdown(f'<div class="spark">{barras}</div>', unsafe_allow_html=True)

    st.markdown("### Puntos débiles")
    filas = consulta(SQL_SRS + """
        WHERE s.veces_fallada > 0 ORDER BY s.veces_fallada DESC LIMIT 8""")
    debiles = [(f, _fila_a_item(f)) for f in filas]
    debiles = [(f, i) for f, i in debiles if i]
    if not debiles:
        st.markdown('<div class="row muted">Todavía no hay fallos registrados. ¡Buen comienzo!</div>',
                    unsafe_allow_html=True)
    else:
        for f, i in debiles:
            q, a = resumen_item(i)
            st.markdown(
                f'<div class="row" style="margin-bottom:.5rem"><div class="t">{esc(q)}</div>'
                f'<div class="m" style="margin:.3rem 0 0 0">✔ {esc(a)} · '
                f'fallada {f["veces_fallada"]}×, acertada {f["veces_acertada"]}×</div></div>',
                unsafe_allow_html=True)
        st.button("🎯  Practicar mis puntos débiles", type="primary", use_container_width=True,
                  key="go_debiles", on_click=_ir_a, args=(PAGINAS[1],), kwargs={"tipo_practica": "debiles"})


# ============================================================
# SIDEBAR
# ============================================================

def sidebar():
    s = stats_globales()
    st.sidebar.markdown(
        '<div class="brand"><div class="logo">🎓</div><div><div class="name">TAI Oposición</div>'
        '<div class="sub">Sistema de estudio</div></div></div>', unsafe_allow_html=True)

    with st.sidebar.container(key="nav"):
        st.radio("Navegación", PAGINAS, key="pagina", label_visibility="collapsed", on_change=_nav_cambiada)

    st.sidebar.markdown(
        f'<div class="side-stats"><div><b>🔥 {s["racha"]}</b><small>racha</small></div>'
        f'<div><b>{s["hoy"]}</b><small>para hoy</small></div></div>', unsafe_allow_html=True)

    st.sidebar.divider()
    st.sidebar.toggle("🌙  Modo oscuro", key="oscuro")
    st.sidebar.caption(f"Versión 0.3 · BD: {DB_PATH.name}")


# ============================================================
# MAIN
# ============================================================

def tema_inicial():
    """Primer arranque: respeta el tema del navegador si Streamlit lo expone."""
    if "oscuro" in st.session_state:
        return
    oscuro = False
    try:
        oscuro = st.context.theme.type == "dark"
    except Exception:
        pass
    st.session_state["oscuro"] = oscuro


def main():
    if not DB_PATH.exists():
        st.error(f"No se encuentra la base de datos en `{DB_PATH}`.")
        st.stop()

    tema_inicial()
    st.session_state.setdefault("pagina", PAGINAS[0])
    sidebar()
    inyectar_tema()

    modo = st.session_state.get("modo")
    if modo == "sesion":
        pantalla_sesion()
    elif modo == "resumen":
        pantalla_resumen()
    else:
        {
            PAGINAS[0]: pantalla_hoy,
            PAGINAS[1]: pantalla_practicar,
            PAGINAS[2]: pantalla_temario,
            PAGINAS[3]: pantalla_material,
            PAGINAS[4]: pantalla_progreso,
        }[st.session_state["pagina"]]()


if __name__ == "__main__":
    main()
