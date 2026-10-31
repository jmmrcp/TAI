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
        (1,  "La Constitución Española de 1978. Derechos y deberes fundamentales. La Corona"),
        (2,  "Las Cortes Generales. El Tribunal Constitucional. El Defensor del Pueblo"),
        (3,  "El Gobierno: composición, nombramiento y cese. Relaciones con las Cortes"),
        (4,  "El TREBEP y demás normativa. Transparencia. Agenda 2030 y ODS"),
        (5,  "Políticas de igualdad. Violencia de género. LGTBI. Discapacidad y dependencia"),
        (6,  "La sociedad de la información. Identidad y firma electrónica. DNIe. Agenda Digital"),
        (7,  "La protección de datos personales. Derechos digitales"),
        (8,  "Acceso electrónico. ENS y ENI. Normas técnicas de Interoperabilidad"),
        (9,  "Instrumentos para el acceso electrónico. Sedes. Infraestructuras comunes"),
    ],
    "bloque-ii": [
        (10, "Informática básica. Representación de la información. Arquitectura de ordenadores"),
        (11, "Periféricos: conectividad y administración. Impresión, almacenamiento, visualización"),
        (12, "Tipos abstractos y estructuras de datos. Algoritmos. Organizaciones de ficheros"),
        (13, "Sistemas operativos: Windows, Unix/Linux, móviles"),
        (14, "SGBD relacionales, orientados a objetos y NoSQL"),
    ],
    "bloque-iii": [
        (15, "Modelado de datos. Diseño de BD. Modelo relacional. Normalización"),
        (16, "Lenguajes de programación: tipos, operadores, control de flujo, funciones"),
        (17, "Lenguajes de interrogación de BD. ANSI SQL. Procedimientos y triggers"),
        (18, "Diseño y programación orientada a objetos. Patrones de diseño. UML"),
        (19, "Arquitectura Java EE/Jakarta EE y plataforma .NET"),
        (20, "Arquitectura cliente/servidor y multicapas. Servicios web y protocolos"),
        (21, "Aplicaciones web. HTML, XML. Lenguajes de script. Front-end y back-end"),
        (22, "Accesibilidad, diseño universal y usabilidad. Seguridad en el desarrollo"),
        (23, "Repositorios. Control de versiones. Metodologías. Pruebas de software"),
    ],
    "bloque-iv": [
        (24, "Administración del SO y software de base. Actualización y mantenimiento"),
        (25, "Administración de BD. Almacenamiento y virtualización. Backup y recuperación"),
        (26, "Servidores de correo. Contenedores y microservicios"),
        (27, "Administración de redes LAN. Gestión de usuarios y dispositivos"),
        (28, "Seguridad de sistemas. Criptografía. Firma digital. CPD. Incidencias"),
        (29, "Comunicaciones. Medios de transmisión. Redes de conmutación y difusión"),
        (30, "Modelo TCP/IP y OSI. Protocolos TCP/IP"),
        (31, "Internet: arquitectura. Protocolos HTTP, HTTPS y SSL/TLS"),
        (32, "Seguridad en redes. Perimetral. VPN. Seguridad en el puesto"),
        (33, "Redes locales. Tipología. Técnicas de transmisión. Dispositivos"),
    ],
}

BLOQUES = [
    ("bloque-i", 1, "Organización del Estado y Administración electrónica",
     "Constitución, Corona, Cortes, TC, Gobierno, TREBEP, Transparencia, "
     "Igualdad, Sociedad de la información, Protección de datos, "
     "Administración electrónica (ENS, ENI, sedes)", 0),
    ("bloque-ii", 2, "Tecnología básica",
     "Informática básica, arquitectura, periféricos, estructuras de datos, "
     "algoritmos, sistemas operativos, SGBD", 0),
    ("bloque-iii", 3, "Desarrollo de sistemas",
     "Modelado de datos, programación, SQL, POO, Java EE/.NET, servicios web, "
     "aplicaciones web, accesibilidad, control de versiones", 1),
    ("bloque-iv", 4, "Sistemas y comunicaciones",
     "Administración SO, BD, correo, contenedores, redes LAN, seguridad, "
     "criptografía, TCP/IP, Internet, VPN, redes locales", 1),
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
    es_semilla BOOLEAN DEFAULT 0,
    es_core BOOLEAN DEFAULT 0
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
-- CONCEPTOS CANDIDATOS (granularidad fina, pendientes de promoción)
-- ============================================================
CREATE TABLE conceptos_candidatos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tema_id TEXT NOT NULL REFERENCES temas(id),
    nombre TEXT NOT NULL,
    descripcion TEXT,
    n_fragmentos INTEGER DEFAULT 0,
    fragmento_ids TEXT DEFAULT '[]',
    estado TEXT NOT NULL DEFAULT 'pendiente',
    primera_aparicion TEXT NOT NULL,
    ultima_actualizacion TEXT NOT NULL,
    concepto_promovido_id TEXT REFERENCES conceptos(id),
    UNIQUE(tema_id, nombre)
);

CREATE INDEX idx_cand_tema ON conceptos_candidatos(tema_id);
CREATE INDEX idx_cand_estado ON conceptos_candidatos(estado);
CREATE INDEX idx_cand_n_frag ON conceptos_candidatos(n_fragmentos);


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
    concepto_id = f"c-{hashlib.sha1((nombre_norm + '|' + valor_norm).encode()).hexdigest()[:12]}"
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
        "preguntas_rebalanceadas": 0,
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

    # 7. Rebalancear opciones ANTES de marcar como completo
    if not dry_run and resultado["preguntas_nuevas"] > 0:
        rebalanceadas = _rebalancear_opciones_tema(conn, tema_id)
        resultado["preguntas_rebalanceadas"] = rebalanceadas
    else:
        resultado["preguntas_rebalanceadas"] = 0

    # 8. Actualizar estado del tema
    if not dry_run and not resultado["errores"]:
        conn.execute("""
            UPDATE temas
            SET estado_ingesta = 'completo', fecha_ingesta = ?
            WHERE id = ?
        """, (date.today().isoformat(), tema_id))

    return resultado


def _rebalancear_opciones_tema(conn: sqlite3.Connection, tema_id: str) -> int:
    """
    Rebalancea las opciones de las preguntas de un tema para evitar
    el sesgo del LLM (respuestas siempre en 'a').

    Excluye las preguntas vinculadas a exámenes oficiales.
    Devuelve el número de preguntas rebalanceadas.
    """
    import random

    cur = conn.execute("""
        SELECT p.id, p.opciones, p.correcta
        FROM preguntas p
        WHERE p.tema_id = ?
          AND p.verificado = 1
          AND p.id NOT IN (
              SELECT pregunta_id FROM examen_preguntas
              WHERE pregunta_id NOT LIKE 'pendiente-%'
          )
    """, (tema_id,))

    actualizadas = 0
    for row in cur.fetchall():
        try:
            opciones = json.loads(row["opciones"]) if row["opciones"] else []
            if len(opciones) < 2:
                continue

            correcta_idx = row["correcta"]
            if correcta_idx < 0 or correcta_idx >= len(opciones):
                continue

            pares = [(op, i == correcta_idx) for i, op in enumerate(opciones)]
            random.shuffle(pares)
            nuevas_opciones = [p[0] for p in pares]
            nuevo_idx = next(i for i, p in enumerate(pares) if p[1])

            if nuevo_idx != correcta_idx:
                conn.execute("""
                    UPDATE preguntas SET opciones = ?, correcta = ? WHERE id = ?
                """, (
                    json.dumps(nuevas_opciones, ensure_ascii=False),
                    nuevo_idx,
                    row["id"],
                ))
                actualizadas += 1
        except Exception:
            continue

    return actualizadas


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
            if resultado.get("preguntas_rebalanceadas", 0) > 0:
                print(f"  Rebalanceo:   {resultado['preguntas_rebalanceadas']} preguntas "
                      f"con opciones barajadas")
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
            "preguntas_rebalanceadas": sum(r.get("preguntas_rebalanceadas", 0) for r in resultados),
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


# ============================================================
# IMPORTACIÓN DE SUPUESTOS
# ============================================================

