#!/usr/bin/env python3
"""
app_v5.py — TAI Oposición (Streamlit). Interfaz nueva: barra superior, hoja de examen con óvalos,
subrayador amarillo como único acento. Misma lógica de datos que la v4.

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

# ============================================================
# CONFIGURACIÓN
# ============================================================

ROOT = Path.home() / "oposicion"
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

PAGINAS = ["Hoy", "Practicar", "Temario", "Material", "Progreso"]
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

st.set_page_config(
    page_title="TAI Oposición",
    page_icon="✏️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# TEMA (CLARO / OSCURO)
#   claro  = papel de cuaderno con subrayador amarillo
#   oscuro = pizarra verde con tiza y el mismo subrayador
# ============================================================

PALETAS = {
    "claro": {
        "bg": "#F1F3EF", "surface": "#FFFFFF", "surface2": "#E6EAE5",
        "text": "#14201B", "muted": "#58675F", "border": "#CDD5CF",
        "mark": "#FFD43B", "mark_soft": "#FFF0AD", "on_mark": "#14201B",
        "ok": "#1E8E4E", "ok_bg": "#DDF3E6", "ok_text": "#146B3A",
        "bad": "#C93A2E", "bad_bg": "#FBE3E0", "bad_text": "#A12A20",
        "warn": "#B26A00", "warn_bg": "#FFEACB",
        "margen": "#E9B7B1",
        "scheme": "light",
    },
    "oscuro": {
        "bg": "#14211C", "surface": "#1C2D26", "surface2": "#263A31",
        "text": "#EBF1ED", "muted": "#9FB3A9", "border": "#34493F",
        "mark": "#FFD43B", "mark_soft": "#4A4519", "on_mark": "#14201B",
        "ok": "#62D48D", "ok_bg": "#1A3A28", "ok_text": "#7FE0A3",
        "bad": "#FF8F80", "bad_bg": "#432220", "bad_text": "#FF9F92",
        "warn": "#FFC45C", "warn_bg": "#43361A",
        "margen": "#5B3A38",
        "scheme": "dark",
    },
}

CSS_BASE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,500..900&family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&display=swap');

:root { --display: "Archivo", "Arial Narrow", system-ui, sans-serif;
        --cuerpo: "Atkinson Hyperlegible", "Segoe UI", system-ui, -apple-system, sans-serif; }

/* ---------- Base ---------- */
html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: var(--bg) !important; color: var(--text); color-scheme: var(--scheme);
}
.stApp, .stApp p, .stApp label, .stApp li, .stApp button, .stApp input, .stApp textarea, .stApp td, .stApp th {
    font-family: var(--cuerpo);
}
[data-testid="stHeader"], [data-testid="stDecoration"], [data-testid="stAppDeployButton"],
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], footer { display: none !important; }
[data-testid="stElementContainer"]:has(> [data-testid="stMarkdown"] style),
[data-testid="stElementContainer"]:has(> [data-testid="stHtml"] style) { display: none; }
.block-container { padding-top: 1.1rem; padding-bottom: 5rem; max-width: 1120px; }
.stApp p, .stApp li, .stMarkdown { color: var(--text); }
[data-testid="stCaptionContainer"], .stApp small { color: var(--muted) !important; }
hr { border-color: var(--border) !important; opacity: 1 !important; }
.stApp h1, .stApp h2, .stApp h3, .stApp h4 { font-family: var(--display); color: var(--text) !important;
    font-stretch: 112%; font-variation-settings: "wdth" 112; letter-spacing: -.01em; }
h3 { font-size: 1.25rem !important; font-weight: 800 !important; margin: 1.6rem 0 .5rem 0 !important; padding: 0 !important; }
:focus-visible { outline: 3px solid var(--mark) !important; outline-offset: 2px; }
@media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } }

/* ---------- Barra superior ---------- */
.st-key-topbar { border-bottom: 2px solid var(--text); padding-bottom: .55rem; margin-bottom: 1.8rem; }
.marca { font-family: var(--display); font-weight: 900; font-stretch: 125%; font-variation-settings: "wdth" 125;
    font-size: 1.35rem; line-height: 1; letter-spacing: -.01em; white-space: nowrap; }
.marca b { background: var(--mark); color: var(--on_mark); padding: .12em .32em .1em; border-radius: 3px; margin-right: .3em; }
.marca span { font-weight: 600; font-stretch: 100%; font-variation-settings: "wdth" 100; }
.sesion-titulo { font-weight: 700; color: var(--muted); }

/* radios sin círculo: navegación, segmentos y menú */
[class*="st-key-nav"] label[data-testid="stRadioOption"] > div > div:first-child,
[class*="st-key-pill_"] label[data-testid="stRadioOption"] > div > div:first-child,
[class*="st-key-tipo"] label[data-testid="stRadioOption"] > div > div:first-child,
[class*="st-key-nav"] [data-baseweb="radio"] > div:first-child,
[class*="st-key-pill_"] [data-baseweb="radio"] > div:first-child,
[class*="st-key-tipo"] [data-baseweb="radio"] > div:first-child { display: none; }

[class*="st-key-nav"] div[role="radiogroup"] { gap: .1rem; flex-wrap: wrap; }
[class*="st-key-nav"] label { padding: .35rem .8rem; border-radius: 4px; cursor: pointer; }
[class*="st-key-nav"] label p { font-weight: 700; font-size: 1rem; color: var(--muted) !important; }
[class*="st-key-nav"] label:hover p { color: var(--text) !important; }
[class*="st-key-nav"] label:has(input:checked) { background: linear-gradient(transparent 58%, var(--mark) 58%, var(--mark) 92%, transparent 92%); }
[class*="st-key-nav"] label:has(input:checked) p { color: var(--text) !important; }

/* segmentos (tamaño, procedencia, dificultad, orden) */
[class*="st-key-pill_"] div[role="radiogroup"] { gap: 0; flex-wrap: wrap; }
[class*="st-key-pill_"] label { padding: .4rem 1rem; border: 1.5px solid var(--text); margin-left: -1.5px; cursor: pointer;
    background: var(--surface); }
[class*="st-key-pill_"] label:first-of-type { border-radius: 6px 0 0 6px; margin-left: 0; }
[class*="st-key-pill_"] label:last-of-type { border-radius: 0 6px 6px 0; }
[class*="st-key-pill_"] label:hover { background: var(--mark_soft); }
[class*="st-key-pill_"] label:has(input:checked) { background: var(--mark); }
[class*="st-key-pill_"] label p { font-weight: 700; color: var(--text) !important; }
[class*="st-key-pill_"] label:has(input:checked) p { color: var(--on_mark) !important; }

/* menú de tipos de práctica */
[class*="st-key-tipo"] div[role="radiogroup"] { gap: 0; width: 100%; flex-direction: column; align-items: stretch; }
[class*="st-key-tipo"] label[data-testid="stRadioOption"] { display: flex; width: 100%; box-sizing: border-box; padding: .72rem 1rem; cursor: pointer;
    border-left: 5px solid transparent; border-bottom: 1px solid var(--border); border-radius: 0; }
[class*="st-key-tipo"] label p { font-weight: 700; font-size: 1.02rem; }
[class*="st-key-tipo"] label[data-testid="stRadioOption"]:hover { background: var(--surface2); }
[class*="st-key-tipo"] label[data-testid="stRadioOption"]:has(input:checked) { background: var(--surface); border-left-color: var(--mark); }

/* ---------- Titulares y paneles ---------- */
.titular { font-family: var(--display); font-weight: 800; font-stretch: 118%; font-variation-settings: "wdth" 118;
    font-size: clamp(1.9rem, 4.6vw, 3.1rem); line-height: 1.04; letter-spacing: -.02em; margin: 0 0 .5rem 0; text-wrap: balance; }
.titular.menor { font-size: clamp(1.6rem, 3.4vw, 2.3rem); }
.fecha { color: var(--muted); font-weight: 700; margin: 0 0 .5rem 0; }
.fecha::first-letter { text-transform: uppercase; }
.lead { color: var(--muted); font-size: 1.08rem; margin: 0 0 1.4rem 0; max-width: 46ch; }

[class*="st-key-panel_"] { background: var(--surface); border: 1px solid var(--border); border-radius: 8px;
    padding: 1.3rem 1.4rem; margin-bottom: 1.1rem; }
[class*="st-key-panel_"] > div { gap: .7rem; }
.sub { font-family: var(--display); font-weight: 800; font-stretch: 112%; font-variation-settings: "wdth" 112;
    font-size: 1.05rem; margin: 0 0 .1rem 0; }
.nota { color: var(--muted); font-size: .92rem; }

.cifras { display: flex; flex-wrap: wrap; margin: .4rem 0 1.4rem 0; }
.cifras > div { padding: 0 1.6rem 0 0; margin-right: 1.6rem; border-right: 1.5px solid var(--border); }
.cifras > div:last-child { border-right: 0; }
.cifras b { display: block; font-family: var(--display); font-size: 1.9rem; font-weight: 800; line-height: 1.1;
    font-stretch: 112%; font-variation-settings: "wdth" 112; font-variant-numeric: tabular-nums; }
.cifras span { color: var(--muted); font-size: .9rem; }

.tag { display: inline-block; font-size: .82rem; font-weight: 700; padding: .12rem .55rem; border: 1.5px solid var(--border);
    border-radius: 4px; color: var(--muted); margin: 0 .35rem .45rem 0; }
.tag.fuerte { background: var(--mark); border-color: var(--mark); color: var(--on_mark); }
.tag.aviso { background: var(--warn_bg); border-color: var(--warn_bg); color: var(--warn); }
.chips { display: flex; flex-wrap: wrap; gap: .3rem .9rem; margin: .3rem 0 .6rem 0; color: var(--muted); font-size: .9rem; }
.chips .aviso { color: var(--warn); font-weight: 700; }

/* ---------- Hoja de examen ---------- */
.hoja { position: relative; background: var(--surface); border: 1.5px solid var(--text); border-radius: 10px;
    padding: 1.5rem 1.7rem 1.5rem 3.2rem; margin-bottom: 1rem;
    background-image: linear-gradient(90deg, transparent 2.2rem, var(--margen) 2.2rem, var(--margen) calc(2.2rem + 2px), transparent calc(2.2rem + 2px));
    box-shadow: 4px 4px 0 var(--text); }
.hoja .q { font-size: 1.28rem; font-weight: 700; line-height: 1.5; }
.hoja .hint { color: var(--muted); margin-top: .5rem; }
.hoja .back { font-size: 1.12rem; line-height: 1.6; }
.hoja .divider { height: 0; border-top: 2px dashed var(--border); margin: 1.1rem 0; }
.hoja .ref { color: var(--muted); font-size: .9rem; margin-top: .6rem; }
.blank { display: inline-block; min-width: 2.2rem; text-align: center; font-weight: 800; color: var(--on_mark);
    background: var(--mark); border-radius: 3px; padding: 0 .5rem; margin: 0 .15rem; }
.fill { display: inline-block; font-weight: 700; padding: 0 .45rem; border-radius: 3px; margin: 0 .1rem; }
.fill.ok { background: var(--ok_bg); color: var(--ok_text); }
.fill.bad { background: var(--bad_bg); color: var(--bad_text); }
.fill s { opacity: .7; font-weight: 400; margin-right: .3rem; }

/* texto del supuesto */
.enunciado { background: var(--mark_soft); border-radius: 8px; padding: 1rem 1.2rem; line-height: 1.6; max-height: 70vh; overflow: auto; }
.enunciado-t { font-family: var(--display); font-weight: 800; margin: 0 0 .4rem 0; }

/* ---------- Opciones ---------- */
.opt { display: flex; gap: .85rem; align-items: flex-start; padding: .75rem 1rem; margin-bottom: .5rem;
    border: 1.5px solid var(--border); border-radius: 8px; background: var(--surface); line-height: 1.45; }
.opt .letter { flex: 0 0 auto; width: 2.1rem; height: 1.5rem; border-radius: 999px; border: 1.5px solid var(--muted);
    display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: .88rem; color: var(--muted); margin-top: .05rem; }
.opt.ok { border-color: var(--ok); background: var(--ok_bg); }
.opt.ok .letter { background: var(--ok); border-color: var(--ok); color: var(--bg); }
.opt.bad { border-color: var(--bad); background: var(--bad_bg); }
.opt.bad .letter { background: var(--bad); border-color: var(--bad); color: var(--bg); }
.opt .note { margin-left: auto; font-size: .85rem; font-weight: 700; white-space: nowrap; }
.opt.ok .note { color: var(--ok_text); }
.opt.bad .note { color: var(--bad_text); }
.opt.dim { opacity: .55; }
.veredicto { font-family: var(--display); font-weight: 800; font-size: 1.2rem; margin: 1rem 0 .6rem 0; }
.veredicto small { font-family: var(--cuerpo); font-weight: 400; margin-left: .6rem; }
.veredicto.ok { color: var(--ok_text); }
.veredicto.bad { color: var(--bad_text); }
.expl { border-left: 4px solid var(--mark); padding: .3rem 0 .3rem 1rem; line-height: 1.6; margin: 0 0 1rem 0; }
.expl .ref { color: var(--muted); font-size: .9rem; margin-top: .4rem; }
.atajos { color: var(--muted); font-size: .85rem; margin-top: 1rem; }
.atajos kbd { background: var(--surface); border: 1.5px solid var(--border); border-bottom-width: 3px; border-radius: 4px;
    padding: 0 .4rem; font-family: var(--cuerpo); font-size: .82rem; }

/* ---------- Sesión: tira de marcas ---------- */
.tira { display: flex; gap: 2px; align-items: center; overflow: hidden; }
.tira i { flex: 1 1 0; height: 12px; min-width: 0; border-radius: 2px; background: var(--surface2); }
.tira i.ok { background: var(--ok); }
.tira i.bad { background: var(--bad); }
.tira i.ahora { background: var(--mark); box-shadow: 0 0 0 2px var(--text); }
.cuenta { font-variant-numeric: tabular-nums; color: var(--muted); font-weight: 700; white-space: nowrap; }
.cuenta b { color: var(--text); }

/* ---------- Barras y mapa ---------- */
.sbar { display: flex; height: 12px; border-radius: 3px; overflow: hidden; background: var(--surface2); gap: 2px; }
.sbar span { display: block; height: 100%; }
.sbar.fina { height: 6px; }
.legend { display: flex; flex-wrap: wrap; gap: .3rem 1.2rem; margin-top: .7rem; font-size: .9rem; color: var(--muted); }
.legend i { display: inline-block; width: .8rem; height: .8rem; border-radius: 2px; margin-right: .4rem; vertical-align: -1px; }
.mapa { display: grid; grid-template-columns: repeat(7, 1fr); gap: 5px; }
.mapa i { aspect-ratio: 1; border-radius: 4px; display: flex; align-items: center; justify-content: center;
    font-style: normal; font-size: .78rem; font-weight: 700; color: var(--muted); }
.mapa i.hoy { outline: 2px solid var(--text); outline-offset: 1px; }
.mapa i.n { color: var(--on_mark); }

/* ---------- Listas (bloques, temas, fallos) ---------- */
.fila-bloque { display: grid; grid-template-columns: minmax(10rem, 17rem) 1fr 5rem; gap: 1rem; align-items: center;
    padding: .65rem 0; border-bottom: 1px solid var(--border); }
.fila-bloque .t { font-weight: 700; }
.fila-bloque .m { color: var(--muted); font-size: .88rem; }
.fila-bloque .p { text-align: right; font-weight: 800; font-family: var(--display); font-variant-numeric: tabular-nums; }
@media (max-width: 640px) { .fila-bloque { grid-template-columns: 1fr 3.5rem; } .fila-bloque .barra { grid-column: 1 / -1; order: 3; } }
.bloque { display: flex; align-items: baseline; gap: .8rem; margin: 2rem 0 .2rem 0; }
.bloque .n { font-family: var(--display); font-weight: 900; font-size: 1.6rem; background: var(--mark); color: var(--on_mark);
    padding: 0 .5rem; border-radius: 3px; }
.bloque .t { font-family: var(--display); font-weight: 800; font-stretch: 112%; font-variation-settings: "wdth" 112; font-size: 1.2rem; }
.tema { padding: .7rem 0 .8rem 0; border-bottom: 1px solid var(--border); }
.tema.vacio { opacity: .6; }
.tema .t { font-weight: 700; line-height: 1.35; }
.tema .t b { font-family: var(--display); font-weight: 900; margin-right: .5rem; }
.tema .m { color: var(--muted); font-size: .9rem; margin: .15rem 0 .45rem 0; }
.peso { height: 4px; background: var(--surface2); border-radius: 2px; margin: .1rem 0 .5rem 0; max-width: 14rem; }
.peso > div { height: 100%; background: var(--text); border-radius: 2px; }
.fallo { padding: .7rem 0; border-bottom: 1px solid var(--border); }
.fallo .t { font-weight: 700; }
.fallo .m { color: var(--muted); font-size: .9rem; margin-top: .2rem; }
.fallo .m b { color: var(--ok_text); }
.grande { font-family: var(--display); font-weight: 900; font-stretch: 125%; font-variation-settings: "wdth" 125;
    font-size: clamp(4rem, 12vw, 7rem); line-height: .95; letter-spacing: -.03em; }
.grande small { font-size: 1.6rem; }

/* ---------- Tablas (cuadros) ---------- */
.tabla-wrap { overflow-x: auto; }
table.tabla { width: 100%; border-collapse: collapse; font-size: .96rem; }
table.tabla th { text-align: left; font-weight: 800; padding: .55rem .8rem; border-bottom: 2px solid var(--text); white-space: nowrap; }
table.tabla td { padding: .55rem .8rem; border-bottom: 1px solid var(--border); vertical-align: top; }
table.tabla tr:nth-child(even) td { background: color-mix(in srgb, var(--surface2) 45%, transparent); }
table.tabla td.f { color: var(--muted); font-size: .84rem; white-space: nowrap; }

/* ---------- Botones ---------- */
.stButton > button, [data-testid="stFormSubmitButton"] > button, [data-testid="stPopover"] > button {
    border-radius: 6px; border: 1.5px solid var(--text); background: var(--surface); color: var(--text);
    padding: .55rem 1.1rem; font-weight: 700; transition: background .12s; box-shadow: none; min-height: 2.6rem; }
.stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover, [data-testid="stPopover"] > button:hover {
    background: var(--mark_soft); border-color: var(--text); color: var(--text); }
.stButton > button p, [data-testid="stFormSubmitButton"] > button p, [data-testid="stPopover"] > button p { color: inherit !important; font-weight: 700; }
.stButton > button[kind="primary"], [data-testid="stFormSubmitButton"] > button[kind="primaryFormSubmit"] {
    background: var(--mark); color: var(--on_mark); border-color: var(--text); box-shadow: 0 3px 0 var(--text); }
.stButton > button[kind="primary"]:hover, [data-testid="stFormSubmitButton"] > button[kind="primaryFormSubmit"]:hover {
    background: var(--mark); filter: brightness(1.05); }
.stButton > button[kind="primary"]:active { transform: translateY(3px); box-shadow: none; }
.stButton > button:disabled { opacity: .45; }
[class*="st-key-opt_"] button { justify-content: flex-start; text-align: left; padding: .75rem 1rem; border-color: var(--border);
    border-width: 1.5px; min-height: 3rem; }
[class*="st-key-opt_"] button:hover { border-color: var(--text); }
[class*="st-key-opt_"] button > div, [class*="st-key-opt_"] button span { justify-content: flex-start !important; width: 100%; text-align: left; }
[class*="st-key-opt_"] button [data-testid="stMarkdownContainer"], [class*="st-key-opt_"] button p {
    display: block !important; white-space: normal !important; overflow: visible !important; text-overflow: clip !important;
    -webkit-line-clamp: unset !important; -webkit-box-orient: initial !important; width: 100%; }
[class*="st-key-opt_"] button p { text-align: left; font-weight: 400; font-size: 1.03rem; line-height: 1.45; }
[class*="st-key-opt_"] button p::first-letter { font-weight: 800; font-size: .9rem; border: 1.5px solid var(--muted); border-radius: 999px;
    padding: .05rem .7rem; margin-right: .5rem; color: var(--muted); }
[class*="st-key-opt_"] button:hover p::first-letter { background: var(--mark); border-color: var(--text); color: var(--on_mark); }
[class*="st-key-salir"] button { border-color: transparent; background: transparent; color: var(--muted); text-decoration: underline; }
[class*="st-key-go_"] button, [class*="st-key-sig_"] button, [class*="st-key-sigc_"] button, [class*="st-key-rev_"] button { min-height: 3.1rem; font-size: 1.05rem; }

/* ---------- Inputs ---------- */
.stTextInput input, [data-baseweb="select"] > div, [data-baseweb="input"], [data-baseweb="base-input"] {
    background: var(--surface) !important; color: var(--text) !important; border-color: var(--text) !important; border-radius: 6px !important; }
.stTextInput input { border: 1.5px solid var(--text) !important; }
[data-baseweb="select"] svg { fill: var(--text); }
[data-baseweb="popover"] *, ul[role="listbox"] { background: var(--surface) !important; color: var(--text) !important; }
[data-testid="stPopoverBody"], [data-testid="stPopoverBody"] > div { background: var(--surface) !important; color: var(--text) !important; }
[data-testid="stPopoverBody"] { border: 1.5px solid var(--text); border-radius: 8px; }
[data-testid="stPopoverBody"] label, [data-testid="stPopoverBody"] p, [data-testid="stPopoverBody"] [data-testid="stWidgetLabel"] * { color: var(--text) !important; }
[data-testid="stPopoverBody"] [data-testid="stCaptionContainer"] * { color: var(--muted) !important; }
[data-testid="stNumberInput"] input { color: var(--text) !important; background: var(--surface2) !important; }
::placeholder { color: var(--muted) !important; opacity: 1 !important; }
li[role="option"]:hover, li[aria-selected="true"] { background: var(--mark_soft) !important; }
[data-testid="stSlider"] { filter: hue-rotate(48deg) saturate(1.4); }
[data-testid="stSlider"] [data-testid="stSliderThumbValue"] { color: var(--text) !important; font-weight: 800; }
[data-testid="stForm"] { border: none !important; padding: 0 !important; background: transparent !important; }
[data-testid="stCheckbox"] label p { color: var(--text) !important; }
[data-testid="stCheckbox"] label:has(input:checked) > div:nth-of-type(1) { background: var(--text) !important; }
[data-testid="stWidgetLabel"] p { font-weight: 700; color: var(--text) !important; }

/* ---------- Pestañas / expanders / alertas ---------- */
[data-baseweb="tab-list"] { gap: .3rem; border-bottom: 2px solid var(--text); }
[data-baseweb="tab"], [data-testid="stTab"] { background: transparent !important; }
[data-baseweb="tab"] p, [data-testid="stTab"] p { color: var(--muted) !important; font-weight: 800; font-size: 1rem; }
[data-baseweb="tab"][aria-selected="true"] p, [data-testid="stTab"][aria-selected="true"] p { color: var(--text) !important; }
[data-baseweb="tab-highlight"], .react-aria-SelectionIndicator { background: var(--mark) !important; height: 5px !important; }
[data-baseweb="tab-border"] { background: transparent !important; }
[data-testid="stExpander"] { background: var(--surface); border: 1px solid var(--border) !important; border-radius: 8px; box-shadow: none; }
[data-testid="stExpander"] summary, [data-testid="stExpander"] summary * { color: var(--text) !important; font-weight: 700; }
[data-testid="stAlert"] { border-radius: 8px; border: 1.5px solid var(--text); background: var(--mark_soft); }
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
      var opts = btns.filter(function (b) { return /^[A-D]\\s/.test(txt(b)); });
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


def panel(key):
    """Contenedor con aspecto de panel (la clave aplica el estilo)."""
    try:
        return st.container(key=f"panel_{key}")
    except TypeError:
        return st.container(border=True)


def num(x, dec=1):
    """Número con coma decimal."""
    return f"{x:.{dec}f}".replace(".", ",")


def barra_estados(dom, prog, porap, nuevo, fina=False):
    total = dom + prog + porap + nuevo
    cls = "sbar fina" if fina else "sbar"
    if total == 0:
        return f'<div class="{cls}"></div>'

    def seg(n, c):
        return f'<span style="width:{n / total * 100:.2f}%;background:var(--{c})"></span>' if n else ""

    return f'<div class="{cls}">{seg(dom, "ok")}{seg(prog, "text")}{seg(porap, "mark")}{seg(nuevo, "border")}</div>'


def leyenda(dom, prog, porap, nuevo):
    def it(c, n, t):
        return f'<span><i style="background:var(--{c})"></i>{n} {t}</span>'

    return ('<div class="legend">' + it("ok", dom, "dominados") + it("text", prog, "en progreso")
            + it("mark", porap, "por aprender") + it("border", nuevo, "sin empezar") + "</div>")


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


def plural(n, uno, varios):
    return f"{n} {uno if n == 1 else varios}"


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


def en_lote(sql, ids, extra=()):
    """Ejecuta `sql` (con el marcador {ids}) por trozos para no pasarse del límite de variables."""
    ids, filas = list(ids), []
    for i in range(0, len(ids), 500):
        trozo = ids[i:i + 500]
        filas += consulta(sql.replace("{ids}", ",".join("?" * len(trozo))), list(extra) + trozo)
    return filas


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


def actualizar_srs(item_key, respuesta, espejos=()):
    """Actualiza un ítem del SRS. Devuelve dict con el resultado.

    `espejos`: claves de fichas gemelas (p. ej. `sup:<pregunta>` de una pregunta que también
    tiene su ficha `test:`). Reciben el mismo estado, sin duplicar el historial.
    """
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

    for clave in (item_key, *espejos):
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
            clave,
        ))
    conn.execute("""
        INSERT INTO srs_historial (item_key, fecha, respuesta, intervalo)
        VALUES (?, ?, ?, ?)
    """, (item_key, hoy_iso(), respuesta, nuevo_intervalo))
    conn.commit()
    return {"intervalo": nuevo_intervalo, "estado": nuevo_estado}


# ============================================================
# AJUSTES Y FILTROS DEL SRS
# ============================================================
#
# Formatos de item_key en srs_items:
#   test:<tema>:<pregunta>   card:<tema>:<flashcard>   cloze:<tema>:<flashcard>
#   cuadro:<tema>:<fila>     sup:<pregunta>  (ficha gemela de una pregunta de supuesto; sin tema)
# Las preguntas de supuesto tienen DOS fichas (test: y sup:). Se trabaja con la test: y la sup:
# se mantiene sincronizada, así que las estadísticas ignoran las sup: para no contar doble.

def solo_verificadas():
    return bool(st.session_state.get("solo_verif", True))


def nuevos_por_dia():
    return int(st.session_state.get("nuevos_dia", 20))


PID_SQL = ("CASE s.tipo WHEN 'test' THEN substr(s.item_key, 7 + length(s.tema_id)) "
           "WHEN 'sup' THEN substr(s.item_key, 5) END")
SRS_FROM = f"FROM srs_items s LEFT JOIN preguntas pv ON pv.id = {PID_SQL}"


def srs_filtro():
    f = " AND s.tipo != 'sup'"
    if solo_verificadas():
        f += " AND (pv.id IS NULL OR pv.verificado = 1)"
    return f


def srs_filtrado():
    """Subconsulta con los ítems del SRS que cuentan (sin gemelas y respetando 'solo verificadas')."""
    return f"(SELECT s.* {SRS_FROM} WHERE 1 = 1 {srs_filtro()})"


def nuevos_introducidos_hoy():
    """Ítems cuya primera respuesta de la historia es de hoy."""
    return consulta("""SELECT COUNT(*) FROM (SELECT item_key FROM srs_historial
                       GROUP BY item_key HAVING MIN(fecha) = ?)""", (hoy_iso(),))[0][0]


# ============================================================
# CONSULTAS DE ESTADÍSTICAS
# ============================================================

def stats_globales():
    hoy = hoy_iso()
    s = dict(consulta(f"""
        SELECT COUNT(*) AS n,
               COALESCE(SUM(s.estado = 'dominado'), 0) AS dom,
               COALESCE(SUM(s.estado = 'en-progreso'), 0) AS prog,
               COALESCE(SUM(s.estado = 'por-aprender'), 0) AS porap,
               COALESCE(SUM(s.estado = 'sin-empezar'), 0) AS nuevo,
               COALESCE(SUM(s.estado IN ('por-aprender', 'en-progreso') AND s.due <= ?), 0) AS repasos,
               COALESCE(SUM(s.veces_acertada), 0) AS ac,
               COALESCE(SUM(s.veces_fallada), 0) AS fa
        {SRS_FROM} WHERE 1 = 1 {srs_filtro()}
    """, (hoy,))[0])
    s["hechas_hoy"] = consulta("SELECT COUNT(*) FROM srs_historial WHERE fecha = ?", (hoy,))[0][0]
    s["nuevos_hechos"] = nuevos_introducidos_hoy()
    s["cupo_nuevos"] = max(0, nuevos_por_dia() - s["nuevos_hechos"])
    s["nuevos_hoy"] = min(s["cupo_nuevos"], s["nuevo"])
    s["hoy"] = s["repasos"] + s["nuevos_hoy"]
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


def listar_bloques_temas():
    bloques = [dict(b) for b in consulta("SELECT * FROM bloques ORDER BY numero")]
    temas = consulta(f"""
        SELECT t.id, t.numero, t.titulo, t.bloque_id, t.estado_ingesta,
               COUNT(s.item_key) AS n_items,
               COALESCE(SUM(s.estado = 'dominado'), 0) AS n_dom,
               COALESCE(SUM(s.estado = 'en-progreso'), 0) AS n_prog,
               COALESCE(SUM(s.estado = 'por-aprender'), 0) AS n_porap,
               COALESCE(SUM(s.estado = 'sin-empezar'), 0) AS n_nuevo,
               COALESCE(SUM(s.estado IN ('por-aprender', 'en-progreso') AND s.due <= ?), 0) AS n_hoy
        FROM temas t LEFT JOIN {srs_filtrado()} s ON s.tema_id = t.id
        GROUP BY t.id ORDER BY t.numero
    """, (hoy_iso(),))
    preg = {r["tema_id"]: r for r in consulta(
        "SELECT tema_id, COUNT(*) AS total, COALESCE(SUM(verificado = 0), 0) AS sin_verif "
        "FROM preguntas GROUP BY tema_id")}
    examen = {r["tema_id"]: r for r in consulta(
        "SELECT tema_id, n_examenes, media_preg, max_preg FROM v_tendencia_temas")}
    fuentes = {r["tema_id"]: r for r in consulta(
        "SELECT tema_id, n_fuentes, n_fragmentos FROM v_cobertura_fuentes")}
    por_bloque = {}
    for t in temas:
        d = dict(t)
        p, e, f = preg.get(d["id"]), examen.get(d["id"]), fuentes.get(d["id"])
        d["n_preg"] = p["total"] if p else 0
        d["sin_verif"] = p["sin_verif"] if p else 0
        d["n_examenes"] = (e["n_examenes"] or 0) if e else 0
        d["media_preg"] = e["media_preg"] if e else None
        d["n_fuentes"] = f["n_fuentes"] if f else 0
        por_bloque.setdefault(d["bloque_id"], []).append(d)
    for b in bloques:
        b["temas"] = por_bloque.get(b["id"], [])
    return bloques


def romano(n):
    return {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI"}.get(n, str(n))


def etiqueta_examen(anio, modelo):
    return f"{anio}" + (f" · modelo {modelo}" if modelo and modelo != "Único" else "")


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


SQL_PREG = """
    SELECT p.id AS pregunta_id, p.tema_id, p.concepto_id, p.enunciado, p.opciones, p.correcta,
           p.explicacion, p.referencia, p.dificultad, p.verificado, p.origen
    FROM preguntas p
