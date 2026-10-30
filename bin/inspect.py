#!/usr/bin/env python3
"""
inspect.py — Inspecciona el contenido de los JSON de un tema.

Uso:
    python inspect.py --tema tema-01-...                    # Resumen general
    python inspect.py --tema tema-01-... --seccion preguntas
    python inspect.py --tema tema-01-... --seccion conceptos
    python inspect.py --tema tema-01-... --seccion cuadros
    python inspect.py --tema tema-01-... --pregunta p-001
"""
import argparse
import json
from pathlib import Path

ROOT = Path("/root/.dsh/oposicion")


def cargar(ruta: Path):
    if not ruta.exists():
        return None
    with ruta.open(encoding="utf-8") as f:
        return json.load(f)


def mostrar_resumen(tema_dir: Path):
    print(f"\n📁 {tema_dir.name}\n")
    archivos = [
        ("00-texto-normalizado.md", "md"),
        ("01-indice-capitulos.json", "json"),
        ("02-conceptos-clave.json", "json"),
        ("03-banco-preguntas.json", "json"),
        ("03-flashcards.json", "json"),
        ("04-verificacion.md", "md"),
    ]
    for nombre, tipo in archivos:
        ruta = tema_dir / nombre
        if ruta.exists():
            tam = ruta.stat().st_size
            print(f"  ✅ {nombre:35s} {tam:>8,} bytes")
        else:
            print(f"  ❌ {nombre:35s} (no existe)")

    cuadros_dir = tema_dir / "06-cuadros"
    if cuadros_dir.exists():
        cuadros = list(cuadros_dir.glob("cuadro-*.json"))
        print(f"  ✅ 06-cuadros/                        {len(cuadros)} cuadros")

    print()
    conceptos = cargar(tema_dir / "02-conceptos-clave.json")
    if conceptos:
        print(f"  📚 Conceptos: {len(conceptos.get('conceptos', []))}")
        tipos = {}
        for c in conceptos.get("conceptos", []):
            tipos[c.get("tipo", "?")] = tipos.get(c.get("tipo", "?"), 0) + 1
        for t, n in sorted(tipos.items()):
            print(f"       {t}: {n}")

    preguntas = cargar(tema_dir / "03-banco-preguntas.json")
    if preguntas:
        n = len(preguntas.get("preguntas", []))
        verificadas = sum(1 for p in preguntas["preguntas"] if p.get("verificado"))
        print(f"\n  📝 Preguntas: {n} ({verificadas} verificadas)")
        tipos = {}
        for p in preguntas["preguntas"]:
            tipos[p.get("tipo", "?")] = tipos.get(p.get("tipo", "?"), 0) + 1
        for t, n in sorted(tipos.items()):
            print(f"       {t}: {n}")

    flashcards = cargar(tema_dir / "03-flashcards.json")
    if flashcards:
        n = len(flashcards.get("flashcards", []))
        print(f"\n  🎴 Flashcards: {n}")
        modos = {}
        for f in flashcards["flashcards"]:
            modos[f.get("modo", "?")] = modos.get(f.get("modo", "?"), 0) + 1
        for m, n in sorted(modos.items()):
            print(f"       {m}: {n}")


def mostrar_conceptos(tema_dir: Path):
    data = cargar(tema_dir / "02-conceptos-clave.json")
    if not data:
        print("No hay conceptos.")
        return
    for c in data.get("conceptos", []):
        print(f"\n[{c.get('id')}]")
        print(f"  Nombre: {c.get('nombre')}")
        print(f"  Tipo:   {c.get('tipo')}")
        print(f"  Valor:  {c.get('valor', '')[:200]}")
        print(f"  Norma:  {c.get('norma')} {c.get('articulo', '')}")
        print(f"  Verif.: {c.get('verificado')}")


def mostrar_preguntas(tema_dir: Path):
    data = cargar(tema_dir / "03-banco-preguntas.json")
    if not data:
        print("No hay preguntas.")
        return
    for p in data.get("preguntas", []):
        print(f"\n[{p.get('id')}] (concepto: {p.get('concepto_id')})")
        print(f"  {p.get('enunciado')}")
        for i, op in enumerate(p.get("opciones", [])):
            marca = "✓" if i == p.get("correcta") else " "
            print(f"    {marca} {chr(97+i)}) {op}")
        print(f"  Explicación: {p.get('explicacion', '')[:150]}")
        print(f"  Verificado: {p.get('verificado')}")


def mostrar_cuadros(tema_dir: Path):
    cuadros_dir = tema_dir / "06-cuadros"
    if not cuadros_dir.exists():
        print("No hay cuadros.")
        return
    for cu_file in sorted(cuadros_dir.glob("cuadro-*.json")):
        data = cargar(cu_file)
        if not data:
            continue
        print(f"\n[{data.get('id')}] {data.get('titulo')}")
        print(f"  Tipo: {data.get('tipo_dato')}")
        print(f"  Columnas: {data.get('columnas')}")
        print(f"  Filas: {len(data.get('filas', []))}")
        for fila in data.get("filas", [])[:3]:
            print(f"    - {fila.get('valores')}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tema", required=True, help="Nombre del directorio del tema")
    parser.add_argument("--seccion", choices=["conceptos", "preguntas", "cuadros"])
    parser.add_argument("--pregunta", help="ID de pregunta a mostrar")
    args = parser.parse_args()

    tema_dir = ROOT / "temario" / args.tema
    if not tema_dir.exists():
        print(f"[error] No existe: {tema_dir}")
        return

    if args.seccion == "conceptos":
        mostrar_conceptos(tema_dir)
    elif args.seccion == "preguntas":
        mostrar_preguntas(tema_dir)
    elif args.seccion == "cuadros":
        mostrar_cuadros(tema_dir)
    else:
        mostrar_resumen(tema_dir)


if __name__ == "__main__":
    main()
