#!/usr/bin/env python3
"""
valida un JSON de supuesto antes de importarlo a SQLite.
Detecta los problemas típicos: placeholders, preguntas sin contexto,
distractores absurdos, longitudes incorrectas.
"""
import json
import re
import sys
from pathlib import Path

# Patrones que NUNCA deben aparecer
PROHIBIDOS = [
    "ninguna de las anteriores",
    "todas son correctas",
    "todas las anteriores",
    "ninguna es correcta",
    "—",       # em dash como contenido
    "___",
    "...",
]

def validar_pregunta(p: dict, index: int) -> list[str]:
    """Devuelve lista de errores de una pregunta."""
    errores = []
    prefijo = f"P{index}:"

    # Campos obligatorios
    for campo in ["enunciado", "opciones", "correcta", "explicacion"]:
        if campo not in p:
            errores.append(f"{prefijo} falta campo '{campo}'")

    if "enunciado" not in p or not p.get("enunciado"):
        return errores  # nada más que validar

    enunciado = p["enunciado"].strip()
    opciones = p.get("opciones", [])
    correcta = p.get("correcta")
    explicacion = p.get("explicacion", "").strip()

    # Longitud del enunciado
    n_palabras = len(enunciado.split())
    if n_palabras < 15:
        errores.append(
            f"{prefijo} enunciado demasiado corto ({n_palabras} palabras, mín 15)"
        )
    if n_palabras > 80:
        errores.append(
            f"{prefijo} enunciado demasiado largo ({n_palabras} palabras, máx 80)"
        )

    # Opciones
    if not isinstance(opciones, list):
        errores.append(f"{prefijo} opciones no es una lista")
        return errores
    if len(opciones) != 4:
        errores.append(f"{prefijo} {len(opciones)} opciones (se esperan 4)")

    if correcta is None or not isinstance(correcta, int):
        errores.append(f"{prefijo} 'correcta' no es un entero")
    elif not (0 <= correcta <= 3):
        errores.append(f"{prefijo} 'correcta' fuera de rango: {correcta}")

    # Detectar placeholders en opciones
    for i, op in enumerate(opciones):
        if not op or op.strip() == "":
            errores.append(f"{prefijo} opción {i} vacía")
            continue
        op_lower = op.strip().lower()
        for prohibido in PROHIBIDOS:
            if op_lower == prohibido or op_lower.startswith(prohibido):
                errores.append(
                    f"{prefijo} opción {i} usa distractor prohibido: '{op}'"
                )

    # Explicación
    if len(explicacion.split()) < 10:
        errores.append(f"{prefijo} explicación demasiado corta")

    # Requiere contexto: no puede ser una pregunta trivial
    # Heurística: si el enunciado empieza por "¿Qué es" o "¿Cuál es la
    # definición de", es sospechosa
    sospechosos = [
        r"^¿qué es ",
        r"^¿cuál es la definición",
        r"^defina ",
        r"^explique qué es ",
    ]
    for patron in sospechosos:
        if re.match(patron, enunciado.lower()):
            errores.append(
                f"{prefijo} pregunta no requiere contexto: '{enunciado[:50]}...'"
            )
            break

    return errores


def validar_supuesto(path: Path) -> tuple[bool, list[str]]:
    """Valida el supuesto completo. Devuelve (es_valido, errores)."""
    try:
        with path.open(encoding="utf-8") as f:
            sup = json.load(f)
    except Exception as e:
        return False, [f"No se puede leer el JSON: {e}"]

    errores = []

    # Campos obligatorios a nivel de supuesto
    for campo in ["id", "bloque_id", "titulo", "tipo", "origen",
                  "contexto_texto", "contexto_json", "preguntas"]:
        if campo not in sup:
            errores.append(f"Falta campo obligatorio '{campo}'")

    if errores:
        return False, errores

    # contexto_texto mínimo 50 palabras
    if len(sup["contexto_texto"].split()) < 50:
        errores.append(
            f"contexto_texto demasiado corto "
            f"({len(sup['contexto_texto'].split())} palabras, mín 50)"
        )

    # Preguntas
    preguntas = sup.get("preguntas", [])
    if len(preguntas) < 15:
        errores.append(
            f"Pocas preguntas ({len(preguntas)}, mín 15)"
        )

    for i, p in enumerate(preguntas, 1):
        errores.extend(validar_pregunta(p, i))

    # Artefactos
    artefactos = sup.get("artefactos", [])
    if len(artefactos) == 0:
        errores.append("Falta al menos 1 artefacto")

    return len(errores) == 0, errores


def main():
    if len(sys.argv) < 2:
        print("Uso: validar_supuesto.py <ruta-al-json>")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"❌ No existe: {path}")
        sys.exit(1)

    ok, errores = validar_supuesto(path)

    if ok:
        with path.open(encoding="utf-8") as f:
            sup = json.load(f)
        print(f"✅ Supuesto válido: {sup.get('id')}")
        print(f"   - {len(sup.get('preguntas', []))} preguntas")
        print(f"   - {len(sup.get('artefactos', []))} artefactos")
        print(f"   - {len(sup.get('temas_implicados', []))} temas vinculados")
        sys.exit(0)
    else:
        print(f"❌ Supuesto INVÁLIDO: {path.name}")
        print(f"   {len(errores)} errores encontrados:")
        for err in errores:
            print(f"   - {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