"""

SQL_CUADRO = """
    SELECT cf.id AS fila_id, cf.valores, cf.fuente, cu.titulo, cu.tema_id,
           cu.columna_clave, cu.columna_respuesta, cu.columna_contexto
    FROM cuadro_filas cf JOIN cuadros cu ON cu.id = cf.cuadro_id
"""


def _meta_preguntas(pids):
    """Procedencia de cada pregunta: veces que ha salido en examen, examen, supuesto."""
    pids = list(set(pids))
    meta = {p: {} for p in pids}
    for r in en_lote("SELECT pregunta_id, n_examenes FROM pregunta_reuso WHERE pregunta_id IN ({ids})", pids):
        meta[r["pregunta_id"]]["reuso"] = r["n_examenes"]
    for r in en_lote("""SELECT ep.pregunta_id, ep.seccion, ep.numero, e.anio, e.modelo
                        FROM examen_preguntas ep JOIN examenes e ON e.id = ep.examen_id
                        WHERE ep.pregunta_id IN ({ids})""", pids):
        meta[r["pregunta_id"]]["examen"] = {
            "label": etiqueta_examen(r["anio"], r["modelo"]), "seccion": r["seccion"], "numero": r["numero"]}
    for r in en_lote("""SELECT sp.pregunta_id, sp.es_reserva, sp.numero_en_supuesto, s.id, s.titulo,
                               s.contexto_texto, e.anio, e.modelo
                        FROM supuesto_preguntas sp
                        JOIN supuestos s ON s.id = sp.supuesto_id
                        LEFT JOIN examenes e ON e.id = s.examen_id
                        WHERE sp.pregunta_id IN ({ids})""", pids):
        meta[r["pregunta_id"]]["supuesto"] = {
            "id": r["id"], "titulo": r["titulo"], "texto": r["contexto_texto"] or "",
            "examen": etiqueta_examen(r["anio"], r["modelo"]) if r["anio"] else "",
            "numero": r["numero_en_supuesto"], "reserva": bool(r["es_reserva"])}
    return meta


def _item_test(f, meta):
    pid = f["pregunta_id"]
    m = meta.get(pid, {})
    return {
        "tipo": "test",
        "pregunta_id": pid,
        "item_key": f"test:{f['tema_id']}:{pid}",
        "espejos": [f"sup:{pid}"] if m.get("supuesto") else [],
        "tema_id": f["tema_id"],
        "concepto_id": f["concepto_id"],
        "enunciado": f["enunciado"],
        "opciones": _parse_json(f["opciones"], []),
        "correcta": f["correcta"],
        "explicacion": f["explicacion"],
        "referencia": f["referencia"],
        "dificultad": f["dificultad"],
        "verificado": bool(f["verificado"]),
        "reuso": m.get("reuso"),
        "examen": m.get("examen"),
        "supuesto": m.get("supuesto"),
    }


def _items_tests(filas):
    meta = _meta_preguntas([f["pregunta_id"] for f in filas])
    return [_item_test(f, meta) for f in filas]


def _item_flash(f, item_key):
    if f["modo"] == "cloze":
        return {"tipo": "cloze", "item_key": item_key, "tema_id": f["tema_id"],
                "texto": f["texto"], "respuestas": _parse_json(f["respuestas"], [])}
    return {"tipo": "card", "item_key": item_key, "tema_id": f["tema_id"],
            "anverso": f["anverso"], "reverso": f["reverso"]}


def _item_cuadro(f):
    v = _parse_json(f["valores"], {})
    ctx = f["columna_contexto"]
    return {
        "tipo": "cuadro", "item_key": f"cuadro:{f['tema_id']}:{f['fila_id']}", "tema_id": f["tema_id"],
        "titulo": f["titulo"],
        "clave_nombre": f["columna_clave"], "clave": v.get(f["columna_clave"], ""),
        "ctx_nombre": ctx, "ctx": v.get(ctx, "") if ctx else "",
        "resp_nombre": f["columna_respuesta"], "respuesta": v.get(f["columna_respuesta"], ""),
        "fuente": f["fuente"],
    }


def resolver_items(keys):
    """Convierte claves de srs_items en ítems listos para mostrar (respeta el orden; omite huérfanos)."""
    keys = list(keys)
    pids, fids, rids = [], [], []
    for k in keys:
        tipo = k.split(":", 1)[0]
        if tipo == "test":
            pids.append(k.split(":", 2)[2])
        elif tipo == "sup":
            pids.append(k.split(":", 1)[1])
        elif tipo in ("card", "cloze"):
            fids.append(k.split(":", 2)[2])
        elif tipo == "cuadro":
            rids.append(k.split(":", 2)[2])
    pregs = {r["pregunta_id"]: r for r in en_lote(SQL_PREG + " WHERE p.id IN ({ids})", pids)}
    meta = _meta_preguntas(pregs)
    fcs = {r["id"]: r for r in en_lote(
        "SELECT id, modo, anverso, reverso, texto, respuestas, tema_id FROM flashcards WHERE id IN ({ids})", fids)}
    cfs = {r["fila_id"]: r for r in en_lote(SQL_CUADRO + " WHERE cf.id IN ({ids})", rids)}
    items = []
    for k in keys:
        tipo = k.split(":", 1)[0]
        it = None
        if tipo in ("test", "sup"):
            r = pregs.get(k.split(":", 2)[2] if tipo == "test" else k.split(":", 1)[1])
            it = _item_test(r, meta) if r else None
        elif tipo in ("card", "cloze"):
            r = fcs.get(k.split(":", 2)[2])
            it = _item_flash(r, k) if r else None
        elif tipo == "cuadro":
            r = cfs.get(k.split(":", 2)[2])
            it = _item_cuadro(r) if r else None
        if it:
            items.append(it)
    return items


def cargar_items_srs_hoy(limite=30):
    """Repasos vencidos primero; el hueco que quede se rellena con nuevos, respetando el cupo diario."""
    claves = [r[0] for r in consulta(f"""
        SELECT s.item_key {SRS_FROM}
        WHERE s.estado IN ('por-aprender', 'en-progreso') AND s.due <= ? {srs_filtro()}
        ORDER BY s.due, RANDOM() LIMIT ?""", (hoy_iso(), limite))]
    hueco = min(limite - len(claves), max(0, nuevos_por_dia() - nuevos_introducidos_hoy()))
    if hueco > 0:
        claves += [r[0] for r in consulta(f"""
            SELECT s.item_key {SRS_FROM}
            WHERE s.estado = 'sin-empezar' {srs_filtro()} ORDER BY RANDOM() LIMIT ?""", (hueco,))]
    items = resolver_items(claves)
    random.shuffle(items)
    return items


def cargar_items_nuevos(limite=10):
    """Ítems sin empezar, ignorando el cupo diario (para cuando ya has hecho el de hoy)."""
    claves = [r[0] for r in consulta(f"""
        SELECT s.item_key {SRS_FROM}
        WHERE s.estado = 'sin-empezar' {srs_filtro()} ORDER BY RANDOM() LIMIT ?""", (limite,))]
    return resolver_items(claves)


SQL_DEBILES = "(s.veces_fallada > 0 OR s.ultima_respuesta IN ('otra_vez', 'dificil'))"


def contar_debiles():
    return consulta(f"SELECT COUNT(*) {SRS_FROM} WHERE {SQL_DEBILES} {srs_filtro()}")[0][0]


def cargar_items_debiles(limite=30):
    claves = [r[0] for r in consulta(f"""
        SELECT s.item_key {SRS_FROM} WHERE {SQL_DEBILES} {srs_filtro()}
        ORDER BY s.veces_fallada DESC, RANDOM() LIMIT ?""", (limite,))]
    return resolver_items(claves)


def scope_sql(col, ambito):
    """Filtro SQL por ámbito: ('todo', None) | ('bloque', id) | ('tema', id)."""
    tipo, valor = ambito
    if tipo == "bloque":
        return f" AND {col} IN (SELECT id FROM temas WHERE bloque_id = ?)", [valor]
    if tipo == "tema":
        return f" AND {col} = ?", [valor]
    return "", []


def filtro_preguntas(ambito, dificultad=None, procedencia=None):
    """procedencia: None (todas) | 'examen' (de convocatorias reales) | 'elaborada' (generadas del temario)."""
    sql, pr = scope_sql("p.tema_id", ambito)
    if solo_verificadas():
        sql += " AND p.verificado = 1"
    if dificultad:
        sql += " AND p.dificultad = ?"
        pr.append(dificultad)
    if procedencia == "elaborada":
        sql += " AND p.origen = 'ingesta-inicial'"
    elif procedencia == "examen":
        sql += " AND COALESCE(p.origen, '') != 'ingesta-inicial'"
    return sql, pr


def cargar_tests(ambito, dificultad, limite, procedencia=None):
    sql, pr = filtro_preguntas(ambito, dificultad, procedencia)
    filas = consulta(SQL_PREG + f" WHERE 1 = 1 {sql} ORDER BY RANDOM() LIMIT ?", pr + [limite])
    return _items_tests(filas)


def cargar_flashcards(ambito, limite):
    sc, pr = scope_sql("f.tema_id", ambito)
    filas = consulta(f"""
        SELECT f.id, f.modo, f.anverso, f.reverso, f.texto, f.respuestas, f.tema_id
        FROM flashcards f WHERE 1 = 1 {sc} ORDER BY RANDOM() LIMIT ?
    """, pr + [limite])
    return [_item_flash(f, f"{'cloze' if f['modo'] == 'cloze' else 'card'}:{f['tema_id']}:{f['id']}")
            for f in filas]


def cargar_cuadros(ambito, limite, cuadro_id=None):
    sc, pr = scope_sql("cu.tema_id", ambito)
    extra = ""
    if cuadro_id:
        extra = " AND cu.id = ?"
        pr.append(cuadro_id)
    filas = consulta(SQL_CUADRO + f" WHERE 1 = 1 {sc} {extra} ORDER BY RANDOM() LIMIT ?", pr + [limite])
    return [_item_cuadro(f) for f in filas]


def cargar_test_preparado(test_id):
    filas = consulta(SQL_PREG + """
        JOIN test_practica_preguntas tp ON tp.pregunta_id = p.id
        WHERE tp.test_id = ? ORDER BY tp.numero
    """, (test_id,))
    return _items_tests(filas)


def contar_disponibles(tipo, ambito, dificultad, procedencia=None):
    sql, pr = filtro_preguntas(ambito, dificultad, procedencia)
    tests = consulta(f"SELECT COUNT(*) FROM preguntas p WHERE 1 = 1 {sql}", pr)[0][0]
    sc, pr = scope_sql("f.tema_id", ambito)
    flash = consulta(f"SELECT COUNT(*) FROM flashcards f WHERE 1 = 1 {sc}", pr)[0][0]
    sc, pr = scope_sql("cu.tema_id", ambito)
    cuad = consulta("SELECT COUNT(*) FROM cuadro_filas cf JOIN cuadros cu ON cu.id = cf.cuadro_id "
                    f"WHERE 1 = 1 {sc}", pr)[0][0]
    return {"test": tests, "flash": flash, "cuadros": cuad, "mixto": tests + flash + cuad}.get(tipo, 0)


# ---------- Exámenes oficiales y supuestos ----------

def listar_examenes():
    return [dict(r) for r in consulta("""
        SELECT e.id, e.anio, e.modelo, e.convocatoria,
               (SELECT COUNT(*) FROM examen_preguntas ep WHERE ep.examen_id = e.id AND ep.seccion = 'teorica') AS n_teo,
               (SELECT COUNT(*) FROM examen_preguntas ep WHERE ep.examen_id = e.id AND ep.seccion = 'reserva') AS n_res
        FROM examenes e ORDER BY e.anio DESC, e.modelo""")]


def listar_supuestos(examen_id=None):
    sql = """SELECT s.id, s.examen_id, s.numero, s.titulo, s.bloque_id, e.anio, e.modelo,
                    (SELECT COUNT(*) FROM supuesto_preguntas sp WHERE sp.supuesto_id = s.id AND sp.es_reserva = 0) AS n,
                    (SELECT COUNT(*) FROM supuesto_preguntas sp WHERE sp.supuesto_id = s.id AND sp.es_reserva = 1) AS n_res
             FROM supuestos s LEFT JOIN examenes e ON e.id = s.examen_id"""
    pr = []
    if examen_id:
        sql += " WHERE s.examen_id = ?"
        pr.append(examen_id)
    return [dict(r) for r in consulta(sql + " ORDER BY e.anio DESC, e.modelo, s.numero", pr)]


def cargar_examen_seccion(examen_id, seccion):
    filas = consulta(SQL_PREG + """
        JOIN examen_preguntas ep ON ep.pregunta_id = p.id
        WHERE ep.examen_id = ? AND ep.seccion = ? ORDER BY ep.numero""", (examen_id, seccion))
    return _items_tests(filas)


def cargar_supuesto(supuesto_id, incluir_reserva=False):
    filas = consulta(SQL_PREG + f"""
        JOIN supuesto_preguntas sp ON sp.pregunta_id = p.id
        WHERE sp.supuesto_id = ? {'' if incluir_reserva else 'AND sp.es_reserva = 0'}
        ORDER BY sp.es_reserva, sp.numero_en_supuesto""", (supuesto_id,))
    return _items_tests(filas)


def cargar_examen_completo(examen_id):
    items = cargar_examen_seccion(examen_id, "teorica")
    for s in listar_supuestos(examen_id):
        items += cargar_supuesto(s["id"])
    return items


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


# Admite {{c1::texto}}, {c1::texto} y {{texto}}
CLOZE_RE = re.compile(r"\{\{c\d+::(.+?)\}\}|\{c\d+::(.+?)\}|\{\{(.+?)\}\}")


def partes_cloze(texto):
    """Devuelve [("t", texto) | ("b", respuesta)] preservando el orden."""
    partes, pos = [], 0
    for m in CLOZE_RE.finditer(texto or ""):
        if m.start() > pos:
            partes.append(("t", texto[pos:m.start()]))
        partes.append(("b", next(g for g in m.groups() if g is not None)))
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
                 "respuesta_actual", "mostrar_reverso", "cloze_res", "ultimo_intervalo", "marcas"]


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
        "modo": "sesion", "titulo_sesion": titulo, "marcas": [],
    })
    return True


def responder(item, respuesta):
    """Registra la respuesta en el SRS y en los contadores de la sesión."""
    res = actualizar_srs(item["item_key"], respuesta, item.get("espejos", ()))
    if respuesta == "otra_vez":
        st.session_state["fallos"] = st.session_state.get("fallos", 0) + 1
    else:
        st.session_state["aciertos"] = st.session_state.get("aciertos", 0) + 1
    if respuesta in ("otra_vez", "dificil"):
        errores = st.session_state.setdefault("errores", [])
        if not any(e["item_key"] == item["item_key"] for e in errores):
            errores.append(item)
    st.session_state.setdefault("marcas", []).append("bad" if respuesta == "otra_vez" else "ok")
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

SIGLAS = {"tls", "ssl", "ip", "tcp", "udp", "http", "https", "dns", "smtp", "imap", "pop3", "url", "api",
          "sql", "cpd", "vpn", "lan", "wan", "dhcp", "ftp", "ssh", "rest", "xml", "html", "css", "ens", "eni"}

ACENTOS = {"descripcion": "descripción", "organo": "órgano", "composicion": "composición",
           "mayoria": "mayoría", "estandar": "estándar", "configuracion": "configuración"}


def nombre_columna(nombre):
    """'puerto_seguro_tls' -> 'Puerto seguro TLS'."""
    palabras = str(nombre).replace("_", " ").split()
    palabras = [p.upper() if p.lower() in SIGLAS else ACENTOS.get(p.lower(), p) for p in palabras]
    texto = " ".join(palabras)
    return texto[:1].upper() + texto[1:]


def reflujo_texto(texto):
    """Une las líneas cortadas por el PDF: un salto solo se mantiene tras un punto/dos puntos
    o antes de un elemento de lista."""
    lineas = [l.strip() for l in str(texto or "").splitlines()]
    salida = []
    for l in lineas:
        if not l:
            salida.append("")
        elif (salida and salida[-1] and not re.search(r"[.:;?!]$", salida[-1])
              and not re.match(r"^([-•+*]|\d+[.)])\s?", l)):
            salida[-1] += " " + l
        else:
            salida.append(l)
    return "\n".join(salida)


def md_escape(texto):
    """Escapa Markdown para etiquetas de botón (LaTeX con $, cursivas con _ y *, HTML, :emoji:)."""
    return re.sub(r"([\\`*_\[\]$~<>:])", r"\\\1", str(texto))


def tags_pregunta(item):
    tags = [("Test", "")]
    if item.get("dificultad"):
        tags.append((f"Dificultad {item['dificultad']}", ""))
    ex, sup = item.get("examen"), item.get("supuesto")
    if ex:
        parte = "teórica" if ex["seccion"] == "teorica" else "reserva"
        tags.append((f"Examen {ex['label']}, {parte} {ex['numero']}", ""))
    if sup:
        pos = "reserva" if sup["reserva"] else f"pregunta {sup['numero']}"
        tags.append((f"{sup['titulo']} {sup['examen']}, {pos}".replace("  ", " "), ""))
    if (item.get("reuso") or 0) > 1:
        tags.append((f"Repetida en {item['reuso']} exámenes", ""))
    if not item.get("verificado", True):
        tags.append(("Sin verificar", "aviso"))
    return "".join(f'<span class="tag {c}">{esc(t)}</span>' for t, c in tags)


def render_pregunta_test(item):
    st.markdown(
        f'<div class="hoja"><div>{tags_pregunta(item)}</div>'
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
            # "A" + espacio largo: el CSS dibuja la letra como un óvalo de hoja de respuestas
            if st.button(f"{letra} {md_escape(opcion)}", key=f"opt_{item['item_key']}_{i}",
                         use_container_width=True):
                st.session_state["respuesta_actual"] = i
                responder(item, "bien" if i == correcta else "otra_vez")
                st.rerun()

    if ya:
        prox = texto_intervalo(st.session_state.get("ultimo_intervalo"))
        sub = f"<small>La verás de nuevo {prox}.</small>" if prox else ""
        if elegida == correcta:
            st.markdown(f'<div class="veredicto ok">Correcto{sub}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="veredicto bad">Incorrecto{sub}</div>', unsafe_allow_html=True)

        if item.get("explicacion") or item.get("referencia"):
            ref = f'<div class="ref">{esc(item["referencia"])}</div>' if item.get("referencia") else ""
            expl = esc(item["explicacion"]) if item.get("explicacion") else ""
            st.markdown(f'<div class="expl">{expl}{ref}</div>', unsafe_allow_html=True)

        if st.button("Siguiente", type="primary", use_container_width=True, key=f"sig_{item['item_key']}"):
            _avanzar()


def _frente_dorso(item):
    """HTML de la cara y del reverso de una flashcard o cuadro."""
    if item["tipo"] == "cuadro":
        pista = nombre_columna(item["resp_nombre"])
        ctx = (f'{esc(nombre_columna(item["ctx_nombre"]))}: <b>{esc(item["ctx"])}</b>. '
               if item.get("ctx") else "")
        frente = (f'<div class="q">{esc(item["clave"])}</div>'
                  f'<div class="hint">{ctx}¿{esc(pista)}?</div>')
        ref = f'<div class="ref">{esc(item["fuente"])}</div>' if item.get("fuente") else ""
        dorso = f'<div class="back"><b>{esc(item["respuesta"])}</b></div>{ref}'
        etiqueta = f"Cuadro: {item['titulo']}"
    else:
        frente = f'<div class="q">{esc(item["anverso"])}</div>'
        dorso = f'<div class="back">{esc(item["reverso"])}</div>'
        etiqueta = "Flashcard"
    return etiqueta, frente, dorso


def render_card(item):
    etiqueta, frente, dorso = _frente_dorso(item)
    visible = "mostrar_reverso" in st.session_state
    st.markdown(
        f'<div class="hoja"><div><span class="tag">{esc(etiqueta)}</span></div>{frente}'
        + (f'<div class="divider"></div>{dorso}' if visible else "") + "</div>",
        unsafe_allow_html=True,
    )

    if not visible:
        if st.button("Mostrar reverso", type="primary", use_container_width=True,
                     key=f"rev_{item['item_key']}"):
            st.session_state["mostrar_reverso"] = True
            st.rerun()
    else:
        st.caption("¿Cómo lo has recordado?")
        cols = st.columns(4)
        opciones = [("Otra vez", "otra_vez"), ("Difícil", "dificil"), ("Bien", "bien"), ("Fácil", "facil")]
        for col, (etiqueta_b, clave) in zip(cols, opciones):
            with col:
                if st.button(etiqueta_b, key=f"rate_{clave}_{item['item_key']}",
                             type="primary" if clave == "bien" else "secondary",
                             use_container_width=True):
                    responder(item, clave)
                    _avanzar()


def render_cloze(item):
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
            f'<div class="hoja"><div><span class="tag">Rellenar huecos</span></div>'
            f'<div class="q">{html_q}</div></div>', unsafe_allow_html=True)

        with st.form(f"form_{item['item_key']}", clear_on_submit=False):
            entradas = []
            for i in range(len(respuestas)):
                etiqueta = "Tu respuesta" if len(respuestas) == 1 else f"Hueco {i + 1}"
                entradas.append(st.text_input(etiqueta, key=f"cz_{item['item_key']}_{i}",
                                              placeholder="Escribe lo que falta"))
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
        f'<div class="hoja"><div><span class="tag">Rellenar huecos</span></div>'
        f'<div class="q">{html_q}</div></div>', unsafe_allow_html=True)

    if res["ok"]:
        st.markdown('<div class="veredicto ok">Correcto</div>', unsafe_allow_html=True)
        if st.button("Siguiente", type="primary", use_container_width=True, key=f"sigc_{item['item_key']}"):
            responder(item, "bien")
            _avanzar()
    else:
        st.markdown('<div class="veredicto bad">Revisa los huecos marcados'
                    '<small>¿Era correcta la tuya? Puedes validarla.</small></div>', unsafe_allow_html=True)
        c1, c2 = st.columns([3, 2])
        with c1:
            if st.button("Siguiente", type="primary", use_container_width=True, key=f"sigc_{item['item_key']}"):
                responder(item, "otra_vez")
                _avanzar()
        with c2:
            if st.button("Era correcta", use_container_width=True, key=f"valc_{item['item_key']}"):
                responder(item, "bien")
                _avanzar()


# ============================================================
# PANTALLAS: SESIÓN Y RESUMEN
# ============================================================

def tira_marcas(index, total, marcas):
    """Una marca por ítem: verde acierto, rojo fallo, amarillo el actual."""
    celdas = []
    for i in range(total):
        if i < len(marcas):
            clase = marcas[i]
        elif i == index:
            clase = "ahora"
        else:
            clase = ""
        celdas.append(f'<i class="{clase}"></i>')
    return f'<div class="tira">{"".join(celdas)}</div>'


def pantalla_sesion():
    items = st.session_state["items"]
    index = st.session_state["index"]
    total = len(items)
    if index >= total:
        st.session_state["modo"] = "resumen"
        st.rerun()
    item = items[index]
    marcas = st.session_state.get("marcas", [])

    c1, c2, c3 = st.columns([7, 2.2, 1.2], vertical_alignment="center")
    with c1:
        st.markdown(tira_marcas(index, total, marcas), unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="cuenta"><b>{index + 1}</b> de {total}, '
                    f'{st.session_state.get("aciertos", 0)} bien, {st.session_state.get("fallos", 0)} mal</div>',
                    unsafe_allow_html=True)
    with c3:
        st.button("Salir", key="salir_sesion", on_click=_terminar, use_container_width=True)
    st.write("")

    tipo = item["tipo"]
    sup = item.get("supuesto") if tipo == "test" else None

    def cuerpo():
        if tipo == "test":
            render_pregunta_test(item)
        elif tipo in ("card", "cuadro"):
            render_card(item)
        elif tipo == "cloze":
            render_cloze(item)

    if sup and sup["texto"]:
        izq, der = st.columns([5, 6], gap="large")
        with izq:
            st.markdown(f'<div class="enunciado-t">{esc(sup["titulo"])}: enunciado</div>'
                        f'<div class="enunciado">{esc(reflujo_texto(sup["texto"]))}</div>', unsafe_allow_html=True)
        with der:
            cuerpo()
    else:
        _, centro, _ = st.columns([1, 3.2, 1])
        with centro:
            cuerpo()

    st.markdown('<div class="atajos" style="text-align:center"><kbd>A</kbd> a <kbd>D</kbd> o <kbd>1</kbd> a <kbd>4</kbd> '
                'responden, <kbd>Intro</kbd> continúa.</div>', unsafe_allow_html=True)
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
        ctx = f" ({item['ctx_nombre']}: {item['ctx']})" if item.get("ctx") else ""
        return f"{item['titulo']}: {item['clave']}{ctx}", item["respuesta"]
    if t == "cloze":
        q = "".join(v if k == "t" else "____" for k, v in partes_cloze(item["texto"])) or item["texto"]
        return q, ", ".join(respuestas_cloze(item))
    return "", ""


def cabecera(titulo, sub=""):
    st.markdown(f'<h1 class="titular menor">{esc(titulo)}</h1>'
                + (f'<p class="lead">{esc(sub)}</p>' if sub else ""), unsafe_allow_html=True)


def pantalla_resumen():
    ss = st.session_state
    total = len(ss.get("items", []))
    aciertos, fallos = ss.get("aciertos", 0), ss.get("fallos", 0)
    respondidos = aciertos + fallos
    pct = round(aciertos / respondidos * 100) if respondidos else 0
    errores = ss.get("errores", [])
    marcas = ss.get("marcas", [])

    izq, der = st.columns([2, 3], gap="large")
    with izq:
        st.markdown(f'<p class="fecha">{esc(ss.get("titulo_sesion", ""))}</p>'
                    f'<div class="grande">{pct if respondidos else "—"}<small>{"%" if respondidos else ""}</small></div>'
                    f'<p class="lead" style="margin-top:.6rem">'
                    f'{"Sesión completada" if respondidos >= total else "Sesión terminada"}: '
                    f'{aciertos} de {respondidos} bien. Tus respuestas ya están en el repaso espaciado.</p>',
                    unsafe_allow_html=True)
        if marcas:
            st.markdown(tira_marcas(-1, len(marcas), marcas), unsafe_allow_html=True)
            st.write("")
        st.button("Volver al inicio", use_container_width=True, key="volver_inicio", on_click=_salir)

    with der:
        if errores:
            st.markdown(f'<h3 style="margin-top:0 !important">Para repasar ({len(errores)})</h3>', unsafe_allow_html=True)
            for e in errores:
                q, a = resumen_item(e)
                st.markdown(f'<div class="fallo"><div class="t">{esc(q)}</div>'
                            f'<div class="m"><b>{esc(a)}</b></div></div>', unsafe_allow_html=True)
            st.write("")
            if st.button(f"Repasar estos {len(errores)} ahora", type="primary", use_container_width=True,
                         key="repasar_errores"):
                iniciar(list(errores), "Repaso de fallos")
                st.rerun()
        else:
            st.markdown('<h3 style="margin-top:0 !important">Sin fallos</h3>'
                        '<p class="lead">No has fallado nada en esta sesión.</p>', unsafe_allow_html=True)


# ============================================================
# PÁGINA: HOY
# ============================================================

def mapa_actividad(datos):
    """Cuadrícula de días: más respuestas, más amarillo."""
    mx = max((n for _, n in datos), default=0) or 1
    hoy = date.today()
    celdas = ""
    for d, n in datos:
        p = round(n / mx * 100)
        fondo = f"color-mix(in srgb, var(--mark) {max(p, 18)}%, var(--surface2))" if n else "var(--surface2)"
        color = "var(--on_mark)" if n and p >= 45 else "var(--muted)"
        celdas += (f'<i class="{"hoy" if d == hoy else ""}" title="{d.day} de {MESES[d.month - 1]}: {n} respuestas" '
                   f'style="background:{fondo};color:{color}">{d.day}</i>')
    return f'<div class="mapa">{celdas}</div>'


def pantalla_hoy():
    s = stats_globales()
    izq, der = st.columns([3, 2], gap="large")

    with izq:
        st.markdown(f'<p class="fecha">{fecha_larga(date.today())}</p>', unsafe_allow_html=True)
        if s["hoy"] > 0:
            if s["repasos"] == 0:
                titular = f"Hoy toca estrenar {plural(s['nuevos_hoy'], 'ítem', 'ítems')}."
            elif s["nuevos_hoy"] == 0:
                titular = f"Hoy tocan {plural(s['repasos'], 'repaso', 'repasos')}."
            else:
                titular = (f"Hoy tocan {plural(s['repasos'], 'repaso', 'repasos')} "
                           f"y {plural(s['nuevos_hoy'], 'ítem nuevo', 'ítems nuevos')}.")
            st.markdown(f'<h1 class="titular">{titular}</h1>'
                        f'<p class="lead">Cupo de nuevos: {s["nuevos_hechos"]} de {nuevos_por_dia()} hoy.</p>',
                        unsafe_allow_html=True)
            with panel("hoy"):
                st.markdown('<div class="sub">Tamaño de la sesión</div>', unsafe_allow_html=True)
                n = st.radio("Tamaño", [10, 20, 30, 50], index=1, horizontal=True,
                             label_visibility="collapsed", key="pill_n_rep")
                n_real = min(n, s["hoy"])
                if st.button(f"Empezar repaso de {n_real} ítems", type="primary",
                             use_container_width=True, key="go_repaso"):
                    if iniciar(cargar_items_srs_hoy(limite=n), "Repaso de hoy"):
                        st.rerun()
                    else:
                        st.warning("No hay ítems disponibles ahora mismo.")
        else:
            st.markdown('<h1 class="titular">Todo al día.</h1>'
                        '<p class="lead">No quedan repasos pendientes para hoy.</p>', unsafe_allow_html=True)
            with panel("hoy"):
                if s["nuevo"]:
                    st.markdown(f'<div class="nota">Cupo de nuevos: {s["nuevos_hechos"]} de {nuevos_por_dia()}. '
                                f'Quedan {s["nuevo"]} sin empezar.</div>', unsafe_allow_html=True)
                    if st.button("Aprender 10 ítems nuevos más", type="primary",
                                 use_container_width=True, key="go_mas_nuevos"):
                        if iniciar(cargar_items_nuevos(10), "Ítems nuevos"):
                            st.rerun()
                st.button("Practicar algo más", use_container_width=True, key="go_practicar_extra",
                          on_click=_ir_a, args=(PAGINAS[1],))

        dom_pct = round(s["dom"] / s["n"] * 100) if s["n"] else 0
        prec = f"{s['precision']:.0f}%" if s["precision"] is not None else "—"
        st.markdown(
            f'<div class="cifras"><div><b>{s["racha"]}</b><span>{"día" if s["racha"] == 1 else "días"} de racha</span></div>'
            f'<div><b>{s["hechas_hoy"]}</b><span>hechas hoy</span></div>'
            f'<div><b>{dom_pct}%</b><span>dominado</span></div>'
            f'<div><b>{prec}</b><span>precisión</span></div></div>', unsafe_allow_html=True)

    with der:
        datos = actividad(14)
        with panel("mapa"):
            st.markdown('<div class="sub">Últimos 14 días</div>'
                        f'<div class="nota">{sum(n for _, n in datos)} respuestas</div>', unsafe_allow_html=True)
            st.markdown(mapa_actividad(datos), unsafe_allow_html=True)
        with panel("estado"):
            st.markdown('<div class="sub">Estado de tus ítems</div>', unsafe_allow_html=True)
            st.markdown(barra_estados(s["dom"], s["prog"], s["porap"], s["nuevo"])
                        + leyenda(s["dom"], s["prog"], s["porap"], s["nuevo"]), unsafe_allow_html=True)

    st.markdown("### Por bloque")
    filas = ""
    for b in listar_bloques_temas():
        n = sum(t["n_items"] for t in b["temas"])
        dom = sum(t["n_dom"] for t in b["temas"])
        prog = sum(t["n_prog"] for t in b["temas"])
        porap = sum(t["n_porap"] for t in b["temas"])
        nuevo = sum(t["n_nuevo"] for t in b["temas"])
        pct = f"{round(dom / n * 100)}%" if n else "—"
        filas += (f'<div class="fila-bloque"><div><div class="t">{romano(b["numero"])}. {esc(b["nombre"])}</div>'
                  f'<div class="m">{plural(len(b["temas"]), "tema", "temas")}, {plural(n, "ítem", "ítems")}</div></div>'
                  f'<div class="barra">{barra_estados(dom, prog, porap, nuevo, fina=True)}</div>'
                  f'<div class="p">{pct}</div></div>')
    st.markdown(filas, unsafe_allow_html=True)


# ============================================================
# PÁGINA: PRACTICAR
# ============================================================

TIPOS_PRACTICA = {
    "test": "Test",
    "flash": "Flashcards",
    "cuadros": "Cuadros",
    "mixto": "Mixto",
    "examen": "Exámenes oficiales",
    "supuesto": "Supuestos prácticos",
    "preparado": "Tests preparados",
    "debiles": "Puntos débiles",
}
DESC_PRACTICA = {
    "test": "Preguntas tipo oposición del ámbito que elijas.",
    "flash": "Anverso y reverso, y frases con huecos.",
    "cuadros": "Plazos, puertos y composiciones, fila a fila.",
    "mixto": "Un poco de todo, en orden aleatorio.",
    "examen": "Convocatorias anteriores, en el orden original.",
    "supuesto": "Cada supuesto con su enunciado al lado.",
    "preparado": "Tests ya generados en la base de datos.",
    "debiles": "Lo que has fallado o marcado como difícil.",
}


def opciones_ambito():
    """Lista de (etiqueta, ambito) con contenido disponible."""
    bloques = listar_bloques_temas()
    opciones = [("Todo el temario", ("todo", None))]
    for b in bloques:
        if any(t["n_items"] for t in b["temas"]):
            opciones.append((f"Bloque {romano(b['numero'])}: {b['nombre']}", ("bloque", b["id"])))
    for b in bloques:
        for t in b["temas"]:
            if t["n_items"]:
                opciones.append((f"Tema {t['numero']}: {t['titulo']}", ("tema", t["id"])))
    return opciones


def etiqueta_scope(scope):
    """Nombre legible del ámbito de un test preparado (examen, tema o nada)."""
    if not scope:
        return ""
    if scope.startswith("examen-"):
        e = next((x for x in listar_examenes() if x["id"] == scope), None)
        return f"TAI {etiqueta_examen(e['anio'], e['modelo'])}" if e else scope
    m = re.match(r"tema-(\d+)", scope)
    return f"Tema {int(m.group(1))}" if m else scope


def bloque_de(bloque_id):
    return (bloque_id or "").split("-")[-1].upper()


def pantalla_practicar():
    cabecera("Practicar", "Elige qué quieres entrenar y cuánto.")
    izq, der = st.columns([2, 3], gap="large")

    with izq:
        tipo = st.radio("Tipo", list(TIPOS_PRACTICA), format_func=TIPOS_PRACTICA.get,
                        key="tipo_practica", label_visibility="collapsed")

    ambitos = opciones_ambito()
    etiquetas = [a[0] for a in ambitos]
    if st.session_state.get("prac_ambito") not in etiquetas:
        st.session_state["prac_ambito"] = etiquetas[0]

    items_fn, titulo, disponibles, ordenado = None, "", 0, False
    with der, panel("lanzador"):
        st.markdown(f'<div class="sub">{TIPOS_PRACTICA[tipo]}</div><div class="nota">{DESC_PRACTICA[tipo]}</div>',
                    unsafe_allow_html=True)
        ambito, dificultad, procedencia = ("todo", None), None, None
        if tipo == "preparado":
            tests = consulta("""SELECT t.*, (SELECT COUNT(*) FROM test_practica_preguntas tp
                                              JOIN preguntas p ON p.id = tp.pregunta_id
                                              WHERE tp.test_id = t.id) AS n_real
                                FROM tests_practica t ORDER BY t.fecha_generacion DESC, t.id DESC""")
            if not tests:
                st.info("Todavía no hay tests preparados.")
                return
            mapa = {}
            for t in tests:
                ambito_t = etiqueta_scope(t["scope"])
                mapa[f"{t['tipo'].capitalize()}, {t['fecha_generacion']}, {t['n_real']} preguntas"
                     + (f", {ambito_t}" if ambito_t else "") + f" ({t['id'][-6:]})"] = t["id"]
            sel = st.selectbox("Test", list(mapa))
            test_id = mapa[sel]
            disponibles = next(t["n_real"] for t in tests if t["id"] == test_id)
            items_fn = lambda n: cargar_test_preparado(test_id)
            titulo, ordenado = "Test preparado", True
        elif tipo == "examen":
            examenes = listar_examenes()
            mapa = {f"TAI {etiqueta_examen(e['anio'], e['modelo'])}": e for e in examenes}
            ex = mapa[st.selectbox("Convocatoria", list(mapa), key="prac_examen")]
            sups = listar_supuestos(ex["id"])
            partes = {f"Parte teórica, {ex['n_teo']} preguntas": ("teorica", None, ex["n_teo"])}
            if ex["n_res"]:
                partes[f"Reserva teórica, {ex['n_res']} preguntas"] = ("reserva", None, ex["n_res"])
            for sp in sups:
                partes[f"{sp['titulo']} (bloque {bloque_de(sp['bloque_id'])}), {sp['n']} preguntas"] = \
                    ("supuesto", sp["id"], sp["n"])
            partes["Examen completo: teórica y supuestos, sin reserva"] = \
                ("completo", None, ex["n_teo"] + sum(sp["n"] for sp in sups))
            parte, ref, disponibles = partes[st.selectbox("Parte", list(partes), key="prac_parte")]
            titulo = f"TAI {etiqueta_examen(ex['anio'], ex['modelo'])}"
            ordenado = True
            if parte in ("teorica", "reserva"):
                items_fn = lambda n: cargar_examen_seccion(ex["id"], parte)
            elif parte == "supuesto":
                items_fn = lambda n: cargar_supuesto(ref)
            else:
                items_fn = lambda n: cargar_examen_completo(ex["id"])
            st.caption("Las preguntas sin verificar también se incluyen.")
        elif tipo == "supuesto":
            sups = listar_supuestos()
            if not sups:
                st.info("Todavía no hay supuestos.")
                return
            mapa = {f"{sp['titulo']}, {etiqueta_examen(sp['anio'], sp['modelo'])}, bloque "
                    f"{bloque_de(sp['bloque_id'])}": sp for sp in sups}
            sp = mapa[st.selectbox("Supuesto", list(mapa), key="prac_supuesto")]
            reserva = st.toggle("Incluir las preguntas de reserva", key="prac_reserva")
            disponibles = sp["n"] + (sp["n_res"] if reserva else 0)
            items_fn = lambda n: cargar_supuesto(sp["id"], reserva)
            titulo, ordenado = sp["titulo"], True
        elif tipo == "debiles":
            disponibles = contar_debiles()
            items_fn = lambda n: cargar_items_debiles(n)
            titulo = "Puntos débiles"
            st.caption("Los más fallados salen primero.")
        else:
            etiqueta_a = st.selectbox("Ámbito", etiquetas, key="prac_ambito")
            ambito = dict(ambitos)[etiqueta_a]
            if tipo in ("test", "mixto"):
                st.caption("Procedencia de las preguntas")
                p = st.radio("Procedencia", ["Todas", "De examen", "Elaboradas"], horizontal=True,
                             label_visibility="collapsed", key="pill_procedencia")
                procedencia = {"De examen": "examen", "Elaboradas": "elaborada"}.get(p)
                st.caption("Dificultad (las preguntas de examen no la tienen)")
                d = st.radio("Dificultad", ["Todas", "Baja", "Media", "Alta"], horizontal=True,
                             label_visibility="collapsed", key="pill_dificultad")
                dificultad = None if d == "Todas" else d.lower()
            disponibles = contar_disponibles(tipo, ambito, dificultad, procedencia)
            titulo = {"test": "Test", "flash": "Flashcards", "cuadros": "Cuadros", "mixto": "Mixto"}[tipo]

            def items_fn(n, tipo=tipo, ambito=ambito, dificultad=dificultad, procedencia=procedencia):
                if tipo == "test":
                    return cargar_tests(ambito, dificultad, n, procedencia)
                if tipo == "flash":
                    return cargar_flashcards(ambito, n)
                if tipo == "cuadros":
                    return cargar_cuadros(ambito, n)
                mezcla = (cargar_tests(ambito, dificultad, n, procedencia) + cargar_flashcards(ambito, n)
                          + cargar_cuadros(ambito, n))
                random.shuffle(mezcla)
                return mezcla[:n]

        if disponibles == 0:
            st.warning("No hay ítems con esos filtros.")
            return

        if ordenado:
            n = disponibles
            st.caption(f"{disponibles} preguntas, en el orden original.")
        else:
            tope = min(50, disponibles)
            if tope > 5:
                n = st.slider("Número de ítems", 5, tope, min(20, tope), 5)
            else:
                n = tope
            st.caption(f"{disponibles} ítems disponibles."
                       + (" Solo preguntas verificadas (se cambia en Ajustes)."
                          if tipo in ("test", "mixto", "debiles") and solo_verificadas() else ""))

        if st.button(f"Empezar con {n} ítems", type="primary", use_container_width=True, key="go_practica"):
            if iniciar(items_fn(n), titulo):
                st.rerun()
            st.warning("No hay ítems con esos filtros.")


# ============================================================
# PÁGINA: TEMARIO
# ============================================================

def fila_tema(t, bloque=None, mx=1.0):
    """Una fila del temario: progreso, peso en examen, fuentes y estado de verificación."""
    datos = []
    if bloque:
        datos.append(f"Bloque {romano(bloque['numero'])}")
    datos.append("temario completo" if t["estado_ingesta"] == "completo" else "solo preguntas de examen")
    if t["n_fuentes"]:
        datos.append(plural(t["n_fuentes"], "fuente", "fuentes"))
    chips = "".join(f"<span>{esc(d)}</span>" for d in datos)
    if t["sin_verif"]:
        chips += f'<span class="aviso">{t["sin_verif"]} sin verificar</span>'

    peso = ""
    if t["n_examenes"]:
        peso = (f'<div class="peso" title="Peso en examen"><div style="width:{(t["media_preg"] or 0) / mx * 100:.0f}%"></div></div>'
                f'<div class="m" style="margin:0 0 .3rem 0">Unas {num(t["media_preg"])} preguntas por examen, '
                f'en {plural(t["n_examenes"], "convocatoria", "convocatorias")}</div>')

    if t["n_items"] == 0:
        meta, barra = "Sin ítems con los filtros actuales", ""
    else:
        pct = round(t["n_dom"] / t["n_items"] * 100)
        meta = (f'{plural(t["n_items"], "ítem", "ítems")}, {pct}% dominado, '
                f'{plural(t["n_hoy"], "repaso", "repasos")} para hoy, {t["n_nuevo"]} nuevos')
        barra = barra_estados(t["n_dom"], t["n_prog"], t["n_porap"], t["n_nuevo"], fina=True)

    c1, c2 = st.columns([5, 1.4], vertical_alignment="center")
    with c1:
        st.markdown(
            f'<div class="tema {"vacio" if t["n_items"] == 0 else ""}">'
            f'<div class="t"><b>{t["numero"]}</b>{esc(t["titulo"])}</div>'
            f'<div class="m">{esc(meta)}</div>{peso}{barra}'
            f'<div class="chips">{chips}</div></div>', unsafe_allow_html=True)
    with c2:
        if t["n_items"]:
            st.button("Practicar", key=f"prac_{t['id']}", use_container_width=True,
                      on_click=_ir_a, args=(PAGINAS[1],),
                      kwargs={"tipo_practica": "mixto",
                              "prac_ambito": f"Tema {t['numero']}: {t['titulo']}"})


def pantalla_temario():
    cabecera("Temario", "Tu progreso tema a tema.")
    st.caption("Ordenar por")
    orden = st.radio("Orden", ["Temario", "Peso en examen"], horizontal=True,
                     label_visibility="collapsed", key="pill_orden_temario")
    bloques = listar_bloques_temas()
    todos = [(t, b) for b in bloques for t in b["temas"]]
    mx = max((t["media_preg"] or 0 for t, _ in todos), default=1) or 1
    if orden == "Peso en examen":
        st.caption("Media de preguntas por examen en las convocatorias cargadas: dónde se juega más puntuación.")
        for t, b in sorted(todos, key=lambda x: (-(x[0]["media_preg"] or 0), x[0]["numero"])):
            fila_tema(t, b, mx)
        return
    for b in bloques:
        st.markdown(
            f'<div class="bloque"><span class="n">{romano(b["numero"])}</span>'
            f'<span class="t">{esc(b["nombre"])}</span></div>'
            f'<div class="nota" style="margin-bottom:.4rem">{esc(b["descripcion"] or "")}</div>',
            unsafe_allow_html=True)
        for t in b["temas"]:
            fila_tema(t, None, mx)


# ============================================================
# PÁGINA: MATERIAL (cuadros y esquemas)
# ============================================================

def html_mermaid(codigo, oscuro):
    p = PALETAS["oscuro" if oscuro else "claro"]
    tema = "dark" if oscuro else "neutral"
    return f"""
    <body style="margin:0;background:{p['surface']};color:{p['text']};font-family:'Atkinson Hyperlegible',system-ui,sans-serif">
    <pre class="mermaid" style="background:{p['surface']};white-space:pre">{html.escape(codigo)}</pre>
    <script type="module">
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
      mermaid.initialize({{startOnLoad: false, theme: '{tema}'}});
      await mermaid.run({{ querySelector: '.mermaid' }});
    </script></body>"""


def pantalla_material():
    cabecera("Material", "Cuadros de datos y esquemas para estudiar con calma.")
    tab_c, tab_e = st.tabs(["Cuadros", "Esquemas"])

    with tab_c:
        cuadros = consulta("""SELECT cu.*, t.numero AS tema_numero FROM cuadros cu
                              LEFT JOIN temas t ON t.id = cu.tema_id ORDER BY cu.tema_id, cu.id""")
        if not cuadros:
            st.info("No hay cuadros todavía.")
        for cu in cuadros:
            cols = _parse_json(cu["columnas"], [])
            filas = consulta("SELECT * FROM cuadro_filas WHERE cuadro_id = ? ORDER BY id", (cu["id"],))
            cab = "".join(f"<th>{esc(nombre_columna(c))}</th>" for c in cols) + "<th>Fuente</th>"
            cuerpo = ""
            for f in filas:
                v = _parse_json(f["valores"], {})
                cuerpo += "<tr>" + "".join(f"<td>{esc(v.get(c, ''))}</td>" for c in cols) \
                          + f'<td class="f">{esc(f["fuente"] or "")}</td></tr>'
            st.markdown(f"### {cu['titulo']}")
            if cu["tema_numero"]:
                st.caption(f"Tema {cu['tema_numero']}")
            st.markdown(f'<div class="tabla-wrap"><table class="tabla"><thead><tr>{cab}</tr></thead>'
                        f'<tbody>{cuerpo}</tbody></table></div>', unsafe_allow_html=True)
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
    cabecera("Progreso", "Constancia, precisión y puntos débiles.")

    prec = f"{s['precision']:.0f}%" if s["precision"] is not None else "—"
    st.markdown(
        f'<div class="cifras"><div><b>{s["racha"]}</b><span>{"día" if s["racha"] == 1 else "días"} de racha</span></div>'
        f'<div><b>{s["n"]}</b><span>ítems en total</span></div>'
        f'<div><b>{s["dom"]}</b><span>dominados</span></div>'
        f'<div><b>{prec}</b><span>precisión</span></div></div>', unsafe_allow_html=True)

    izq, der = st.columns([2, 3], gap="large")
    with izq:
        datos = actividad(14)
        with panel("actividad"):
            st.markdown('<div class="sub">Últimos 14 días</div>'
                        f'<div class="nota">{sum(n for _, n in datos)} respuestas</div>', unsafe_allow_html=True)
            st.markdown(mapa_actividad(datos), unsafe_allow_html=True)
        with panel("estado_p"):
            st.markdown('<div class="sub">Estado de tus ítems</div>', unsafe_allow_html=True)
            st.markdown(barra_estados(s["dom"], s["prog"], s["porap"], s["nuevo"])
                        + leyenda(s["dom"], s["prog"], s["porap"], s["nuevo"]), unsafe_allow_html=True)

    with der:
        st.markdown('<h3 style="margin-top:0 !important">Puntos débiles</h3>', unsafe_allow_html=True)
        filas = consulta(f"""
            SELECT s.item_key, s.veces_fallada, s.veces_acertada {SRS_FROM}
            WHERE s.veces_fallada > 0 {srs_filtro()} ORDER BY s.veces_fallada DESC LIMIT 8""")
        conteo = {f["item_key"]: f for f in filas}
        debiles = [(conteo[i["item_key"]], i) for i in resolver_items(list(conteo))]
        if not debiles:
            st.markdown('<p class="lead">Todavía no hay fallos registrados.</p>', unsafe_allow_html=True)
        else:
            for f, i in debiles:
                q, a = resumen_item(i)
                st.markdown(
                    f'<div class="fallo"><div class="t">{esc(q)}</div>'
                    f'<div class="m"><b>{esc(a)}</b>. Fallada {f["veces_fallada"]} '
                    f'{"vez" if f["veces_fallada"] == 1 else "veces"}, acertada {f["veces_acertada"]}.</div></div>',
                    unsafe_allow_html=True)
            st.write("")
            st.button("Practicar mis puntos débiles", type="primary", use_container_width=True,
                      key="go_debiles", on_click=_ir_a, args=(PAGINAS[1],), kwargs={"tipo_practica": "debiles"})


# ============================================================
# BARRA SUPERIOR
# ============================================================

def barra_superior(en_sesion=False):
    with st.container(key="topbar"):
        c1, c2, c3 = st.columns([2.3, 6, 1.5], vertical_alignment="center")
        with c1:
            st.markdown('<div class="marca"><b>TAI</b><span>Oposición</span></div>', unsafe_allow_html=True)
        with c2:
            if en_sesion:
                st.markdown(f'<div class="sesion-titulo">{esc(st.session_state.get("titulo_sesion", ""))}</div>',
                            unsafe_allow_html=True)
            else:
                with st.container(key="nav"):
                    st.radio("Navegación", PAGINAS, key="pagina", horizontal=True,
                             label_visibility="collapsed", on_change=_nav_cambiada)
        with c3:
            with st.popover("Ajustes", use_container_width=True):
                st.toggle("Modo oscuro", key="oscuro")
                st.toggle("Solo preguntas verificadas", key="solo_verif",
                          help="Oculta del repaso y de la práctica libre las preguntas sin verificar. "
                               "Los exámenes y supuestos oficiales las incluyen siempre.")
                st.number_input("Ítems nuevos por día", min_value=0, max_value=500, step=5, key="nuevos_dia",
                                help="Máximo de ítems sin empezar que se añaden al repaso diario.")
                st.caption(f"Versión 0.5. Base de datos: {DB_PATH.name}")


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

    ss = st.session_state
    tema_inicial()
    # La navegación no se dibuja durante una sesión; se recuerda aparte para no perder la página.
    if ss.get("pagina") not in PAGINAS:
        ss["pagina"] = ss.get("_pagina", PAGINAS[0])
    ss.setdefault("solo_verif", True)
    ss.setdefault("nuevos_dia", 20)

    modo = ss.get("modo")
    barra_superior(en_sesion=modo in ("sesion", "resumen"))
    ss["_pagina"] = ss["pagina"]
    inyectar_tema()

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
        }[ss["pagina"]]()


if __name__ == "__main__":
    main()
