#!/usr/bin/env python3
"""
db.py — Gestor de la base de datos SQLite del sistema TAI Oposición.

Uso:
    python db.py init --root ~/oposicion
    python db.py init --root ~/oposicion --force

Subcomandos disponibles (en este script):
    init       Crea el schema + inserta los 4 bloques y los 33 temas vacíos
"""

import argparse
import sqlite3
import sys
from pathlib import Path

# ============================================================
# DISTRIBUCIÓN DE LOS 33 TEMAS TAI 2026
# ============================================================
# NOTA: Ajustar según el BOE oficial de la convocatoria vigente.
# La distribución aquí indicada es la habitual en convocatorias recientes.
TEMAS_TAI = {
    "bloque-i": [
        (1,  "La Constitución Española de 1978"),
        (2,  "La Corona"),
        (3,  "Las Cortes Generales"),
        (4,  "El Gobierno y la Administración"),
        (5,  "El Poder Judicial"),
        (6,  "El Tribunal Constitucional"),
        (7,  "La organización territorial del Estado"),
        (8,  "La Unión Europea"),
    ],
    "bloque-ii": [
        (9,  "El Estatuto Básico del Empleado Público"),
        (10, "La Ley 39/2015 del Procedimiento Administrativo Común"),
        (11, "La Ley 40/2015 de Régimen Jurídico del Sector Público"),
        (12, "La Ley 19/2013 de Transparencia y Buen Gobierno"),
        (13, "Contratos del Sector Público"),
        (14, "Presupuestos Generales del Estado"),
    ],
    "bloque-iii": [
        (15, "Modelado de datos, metodologías y reglas"),
        (16, "Bases de datos relacionales: SQL"),
        (17, "Bases de datos NoSQL y Big Data"),
        (18, "Metodologías de desarrollo"),
        (19, "Lenguajes de programación"),
        (20, "Arquitectura de aplicaciones"),
        (21, "Servicios web y APIs"),
        (22, "Pruebas de software"),
        (23, "Accesibilidad y usabilidad"),
        (24, "Seguridad en aplicaciones"),
    ],
    "bloque-iv": [
        (25, "Redes de comunicaciones"),
        (26, "Protocolos TCP/IP"),
        (27, "Seguridad en redes"),
        (28, "Sistemas operativos"),
        (29, "Virtualización y contenedores"),
        (30, "Almacenamiento y backup"),
        (31, "Centros de procesamiento de datos"),
        (32, "Cloud computing"),
        (33, "Gestión de incidentes y continuidad"),
    ],
}

BLOQUES = [
    ("bloque-i", 1, "Organización del Estado y Administración electrónica",
     "Constitución, Corona, Cortes, Gobierno, Poder Judicial, TC, organización territorial, UE", 0),
    ("bloque-ii", 2, "Administración Pública",
     "Empleado público, procedimiento administrativo, transparencia, contratos, presupuestos", 0),
    ("bloque-iii", 3, "Informática básica",
     "Modelado de datos, bases de datos, desarrollo de software, testing, accesibilidad", 1),
    ("bloque-iv", 4, "Sistemas y comunicaciones",
     "Redes, protocolos, seguridad, sistemas operativos, virtualización, cloud, CPD", 1),
]


# ============================================================
# SCHEMA
# ============================================================