def importar_supuesto(
    conn: sqlite3.Connection,
    supuesto: dict,
    update: bool = False,
) -> dict:
    """
    Importa un supuesto (JSON de Fase 3) a SQLite.
    """
    stats = {
        "supuesto_id": supuesto.get("id"),
        "accion": "skip",
        "preguntas_nuevas": 0,
        "preguntas_reutilizadas": 0,
        "preguntas_dup_conceptual": 0,
        "temas_vinculados": 0,
        "artefactos": 0,
        "errores": [],
    }

    sup_id = supuesto.get("id")
    if not sup_id:
        stats["errores"].append("Falta el campo 'id' del supuesto")
        return stats

    bloque_id = supuesto.get("bloque_id")
    if bloque_id:
        cur = conn.execute(
            "SELECT id, tiene_supuestos FROM bloques WHERE id = ?",
            (bloque_id,)
        )
        row = cur.fetchone()
        if not row:
            stats["errores"].append(f"Bloque no existe: {bloque_id}")
            return stats
        if not row[1]:
            stats["errores"].append(
                f"El bloque {bloque_id} no admite supuestos (tiene_supuestos=0)"
            )
            return stats

    cur = conn.execute("SELECT id FROM supuestos WHERE id = ?", (sup_id,))
    existe = cur.fetchone() is not None

    if existe and not update:
        stats["accion"] = "ya_existe"
        return stats

    contexto_json_str = json.dumps(
        supuesto.get("contexto_json", {}), ensure_ascii=False
    )

    if existe:
        conn.execute("""
            UPDATE supuestos SET
                examen_id = ?, bloque_id = ?, numero = ?, titulo = ?,
                tipo = ?, origen = ?, contexto_texto = ?, contexto_json = ?,
                verificado = ?
            WHERE id = ?
        """, (
            supuesto.get("examen_id"),
            bloque_id,
            supuesto.get("numero"),
            supuesto.get("titulo"),
            supuesto.get("tipo"),
            supuesto.get("origen", "real"),
            supuesto.get("contexto_texto"),
            contexto_json_str,
            int(supuesto.get("verificado", False)),
            sup_id,
        ))
        stats["accion"] = "actualizado"
    else:
        conn.execute("""
            INSERT INTO supuestos (
                id, examen_id, bloque_id, numero, titulo, tipo, origen,
                contexto_texto, contexto_json, verificado
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sup_id,
            supuesto.get("examen_id"),
            bloque_id,
            supuesto.get("numero"),
            supuesto.get("titulo"),
            supuesto.get("tipo"),
            supuesto.get("origen", "real"),
            supuesto.get("contexto_texto"),
            contexto_json_str,
            int(supuesto.get("verificado", False)),
        ))
        stats["accion"] = "nuevo"

    for p in supuesto.get("preguntas", []):
        numero = p.get("numero_en_supuesto")
        if not numero:
            stats["errores"].append("Pregunta sin numero_en_supuesto")
            continue

        enunciado = p.get("enunciado", "").strip()
        opciones = p.get("opciones", [])
        correcta = p.get("correcta", 0)
        concepto_id = p.get("concepto_id")
        tema_id = p.get("tema_id")

        if not enunciado or len(opciones) < 2:
            stats["errores"].append(
                f"Pregunta {numero}: enunciado u opciones incompletas"
            )
            continue

        pid = p.get("pregunta_id")
        if pid:
            cur = conn.execute(
                "SELECT id FROM preguntas WHERE id = ?", (pid,)
            )
            if not cur.fetchone():
                pid = None

        if not pid:
            pid_dup, motivo = buscar_pregunta_duplicada(
                conn, enunciado, opciones, correcta, concepto_id, p.get("tipo")
            )
            if pid_dup:
                pid = pid_dup
                if motivo == "exacta":
                    stats["preguntas_reutilizadas"] += 1
                else:
                    stats["preguntas_dup_conceptual"] += 1

        if not pid:
            h_exacto = sha256_exacto(enunciado, *opciones, str(correcta))
            h_norm = normalizar_texto(enunciado)
            pid = f"p-{hashlib.sha1(h_exacto.encode()).hexdigest()[:10]}"

            conn.execute("""
                INSERT INTO preguntas (
                    id, tema_id, concepto_id, tipo, dificultad, origen,
                    enunciado, opciones, correcta, explicacion, referencia,
                    verificado, hash_exacto, hash_normalizado, fecha_alta
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                pid,
                tema_id,
                concepto_id,
                p.get("tipo", "definicion"),
                p.get("dificultad", "media"),
                f"supuesto:{sup_id}",
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
            stats["preguntas_nuevas"] += 1

        conn.execute("""
            INSERT OR REPLACE INTO supuesto_preguntas (
                supuesto_id, pregunta_id, numero_en_supuesto, es_reserva
            ) VALUES (?, ?, ?, ?)
        """, (
            sup_id, pid, numero, int(p.get("es_reserva", False)),
        ))

    for t in supuesto.get("temas_implicados", []):
        tema_id = t.get("tema_id")
        if not tema_id:
            continue
        cur = conn.execute("SELECT id FROM temas WHERE id = ?", (tema_id,))
        if not cur.fetchone():
            stats["errores"].append(f"Tema no existe: {tema_id}")
            continue

        conn.execute("""
            INSERT OR REPLACE INTO supuesto_temas (
                supuesto_id, tema_id, n_preguntas
            ) VALUES (?, ?, ?)
        """, (sup_id, tema_id, t.get("n_preguntas", 0)))
        stats["temas_vinculados"] += 1

    for i, art in enumerate(supuesto.get("artefactos", []), 1):
        art_id = art.get("id") or f"art-{sup_id}-{i}"
        conn.execute("""
            INSERT OR REPLACE INTO supuesto_artefactos (
                id, supuesto_id, tipo, titulo, contenido, orden
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            art_id,
            sup_id,
            art.get("tipo", "texto"),
            art.get("titulo", ""),
            art.get("contenido", ""),
            art.get("orden", i),
        ))
        stats["artefactos"] += 1

    return stats


def cmd_importar_supuesto(args) -> int:
    """Comando: importar un JSON de supuesto a SQLite."""
    root = Path(args.root).expanduser().resolve()
    conn = conectar(root / "oposicion.db")

    try:
        archivo = Path(args.archivo).expanduser().resolve()
        if not archivo.exists():
            print(f"[error] No existe el archivo: {archivo}")
            return 1

        with archivo.open(encoding="utf-8") as f:
            supuesto = json.load(f)

        print(f"[importar-supuesto] {archivo.name}")
        print(f"[importar-supuesto] ID: {supuesto.get('id')}")
        print(f"[importar-supuesto] Modo: {'UPDATE' if args.update else 'SKIP duplicados'}")
        print()

        stats = importar_supuesto(conn, supuesto, update=args.update)

        if stats["errores"]:
            print("⚠️  Errores detectados:")
            for err in stats["errores"]:
                print(f"   - {err}")
            print()

        if stats["accion"] == "ya_existe":
            print(f"ℹ️  El supuesto ya existe. Usa --update para sobreescribir.")
            return 0

        if args.dry_run:
            conn.rollback()
            print("[importar-supuesto] DRY-RUN: cambios revertidos")
        else:
            conn.commit()
            print("[importar-supuesto] ✅ Cambios confirmados")

        print()
        print("=" * 60)
        print(f"  Acción:                {stats['accion']}")
        print(f"  Preguntas nuevas:      {stats['preguntas_nuevas']}")
        print(f"  Preguntas reutilizadas:{stats['preguntas_reutilizadas']}")
        print(f"  Dup conceptual:        {stats['preguntas_dup_conceptual']}")
        print(f"  Temas vinculados:      {stats['temas_vinculados']}")
        print(f"  Artefactos:            {stats['artefactos']}")
        print("=" * 60)

        if not args.dry_run and not stats["errores"]:
            print()
            print("💡 Siguiente paso: reconciliar el SRS")
            print(f"   make reconciliar")

        return 0 if not stats["errores"] else 1

    except Exception as e:
        conn.rollback()
        print(f"[error] {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        conn.close()

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



def cmd_migrar_estructura(args) -> int:
    """Comando: migrar estructura de temas sin perder datos completos."""
    root = Path(args.root).expanduser().resolve()
    conn = conectar(root / "oposicion.db")

    try:
        # 1. Backup automático
        backups_dir = root / "backups"
        backups_dir.mkdir(exist_ok=True)
        backup_path = backups_dir / f"pre-migracion-{date.today().isoformat()}.db"
        conn.execute(f"VACUUM INTO '{backup_path}'")
        print(f"[migrar-estructura] Backup: {backup_path}")

        # 2. Temas completos (se preservan)
        cur = conn.execute(
            "SELECT id FROM temas WHERE estado_ingesta = 'completo'"
        )
        completos = {row[0] for row in cur.fetchall()}
        print(f"[migrar-estructura] Temas completos a preservar: {len(completos)}")
        for t in sorted(completos):
            print(f"    - {t}")

        # 3. Borrar temas pendientes (se reinsertarán)
        cur = conn.execute(
            "SELECT COUNT(*) FROM temas WHERE estado_ingesta = 'pendiente'"
        )
        n_pend = cur.fetchone()[0]
        conn.execute("DELETE FROM temas WHERE estado_ingesta = 'pendiente'")
        print(f"[migrar-estructura] {n_pend} temas pendientes borrados")

        # 4. Borrar temas que ya no existen en la nueva estructura
        nuevos_ids = set()
        for bloque_id, temas in TEMAS_TAI.items():
            for numero, titulo in temas:
                tema_id = f"tema-{numero:02d}-{slugify(titulo)}"
                nuevos_ids.add(tema_id)

        cur = conn.execute("SELECT id FROM temas")
        existentes = {row[0] for row in cur.fetchall()}
        sobrantes = existentes - nuevos_ids - completos
        for t in sobrantes:
            conn.execute("DELETE FROM temas WHERE id = ?", (t,))
        print(f"[migrar-estructura] {len(sobrantes)} temas sobrantes borrados")

        # 5. Reinsertar los que faltan
        insertados = 0
        for bloque_id, temas in TEMAS_TAI.items():
            tipo = "tecnico" if bloque_id in ("bloque-iii", "bloque-iv") else "juridico"
            for numero, titulo in temas:
                tema_id = f"tema-{numero:02d}-{slugify(titulo)}"
                if tema_id in completos:
                    continue
                conn.execute("""
                    INSERT OR IGNORE INTO temas
                    (id, numero, titulo, bloque_id, tipo, estado_ingesta)
                    VALUES (?, ?, ?, ?, ?, 'pendiente')
                """, (tema_id, numero, titulo, bloque_id, tipo))
                insertados += 1

        conn.commit()

        print(f"[migrar-estructura] {insertados} temas nuevos insertados")
        print()
        print("=" * 60)
        print("  ✅ Migración completada")
        print("=" * 60)

        # Verificación
        cur = conn.execute("""
            SELECT b.numero, b.nombre, COUNT(t.id) AS n
            FROM bloques b
            LEFT JOIN temas t ON t.bloque_id = b.id
            GROUP BY b.id ORDER BY b.numero
        """)
        print("  Distribución por bloque:")
        for num, nombre, n in cur.fetchall():
            print(f"    Bloque {num} ({nombre[:40]}): {n} temas")

        return 0
    except Exception as e:
        conn.rollback()
        print(f"[error] {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        conn.close()


def cmd_migrar_fuentes(args) -> int:
    """Comando: crear tablas de fuentes y fragmentos + ampliar conceptos."""
    root = Path(args.root).expanduser().resolve()
    conn = conectar(root / "oposicion.db")

    try:
        # Backup automático
        backup = root / "backups" / f"pre-migracion-fuentes-{date.today().isoformat()}.db"
        backup.parent.mkdir(exist_ok=True)
        if backup.exists():
            backup.unlink()
        conn.execute(f"VACUUM INTO '{backup}'")
        print(f"[migrar-fuentes] Backup: {backup}")

        # Aplicar schema de tablas nuevas
        sql_path = root / "db" / "migrate_fuentes.sql"
        if not sql_path.exists():
            print(f"[error] No existe: {sql_path}")
            return 1

        with sql_path.open(encoding="utf-8") as f:
            conn.executescript(f.read())
        print("[migrar-fuentes] Tablas fuentes/fragmentos/concepto_fragmentos creadas")

        # Añadir columnas nuevas a conceptos (si no existen)
        cur = conn.execute("PRAGMA table_info(conceptos)")
        columnas_existentes = {row[1] for row in cur.fetchall()}

        nuevas_columnas = [
            ("resumen", "TEXT"),
            ("completitud", "REAL DEFAULT 0"),
            ("fuentes_count", "INTEGER DEFAULT 0"),
            ("ultima_actualizacion", "TEXT"),
            ("discrepancia", "INTEGER DEFAULT 0"),
            ("fusionado_en", "TEXT"),
            ("es_core", "BOOLEAN DEFAULT 0"),
        ]

        for nombre, tipo in nuevas_columnas:
            if nombre not in columnas_existentes:
                conn.execute(f"ALTER TABLE conceptos ADD COLUMN {nombre} {tipo}")
                print(f"[migrar-fuentes] Columna añadida: conceptos.{nombre}")
            else:
                print(f"[migrar-fuentes] Columna ya existe: conceptos.{nombre}")

        conn.commit()

        # Verificación
        cur = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name IN ('fuentes', 'fragmentos', 'concepto_fragmentos')"
        )
        tablas = [row[0] for row in cur.fetchall()]
        print()
        print("=" * 60)
        print(f"  ✅ Migración completada")
        print("=" * 60)
        print(f"  Tablas nuevas:     {', '.join(tablas)}")
        print(f"  Columnas nuevas:   {len(nuevas_columnas)}")

        return 0
    except Exception as e:
        conn.rollback()
        print(f"[error] {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        conn.close()


def _hash_archivo(path: Path) -> str:
    """SHA-256 del archivo para detectar duplicados."""
    import hashlib
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _hash_fragmento(texto: str) -> str:
    """SHA-256 del texto normalizado del fragmento."""
    import hashlib
    normalizado = normalizar_texto(texto)
    return hashlib.sha256(normalizado.encode("utf-8")).hexdigest()


def cmd_ingestar_fuente(args) -> int:
    """
    Comando: ingestar un archivo JSON de fragmentos ya extraídos.

    El usuario (o la skill Fase 0) genera un JSON con:
    {
      "fuente": {
        "id": "fuente-2024-mad-bd",
        "titulo": "Manual MAD — Bases de datos 2024",
        "tipo": "manual",
        "editor": "MAD",
        "version": "3ª ed.",
        "fecha": "2024-05-01",
        "archivo_path": "temario/tema-15/fuente/manual-mad.pdf",
        "paginas": 320
      },
      "tema_id": "tema-15-modelado-de-datos",
      "fragmentos": [
        {
          "numero_pagina": 12,
          "numero_seccion": "2.1",
          "titulo_seccion": "Entidades",
          "texto": "..."
        }
      ],
      "conceptos": [
        {
          "id": "c-entidad-debil",
          "nombre": "Entidad débil",
          "tipo": "definicion",
          "resumen": "Entidad cuya existencia depende de otra...",
          "fragmentos_indices": [3, 7, 12],
          "es_principal": true
        }
      ]
    }
    """
    root = Path(args.root).expanduser().resolve()
    conn = conectar(root / "oposicion.db")

    try:
        archivo = Path(args.archivo).expanduser().resolve()
        if not archivo.exists():
            print(f"[error] No existe: {archivo}")
            return 1

        with archivo.open(encoding="utf-8") as f:
            data = json.load(f)

        tema_id = data.get("tema_id") or args.tema
        if not tema_id:
            print("[error] Falta tema_id en el JSON o en --tema")
            return 1

        # 1. Verificar que el tema existe y es técnico
        cur = conn.execute(
            "SELECT id, tipo FROM temas WHERE id = ?", (tema_id,)
        )
        row = cur.fetchone()
        if not row:
            print(f"[error] Tema no existe: {tema_id}")
            return 1
        if row[1] != "tecnico":
            print(f"[warn] Tema {tema_id} es de tipo '{row[1]}'. "
                  f"El modelo de fuentes está pensado para técnicos.")

        # 2. Insertar/verificar fuente
        fuente_data = data["fuente"]
        hash_arch = fuente_data.get("hash_archivo")
        if not hash_arch and fuente_data.get("archivo_path"):
            pdf_path = root / fuente_data["archivo_path"]
            if pdf_path.exists():
                hash_arch = _hash_archivo(pdf_path)

        cur = conn.execute(
            "SELECT id, estado FROM fuentes WHERE id = ?", (fuente_data["id"],)
        )
        row = cur.fetchone()
        if row:
            print(f"[ingestar] Fuente ya existe: {row[0]} ({row[1]})")
            fuente_id = row[0]
            if not args.force:
                # Comprobar si hay fragmentos nuevos
                pass
        else:
            conn.execute("""
                INSERT INTO fuentes (
                    id, titulo, tipo, editor, version, fecha,
                    archivo_path, hash_archivo, paginas,
                    estado, fecha_ingesta
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'ingestado', ?)
            """, (
                fuente_data["id"],
                fuente_data["titulo"],
                fuente_data["tipo"],
                fuente_data.get("editor"),
                fuente_data.get("version"),
                fuente_data.get("fecha"),
                fuente_data.get("archivo_path"),
                hash_arch,
                fuente_data.get("paginas"),
                date.today().isoformat(),
            ))
            fuente_id = fuente_data["id"]
            print(f"[ingestar] Fuente creada: {fuente_id}")

        # 3. Insertar fragmentos (con dedup por hash)
        fragmentos_data = data.get("fragmentos", [])
        stats = {
            "fragmentos_nuevos": 0,
            "fragmentos_duplicados": 0,
            "fragmentos_totales": len(fragmentos_data),
            "conceptos_nuevos": 0,
            "conceptos_ampliados": 0,
            "vinculos_creados": 0,
        }

        ids_fragmentos_creados = []  # por índice del JSON

        for i, frag in enumerate(fragmentos_data):
            texto = frag["texto"].strip()
            if len(texto) < 50:
                continue

            hash_norm = _hash_fragmento(texto)

            cur = conn.execute(
                "SELECT id FROM fragmentos WHERE hash_normalizado = ?",
                (hash_norm,)
            )
            row = cur.fetchone()
            if row:
                ids_fragmentos_creados.append(row[0])
                stats["fragmentos_duplicados"] += 1
                continue

            frag_id = f"frag-{fuente_id}-p{frag.get('numero_pagina', 0)}-{i}"
            conn.execute("""
                INSERT INTO fragmentos (
                    id, fuente_id, tema_id, numero_pagina, numero_seccion,
                    titulo_seccion, texto, hash_normalizado, estado, fecha_ingesta
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'activo', ?)
            """, (
                frag_id,
                fuente_id,
                tema_id,
                frag.get("numero_pagina"),
                frag.get("numero_seccion"),
                frag.get("titulo_seccion"),
                texto,
                hash_norm,
                date.today().isoformat(),
            ))
            ids_fragmentos_creados.append(frag_id)
            stats["fragmentos_nuevos"] += 1

        # 4. Procesar conceptos
        for concepto_data in data.get("conceptos", []):
            cid = concepto_data["id"]

            cur = conn.execute(
                "SELECT id, fuentes_count FROM conceptos WHERE id = ?", (cid,)
            )
            row = cur.fetchone()

            # ================================================
            # Antes de crear: buscar concepto similar existente
            # ================================================
            conn.row_factory = sqlite3.Row
            if not row:
                cur = conn.execute("""
                    SELECT c.id, c.nombre, c.valor, c.resumen, c.tipo
                    FROM conceptos c
                    JOIN concepto_temas ct ON ct.concepto_id = c.id
                    WHERE ct.tema_id = ?
                      AND (c.fusionado_en IS NULL OR c.fusionado_en = '')
                """, (tema_id,))

                candidato_auto = None
                candidato_revisar = None

                for r in cur.fetchall():
                    info = _clasificar_par(
                        {
                            "id": r["id"], "nombre": r["nombre"],
                            "valor": r["valor"], "resumen": r["resumen"], "tipo": r["tipo"],
                        },
                        {
                            "id": concepto_data["id"],
                            "nombre": concepto_data["nombre"],
                            "valor": concepto_data.get("valor"),
                            "resumen": concepto_data.get("resumen"),
                            "tipo": concepto_data.get("tipo"),
                        },
                    )
                    if not info:
                        continue

                    if info["nivel"] == 1 and not candidato_auto:
                        candidato_auto = r["id"]
                        break
                    elif info["nivel"] == 2 and not candidato_revisar:
                        candidato_revisar = r["id"]

                if candidato_auto:
                    # Auto-fusión segura
                    print(f"[ingestar] '{concepto_data['nombre']}' -> concepto existente "
                          f"{candidato_auto} (auto)")
                    cid = candidato_auto
                    row = (cid, None)
                elif candidato_revisar:
                    # Candidato ambiguo -> crear vinculado como "revisar"
                    print(f"[ingestar] ADVERTENCIA: '{concepto_data['nombre']}' tiene un posible "
                          f"duplicado ({candidato_revisar}). Se crea nuevo. Revisar después.")

            if not row:
                # Concepto nuevo
                conn.execute("""
                    INSERT INTO conceptos (
                        id, nombre, tipo, valor, resumen,
                        fuentes_count, completitud, verificado,
                        ultima_actualizacion
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    cid,
                    concepto_data["nombre"],
                    concepto_data.get("tipo"),
                    concepto_data.get("valor"),
                    concepto_data.get("resumen"),
                    1,
                    50.0,
                    int(args.marcar_verificado),
                    date.today().isoformat(),
                ))
                # Vincular al tema
                conn.execute("""
                    INSERT OR IGNORE INTO concepto_temas (
                        concepto_id, tema_id, es_principal
                    ) VALUES (?, ?, ?)
                """, (cid, tema_id, int(concepto_data.get("es_principal", True))))
                stats["conceptos_nuevos"] += 1
            else:
                # Concepto existente: ampliar resumen
                resumen_nuevo = concepto_data.get("resumen")
                if resumen_nuevo and args.actualizar_resumen:
                    conn.execute("""
                        UPDATE conceptos SET
                            resumen = ?,
                            fuentes_count = fuentes_count + 1,
                            ultima_actualizacion = ?
                        WHERE id = ?
                    """, (
                        resumen_nuevo,
                        date.today().isoformat(),
                        cid,
                    ))
                else:
                    conn.execute("""
                        UPDATE conceptos SET
                            fuentes_count = fuentes_count + 1,
                            ultima_actualizacion = ?
                        WHERE id = ?
                    """, (date.today().isoformat(), cid))
                stats["conceptos_ampliados"] += 1

            # Vincular fragmentos al concepto
            indices = concepto_data.get("fragmentos_indices", [])
            for idx in indices:
                if 0 <= idx < len(ids_fragmentos_creados):
                    frag_id = ids_fragmentos_creados[idx]
                    try:
                        conn.execute("""
                            INSERT OR IGNORE INTO concepto_fragmentos (
                                concepto_id, fragmento_id, es_principal,
                                aportacion, fecha_vinculo
                            ) VALUES (?, ?, ?, ?, ?)
                        """, (
                            cid,
                            frag_id,
                            int(concepto_data.get("es_principal", False) and idx == indices[0]),
                            concepto_data.get("aportacion", "definicion"),
                            date.today().isoformat(),
                        ))
                        stats["vinculos_creados"] += 1
                    except sqlite3.IntegrityError:
                        pass

        # 5. Marcar fuente como ingestada
        conn.execute("""
            UPDATE fuentes SET estado = 'ingestado', fecha_ingesta = ?
            WHERE id = ?
        """, (date.today().isoformat(), fuente_id))

        conn.commit()

        # 6. Reporte
        print()
        print("=" * 60)
        print(f"  ✅ Ingesta completada")
        print("=" * 60)
        print(f"  Fuente:               {fuente_id}")
        print(f"  Tema:                 {tema_id}")
        print(f"  Fragmentos nuevos:    {stats['fragmentos_nuevos']}")
        print(f"  Fragmentos duplicados:{stats['fragmentos_duplicados']}")
        print(f"  Fragmentos totales:   {stats['fragmentos_totales']}")
        print(f"  Conceptos nuevos:     {stats['conceptos_nuevos']}")
        print(f"  Conceptos ampliados:  {stats['conceptos_ampliados']}")
        print(f"  Vínculos creados:     {stats['vinculos_creados']}")

        if stats["fragmentos_duplicados"] > 0:
            pct = stats["fragmentos_duplicados"] * 100 / stats["fragmentos_totales"]
            print(f"  Solapamiento con otras fuentes: {pct:.1f}%")

        return 0

    except Exception as e:
        conn.rollback()
        print(f"[error] {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        conn.close()


def cmd_ingestar_fuente_v2(args) -> int:
    """
    Comando: ingestar un archivo JSON de fragmentos ya extraídos.

    El usuario (o la skill Fase 0) genera un JSON con:
    {
      "fuente": {
        "id": "fuente-2024-mad-bd",
        "titulo": "Manual MAD — Bases de datos 2024",
        "tipo": "manual",
        "editor": "MAD",
        "version": "3ª ed.",
        "fecha": "2024-05-01",
        "archivo_path": "temario/tema-15/fuente/manual-mad.pdf",
        "paginas": 320
      },
      "tema_id": "tema-15-modelado-de-datos",
      "fragmentos": [
        {
          "numero_pagina": 12,
          "numero_seccion": "2.1",
          "titulo_seccion": "Entidades",
          "texto": "..."
        }
      ],
      "conceptos": [
        {
          "id": "c-entidad-debil",
          "nombre": "Entidad débil",
          "tipo": "definicion",
          "resumen": "Entidad cuya existencia depende de otra...",
          "fragmentos_indices": [3, 7, 12],
          "es_principal": true
        }
      ]
    }
    """
    root = Path(args.root).expanduser().resolve()
    conn = conectar(root / "oposicion.db")

    try:
        archivo = Path(args.archivo).expanduser().resolve()
        if not archivo.exists():
            print(f"[error] No existe: {archivo}")
            return 1

        with archivo.open(encoding="utf-8") as f:
            data = json.load(f)

        tema_id = data.get("tema_id") or args.tema
        if not tema_id:
            print("[error] Falta tema_id en el JSON o en --tema")
            return 1

        # 1. Verificar que el tema existe y es técnico
        cur = conn.execute(
            "SELECT id, tipo FROM temas WHERE id = ?", (tema_id,)
        )
        row = cur.fetchone()
        if not row:
            print(f"[error] Tema no existe: {tema_id}")
            return 1
        if row[1] != "tecnico":
            print(f"[warn] Tema {tema_id} es de tipo '{row[1]}'. "
                  f"El modelo de fuentes está pensado para técnicos.")

        # 2. Insertar/verificar fuente
        fuente_data = data["fuente"]
        hash_arch = fuente_data.get("hash_archivo")
        if not hash_arch and fuente_data.get("archivo_path"):
            pdf_path = root / fuente_data["archivo_path"]
            if pdf_path.exists():
                hash_arch = _hash_archivo(pdf_path)

        cur = conn.execute(
            "SELECT id, estado FROM fuentes WHERE id = ?", (fuente_data["id"],)
        )
        row = cur.fetchone()
        if row:
            print(f"[ingestar] Fuente ya existe: {row[0]} ({row[1]})")
            fuente_id = row[0]
            if not args.force:
                # Comprobar si hay fragmentos nuevos
                pass
        else:
            conn.execute("""
                INSERT INTO fuentes (
                    id, titulo, tipo, editor, version, fecha,
                    archivo_path, hash_archivo, paginas,
                    estado, fecha_ingesta
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'ingestado', ?)
            """, (
                fuente_data["id"],
                fuente_data["titulo"],
                fuente_data["tipo"],
                fuente_data.get("editor"),
                fuente_data.get("version"),
                fuente_data.get("fecha"),
                fuente_data.get("archivo_path"),
                hash_arch,
                fuente_data.get("paginas"),
                date.today().isoformat(),
            ))
            fuente_id = fuente_data["id"]
            print(f"[ingestar] Fuente creada: {fuente_id}")

        # 3. Insertar fragmentos (con dedup por hash)
        fragmentos_data = data.get("fragmentos", [])
        stats = {
            "fragmentos_nuevos": 0,
            "fragmentos_duplicados": 0,
            "fragmentos_totales": len(fragmentos_data),
            "conceptos_asignados_a_core": 0,
            "candidatos_ampliados": 0,
            "candidatos_promovidos": 0,
            "candidatos_nuevos": 0,
            "vinculos_creados": 0,
        }

        ids_fragmentos_creados = []  # por índice del JSON

        for i, frag in enumerate(fragmentos_data):
            texto = frag["texto"].strip()
            if len(texto) < 50:
                continue

            hash_norm = _hash_fragmento(texto)

            cur = conn.execute(
                "SELECT id FROM fragmentos WHERE hash_normalizado = ?",
                (hash_norm,)
            )
            row = cur.fetchone()
            if row:
                ids_fragmentos_creados.append(row[0])
                stats["fragmentos_duplicados"] += 1
                continue

            frag_id = f"frag-{fuente_id}-p{frag.get('numero_pagina', 0)}-{i}"
            conn.execute("""
                INSERT INTO fragmentos (
                    id, fuente_id, tema_id, numero_pagina, numero_seccion,
                    titulo_seccion, texto, hash_normalizado, estado, fecha_ingesta
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'activo', ?)
            """, (
                frag_id,
                fuente_id,
                tema_id,
                frag.get("numero_pagina"),
                frag.get("numero_seccion"),
                frag.get("titulo_seccion"),
                texto,
                hash_norm,
                date.today().isoformat(),
            ))
            ids_fragmentos_creados.append(frag_id)
            stats["fragmentos_nuevos"] += 1

        conn.row_factory = sqlite3.Row
        # 4. Procesar conceptos (v2: core + candidatos)
        for concepto_data in data.get("conceptos", []):
            # 1. Intentar asignar a un concepto core existente
            cur = conn.execute("""
                SELECT c.id, c.nombre, c.valor, c.resumen
                FROM conceptos c
                JOIN concepto_temas ct ON ct.concepto_id = c.id
                WHERE ct.tema_id = ?
                  AND c.es_core = 1
                  AND (c.fusionado_en IS NULL OR c.fusionado_en = '')
            """, (tema_id,))

            candidato_core = None
            mejor_sim = 0.0

            for r in cur.fetchall():
                sim = _similitud_concepto(concepto_data, r)
                if sim > mejor_sim and sim >= getattr(args, "umbral_core", 0.6):
                    mejor_sim = sim
                    candidato_core = r["id"]

            if candidato_core:
                # Asignar al core
                cid = candidato_core
                conn.execute("""
                    UPDATE conceptos SET
                        fuentes_count = fuentes_count + 1,
                        ultima_actualizacion = ?
                    WHERE id = ?
                """, (date.today().isoformat(), cid))
                stats["conceptos_asignados_a_core"] += 1
            else:
                # Buscar candidato existente
                cur = conn.execute("""
                    SELECT id, nombre, n_fragmentos, fragmento_ids
                    FROM conceptos_candidatos
                    WHERE tema_id = ?
                      AND estado = 'pendiente'
                      AND nombre = ?
                """, (tema_id, concepto_data["nombre"]))

                row = cur.fetchone()
                if row:
                    # Incrementar contador
                    frag_ids = json.loads(row["fragmento_ids"] or "[]")
                    frag_ids.extend(ids_fragmentos_creados)
                    conn.execute("""
                        UPDATE conceptos_candidatos
                        SET n_fragmentos = n_fragmentos + ?,
                            fragmento_ids = ?,
                            ultima_actualizacion = ?
                        WHERE id = ?
                    """, (
                        len(ids_fragmentos_creados),
                        json.dumps(frag_ids, ensure_ascii=False),
                        date.today().isoformat(),
                        row["id"],
                    ))
                    stats["candidatos_ampliados"] += 1

                    # Promover si alcanza umbral
                    if (row["n_fragmentos"] or 0) + len(ids_fragmentos_creados) >= getattr(args, "min_fragmentos", 2):
                        _promover_candidato(conn, row["id"], tema_id)
                        stats["candidatos_promovidos"] += 1
                else:
                    # Crear nuevo candidato
                    conn.execute("""
                        INSERT INTO conceptos_candidatos (
                            tema_id, nombre, descripcion, n_fragmentos,
                            fragmento_ids, estado,
                            primera_aparicion, ultima_actualizacion
                        ) VALUES (?, ?, ?, ?, ?, 'pendiente', ?, ?)
                    """, (
                        tema_id,
                        concepto_data["nombre"],
                        concepto_data.get("resumen"),
                        len(ids_fragmentos_creados),
                        json.dumps(ids_fragmentos_creados, ensure_ascii=False),
                        date.today().isoformat(),
                        date.today().isoformat(),
                    ))
                    stats["candidatos_nuevos"] += 1

                cid = None  # no concepto real creado

            # Vincular fragmentos al concepto (solo si hay concepto real)
            if cid:
                indices = concepto_data.get("fragmentos_indices", [])
                for idx in indices:
                    if 0 <= idx < len(ids_fragmentos_creados):
                        frag_id = ids_fragmentos_creados[idx]
                        try:
                            conn.execute("""
                                INSERT OR IGNORE INTO concepto_fragmentos (
                                    concepto_id, fragmento_id, es_principal,
                                    aportacion, fecha_vinculo
                                ) VALUES (?, ?, ?, ?, ?)
                            """, (
                                cid,
                                frag_id,
                                int(concepto_data.get("es_principal", False) and idx == indices[0]),
                                concepto_data.get("aportacion", "definicion"),
                                date.today().isoformat(),
                            ))
                            stats["vinculos_creados"] += 1
                        except sqlite3.IntegrityError:
                            pass

        # 5. Marcar fuente como ingestada
        conn.execute("""
            UPDATE fuentes SET estado = 'ingestado', fecha_ingesta = ?
            WHERE id = ?
        """, (date.today().isoformat(), fuente_id))

        conn.commit()

        # 6. Reporte
        print()
        print("=" * 60)
        print(f"  ✅ Ingesta completada")
        print("=" * 60)
        print(f"  Fuente:               {fuente_id}")
        print(f"  Tema:                 {tema_id}")
        print(f"  Fragmentos nuevos:    {stats['fragmentos_nuevos']}")
        print(f"  Fragmentos duplicados:{stats['fragmentos_duplicados']}")
        print(f"  Fragmentos totales:   {stats['fragmentos_totales']}")
        print(f"  Asignados a core:     {stats['conceptos_asignados_a_core']}")
        print(f"  Candidatos nuevos:    {stats['candidatos_nuevos']}")
        print(f"  Candidatos ampliados: {stats['candidatos_ampliados']}")
        print(f"  Candidatos promovidos:{stats['candidatos_promovidos']}")
        print(f"  Vínculos creados:     {stats['vinculos_creados']}")

        if stats["fragmentos_duplicados"] > 0:
            pct = stats["fragmentos_duplicados"] * 100 / stats["fragmentos_totales"]
            print(f"  Solapamiento con otras fuentes: {pct:.1f}%")

        return 0

    except Exception as e:
        conn.rollback()
        print(f"[error] {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        conn.close()



def cmd_consolidar_tema(args) -> int:
    """
    Comando: consolidar los conceptos de un tema técnico.
    Por ahora solo actualiza 'completitud' y reporta conceptos
    que necesitan re-resumen (con múltiples fragmentos de fuentes distintas).

    La síntesis real del resumen la hará el LLM externo (skill tai-oposicion),
    este comando prepara el material.
    """
    root = Path(args.root).expanduser().resolve()
    conn = conectar(root / "oposicion.db")

    try:
        tema_id = args.tema
        if not tema_id:
            print("[error] Falta --tema")
            return 1

        # 1. Calcular completitud de cada concepto
        cur = conn.execute("""
            SELECT
                c.id,
                c.nombre,
                COUNT(DISTINCT f.fuente_id) AS n_fuentes,
                COUNT(cf.fragmento_id) AS n_fragmentos
            FROM conceptos c
            JOIN concepto_temas ct ON ct.concepto_id = c.id
            LEFT JOIN concepto_fragmentos cf ON cf.concepto_id = c.id
            LEFT JOIN fragmentos f ON f.id = cf.fragmento_id
            WHERE ct.tema_id = ?
              AND (c.fusionado_en IS NULL OR c.fusionado_en = '')
            GROUP BY c.id
        """, (tema_id,))

        conceptos = cur.fetchall()
        print(f"[consolidar] {len(conceptos)} conceptos en {tema_id}")
        print()

        # 2. Completitud = min(100, n_fuentes * 33.3) si hay 3 fuentes → 100%
        #    + bonus por n_fragmentos
        actualizados = 0
        for cid, nombre, n_fuentes, n_frag in conceptos:
            n_fuentes = n_fuentes or 0
            n_frag = n_frag or 0
            completitud = min(100.0, n_fuentes * 33.3)
            if n_frag >= 5:
                completitud = min(100.0, completitud + 10)

            conn.execute("""
                UPDATE conceptos SET
                    completitud = ?,
                    fuentes_count = ?
                WHERE id = ?
            """, (completitud, n_fuentes, cid))
            actualizados += 1

        conn.commit()

        # 3. Reporte
        cur = conn.execute("""
            SELECT
                COUNT(*) AS total,
                SUM(CASE WHEN completitud >= 80 THEN 1 ELSE 0 END) AS alta,
                SUM(CASE WHEN completitud >= 50 AND completitud < 80 THEN 1 ELSE 0 END) AS media,
                SUM(CASE WHEN completitud < 50 THEN 1 ELSE 0 END) AS baja
            FROM conceptos c
            JOIN concepto_temas ct ON ct.concepto_id = c.id
            WHERE ct.tema_id = ?
              AND (c.fusionado_en IS NULL OR c.fusionado_en = '')
        """, (tema_id,))
        row = cur.fetchone()

        print(f"[consolidar] Completitud actualizada:")
        print(f"  Alta  (≥80%):  {row[1]} conceptos")
        print(f"  Media (50-79%): {row[2]} conceptos")
        print(f"  Baja  (<50%):  {row[3]} conceptos")
        print()
        print(f"💡 Para los de completitud baja, ingesta más fuentes o")
        print(f"   ejecuta la Fase 0 de tai-oposicion para regenerar resúmenes.")

        # 4. Exportar conceptos con completitud baja
        if args.exportar_baja:
            cur = conn.execute("""
                SELECT c.id, c.nombre, c.completitud, c.fuentes_count
                FROM conceptos c
                JOIN concepto_temas ct ON ct.concepto_id = c.id
                WHERE ct.tema_id = ? AND c.completitud < 50
                  AND (c.fusionado_en IS NULL OR c.fusionado_en = '')
                ORDER BY c.completitud ASC
            """, (tema_id,))
            bajos = [
                {"id": r[0], "nombre": r[1], "completitud": r[2], "fuentes": r[3]}
                for r in cur.fetchall()
            ]
            archivo = root / f"conceptos-baja-{tema_id}.json"
            with archivo.open("w", encoding="utf-8") as f:
                json.dump(bajos, f, ensure_ascii=False, indent=2)
            print(f"  Exportados {len(bajos)} conceptos a: {archivo}")

        return 0

    except Exception as e:
        conn.rollback()
        print(f"[error] {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        conn.close()

import re as _re
import unicodedata as _unicodedata
from difflib import SequenceMatcher as _SequenceMatcher


def _similitud_nombre(n1: str, n2: str) -> float:
    """Similitud de nombres con normalización agresiva."""
    def normalizar(s):
        s = _unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
        s = s.lower()
        s = _re.sub(r"\b(el|la|los|las|un|una|de|del|y|o|en)\b", " ", s)
        s = _re.sub(r"\b(\w+)es\b", r"\1", s)
        s = _re.sub(r"\b(\w+)s\b", r"\1", s)
        s = _re.sub(r"[^a-z0-9\s]", " ", s)
        return _re.sub(r"\s+", " ", s).strip()

    n1n = normalizar(n1)
    n2n = normalizar(n2)
    if not n1n or not n2n:
        return 0.0
    return _SequenceMatcher(None, n1n, n2n).ratio()


def _similitud_valor(v1: str, v2: str) -> float:
    """Similitud de valores por Jaccard de tokens."""
    def tokenizar(s):
        if not s:
            return set()
        s = _unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
        s = s.lower()
        s = _re.sub(r"[^a-z0-9\s]", " ", s)
        return {t for t in s.split() if len(t) > 2}

    t1 = tokenizar(v1)
    t2 = tokenizar(v2)
    if not t1 or not t2:
        return 0.0
    return len(t1 & t2) / len(t1 | t2)



def _clasificar_par(c1: dict, c2: dict) -> dict | None:
    """
    Clasifica un par de conceptos en uno de los 3 niveles.
    Devuelve dict con la información o None si no es candidato.
    """
    # Solo mismo tipo
    if c1["tipo"] != c2["tipo"]:
        return None

    sim_n = _similitud_nombre(c1["nombre"], c2["nombre"])
    sim_v = _similitud_valor(
        (c1["valor"] or "") + " " + (c1["resumen"] or ""),
        (c2["valor"] or "") + " " + (c2["resumen"] or ""),
    )

    # Nivel 1: nombre prácticamente idéntico → auto
    if sim_n >= 0.95:
        return {
            "nivel": 1,
            "accion": "auto",
            "sim_nombre": round(sim_n, 3),
            "sim_valor": round(sim_v, 3),
            "score": 1.0,
            "razon": "nombre_idéntico",
        }

    # Nivel 2: nombre muy similar + algo de contenido → candidato fuerte
    if sim_n >= 0.80 and sim_v >= 0.15:
        return {
            "nivel": 2,
            "accion": "revisar",
            "sim_nombre": round(sim_n, 3),
            "sim_valor": round(sim_v, 3),
            "score": round(0.7 * sim_n + 0.3 * sim_v, 3),
            "razon": "nombre_muy_similar",
        }

    # Nivel 3: score combinado con nombre dominante
    score = 0.7 * sim_n + 0.3 * sim_v
    if score >= 0.70:
        return {
            "nivel": 3,
            "accion": "revisar",
            "sim_nombre": round(sim_n, 3),
            "sim_valor": round(sim_v, 3),
            "score": round(score, 3),
            "razon": "score_combinado",
        }

    return None


def _similitud_concepto(concepto_data: dict, r) -> float:
    """Similitud entre un concepto nuevo (dict del JSON) y un concepto core (Row).

    El nombre domina: los conceptos core provienen de clasificación de exámenes
    y tienen descripciones mínimas, por lo que la similitud de contenido es baja.
    """
    sim_n = _similitud_nombre(concepto_data.get("nombre", ""), r["nombre"])
    v1 = (concepto_data.get("resumen") or concepto_data.get("valor") or "")
    v2 = (r["resumen"] or r["valor"] or "")
    sim_v = _similitud_valor(v1, v2)
    return round(0.8 * sim_n + 0.2 * sim_v, 4)


def _promover_candidato(conn, candidato_id: int, tema_id: str) -> str:
    """
    Promueve un candidato a concepto real.
    Devuelve el id del concepto creado.
    """
    import hashlib
    import json
    from datetime import date

    cur = conn.execute("""
        SELECT nombre, descripcion, n_fragmentos, fragmento_ids
        FROM conceptos_candidatos WHERE id = ?
    """, (candidato_id,))
    cand = cur.fetchone()
    if not cand:
        return ""

    nombre = cand["nombre"]
    descripcion = cand["descripcion"]

    # Reutilizar concepto existente con el mismo nombre si ya existe
    cur = conn.execute("SELECT id FROM conceptos WHERE lower(nombre) = lower(?)", (nombre,))
    existing = cur.fetchone()
    if existing:
        concepto_id = existing["id"]
    else:
        concepto_id = f"c-{hashlib.sha1(nombre.encode()).hexdigest()[:12]}"
        conn.execute("""
            INSERT OR IGNORE INTO conceptos (
                id, nombre, tipo, valor, resumen, es_core, verificado,
                fuentes_count, completitud, ultima_actualizacion
            ) VALUES (?, ?, 'definicion', NULL, ?, 0, 0, 1, 50.0, ?)
        """, (
            concepto_id,
            nombre,
            descripcion,
            date.today().isoformat(),
        ))

    conn.execute("""
        INSERT OR IGNORE INTO concepto_temas (concepto_id, tema_id, es_principal)
        VALUES (?, ?, 0)
    """, (concepto_id, tema_id))

    try:
        frag_ids = json.loads(cand["fragmento_ids"] or "[]")
    except Exception:
        frag_ids = []
    for frag_id in frag_ids:
        try:
            conn.execute("""
                INSERT OR IGNORE INTO concepto_fragmentos (
                    concepto_id, fragmento_id, es_principal, aportacion, fecha_vinculo
                ) VALUES (?, ?, 0, 'ampliacion', ?)
            """, (concepto_id, frag_id, date.today().isoformat()))
        except sqlite3.IntegrityError:
            pass

    conn.execute("""
        UPDATE conceptos_candidatos
        SET estado = 'promovido', concepto_promovido_id = ?
        WHERE id = ?
    """, (concepto_id, candidato_id))

    return concepto_id


def cmd_detectar_fusiones(args) -> int:
    """Detecta grupos de conceptos candidatos a fusionar (v2, por niveles)."""
    import json

    root = Path(args.root).expanduser().resolve()
    conn = conectar(root / "oposicion.db")
    conn.row_factory = sqlite3.Row

    try:
        tema_id = args.tema
        if not tema_id:
            print("[error] Falta --tema")
            return 1

        # Cargar conceptos
        cur = conn.execute("""
            SELECT c.id, c.nombre, c.valor, c.resumen, c.tipo
            FROM conceptos c
            JOIN concepto_temas ct ON ct.concepto_id = c.id
            WHERE ct.tema_id = ?
              AND (c.fusionado_en IS NULL OR c.fusionado_en = '')
        """, (tema_id,))

        conceptos = [
            {
                "id": r["id"], "nombre": r["nombre"],
                "valor": r["valor"], "resumen": r["resumen"], "tipo": r["tipo"],
            }
            for r in cur.fetchall()
        ]
        print(f"[detectar] {len(conceptos)} conceptos en {tema_id}")

        # Clasificar todos los pares
        pares = []
        for i in range(len(conceptos)):
            for j in range(i + 1, len(conceptos)):
                info = _clasificar_par(conceptos[i], conceptos[j])
                if info:
                    info["c1"] = conceptos[i]["id"]
                    info["c1_nombre"] = conceptos[i]["nombre"]
                    info["c2"] = conceptos[j]["id"]
                    info["c2_nombre"] = conceptos[j]["nombre"]
                    pares.append(info)

        # Agrupar por nivel
        nivel_1 = [p for p in pares if p["nivel"] == 1]
        nivel_2 = [p for p in pares if p["nivel"] == 2]
        nivel_3 = [p for p in pares if p["nivel"] == 3]

        print(f"[detectar] Nivel 1 (auto-fusión):  {len(nivel_1)} pares")
        print(f"[detectar] Nivel 2 (revisar):      {len(nivel_2)} pares")
        print(f"[detectar] Nivel 3 (revisar):      {len(nivel_3)} pares")

        # Construir clusters (union-find)
        padre = {c["id"]: c["id"] for c in conceptos}

        def find(x):
            while padre[x] != x:
                padre[x] = padre[padre[x]]
                x = padre[x]
            return x

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                padre[ra] = rb

        # Solo nivel 1 se auto-fusiona por defecto
        for p in nivel_1:
            union(p["c1"], p["c2"])

        # Para nivel 2 y 3, se sugiere pero no se auto-fusiona
        # (el usuario decide con --auto-nivel-2 / --auto-nivel-3)
        if getattr(args, "auto_nivel_2", False):
            for p in nivel_2:
                union(p["c1"], p["c2"])

        if getattr(args, "auto_nivel_3", False):
            for p in nivel_3:
                union(p["c1"], p["c2"])

        # Construir grupos
        grupos_dict = {}
        for c in conceptos:
            raiz = find(c["id"])
            grupos_dict.setdefault(raiz, []).append(c)

        grupos = [g for g in grupos_dict.values() if len(g) > 1]

        print()
        print(f"[detectar] {len(grupos)} grupos a fusionar "
              f"({sum(len(g) for g in grupos)} conceptos)")
        print(f"[detectar] Reducción: {sum(len(g) for g in grupos) - len(grupos)} conceptos")

        # Guardar
        salida = root / f"fusiones-{tema_id}.json"
        with salida.open("w", encoding="utf-8") as f:
            json.dump({
                "tema_id": tema_id,
                "auto_nivel_2": getattr(args, "auto_nivel_2", False),
                "auto_nivel_3": getattr(args, "auto_nivel_3", False),
                "grupos": [
                    {
                        "concepto_principal_sugerido": g[0]["id"],
                        "conceptos": [
                            {
                                "id": c["id"], "nombre": c["nombre"],
                                "tipo": c["tipo"],
                                "longitud_contenido": len((c["valor"] or "") + (c["resumen"] or "")),
                            }
                            for c in g
                        ],
                    }
                    for g in grupos
                ],
                "pares_nivel_2": nivel_2,
                "pares_nivel_3": nivel_3,
            }, f, ensure_ascii=False, indent=2)

        print()
        print(f"💡 Revisa: {salida}")
        print(f"💡 Aplica: db.py aplicar-fusiones --archivo {salida}")

        return 0

    except Exception as e:
        print(f"[error] {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        conn.close()


def cmd_aplicar_fusiones(args) -> int:
    """Aplica las fusiones aprobadas del JSON."""
    import json
    from datetime import date

    root = Path(args.root).expanduser().resolve()
    conn = conectar(root / "oposicion.db")

    try:
        archivo = Path(args.archivo).expanduser().resolve()
        with archivo.open(encoding="utf-8") as f:
            data = json.load(f)

        backup = root / "backups" / f"pre-fusion-{date.today().isoformat()}.db"
        backup.parent.mkdir(exist_ok=True)
        if backup.exists():
            backup.unlink()
        conn.execute(f"VACUUM INTO '{backup}'")
        print(f"[fusionar] Backup: {backup}")

        total_fusionados = 0
        total_vinculos_movidos = 0
        total_preguntas_movidas = 0

        for grupo in data["grupos"]:
            principal = grupo.get("concepto_principal_sugerido") or grupo["conceptos"][0]["id"]
            absorbidos = [c["id"] for c in grupo["conceptos"] if c["id"] != principal]

            if not absorbidos:
                continue

            print(f"[fusionar] Grupo: {principal} <- {len(absorbidos)} absorbidos")

            for cid in absorbidos:
                conn.execute("""
                    INSERT OR IGNORE INTO concepto_temas (concepto_id, tema_id, es_principal)
                    SELECT ?, tema_id, es_principal
                    FROM concepto_temas
                    WHERE concepto_id = ?
                """, (principal, cid))
                conn.execute("DELETE FROM concepto_temas WHERE concepto_id = ?", (cid,))

                conn.execute("""
                    INSERT OR IGNORE INTO concepto_fragmentos (
                        concepto_id, fragmento_id, es_principal, aportacion, fecha_vinculo
                    )
                    SELECT ?, fragmento_id, 0, aportacion, fecha_vinculo
                    FROM concepto_fragmentos
                    WHERE concepto_id = ?
                """, (principal, cid))
                total_vinculos_movidos += conn.execute(
                    "SELECT COUNT(*) FROM concepto_fragmentos WHERE concepto_id = ?",
                    (cid,)
                ).fetchone()[0]
                conn.execute("DELETE FROM concepto_fragmentos WHERE concepto_id = ?", (cid,))

                n_preg = conn.execute(
                    "SELECT COUNT(*) FROM preguntas WHERE concepto_id = ?", (cid,)
                ).fetchone()[0]
                conn.execute(
                    "UPDATE preguntas SET concepto_id = ? WHERE concepto_id = ?",
                    (principal, cid)
                )
                total_preguntas_movidas += n_preg

                conn.execute(
                    "UPDATE flashcards SET concepto_id = ? WHERE concepto_id = ?",
                    (principal, cid)
                )

                conn.execute(
                    "UPDATE srs_items SET concepto_id = ? WHERE concepto_id = ?",
                    (principal, cid)
                )

                conn.execute(
                    "UPDATE conceptos SET fusionado_en = ? WHERE id = ?",
                    (principal, cid)
                )

                total_fusionados += 1

        conn.commit()

        print()
        print("=" * 60)
        print(f"  OK Fusiones aplicadas")
        print("=" * 60)
        print(f"  Conceptos fusionados:    {total_fusionados}")
        print(f"  Vinculos movidos:        {total_vinculos_movidos}")
        print(f"  Preguntas movidas:       {total_preguntas_movidas}")
        print(f"\nRecalcula la completitud con:")
        print(f"   db.py consolidar-tema --tema {data['tema_id']}")

        return 0

    except Exception as e:
        conn.rollback()
        print(f"[error] {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        conn.close()


def cmd_extraer_conceptos_core(args) -> int:
    """Extrae conceptos core desde exámenes oficiales (clasificación).

    Lee el JSON de clasificación de preguntas, filtra por tema, agrupa por
    concepto (por concepto_aproximado o por agrupación LLM previa) y marca
    los conceptos resultantes como es_core = 1 en la BD.

    Input:  /tmp/clasificacion.json (o --input) con clave 'clasificacion'
            o un JSON ya agrupado con clave 'conceptos'.
    Output: conceptos-core-tema-XX.json
    """
    import json
    import re
    import unicodedata
    from datetime import date

    root = Path(args.root).expanduser().resolve()
    conn = conectar(root / "oposicion.db")
    conn.row_factory = sqlite3.Row

    try:
        tema_arg = args.tema
        # Resolver tema_id y número
        if tema_arg.startswith("tema-"):
            tema_id = tema_arg
            cur = conn.execute("SELECT numero FROM temas WHERE id = ?", (tema_id,))
            row = cur.fetchone()
            tema_numero = row["numero"] if row else None
        else:
            tema_numero = int(tema_arg)
            cur = conn.execute("SELECT id FROM temas WHERE numero = ?", (tema_numero,))
            row = cur.fetchone()
            if not row:
                print(f"[error] Tema número {tema_numero} no encontrado")
                return 1
            tema_id = row["id"]

        if not tema_numero:
            # intentar extraer del id
            m = re.search(r"tema-(\d+)", tema_id)
            tema_numero = int(m.group(1)) if m else None

        input_path = Path(args.input).expanduser().resolve() if getattr(args, "input", None) else Path("/tmp/clasificacion.json")
        if not input_path.exists():
            print(f"[error] No existe: {input_path}")
            return 1

        with input_path.open(encoding="utf-8") as f:
            data = json.load(f)

        # Determinar formato de entrada
        if "conceptos" in data:
            # Ya agrupado (por LLM o manual)
            conceptos_grouped = data["conceptos"]
            total_preguntas = data.get("total_preguntas", sum(c.get("n_preguntas", len(c.get("preguntas", []))) for c in conceptos_grouped))
        elif "clasificacion" in data:
            # Filtrar por tema y agrupar por concepto_aproximado
            items = [x for x in data["clasificacion"] if x.get("tema_numero") == tema_numero]
            grupos = {}
            for it in items:
                key = (it.get("concepto_aproximado") or "").strip()
                if not key:
                    continue
                # normalizar para agrupar
                norm = re.sub(r"\s+", " ", key.lower()).strip()
                grupos.setdefault(norm, {"nombre_raw": key, "items": []})
                grupos[norm]["items"].append(it)
            conceptos_grouped = []
            for norm, g in grupos.items():
                preg_ids = [f"{it['examen']}:{it['seccion']}:{it['numero']}" for it in g["items"]]
                conceptos_grouped.append({
                    "nombre": g["nombre_raw"],
                    "descripcion": g["nombre_raw"],
                    "preguntas": preg_ids,
                    "n_preguntas": len(preg_ids),
                })
            total_preguntas = len(items)
        else:
            print("[error] El JSON no tiene clave 'clasificacion' ni 'conceptos'")
            return 1

        # Normalizar nombres de conceptos (title case-ish, keep as-is)
        for c in conceptos_grouped:
            c.setdefault("descripcion", c.get("nombre", ""))
            c.setdefault("preguntas", [])
            c.setdefault("n_preguntas", len(c["preguntas"]))

        # Output JSON
        output_name = getattr(args, "output", None)
        if not output_name:
            output_name = f"conceptos-core-tema-{tema_numero:02d}.json"
        output_path = root / output_name
        out_data = {
            "tema_id": tema_id,
            "tema_numero": tema_numero,
            "conceptos": conceptos_grouped,
            "total_preguntas": total_preguntas,
            "n_conceptos": len(conceptos_grouped),
        }
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(out_data, f, ensure_ascii=False, indent=2)
        print(f"[core] {len(conceptos_grouped)} conceptos core extraídos → {output_path}")

        # DB: crear/marcar conceptos como es_core = 1
        for c in conceptos_grouped:
            nombre = c["nombre"]
            # Buscar concepto existente por nombre (case-insensitive)
            cur = conn.execute(
                "SELECT id FROM conceptos WHERE lower(nombre) = lower(?)", (nombre,)
            )
            row = cur.fetchone()
            if row:
                cid = row["id"]
                conn.execute("UPDATE conceptos SET es_core = 1 WHERE id = ?", (cid,))
                print(f"[core] Marcado es_core: {nombre} ({cid})")
            else:
                # Crear nuevo concepto core
                import uuid
                cid = f"c-{uuid.uuid4().hex[:12]}"
                conn.execute("""
                    INSERT INTO conceptos (id, nombre, tipo, valor, resumen, es_core, verificado, fuentes_count, completitud, ultima_actualizacion)
                    VALUES (?, ?, ?, ?, ?, 1, 0, 0, 0, ?)
                """, (cid, nombre, "core", c.get("descripcion"), c.get("descripcion"), date.today().isoformat()))
                print(f"[core] Creado es_core: {nombre} ({cid})")
            # Vincular al tema
            conn.execute(
                "INSERT OR IGNORE INTO concepto_temas (concepto_id, tema_id, es_principal) VALUES (?, ?, 1)",
                (cid, tema_id)
            )

        conn.commit()
        print(f"[core] {len(conceptos_grouped)} conceptos marcados como core en BD")
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

    # importar-supuesto
    p_imp_sup = sub.add_parser("importar-supuesto",
                               help="Importar un JSON de supuesto práctico a SQLite")
    p_imp_sup.add_argument("--root", default="~/oposicion")
    p_imp_sup.add_argument("--archivo", required=True, help="Ruta al JSON del supuesto")
    p_imp_sup.add_argument("--update", action="store_true",
                           help="Actualizar existente en lugar de saltar")
    p_imp_sup.add_argument("--dry-run", action="store_true")
    p_imp_sup.set_defaults(func=cmd_importar_supuesto)

    # migrar-estructura
    p_migest = sub.add_parser("migrar-estructura",
                              help="Migrar estructura de temas preservando completos")
    p_migest.add_argument("--root", default="~/oposicion")
    p_migest.set_defaults(func=cmd_migrar_estructura)

    # migrar-fuentes
    p_migf = sub.add_parser("migrar-fuentes",
                            help="Crear tablas de fuentes y fragmentos")
    p_migf.add_argument("--root", default="~/oposicion")
    p_migf.set_defaults(func=cmd_migrar_fuentes)

    # ingesta-fuente
    p_ingf = sub.add_parser("ingestar-fuente",
                            help="Ingestar un JSON de fragmentos + conceptos")
    p_ingf.add_argument("--root", default="~/oposicion")
    p_ingf.add_argument("--archivo", required=True)
    p_ingf.add_argument("--tema", help="Tema (si no está en el JSON)")
    p_ingf.add_argument("--force", action="store_true")
    p_ingf.add_argument("--actualizar-resumen", action="store_true",
                        help="Regenerar resumen de conceptos existentes")
    p_ingf.add_argument("--marcar-verificado", action="store_true")
    p_ingf.set_defaults(func=cmd_ingestar_fuente)

    # consolidar-tema
    p_cons = sub.add_parser("consolidar-tema",
                            help="Recalcular completitud de conceptos")
    p_cons.add_argument("--root", default="~/oposicion")
    p_cons.add_argument("--tema", required=True)
    p_cons.add_argument("--exportar-baja", action="store_true")
    p_cons.set_defaults(func=cmd_consolidar_tema)

    # detectar-fusiones
    p_det = sub.add_parser("detectar-fusiones",
                           help="Detectar conceptos candidatos a fusionar")
    p_det.add_argument("--root", default="~/oposicion")
    p_det.add_argument("--tema", required=True)
    p_det.add_argument("--umbral", type=float, default=0.6)
    p_det.add_argument("--auto-nivel-2", action="store_true",
                        help="Auto-fusionar nivel 2 (nombre>=0.80, valor>=0.15)")
    p_det.add_argument("--auto-nivel-3", action="store_true",
                        help="Auto-fusionar nivel 3 (score>=0.70)")
    p_det.set_defaults(func=cmd_detectar_fusiones)

    # aplicar-fusiones
    p_apl = sub.add_parser("aplicar-fusiones",
                           help="Aplicar fusiones aprobadas desde JSON")
    p_apl.add_argument("--root", default="~/oposicion")
    p_apl.add_argument("--archivo", required=True)
    p_apl.set_defaults(func=cmd_aplicar_fusiones)

    # ingestar-fuente-v2
    p_ing2 = sub.add_parser("ingestar-fuente-v2",
                            help="Ingestar fuente (v2: core + candidatos)")
    p_ing2.add_argument("--root", default="~/oposicion")
    p_ing2.add_argument("--tema", required=True)
    p_ing2.add_argument("--archivo", required=True)
    p_ing2.add_argument("--fuente-id", required=True)
    p_ing2.add_argument("--tipo-fuente", required=True)
    p_ing2.add_argument("--url", default=None)
    p_ing2.add_argument("--titulo", default=None)
    p_ing2.add_argument("--marcar-verificado", action="store_true")
    p_ing2.add_argument("--actualizar-resumen", action="store_true")
    p_ing2.add_argument("--force", action="store_true")
    p_ing2.add_argument("--umbral-core", type=float, default=0.6)
    p_ing2.add_argument("--min-fragmentos", type=int, default=2)
    p_ing2.set_defaults(func=cmd_ingestar_fuente_v2)

    # extraer-conceptos-core
    p_core = sub.add_parser("extraer-conceptos-core",
                            help="Extraer conceptos core desde exámenes oficiales")
    p_core.add_argument("--root", default="~/oposicion")
    p_core.add_argument("--tema", required=True,
                        help="Número de tema (26) o id (tema-26-...)")
    p_core.add_argument("--input", default="/tmp/clasificacion.json",
                        help="JSON de clasificación o JSON ya agrupado")
    p_core.add_argument("--output", default=None,
                        help="Nombre del archivo de salida (default: conceptos-core-tema-XX.json)")
    p_core.set_defaults(func=cmd_extraer_conceptos_core)

    args = parser.parse_args()
    return args.func(args)

if __name__ == "__main__":
    sys.exit(main())