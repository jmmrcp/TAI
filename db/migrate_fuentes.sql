-- ============================================================
-- Migración v3: modelo de fuentes + fragmentos
-- Solo afecta a temas técnicos (tipo = 'tecnico')
-- Retrocompatible: el Tema 1 (jurídico) sigue igual
-- ============================================================

BEGIN TRANSACTION;

-- 1. Tabla de fuentes (PDFs, manuales, apuntes)
CREATE TABLE IF NOT EXISTS fuentes (
    id TEXT PRIMARY KEY,              -- "fuente-2024-mad-bd"
    titulo TEXT NOT NULL,             -- "Manual MAD — Bases de datos 2024"
    tipo TEXT NOT NULL,               -- "boe" | "manual" | "apuntes" | "transcripcion"
    editor TEXT,                      -- "MAD", "Adams", "BOE", "Academia X"
    version TEXT,                     -- "3ª ed.", "consolidado 2025-10"
    fecha TEXT,                       -- ISO date
    archivo_path TEXT,                -- ruta relativa al proyecto
    hash_archivo TEXT UNIQUE,         -- SHA-256 del PDF
    paginas INTEGER,
    estado TEXT NOT NULL DEFAULT 'pendiente',
        -- pendiente | ingestado | verificado | obsoleto
    fecha_ingesta TEXT,
    notas TEXT
);

CREATE INDEX IF NOT EXISTS idx_fuentes_tipo ON fuentes(tipo);
CREATE INDEX IF NOT EXISTS idx_fuentes_estado ON fuentes(estado);

-- 2. Tabla de fragmentos (unidades atómicas deduplicables)
CREATE TABLE IF NOT EXISTS fragmentos (
    id TEXT PRIMARY KEY,              -- "frag-fuente-2024-mad-bd-p12-s2"
    fuente_id TEXT NOT NULL REFERENCES fuentes(id),
    tema_id TEXT REFERENCES temas(id),
    numero_pagina INTEGER,
    numero_seccion TEXT,              -- "2.1.2", "Cap. III"
    titulo_seccion TEXT,
    texto TEXT NOT NULL,              -- contenido literal del fragmento
    hash_normalizado TEXT UNIQUE,     -- SHA-256 del texto normalizado
    idioma TEXT DEFAULT 'es',
    estado TEXT NOT NULL DEFAULT 'activo',
        -- activo | obsoleto
    fecha_ingesta TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_frag_fuente ON fragmentos(fuente_id);
CREATE INDEX IF NOT EXISTS idx_frag_tema ON fragmentos(tema_id);
CREATE INDEX IF NOT EXISTS idx_frag_hash ON fragmentos(hash_normalizado);
CREATE INDEX IF NOT EXISTS idx_frag_estado ON fragmentos(estado);

-- 3. Ampliar conceptos (solo campos nuevos, nullable)
-- SQLite no tiene "ADD COLUMN IF NOT EXISTS", así que usamos
-- una comprobación previa desde Python antes de aplicar este ALTER.
-- Se hacen en el script Python (ver paso 2).

-- 4. Tabla de relación concepto ↔ fragmentos (N:M)
--    Permite saber de qué fragmentos se sintetizó el resumen.
CREATE TABLE IF NOT EXISTS concepto_fragmentos (
    concepto_id TEXT NOT NULL REFERENCES conceptos(id),
    fragmento_id TEXT NOT NULL REFERENCES fragmentos(id),
    es_principal BOOLEAN DEFAULT 0,
    aportacion TEXT,                  -- "definicion" | "ejemplo" | "ampliacion" | "correccion"
    fecha_vinculo TEXT NOT NULL,
    PRIMARY KEY (concepto_id, fragmento_id)
);

CREATE INDEX IF NOT EXISTS idx_cf_concepto ON concepto_fragmentos(concepto_id);
CREATE INDEX IF NOT EXISTS idx_cf_fragmento ON concepto_fragmentos(fragmento_id);
CREATE INDEX IF NOT EXISTS idx_cf_principal ON concepto_fragmentos(es_principal);

-- 5. Vista de cobertura de fuentes por tema
CREATE VIEW IF NOT EXISTS v_cobertura_fuentes AS
SELECT
    f.tema_id,
    COUNT(DISTINCT f.fuente_id) AS n_fuentes,
    COUNT(*) AS n_fragmentos,
    SUM(CASE WHEN f.estado = 'activo' THEN 1 ELSE 0 END) AS n_activos,
    SUM(CASE WHEN f.estado = 'obsoleto' THEN 1 ELSE 0 END) AS n_obsoletos,
    MIN(f.fecha_ingesta) AS primera_ingesta,
    MAX(f.fecha_ingesta) AS ultima_ingesta
FROM fragmentos f
WHERE f.tema_id IS NOT NULL
GROUP BY f.tema_id;

COMMIT;

-- ============================================================
-- Tabla de conceptos candidatos (granularidad fina)
-- ============================================================
CREATE TABLE IF NOT EXISTS conceptos_candidatos (
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

CREATE INDEX IF NOT EXISTS idx_cand_tema ON conceptos_candidatos(tema_id);
CREATE INDEX IF NOT EXISTS idx_cand_estado ON conceptos_candidatos(estado);
CREATE INDEX IF NOT EXISTS idx_cand_n_frag ON conceptos_candidatos(n_fragmentos);