SCHEMA_SQL = """
-- ============================================================
-- NIVEL 1: BLOQUES
-- ============================================================
CREATE TABLE bloques (
    id TEXT PRIMARY KEY,
    numero INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    tiene_supuestos BOOLEAN DEFAULT 0
);

CREATE INDEX idx_bloques_numero ON bloques(numero);

-- ============================================================
-- NIVEL 2: TEMAS
-- ============================================================
CREATE TABLE temas (
    id TEXT PRIMARY KEY,
    numero INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    bloque_id TEXT NOT NULL REFERENCES bloques(id),
    tipo TEXT,
    estado_ingesta TEXT DEFAULT 'pendiente',
    fecha_ingesta TEXT,
    UNIQUE(bloque_id, numero)
);

CREATE INDEX idx_temas_bloque ON temas(bloque_id);
CREATE INDEX idx_temas_estado ON temas(estado_ingesta);

-- ============================================================
-- NIVEL 3: CONCEPTOS (transversales)
-- ============================================================
CREATE TABLE conceptos (
    id TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    tipo TEXT,
    valor TEXT,
    norma TEXT,
    articulo TEXT,
    tags TEXT,
    verificado BOOLEAN DEFAULT 0,
    es_semilla BOOLEAN DEFAULT 0
);

CREATE INDEX idx_conceptos_tipo ON conceptos(tipo);
CREATE INDEX idx_conceptos_verificado ON conceptos(verificado);

CREATE TABLE concepto_temas (
    concepto_id TEXT NOT NULL REFERENCES conceptos(id),
    tema_id TEXT NOT NULL REFERENCES temas(id),
    es_principal BOOLEAN DEFAULT 0,
    PRIMARY KEY (concepto_id, tema_id)
);

CREATE INDEX idx_ct_concepto ON concepto_temas(concepto_id);
CREATE INDEX idx_ct_tema ON concepto_temas(tema_id);
CREATE INDEX idx_ct_principal ON concepto_temas(es_principal);

-- ============================================================
-- CONTENIDO: PREGUNTAS
-- ============================================================
CREATE TABLE preguntas (
    id TEXT PRIMARY KEY,
    tema_id TEXT REFERENCES temas(id),
    concepto_id TEXT REFERENCES conceptos(id),
    capitulo TEXT,
    tipo TEXT,
    dificultad TEXT,
    origen TEXT,
    enunciado TEXT NOT NULL,
    opciones TEXT NOT NULL,
    correcta INTEGER NOT NULL CHECK (correcta >= 0 AND correcta <= 3),
    explicacion TEXT,
    referencia TEXT,
    verificado BOOLEAN DEFAULT 0,
    hash_exacto TEXT UNIQUE,
    hash_normalizado TEXT,
    veces_fallada INTEGER DEFAULT 0,
    veces_acertada INTEGER DEFAULT 0,
    fecha_alta TEXT
);

CREATE INDEX idx_preg_tema ON preguntas(tema_id);
CREATE INDEX idx_preg_concepto ON preguntas(concepto_id);
CREATE INDEX idx_preg_hash_norm ON preguntas(hash_normalizado);
CREATE INDEX idx_preg_tipo ON preguntas(tipo);
CREATE INDEX idx_preg_verificado ON preguntas(verificado);

-- ============================================================
-- CONTENIDO: FLASHCARDS
-- ============================================================
CREATE TABLE flashcards (
    id TEXT PRIMARY KEY,
    tema_id TEXT REFERENCES temas(id),
    concepto_id TEXT REFERENCES conceptos(id),
    modo TEXT NOT NULL,
    anverso TEXT,
    reverso TEXT,
    texto TEXT,
    respuestas TEXT,
    tags TEXT,
    verificado BOOLEAN DEFAULT 0,
    hash_normalizado TEXT
);

CREATE INDEX idx_card_tema ON flashcards(tema_id);
CREATE INDEX idx_card_concepto ON flashcards(concepto_id);
CREATE INDEX idx_card_modo ON flashcards(modo);

-- ============================================================
-- CONTENIDO: CUADROS TRANSVERSALES
-- ============================================================
CREATE TABLE cuadros (
    id TEXT PRIMARY KEY,
    tema_id TEXT REFERENCES temas(id),
    tipo_dato TEXT NOT NULL,
    titulo TEXT NOT NULL,
    semilla BOOLEAN DEFAULT 0,
    n_filas INTEGER DEFAULT 0,
    n_fuentes_distintas INTEGER DEFAULT 0,
    columnas TEXT NOT NULL,
    columna_clave TEXT,
    columna_respuesta TEXT,
    columna_contexto TEXT,
    columna_fuente TEXT,
    verificado BOOLEAN DEFAULT 0
);

CREATE INDEX idx_cuadro_tema ON cuadros(tema_id);
CREATE INDEX idx_cuadro_tipo ON cuadros(tipo_dato);

CREATE TABLE cuadro_filas (
    id TEXT PRIMARY KEY,
    cuadro_id TEXT NOT NULL REFERENCES cuadros(id),
    fuente TEXT,
    fuente_tipo TEXT,
    valores TEXT NOT NULL,
    pasaje_origen TEXT,
    ubicacion TEXT,
    verificado BOOLEAN DEFAULT 0
);

CREATE INDEX idx_cf_cuadro ON cuadro_filas(cuadro_id);
CREATE INDEX idx_cf_fuente_tipo ON cuadro_filas(fuente_tipo);

-- ============================================================
-- CONTENIDO: ESQUEMAS
-- ============================================================
CREATE TABLE esquemas (
    id TEXT PRIMARY KEY,
    tema_id TEXT REFERENCES temas(id),
    formato TEXT NOT NULL,
    seleccion_modo TEXT,
    seleccion_valor TEXT,
    contenido TEXT NOT NULL,
    n_nodos INTEGER,
    verificado BOOLEAN DEFAULT 0
);

CREATE INDEX idx_esq_tema ON esquemas(tema_id);
CREATE INDEX idx_esq_formato ON esquemas(formato);

-- ============================================================
-- SUPUESTOS PRÁCTICOS
-- ============================================================
CREATE TABLE supuestos (
    id TEXT PRIMARY KEY,
    examen_id TEXT,
    bloque_id TEXT NOT NULL REFERENCES bloques(id),
    numero INTEGER,
    titulo TEXT NOT NULL,
    tipo TEXT,
    origen TEXT DEFAULT 'real',
    contexto_texto TEXT,
    contexto_json TEXT,
    verificado BOOLEAN DEFAULT 0
);

CREATE INDEX idx_sup_bloque ON supuestos(bloque_id);
CREATE INDEX idx_sup_origen ON supuestos(origen);
CREATE INDEX idx_sup_examen ON supuestos(examen_id);

CREATE TABLE supuesto_preguntas (
    supuesto_id TEXT NOT NULL REFERENCES supuestos(id),
    pregunta_id TEXT NOT NULL REFERENCES preguntas(id),
    numero_en_supuesto INTEGER,
    es_reserva BOOLEAN DEFAULT 0,
    PRIMARY KEY (supuesto_id, pregunta_id)
);

CREATE INDEX idx_sp_pregunta ON supuesto_preguntas(pregunta_id);

CREATE TABLE supuesto_temas (
    supuesto_id TEXT NOT NULL REFERENCES supuestos(id),
    tema_id TEXT NOT NULL REFERENCES temas(id),
    n_preguntas INTEGER DEFAULT 0,
    PRIMARY KEY (supuesto_id, tema_id)
);

CREATE INDEX idx_st_tema ON supuesto_temas(tema_id);

CREATE TABLE supuesto_artefactos (
    id TEXT PRIMARY KEY,
    supuesto_id TEXT NOT NULL REFERENCES supuestos(id),
    tipo TEXT NOT NULL,
    titulo TEXT,
    contenido TEXT NOT NULL,
    orden INTEGER DEFAULT 0
);

CREATE INDEX idx_art_sup ON supuesto_artefactos(supuesto_id);

-- ============================================================
-- EXÁMENES OFICIALES
-- ============================================================
CREATE TABLE examenes (
    id TEXT PRIMARY KEY,
    anio INTEGER,
    convocatoria TEXT,
    modelo TEXT,
    tipo TEXT,
    fecha TEXT,
    total_teoricas INTEGER,
    total_reserva INTEGER,
    n_supuestos INTEGER,
    verificado BOOLEAN DEFAULT 0
);

CREATE INDEX idx_exam_anio ON examenes(anio);

CREATE TABLE examen_preguntas (
    examen_id TEXT NOT NULL REFERENCES examenes(id),
    pregunta_id TEXT NOT NULL,
    seccion TEXT NOT NULL,
    numero INTEGER NOT NULL,
    respuesta_oficial TEXT,
    PRIMARY KEY (examen_id, seccion, numero)
);

CREATE INDEX idx_examp_pregunta ON examen_preguntas(pregunta_id);
CREATE INDEX idx_examp_seccion ON examen_preguntas(seccion);

CREATE TABLE examen_resultados (
    examen_id TEXT NOT NULL REFERENCES examenes(id),
    fecha TEXT NOT NULL,
    puntuacion INTEGER,
    por_bloque TEXT,
    por_seccion TEXT,
    PRIMARY KEY (examen_id, fecha)
);

-- ============================================================
-- TESTS DE PRÁCTICA
-- ============================================================
CREATE TABLE tests_practica (
    id TEXT PRIMARY KEY,
    tipo TEXT NOT NULL,
    scope TEXT,
    fecha_generacion TEXT NOT NULL,
    n_preguntas INTEGER NOT NULL,
    cuotas TEXT,
    origen TEXT
);

CREATE INDEX idx_tp_tipo ON tests_practica(tipo);
CREATE INDEX idx_tp_scope ON tests_practica(scope);
CREATE INDEX idx_tp_fecha ON tests_practica(fecha_generacion);

CREATE TABLE test_practica_preguntas (
    test_id TEXT NOT NULL REFERENCES tests_practica(id),
    pregunta_id TEXT NOT NULL REFERENCES preguntas(id),
    numero INTEGER NOT NULL,
    PRIMARY KEY (test_id, numero)
);

CREATE INDEX idx_tpp_pregunta ON test_practica_preguntas(pregunta_id);

-- ============================================================
-- SRS: REPASO ESPACIADO
-- ============================================================
CREATE TABLE srs_items (
    item_key TEXT PRIMARY KEY,
    tipo TEXT NOT NULL,
    tema_id TEXT,
    bloque_id TEXT,
    concepto_id TEXT,
    estado TEXT NOT NULL DEFAULT 'sin-empezar',
    ease REAL DEFAULT 2.5,
    intervalo_dias INTEGER DEFAULT 0,
    due TEXT NOT NULL,
    veces_fallada INTEGER DEFAULT 0,
    veces_acertada INTEGER DEFAULT 0,
    ultima_respuesta TEXT,
    problematico BOOLEAN DEFAULT 0
);

CREATE INDEX idx_srs_due ON srs_items(due);
CREATE INDEX idx_srs_tema ON srs_items(tema_id);
CREATE INDEX idx_srs_bloque ON srs_items(bloque_id);
CREATE INDEX idx_srs_concepto ON srs_items(concepto_id);
CREATE INDEX idx_srs_estado ON srs_items(estado);
CREATE INDEX idx_srs_problematico ON srs_items(problematico);

CREATE TABLE srs_historial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_key TEXT NOT NULL REFERENCES srs_items(item_key),
    fecha TEXT NOT NULL,
    respuesta TEXT NOT NULL,
    intervalo INTEGER
);

CREATE INDEX idx_hist_item ON srs_historial(item_key);
CREATE INDEX idx_hist_fecha ON srs_historial(fecha);
"""


VISTAS_SQL = """
-- Vista: qué toca hoy (agrupado por tema/bloque/concepto)
CREATE VIEW v_para_hoy AS
SELECT
    s.tema_id,
    s.bloque_id,
    s.concepto_id,
    COUNT(*) AS n_items,
    MIN(s.estado) AS peor_estado,
    MIN(s.due) AS due_mas_temprano
FROM srs_items s
WHERE s.due <= date('now')
  AND s.estado != 'dominado'
GROUP BY s.tema_id, s.bloque_id, s.concepto_id;

-- Vista: cobertura por tema
CREATE VIEW v_cobertura AS
SELECT
    t.id AS tema_id,
    t.titulo,
    t.estado_ingesta,
    COUNT(DISTINCT p.id) AS total_preguntas,
    COUNT(DISTINCT p.concepto_id) AS conceptos_cubiertos,
    SUM(CASE WHEN p.verificado = 0 THEN 1 ELSE 0 END) AS sin_verificar
FROM temas t
LEFT JOIN preguntas p ON p.tema_id = t.id
GROUP BY t.id;

-- Vista: distribución por dificultad y tipo
CREATE VIEW v_dificultad AS
SELECT
    tema_id,
    tipo,
    dificultad,
    COUNT(*) AS n
FROM preguntas
GROUP BY tema_id, tipo, dificultad;

-- Vista: ítems problemáticos (leech)
CREATE VIEW v_problematicos AS
SELECT
    s.*,
    p.enunciado
FROM srs_items s
LEFT JOIN preguntas p
    ON s.item_key = 'test:' || s.tema_id || ':' || p.id
WHERE s.veces_fallada >= 8;
"""


# ============================================================
# FUNCIONES
# ============================================================

def conectar(db_path: Path) -> sqlite3.Connection:
    """Abre conexión con pragmas óptimos."""
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA synchronous = NORMAL")
    conn.execute("PRAGMA cache_size = -64000")  # 64 MB
    return conn


def crear_schema(conn: sqlite3.Connection) -> None:
    """Crea todas las tablas y vistas."""
    conn.executescript(SCHEMA_SQL)
    conn.executescript(VISTAS_SQL)
    conn.commit()


def insertar_bloques(conn: sqlite3.Connection) -> int:
    """Inserta los 4 bloques. Devuelve el número insertado."""
    conn.executemany(
        "INSERT INTO bloques (id, numero, nombre, descripcion, tiene_supuestos) "
        "VALUES (?, ?, ?, ?, ?)",
        BLOQUES,
    )
    conn.commit()
    return len(BLOQUES)


def insertar_temas(conn: sqlite3.Connection) -> int:
    """Inserta los 33 temas vacíos con estado_ingesta='pendiente'."""
    total = 0
    for bloque_id, temas in TEMAS_TAI.items():
        # Determinar tipo de tema por bloque
        tipo = "tecnico" if bloque_id in ("bloque-iii", "bloque-iv") else "juridico"
        for numero, titulo in temas:
            tema_id = f"tema-{numero:02d}-{slugify(titulo)}"
            conn.execute(
                "INSERT INTO temas (id, numero, titulo, bloque_id, tipo, estado_ingesta) "
                "VALUES (?, ?, ?, ?, ?, 'pendiente')",
                (tema_id, numero, titulo, bloque_id, tipo),
            )
            total += 1
    conn.commit()
    return total


def slugify(texto: str) -> str:
    """Convierte un título en un slug válido para id."""
    import unicodedata
    import re
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("ascii")
    texto = texto.lower()
    texto = re.sub(r"[^a-z0-9]+", "-", texto)
    texto = texto.strip("-")
    return texto[:60]  # truncar para mantener IDs cortos


def verificar(conn: sqlite3.Connection) -> dict:
    """Comprueba que el schema y los inserts están correctos."""
    resultado = {}

    # Tablas
    cur = conn.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type='table' "
        "AND name NOT LIKE 'sqlite_%'"
    )
    resultado["tablas"] = cur.fetchone()[0]

    # Vistas
    cur = conn.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type='view'"
    )
    resultado["vistas"] = cur.fetchone()[0]

    # Índices
    cur = conn.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type='index' "
        "AND name NOT LIKE 'sqlite_%' AND name NOT LIKE 'sqlite_autoindex%'"
    )
    resultado["indices"] = cur.fetchone()[0]

    # Bloques
    cur = conn.execute("SELECT COUNT(*) FROM bloques")
    resultado["bloques"] = cur.fetchone()[0]

    # Temas por bloque
    cur = conn.execute(
        "SELECT bloque_id, COUNT(*) FROM temas GROUP BY bloque_id ORDER BY bloque_id"
    )
    resultado["temas_por_bloque"] = dict(cur.fetchall())

    # Total temas
    cur = conn.execute("SELECT COUNT(*) FROM temas")
    resultado["temas_total"] = cur.fetchone()[0]

    # Integridad de FK
    cur = conn.execute("PRAGMA foreign_key_check")
    resultado["fk_errores"] = len(cur.fetchall())

    return resultado


# ============================================================
# COMANDOS CLI
# ============================================================

def cmd_init(args) -> int:
    """Comando: crear la BD + insertar bloques y temas."""
    root = Path(args.root).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    db_path = root / "oposicion.db"

    if db_path.exists():
        if not args.force:
            print(f"[error] La BD ya existe: {db_path}")
            print(f"        Usa --force para sobreescribirla (¡se perderán los datos!).")
            return 1
        print(f"[aviso] Sobreescribiendo BD existente: {db_path}")
        db_path.unlink()

    print(f"[init] Creando BD en {db_path}")
    conn = conectar(db_path)

    try:
        print(f"[init] Creando schema...")
        crear_schema(conn)

        print(f"[init] Insertando {len(BLOQUES)} bloques...")
        n_bloques = insertar_bloques(conn)

        print(f"[init] Insertando {sum(len(v) for v in TEMAS_TAI.values())} temas...")
        n_temas = insertar_temas(conn)

        print(f"[init] Verificando integridad...")
        resultado = verificar(conn)

        print()
        print("=" * 60)
        print(f"  ✅ Base de datos creada correctamente")
        print("=" * 60)
        print(f"  Ruta:        {db_path}")
        print(f"  Tamaño:      {db_path.stat().st_size / 1024:.1f} KB")
        print(f"  Tablas:      {resultado['tablas']}")
        print(f"  Vistas:      {resultado['vistas']}")
        print(f"  Índices:     {resultado['indices']}")
        print(f"  Bloques:     {resultado['bloques']}")
        print(f"  Temas:       {resultado['temas_total']}")
        print(f"  Errores FK:  {resultado['fk_errores']}")
        print()
        print("  Distribución por bloque:")
        for bloque_id, n in resultado["temas_por_bloque"].items():
            print(f"    {bloque_id}: {n} temas")
        print("=" * 60)

        if resultado["fk_errores"] > 0:
            print(f"\n[error] Hay {resultado['fk_errores']} errores de integridad")
            return 1

        return 0

    except Exception as e:
        print(f"[error] {e}")
        return 1
    finally:
        conn.close()

# ============================================================
# MIGRACIÓN: JSON → SQLite
# ============================================================

import hashlib
import json
import re
import unicodedata
from datetime import date


# ------------------------------------------------------------
# Utilidades de normalización y similitud
# ------------------------------------------------------------

def normalizar_texto(texto: str) -> str:
    """Lowercase + sin acentos + sin puntuación. Para hash_normalizado."""
    if not texto:
        return ""
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("ascii")
    texto = texto.lower()
    texto = re.sub(r"[^a-z0-9\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


def sha256_exacto(*partes: str) -> str:
    """Hash SHA-256 de la concatenación de partes (para dedup exacta)."""
    texto = "||".join(str(p) for p in partes)
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def similitud_jaccard(a: str, b: str) -> float:
    """Similitud Jaccard por tokens. Umbral típico: 0.85."""
    tokens_a = set(normalizar_texto(a).split())
    tokens_b = set(normalizar_texto(b).split())
    if not tokens_a or not tokens_b:
        return 0.0
    inter = tokens_a & tokens_b
    union = tokens_a | tokens_b
    return len(inter) / len(union)


# ------------------------------------------------------------
# Deduplicación de conceptos
# ------------------------------------------------------------

def buscar_o_crear_concepto(
    conn: sqlite3.Connection,
    nombre: str,
    tipo: str | None,
    valor: str | None,
    norma: str | None,
    articulo: str | None,
    tags: list[str] | None,
    verificado: bool,
) -> tuple[str, bool]:
    """
    Busca un concepto por nombre normalizado + valor.
    Si existe, devuelve (id_existente, False).
    Si no existe, lo crea y devuelve (id_nuevo, True).
    """
    nombre_norm = normalizar_texto(nombre)
    valor_norm = normalizar_texto(valor or "")

    # Buscar por nombre normalizado + valor normalizado
    cur = conn.execute("""
        SELECT id FROM conceptos
        WHERE lower(nombre) = lower(?)
          AND COALESCE(lower(valor), '') = lower(?)
        LIMIT 1
    """, (nombre, valor or ""))
    row = cur.fetchone()
    if row:
        return row[0], False

    # Crear nuevo
    concepto_id = f"c-{hashlib.sha1(nombre_norm.encode()).hexdigest()[:12]}"
    conn.execute("""
        INSERT INTO conceptos (
            id, nombre, tipo, valor, norma, articulo, tags, verificado, es_semilla
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
    """, (
        concepto_id, nombre, tipo, valor, norma, articulo,
        json.dumps(tags or [], ensure_ascii=False),
        int(verificado),
    ))
    return concepto_id, True


def vincular_concepto_tema(
    conn: sqlite3.Connection,
    concepto_id: str,
    tema_id: str,
    es_principal: bool,
) -> bool:
    """
    Crea la relación concepto-tema si no existe.
    Devuelve True si es nueva, False si ya existía.
    """
    cur = conn.execute("""
        SELECT 1 FROM concepto_temas
        WHERE concepto_id = ? AND tema_id = ?
    """, (concepto_id, tema_id))
    if cur.fetchone():
        return False

    conn.execute("""
        INSERT INTO concepto_temas (concepto_id, tema_id, es_principal)
        VALUES (?, ?, ?)
    """, (concepto_id, tema_id, int(es_principal)))
    return True


# ------------------------------------------------------------
# Deduplicación de preguntas
# ------------------------------------------------------------

def buscar_pregunta_duplicada(
    conn: sqlite3.Connection,
    enunciado: str,
    opciones: list[str],
    correcta: int,
    concepto_id: str | None,
    tipo: str | None,
) -> tuple[str | None, str]:
    """
    Devuelve (id_existente, motivo) o (None, 'nueva').
    Motivos: 'exacta', 'conceptual', 'nueva'.
    """
    # 1. Hash exacto
    h_exacto = sha256_exacto(enunciado, *opciones, str(correcta))
    cur = conn.execute(
        "SELECT id FROM preguntas WHERE hash_exacto = ?", (h_exacto,)
    )
    row = cur.fetchone()
    if row:
        return row[0], "exacta"

    # 2. Mismo concepto + tipo + similitud
    if concepto_id:
        cur = conn.execute("""
            SELECT id, enunciado FROM preguntas
            WHERE concepto_id = ?
              AND COALESCE(tipo, '') = COALESCE(?, '')
        """, (concepto_id, tipo))
        for pid, penun in cur.fetchall():
            if similitud_jaccard(enunciado, penun) > 0.85:
                return pid, "conceptual"

    return None, "nueva"


# ------------------------------------------------------------
# Migración de un tema
# ------------------------------------------------------------

def migrar_tema(
    conn: sqlite3.Connection,
    tema_dir: Path,
    dry_run: bool = False,
) -> dict:
    """
    Migra un tema completo (conceptos, preguntas, flashcards, cuadros,
    esquemas) desde sus JSON a SQLite.
    """
    resultado = {
        "tema_id": None,
        "estado": "ok",
        "conceptos_nuevos": 0,
        "conceptos_reutilizados": 0,
        "vinculos_nuevos": 0,
        "preguntas_nuevas": 0,
        "preguntas_dup_exacta": 0,
        "preguntas_dup_conceptual": 0,
        "flashcards_nuevas": 0,
        "flashcards_dup": 0,
        "cuadros_nuevos": 0,
        "cuadro_filas_nuevas": 0,
        "esquemas_nuevos": 0,
        "errores": [],
    }

    # 1. Verificar que el tema existe en la BD
    tema_id = tema_dir.name
    cur = conn.execute("SELECT id, tipo FROM temas WHERE id = ?", (tema_id,))
    row = cur.fetchone()
    if not row:
        resultado["estado"] = "tema_no_encontrado"
        resultado["errores"].append(f"Tema {tema_id} no está en la BD. Ejecuta init primero.")
        return resultado

    resultado["tema_id"] = tema_id
    tipo_tema = row[1]  # 'juridico' o 'tecnico'

    # 2. Conceptos clave
    conceptos_path = tema_dir / "02-conceptos-clave.json"
    mapa_conceptos = {}  # {id_original: id_en_bd}
    if conceptos_path.exists():
        with conceptos_path.open(encoding="utf-8") as f:
            data = json.load(f)
        for c in data.get("conceptos", []):
            cid, es_nuevo = buscar_o_crear_concepto(
                conn,
                nombre=c.get("nombre", ""),
                tipo=c.get("tipo"),
                valor=c.get("valor") or c.get("definicion"),
                norma=c.get("norma"),
                articulo=c.get("articulo"),
                tags=c.get("tags_transversales") or c.get("tags", []),
                verificado=c.get("verificado", False),
            )
            mapa_conceptos[c.get("id", cid)] = cid
            if es_nuevo:
                resultado["conceptos_nuevos"] += 1
            else:
                resultado["conceptos_reutilizados"] += 1

            # Vincular al tema
            es_principal = c.get("es_principal", True)
            if vincular_concepto_tema(conn, cid, tema_id, es_principal):
                resultado["vinculos_nuevos"] += 1

    # 3. Banco de preguntas
    bp_path = tema_dir / "03-banco-preguntas.json"
    if bp_path.exists():
        with bp_path.open(encoding="utf-8") as f:
            data = json.load(f)
        for p in data.get("preguntas", []):
            concepto_id = mapa_conceptos.get(p.get("concepto_id"), p.get("concepto_id"))
            opciones = p.get("opciones", [])
            enunciado = p.get("enunciado", "")
            correcta = p.get("correcta", 0)

            pid_dup, motivo = buscar_pregunta_duplicada(
                conn, enunciado, opciones, correcta, concepto_id, p.get("tipo")
            )
            if pid_dup:
                if motivo == "exacta":
                    resultado["preguntas_dup_exacta"] += 1
                else:
                    resultado["preguntas_dup_conceptual"] += 1
                continue

            # Insertar nueva
            h_exacto = sha256_exacto(enunciado, *opciones, str(correcta))
            h_norm = normalizar_texto(enunciado)
            if not dry_run:
                conn.execute("""
                    INSERT INTO preguntas (
                        id, tema_id, concepto_id, capitulo, tipo, dificultad, origen,
                        enunciado, opciones, correcta, explicacion, referencia,
                        verificado, hash_exacto, hash_normalizado, fecha_alta
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    p.get("id", f"p-{hashlib.sha1(h_exacto.encode()).hexdigest()[:10]}"),
                    tema_id,
                    concepto_id,
                    p.get("capitulo"),
                    p.get("tipo"),
                    p.get("dificultad", "media"),
                    p.get("origen", "ingesta-inicial"),
                    enunciado,
                    json.dumps(opciones, ensure_ascii=False),
                    correcta,
                    p.get("explicacion"),
                    p.get("referencia"),
                    int(p.get("verificado", False)),
                    h_exacto,
                    h_norm,
                    p.get("fecha_alta", date.today().isoformat()),
                ))
            resultado["preguntas_nuevas"] += 1

    # 4. Flashcards
    fc_path = tema_dir / "03-flashcards.json"
    if fc_path.exists():
        with fc_path.open(encoding="utf-8") as f:
            data = json.load(f)
        for c in data.get("flashcards", []):
            concepto_id = mapa_conceptos.get(c.get("concepto_id"), c.get("concepto_id"))
            # Dedup por hash normalizado
            texto_para_hash = c.get("anverso") or c.get("texto", "")
            h_norm = normalizar_texto(texto_para_hash)
            cur = conn.execute(
                "SELECT id FROM flashcards WHERE hash_normalizado = ?", (h_norm,)
            )
            if cur.fetchone():
                resultado["flashcards_dup"] += 1
                continue

            if not dry_run:
                conn.execute("""
                    INSERT INTO flashcards (
                        id, tema_id, concepto_id, modo, anverso, reverso, texto,
                        respuestas, tags, verificado, hash_normalizado
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    c.get("id", f"fc-{hashlib.sha1(h_norm.encode()).hexdigest()[:10]}"),
                    tema_id,
                    concepto_id,
                    c.get("modo", "anverso-reverso"),
                    c.get("anverso"),
                    c.get("reverso"),
                    c.get("texto"),
                    json.dumps(c.get("respuestas", []), ensure_ascii=False),
                    json.dumps(c.get("tags", []), ensure_ascii=False),
                    int(c.get("verificado", False)),
                    h_norm,
                ))
            resultado["flashcards_nuevas"] += 1

    # 5. Cuadros transversales
    cuadros_dir = tema_dir / "06-cuadros"
    if cuadros_dir.exists():
        for cu_file in cuadros_dir.glob("cuadro-*.json"):
            with cu_file.open(encoding="utf-8") as f:
                cu = json.load(f)
            cuadro_id = cu.get("id", cu_file.stem)
            # Dedup por id
            cur = conn.execute("SELECT id FROM cuadros WHERE id = ?", (cuadro_id,))
            if cur.fetchone():
                continue

            if not dry_run:
                conn.execute("""
                    INSERT INTO cuadros (
                        id, tema_id, tipo_dato, titulo, semilla, n_filas,
                        n_fuentes_distintas, columnas, columna_clave, columna_respuesta,
                        columna_contexto, columna_fuente, verificado
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    cuadro_id,
                    tema_id,
                    cu.get("tipo_dato"),
                    cu.get("titulo"),
                    int(cu.get("semilla", False)),
                    cu.get("n_filas", len(cu.get("filas", []))),
                    cu.get("n_fuentes_distintas", 0),
                    json.dumps(cu.get("columnas", []), ensure_ascii=False),
                    cu.get("columna_clave"),
                    cu.get("columna_respuesta"),
                    cu.get("columna_contexto"),
                    cu.get("columna_fuente"),
                    int(cu.get("verificado", True)),
                ))
            resultado["cuadros_nuevos"] += 1

            # Filas
            for fila in cu.get("filas", []):
                if not dry_run:
                    conn.execute("""
                        INSERT OR IGNORE INTO cuadro_filas (
                            id, cuadro_id, fuente, fuente_tipo, valores,
                            pasaje_origen, ubicacion, verificado
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        fila.get("id"),
                        cuadro_id,
                        fila.get("fuente"),
                        fila.get("fuente_tipo"),
                        json.dumps(fila.get("valores", {}), ensure_ascii=False),
                        fila.get("pasaje_origen"),
                        json.dumps(fila.get("ubicacion", {}), ensure_ascii=False),
                        int(fila.get("verificado", True)),
                    ))
                resultado["cuadro_filas_nuevas"] += 1

    # 6. Esquemas
    esq_dir = tema_dir / "02-esquemas"
    if esq_dir.exists():
        for esq_file in esq_dir.glob("esq-*.json"):
            with esq_file.open(encoding="utf-8") as f:
                esq = json.load(f)
            esq_id = esq.get("id", esq_file.stem)
            cur = conn.execute("SELECT id FROM esquemas WHERE id = ?", (esq_id,))
            if cur.fetchone():
                continue

            if not dry_run:
                conn.execute("""
                    INSERT INTO esquemas (
                        id, tema_id, formato, seleccion_modo, seleccion_valor,
                        contenido, n_nodos, verificado
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    esq_id,
                    tema_id,
                    esq.get("formato", "mapa"),
                    esq.get("seleccion", {}).get("modo"),
                    json.dumps(esq.get("seleccion", {}).get("valor", []), ensure_ascii=False),
                    esq.get("mermaid", ""),
                    len(esq.get("nodos", [])),
                    int(esq.get("verificado", True)),
                ))
            resultado["esquemas_nuevos"] += 1

    # 7. Actualizar estado del tema
    if not dry_run and not resultado["errores"]:
        conn.execute("""
            UPDATE temas
            SET estado_ingesta = 'completo', fecha_ingesta = ?
            WHERE id = ?
        """, (date.today().isoformat(), tema_id))

    return resultado


def cmd_migrar(args) -> int:
    """Comando: migrar JSON de temas a SQLite."""
    root = Path(args.root).expanduser().resolve()
    db_path = root / "oposicion.db"

    if not db_path.exists():
        print(f"[error] La BD no existe: {db_path}")
        print(f"        Ejecuta primero: python bin/db.py init --root {root}")
        return 1

    temario_dir = root / "temario"
    if not temario_dir.exists():
        print(f"[error] No existe el directorio: {temario_dir}")
        return 1

    # Listar temas a migrar
    if args.tema:
        tema_dirs = [temario_dir / args.tema]
    else:
        tema_dirs = sorted(temario_dir.glob("tema-*"))

    if not tema_dirs:
        print(f"[error] No hay temas en {temario_dir}")
        return 1

    print(f"[migrar] Modo: {'DRY-RUN (sin escribir)' if args.dry_run else 'REAL'}")
    print(f"[migrar] Temas a procesar: {len(tema_dirs)}")
    print()

    conn = conectar(db_path)
    resultados = []

    try:
        for tema_dir in tema_dirs:
            if not tema_dir.exists():
                print(f"[skip] {tema_dir.name} (no existe)")
                continue

            print(f"[migrar] {tema_dir.name}")
            resultado = migrar_tema(conn, tema_dir, dry_run=args.dry_run)
            resultados.append(resultado)

            if resultado["estado"] != "ok":
                print(f"  ⚠️  {resultado['estado']}")
                for err in resultado["errores"]:
                    print(f"      - {err}")
                continue

            print(f"  Conceptos:    +{resultado['conceptos_nuevos']} nuevos, "
                  f"{resultado['conceptos_reutilizados']} reutilizados, "
                  f"{resultado['vinculos_nuevos']} vínculos")
            print(f"  Preguntas:    +{resultado['preguntas_nuevas']} nuevas, "
                  f"{resultado['preguntas_dup_exacta']} dup exactas, "
                  f"{resultado['preguntas_dup_conceptual']} dup conceptuales")
            print(f"  Flashcards:   +{resultado['flashcards_nuevas']} nuevas, "
                  f"{resultado['flashcards_dup']} duplicadas")
            print(f"  Cuadros:      +{resultado['cuadros_nuevos']} nuevos "
                  f"({resultado['cuadro_filas_nuevas']} filas)")
            print(f"  Esquemas:     +{resultado['esquemas_nuevos']} nuevos")
            print()

        # Commit final
        if not args.dry_run:
            conn.commit()
            print("[migrar] Cambios confirmados.")

        # Resumen global
        print()
        print("=" * 60)
        print("  RESUMEN DE MIGRACIÓN")
        print("=" * 60)
        total = {
            "temas": len(resultados),
            "conceptos_nuevos": sum(r["conceptos_nuevos"] for r in resultados),
            "conceptos_reutilizados": sum(r["conceptos_reutilizados"] for r in resultados),
            "vinculos_nuevos": sum(r["vinculos_nuevos"] for r in resultados),
            "preguntas_nuevas": sum(r["preguntas_nuevas"] for r in resultados),
            "preguntas_dup_exacta": sum(r["preguntas_dup_exacta"] for r in resultados),
            "preguntas_dup_conceptual": sum(r["preguntas_dup_conceptual"] for r in resultados),
            "flashcards_nuevas": sum(r["flashcards_nuevas"] for r in resultados),
            "flashcards_dup": sum(r["flashcards_dup"] for r in resultados),
            "cuadros_nuevos": sum(r["cuadros_nuevos"] for r in resultados),
            "cuadro_filas_nuevas": sum(r["cuadro_filas_nuevas"] for r in resultados),
            "esquemas_nuevos": sum(r["esquemas_nuevos"] for r in resultados),
        }
        for k, v in total.items():
            print(f"  {k:30s} {v}")
        print("=" * 60)

        # Verificación post-migración
        if not args.dry_run:
            print()
            print("  Estado de la BD:")
            cur = conn.execute("SELECT COUNT(*) FROM conceptos")
            print(f"    Conceptos totales:   {cur.fetchone()[0]}")
            cur = conn.execute("SELECT COUNT(*) FROM preguntas")
            print(f"    Preguntas totales:   {cur.fetchone()[0]}")
            cur = conn.execute("SELECT COUNT(*) FROM flashcards")
            print(f"    Flashcards totales:  {cur.fetchone()[0]}")
            cur = conn.execute("SELECT COUNT(*) FROM cuadros")
            print(f"    Cuadros totales:     {cur.fetchone()[0]}")
            cur = conn.execute(
                "SELECT COUNT(*) FROM temas WHERE estado_ingesta = 'completo'"
            )
            print(f"    Temas completos:     {cur.fetchone()[0]}")

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
# EXPORTACIÓN: SQLite → JSON
# ============================================================

def _leer_tabla(conn: sqlite3.Connection, sql: str, params: tuple = ()) -> list[dict]:
    """Devuelve una lista de dicts a partir de una consulta."""
    cur = conn.execute(sql, params)
    columnas = [d[0] for d in cur.description]
    return [dict(zip(columnas, row)) for row in cur.fetchall()]


def _parsear_json_field(valor: str | None, default):
    """Parsea un campo JSON; si falla, devuelve default."""
    if not valor:
        return default
    try:
        return json.loads(valor)
    except (json.JSONDecodeError, TypeError):
        return default


def exportar_tema(conn: sqlite3.Connection, tema_id: str, output_dir: Path,
                  incluir_srs: bool = False) -> dict:
    """Exporta un tema completo a JSON."""
    resultado = {"tema_id": tema_id, "archivos": []}
    tema_dir = output_dir / tema_id
    tema_dir.mkdir(parents=True, exist_ok=True)

    # 1. Metadatos del tema
    cur = conn.execute(
        "SELECT * FROM temas WHERE id = ?", (tema_id,)
    )
    row = cur.fetchone()
    if not row:
        return {"error": f"Tema no encontrado: {tema_id}"}

    cols = [d[0] for d in cur.description]
    tema = dict(zip(cols, row))

    # 2. Conceptos del tema
    conceptos = _leer_tabla(conn, """
        SELECT
            c.id, c.nombre, c.tipo, c.valor, c.norma, c.articulo,
            c.tags, c.verificado, c.es_semilla,
            ct.es_principal
        FROM conceptos c
        JOIN concepto_temas ct ON ct.concepto_id = c.id
        WHERE ct.tema_id = ?
        ORDER BY c.id
    """, (tema_id,))

    for c in conceptos:
        c["tags"] = _parsear_json_field(c["tags"], [])
        c["es_principal"] = bool(c["es_principal"])
        c["verificado"] = bool(c["verificado"])
        c["es_semilla"] = bool(c["es_semilla"])

    # Conceptos compartidos (para saber qué otros temas los tienen)
    for c in conceptos:
        cur = conn.execute("""
            SELECT tema_id FROM concepto_temas
            WHERE concepto_id = ? AND tema_id != ?
        """, (c["id"], tema_id))
        c["otros_temas"] = [r[0] for r in cur.fetchall()]

    data_conceptos = {
        "tema_id": tema_id,
        "total": len(conceptos),
        "conceptos": conceptos,
    }
    archivo = tema_dir / "02-conceptos-clave.json"
    archivo.write_text(
        json.dumps(data_conceptos, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    resultado["archivos"].append(str(archivo.name))

    # 3. Preguntas
    preguntas = _leer_tabla(conn, """
        SELECT
            id, concepto_id, capitulo, tipo, dificultad, origen,
            enunciado, opciones, correcta, explicacion, referencia,
            verificado, fecha_alta
        FROM preguntas
        WHERE tema_id = ?
        ORDER BY id
    """, (tema_id,))

    for p in preguntas:
        p["opciones"] = _parsear_json_field(p["opciones"], [])
        p["verificado"] = bool(p["verificado"])

    data_preguntas = {
        "tema_id": tema_id,
        "total": len(preguntas),
        "preguntas": preguntas,
    }
    archivo = tema_dir / "03-banco-preguntas.json"
    archivo.write_text(
        json.dumps(data_preguntas, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    resultado["archivos"].append(str(archivo.name))

    # 4. Flashcards
    flashcards = _leer_tabla(conn, """
        SELECT
            id, concepto_id, modo, anverso, reverso, texto,
            respuestas, tags, verificado
        FROM flashcards
        WHERE tema_id = ?
        ORDER BY id
    """, (tema_id,))

    for f in flashcards:
        f["respuestas"] = _parsear_json_field(f["respuestas"], [])
        f["tags"] = _parsear_json_field(f["tags"], [])
        f["verificado"] = bool(f["verificado"])

    data_flashcards = {
        "tema_id": tema_id,
        "total": len(flashcards),
        "flashcards": flashcards,
    }
    archivo = tema_dir / "03-flashcards.json"
    archivo.write_text(
        json.dumps(data_flashcards, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    resultado["archivos"].append(str(archivo.name))

    # 5. Cuadros
    cuadros_dir = tema_dir / "06-cuadros"
    cuadros = _leer_tabla(conn, """
        SELECT * FROM cuadros WHERE tema_id = ?
    """, (tema_id,))

    if cuadros:
        cuadros_dir.mkdir(parents=True, exist_ok=True)
        indice = {"tema_id": tema_id, "cuadros": []}

        for cu in cuadros:
            filas = _leer_tabla(conn, """
                SELECT id, fuente, fuente_tipo, valores, pasaje_origen,
                       ubicacion, verificado
                FROM cuadro_filas
                WHERE cuadro_id = ?
                ORDER BY id
            """, (cu["id"],))

            for f in filas:
                f["valores"] = _parsear_json_field(f["valores"], {})
                f["ubicacion"] = _parsear_json_field(f["ubicacion"], {})
                f["verificado"] = bool(f["verificado"])

            data_cuadro = {
                "id": cu["id"],
                "tipo_dato": cu["tipo_dato"],
                "titulo": cu["titulo"],
                "semilla": bool(cu["semilla"]),
                "n_filas": cu["n_filas"],
                "n_fuentes_distintas": cu["n_fuentes_distintas"],
                "columnas": _parsear_json_field(cu["columnas"], []),
                "columna_clave": cu["columna_clave"],
                "columna_respuesta": cu["columna_respuesta"],
                "columna_contexto": cu["columna_contexto"],
                "columna_fuente": cu["columna_fuente"],
                "verificado": bool(cu["verificado"]),
                "filas": filas,
            }
            archivo = cuadros_dir / f"{cu['id']}.json"
            archivo.write_text(
                json.dumps(data_cuadro, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            indice["cuadros"].append({
                "id": cu["id"],
                "tipo_dato": cu["tipo_dato"],
                "n_filas": cu["n_filas"],
                "semilla": bool(cu["semilla"]),
            })

        archivo = cuadros_dir / "indice.json"
        archivo.write_text(
            json.dumps(indice, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        resultado["archivos"].append("06-cuadros/")

    # 6. Esquemas
    esquemas_dir = tema_dir / "02-esquemas"
    esquemas = _leer_tabla(conn, """
        SELECT * FROM esquemas WHERE tema_id = ?
    """, (tema_id,))

    if esquemas:
        esquemas_dir.mkdir(parents=True, exist_ok=True)
        for esq in esquemas:
            data_esq = {
                "id": esq["id"],
                "formato": esq["formato"],
                "seleccion": {
                    "modo": esq["seleccion_modo"],
                    "valor": _parsear_json_field(esq["seleccion_valor"], []),
                },
                "contenido": esq["contenido"],
                "n_nodos": esq["n_nodos"],
                "verificado": bool(esq["verificado"]),
            }
            archivo = esquemas_dir / f"{esq['id']}.json"
            archivo.write_text(
                json.dumps(data_esq, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        resultado["archivos"].append("02-esquemas/")

    # 7. Metadatos del tema
    data_tema = {
        "id": tema["id"],
        "numero": tema["numero"],
        "titulo": tema["titulo"],
        "bloque_id": tema["bloque_id"],
        "tipo": tema["tipo"],
        "estado_ingesta": tema["estado_ingesta"],
        "fecha_ingesta": tema["fecha_ingesta"],
    }
    archivo = tema_dir / "_tema.json"
    archivo.write_text(
        json.dumps(data_tema, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    resultado["archivos"].append(str(archivo.name))

    # 8. SRS (opcional)
    if incluir_srs:
        srs = _leer_tabla(conn, """
            SELECT item_key, tipo, tema_id, bloque_id, concepto_id,
                   estado, ease, intervalo_dias, due,
                   veces_fallada, veces_acertada, ultima_respuesta, problematico
            FROM srs_items
            WHERE tema_id = ?
            ORDER BY item_key
        """, (tema_id,))

        historial = _leer_tabla(conn, """
            SELECT h.item_key, h.fecha, h.respuesta, h.intervalo
            FROM srs_historial h
            JOIN srs_items s ON s.item_key = h.item_key
            WHERE s.tema_id = ?
            ORDER BY h.item_key, h.id
        """, (tema_id,))

        data_srs = {
            "tema_id": tema_id,
            "items": srs,
            "historial": historial,
        }
        archivo = tema_dir / "srs.json"
        archivo.write_text(
            json.dumps(data_srs, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        resultado["archivos"].append(str(archivo.name))

    return resultado


def cmd_exportar(args) -> int:
    """Comando: exportar SQLite → JSON."""
    root = Path(args.root).expanduser().resolve()
    conn = conectar(root / "oposicion.db")

    try:
        output_dir = Path(args.output).expanduser().resolve()
        output_dir.mkdir(parents=True, exist_ok=True)

        if args.tema:
            temas = [args.tema]
        else:
            cur = conn.execute(
                "SELECT id FROM temas WHERE estado_ingesta != 'pendiente' "
                "ORDER BY numero"
            )
            temas = [row[0] for row in cur.fetchall()]

        if not temas:
            print("[exportar] No hay temas para exportar.")
            return 0

        print(f"[exportar] Modo: {'CON SRS' if args.srs else 'SIN SRS'}")
        print(f"[exportar] Temas: {len(temas)}")
        print(f"[exportar] Destino: {output_dir}")
        print()

        for tema_id in temas:
            resultado = exportar_tema(
                conn, tema_id, output_dir, incluir_srs=args.srs
            )
            if "error" in resultado:
                print(f"[exportar] {tema_id}: ❌ {resultado['error']}")
                continue
            print(f"[exportar] {tema_id}: {len(resultado['archivos'])} archivos")

        # Exportar supuestos si existen
        if args.supuestos:
            supuestos_dir = output_dir / "supuestos"
            supuestos_dir.mkdir(exist_ok=True)
            cur = conn.execute("SELECT id FROM supuestos ORDER BY id")
            for (sup_id,) in cur.fetchall():
                exportar_supuesto(conn, sup_id, supuestos_dir)
                print(f"[exportar] supuesto: {sup_id}")

        # Exportar exámenes
        if args.examenes:
            examenes_dir = output_dir / "examenes"
            examenes_dir.mkdir(exist_ok=True)
            cur = conn.execute("SELECT id FROM examenes ORDER BY anio")
            for (exam_id,) in cur.fetchall():
                exportar_examen(conn, exam_id, examenes_dir)
                print(f"[exportar] examen: {exam_id}")

        print()
        print(f"[exportar] ✅ Exportación completada en {output_dir}")

        if args.git:
            print()
            print("[exportar] Sugerencia para git:")
            print(f"  git add {output_dir}")
            print(f"  git commit -m 'backup: exportar estado {date.today().isoformat()}'")

        return 0

    except Exception as e:
        print(f"[error] {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        conn.close()


def exportar_supuesto(conn: sqlite3.Connection, supuesto_id: str,
                      output_dir: Path) -> None:
    """Exporta un supuesto completo a JSON."""
    sup_dir = output_dir / supuesto_id
    sup_dir.mkdir(parents=True, exist_ok=True)

    cur = conn.execute("SELECT * FROM supuestos WHERE id = ?", (supuesto_id,))
    row = cur.fetchone()
    if not row:
        return
    cols = [d[0] for d in cur.description]
    sup = dict(zip(cols, row))
    sup["contexto_json"] = _parsear_json_field(sup["contexto_json"], {})

    # Preguntas
    preguntas = _leer_tabla(conn, """
        SELECT
            sp.numero_en_supuesto, sp.es_reserva,
            p.id, p.enunciado, p.opciones, p.correcta,
            p.explicacion, p.referencia, p.concepto_id, p.verificado
        FROM supuesto_preguntas sp
        JOIN preguntas p ON p.id = sp.pregunta_id
        WHERE sp.supuesto_id = ?
        ORDER BY sp.numero_en_supuesto
    """, (supuesto_id,))

    for p in preguntas:
        p["opciones"] = _parsear_json_field(p["opciones"], [])
        p["verificado"] = bool(p["verificado"])
        p["es_reserva"] = bool(p["es_reserva"])

    # Temas implicados
    temas = _leer_tabla(conn, """
        SELECT st.tema_id, st.n_preguntas, t.numero, t.titulo
        FROM supuesto_temas st
        JOIN temas t ON t.id = st.tema_id
        WHERE st.supuesto_id = ?
    """, (supuesto_id,))

    # Artefactos
    artefactos = _leer_tabla(conn, """
        SELECT id, tipo, titulo, contenido, orden
        FROM supuesto_artefactos
        WHERE supuesto_id = ?
        ORDER BY orden
    """, (supuesto_id,))

    data = {
        "id": sup["id"],
        "examen_id": sup["examen_id"],
        "bloque_id": sup["bloque_id"],
        "numero": sup["numero"],
        "titulo": sup["titulo"],
        "tipo": sup["tipo"],
        "origen": sup["origen"],
        "contexto_texto": sup["contexto_texto"],
        "contexto_json": sup["contexto_json"],
        "verificado": bool(sup["verificado"]),
        "temas_implicados": temas,
        "preguntas": preguntas,
        "artefactos": artefactos,
    }

    archivo = sup_dir / "00-supuesto.json"
    archivo.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def exportar_examen(conn: sqlite3.Connection, examen_id: str,
                    output_dir: Path) -> None:
    """Exporta un examen completo a JSON."""
    exam_dir = output_dir / examen_id
    exam_dir.mkdir(parents=True, exist_ok=True)

    cur = conn.execute("SELECT * FROM examenes WHERE id = ?", (examen_id,))
    row = cur.fetchone()
    if not row:
        return
    cols = [d[0] for d in cur.description]
    exam = dict(zip(cols, row))

    # Preguntas
    preguntas = _leer_tabla(conn, """
        SELECT
            ep.seccion, ep.numero, ep.respuesta_oficial, ep.pregunta_id,
            p.enunciado, p.opciones, p.correcta, p.concepto_id, p.tema_id
        FROM examen_preguntas ep
        LEFT JOIN preguntas p ON p.id = ep.pregunta_id
        WHERE ep.examen_id = ?
        ORDER BY ep.seccion, ep.numero
    """, (examen_id,))

    for p in preguntas:
        if p["opciones"]:
            p["opciones"] = _parsear_json_field(p["opciones"], [])

    data = {
        **exam,
        "verificado": bool(exam["verificado"]),
        "preguntas": preguntas,
    }

    archivo = exam_dir / "00-examen.json"
    archivo.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


# ============================================================
# IMPORTACIÓN INCREMENTAL: JSON → SQLite
# ============================================================

def importar_preguntas(conn: sqlite3.Connection, archivo: Path,
                       tema_id: str, update: bool = False) -> dict:
    """Importa un JSON de preguntas. Devuelve estadísticas."""
    with archivo.open(encoding="utf-8") as f:
        data = json.load(f)

    preguntas = data.get("preguntas", [])
    stats = {"nuevas": 0, "dup_exacta": 0, "dup_conceptual": 0,
             "actualizadas": 0, "sin_concepto": 0}

    for p in preguntas:
        concepto_id = p.get("concepto_id")
        if not concepto_id:
            stats["sin_concepto"] += 1

        pid_dup, motivo = buscar_pregunta_duplicada(
            conn,
            p.get("enunciado", ""),
            p.get("opciones", []),
            p.get("correcta", 0),
            concepto_id,
            p.get("tipo"),
        )

        if pid_dup:
            if update:
                # Actualizar la existente (excepto id, hash)
                conn.execute("""
                    UPDATE preguntas SET
                        concepto_id = COALESCE(?, concepto_id),
                        explicacion = COALESCE(?, explicacion),
                        referencia = COALESCE(?, referencia),
                        verificado = ?
                    WHERE id = ?
                """, (
                    concepto_id,
                    p.get("explicacion"),
                    p.get("referencia"),
                    int(p.get("verificado", False)),
                    pid_dup,
                ))
                stats["actualizadas"] += 1
            else:
                if motivo == "exacta":
                    stats["dup_exacta"] += 1
                else:
                    stats["dup_conceptual"] += 1
            continue

        # Insertar nueva
        enunciado = p.get("enunciado", "")
        opciones = p.get("opciones", [])
        correcta = p.get("correcta", 0)
        h_exacto = sha256_exacto(enunciado, *opciones, str(correcta))
        h_norm = normalizar_texto(enunciado)

        conn.execute("""
            INSERT INTO preguntas (
                id, tema_id, concepto_id, capitulo, tipo, dificultad, origen,
                enunciado, opciones, correcta, explicacion, referencia,
                verificado, hash_exacto, hash_normalizado, fecha_alta
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p.get("id", f"p-{hashlib.sha1(h_exacto.encode()).hexdigest()[:10]}"),
            tema_id,
            concepto_id,
            p.get("capitulo"),
            p.get("tipo"),
            p.get("dificultad", "media"),
            p.get("origen", "ampliacion"),
            enunciado,
            json.dumps(opciones, ensure_ascii=False),
            correcta,
            p.get("explicacion"),
            p.get("referencia"),
            int(p.get("verificado", False)),
            h_exacto,
            h_norm,
            date.today().isoformat(),
        ))
        stats["nuevas"] += 1

    return stats


def importar_flashcards(conn: sqlite3.Connection, archivo: Path,
                        tema_id: str, update: bool = False) -> dict:
    """Importa un JSON de flashcards."""
    with archivo.open(encoding="utf-8") as f:
        data = json.load(f)

    flashcards = data.get("flashcards", [])
    stats = {"nuevas": 0, "duplicadas": 0, "actualizadas": 0}

    for c in flashcards:
        texto_para_hash = c.get("anverso") or c.get("texto", "")
        h_norm = normalizar_texto(texto_para_hash)

        cur = conn.execute(
            "SELECT id FROM flashcards WHERE hash_normalizado = ?", (h_norm,)
        )
        row = cur.fetchone()

        if row:
            if update:
                conn.execute("""
                    UPDATE flashcards SET
                        concepto_id = COALESCE(?, concepto_id),
                        verificado = ?
                    WHERE id = ?
                """, (
                    c.get("concepto_id"),
                    int(c.get("verificado", False)),
                    row[0],
                ))
                stats["actualizadas"] += 1
            else:
                stats["duplicadas"] += 1
            continue

        conn.execute("""
            INSERT INTO flashcards (
                id, tema_id, concepto_id, modo, anverso, reverso, texto,
                respuestas, tags, verificado, hash_normalizado
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            c.get("id", f"fc-{hashlib.sha1(h_norm.encode()).hexdigest()[:10]}"),
            tema_id,
            c.get("concepto_id"),
            c.get("modo", "anverso-reverso"),
            c.get("anverso"),
            c.get("reverso"),
            c.get("texto"),
            json.dumps(c.get("respuestas", []), ensure_ascii=False),
            json.dumps(c.get("tags", []), ensure_ascii=False),
            int(c.get("verificado", False)),
            h_norm,
        ))
        stats["nuevas"] += 1

    return stats


def importar_cuadro(conn: sqlite3.Connection, archivo: Path,
                    tema_id: str, update: bool = False) -> dict:
    """Importa un JSON de cuadro transversal."""
    with archivo.open(encoding="utf-8") as f:
        cu = json.load(f)

    cuadro_id = cu.get("id", archivo.stem)
    stats = {"cuadro": cuadro_id, "nuevo": False, "actualizado": False,
             "filas_nuevas": 0, "filas_duplicadas": 0}

    cur = conn.execute("SELECT id FROM cuadros WHERE id = ?", (cuadro_id,))
    existe = cur.fetchone() is not None

    if existe and not update:
        stats["filas_duplicadas"] = len(cu.get("filas", []))
        return stats

    if existe:
        conn.execute("""
            UPDATE cuadros SET
                titulo = ?, semilla = ?, n_filas = ?,
                n_fuentes_distintas = ?, columnas = ?,
                verificado = ?
            WHERE id = ?
        """, (
            cu.get("titulo"),
            int(cu.get("semilla", False)),
            cu.get("n_filas", len(cu.get("filas", []))),
            cu.get("n_fuentes_distintas", 0),
            json.dumps(cu.get("columnas", []), ensure_ascii=False),
            int(cu.get("verificado", True)),
            cuadro_id,
        ))
        stats["actualizado"] = True
    else:
        conn.execute("""
            INSERT INTO cuadros (
                id, tema_id, tipo_dato, titulo, semilla, n_filas,
                n_fuentes_distintas, columnas, columna_clave, columna_respuesta,
                columna_contexto, columna_fuente, verificado
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            cuadro_id,
            tema_id,
            cu.get("tipo_dato"),
            cu.get("titulo"),
            int(cu.get("semilla", False)),
            cu.get("n_filas", len(cu.get("filas", []))),
            cu.get("n_fuentes_distintas", 0),
            json.dumps(cu.get("columnas", []), ensure_ascii=False),
            cu.get("columna_clave"),
            cu.get("columna_respuesta"),
            cu.get("columna_contexto"),
            cu.get("columna_fuente"),
            int(cu.get("verificado", True)),
        ))
        stats["nuevo"] = True

    # Filas
    for fila in cu.get("filas", []):
        fila_id = fila.get("id", f"f-{hashlib.sha1(json.dumps(fila).encode()).hexdigest()[:8]}")
        cur = conn.execute(
            "SELECT id FROM cuadro_filas WHERE id = ?", (fila_id,)
        )
        if cur.fetchone():
            stats["filas_duplicadas"] += 1
            continue

        conn.execute("""
            INSERT INTO cuadro_filas (
                id, cuadro_id, fuente, fuente_tipo, valores,
                pasaje_origen, ubicacion, verificado
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            fila_id,
            cuadro_id,
            fila.get("fuente"),
            fila.get("fuente_tipo"),
            json.dumps(fila.get("valores", {}), ensure_ascii=False),
            fila.get("pasaje_origen"),
            json.dumps(fila.get("ubicacion", {}), ensure_ascii=False),
            int(fila.get("verificado", True)),
        ))
        stats["filas_nuevas"] += 1

    return stats


def cmd_importar(args) -> int:
    """Comando: importar un JSON a SQLite."""
    root = Path(args.root).expanduser().resolve()
    conn = conectar(root / "oposicion.db")

    try:
        # Verificar tema
        if args.tema:
            cur = conn.execute(
                "SELECT id FROM temas WHERE id = ?", (args.tema,)
            )
            if not cur.fetchone():
                print(f"[error] Tema no existe: {args.tema}")
                return 1
            tema_id = args.tema
        else:
            tema_id = None

        # Determinar modo
        if args.from_export:
            return importar_desde_export(conn, Path(args.from_export), args.update)

        if not args.archivo:
            print("[error] Debes indicar --archivo o --from-export")
            return 1

        archivo = Path(args.archivo).expanduser().resolve()
        if not archivo.exists():
            print(f"[error] No existe el archivo: {archivo}")
            return 1

        if not tema_id:
            print("[error] Debes indicar --tema (a qué tema pertenece)")
            return 1

        print(f"[importar] Modo: {'UPDATE' if args.update else 'SKIP duplicados'}")
        print(f"[importar] Tema: {tema_id}")
        print(f"[importar] Archivo: {archivo.name}")

        # Detectar tipo automáticamente o usar el forzado
        tipo = args.tipo
        if not tipo:
            if archivo.name.startswith("03-banco-preguntas"):
                tipo = "preguntas"
            elif archivo.name.startswith("03-flashcards"):
                tipo = "flashcards"
            elif archivo.name.startswith("cuadro-") or "cuadro" in archivo.name:
                tipo = "cuadros"
            else:
                print(f"[error] No puedo detectar el tipo. Usa --tipo.")
                return 1

        print(f"[importar] Tipo: {tipo}")
        print()

        if tipo == "preguntas":
            stats = importar_preguntas(conn, archivo, tema_id, args.update)
            print(f"  Nuevas:          {stats['nuevas']}")
            print(f"  Dup exactas:     {stats['dup_exacta']}")
            print(f"  Dup conceptual:  {stats['dup_conceptual']}")
            if args.update:
                print(f"  Actualizadas:    {stats['actualizadas']}")
            if stats["sin_concepto"] > 0:
                print(f"  Sin concepto:    {stats['sin_concepto']}")

        elif tipo == "flashcards":
            stats = importar_flashcards(conn, archivo, tema_id, args.update)
            print(f"  Nuevas:          {stats['nuevas']}")
            print(f"  Duplicadas:      {stats['duplicadas']}")
            if args.update:
                print(f"  Actualizadas:    {stats['actualizadas']}")

        elif tipo == "cuadros":
            stats = importar_cuadro(conn, archivo, tema_id, args.update)
            print(f"  Cuadro:          {stats['cuadro']}")
            print(f"  Nuevo:           {stats['nuevo']}")
            print(f"  Actualizado:     {stats['actualizado']}")
            print(f"  Filas nuevas:    {stats['filas_nuevas']}")
            print(f"  Filas dup:       {stats['filas_duplicadas']}")

        if args.dry_run:
            conn.rollback()
            print()
            print("[importar] DRY-RUN: cambios revertidos")
        else:
            conn.commit()
            print()
            print("[importar] ✅ Cambios confirmados")

        return 0

    except Exception as e:
        conn.rollback()
        print(f"[error] {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        conn.close()


def importar_desde_export(conn: sqlite3.Connection, export_dir: Path,
                          update: bool = False) -> int:
    """
    Reimporta todos los JSON de una carpeta export/ (restaurar backup).
    """
    if not export_dir.exists():
        print(f"[error] No existe la carpeta: {export_dir}")
        return 1

    temas = [d for d in export_dir.iterdir() if d.is_dir() and d.name.startswith("tema-")]

    print(f"[importar] Restaurando desde {export_dir}")
    print(f"[importar] Temas encontrados: {len(temas)}")
    print()

    for tema_dir in sorted(temas):
        tema_id = tema_dir.name

        # Verificar que el tema existe en la BD
        cur = conn.execute("SELECT id FROM temas WHERE id = ?", (tema_id,))
        if not cur.fetchone():
            print(f"[skip] {tema_id} (no está en la BD, ejecuta init primero)")
            continue

        # Importar cada archivo
        total_preg = total_card = total_cuad = 0

        if (tema_dir / "03-banco-preguntas.json").exists():
            s = importar_preguntas(
                conn, tema_dir / "03-banco-preguntas.json", tema_id, update
            )
            total_preg = s["nuevas"]

        if (tema_dir / "03-flashcards.json").exists():
            s = importar_flashcards(
                conn, tema_dir / "03-flashcards.json", tema_id, update
            )
            total_card = s["nuevas"]

        cuadros_dir = tema_dir / "06-cuadros"
        if cuadros_dir.exists():
            for cu_file in cuadros_dir.glob("cuadro-*.json"):
                s = importar_cuadro(conn, cu_file, tema_id, update)
                total_cuad += 1 if s["nuevo"] else 0

        print(f"[importar] {tema_id}: +{total_preg} preguntas, "
              f"+{total_card} flashcards, +{total_cuad} cuadros")

    conn.commit()
    print()
    print(f"[importar] ✅ Restauración completada")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Gestor de la base de datos TAI Oposición",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # init
    p_init = sub.add_parser("init", help="Crear la BD + insertar bloques y temas")
    p_init.add_argument("--root", default="~/oposicion")
    p_init.add_argument("--force", action="store_true")
    p_init.set_defaults(func=cmd_init)

    # migrar
    p_mig = sub.add_parser("migrar", help="Importar JSON de temas completos a SQLite")
    p_mig.add_argument("--root", default="~/oposicion")
    p_mig.add_argument("--tema", help="Migrar solo un tema")
    p_mig.add_argument("--dry-run", action="store_true")
    p_mig.set_defaults(func=cmd_migrar)

    # exportar
    p_exp = sub.add_parser("exportar", help="Exportar SQLite → JSON (backup/git)")
    p_exp.add_argument("--root", default="~/oposicion")
    p_exp.add_argument("--output", default="~/oposicion/export",
                       help="Carpeta de destino")
    p_exp.add_argument("--tema", help="Exportar solo un tema")
    p_exp.add_argument("--srs", action="store_true",
                       help="Incluir estado SRS")
    p_exp.add_argument("--supuestos", action="store_true",
                       help="Incluir supuestos")
    p_exp.add_argument("--examenes", action="store_true",
                       help="Incluir exámenes oficiales")
    p_exp.add_argument("--git", action="store_true",
                       help="Mostrar comandos git sugeridos")
    p_exp.set_defaults(func=cmd_exportar)

    # importar
    p_imp = sub.add_parser("importar",
                           help="Importar un JSON individual a SQLite")
    p_imp.add_argument("--root", default="~/oposicion")
    p_imp.add_argument("--archivo", help="Ruta al JSON")
    p_imp.add_argument("--tema", help="Tema al que pertenece")
    p_imp.add_argument("--tipo",
                       choices=["preguntas", "flashcards", "cuadros"],
                       help="Tipo de contenido (auto-detectado si se omite)")
    p_imp.add_argument("--update", action="store_true",
                       help="Actualizar existentes en lugar de saltar")
    p_imp.add_argument("--dry-run", action="store_true")
    p_imp.add_argument("--from-export",
                       help="Restaurar todo desde una carpeta export/")
    p_imp.set_defaults(func=cmd_importar)

    args = parser.parse_args()
    return args.func(args)

if __name__ == "__main__":
    sys.exit(main())