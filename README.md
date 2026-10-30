# 🎓 Sistema TAI Oposición

Sistema personal de preparación de la oposición **TAI (Técnicos Auxiliares de Informática)**. Cubre el ciclo completo: ingesta de temario, consolidación con transcripciones de clase, generación de artefactos de estudio, repaso espaciado, simulacros y supuestos prácticos.

Todo corre **localmente** (privacidad total, coste cero). Base operativa en SQLite. Los JSON son solo para intercambio y backup versionado en git.

---

## 📋 Índice

- [Instalación](#-instalación)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Uso diario](#-uso-diario)
- [Comandos por fase](#-comandos-por-fase)
- [Estructura del temario](#-estructura-del-temario)
- [Flujo completo](#-flujo-completo)
- [Troubleshooting](#-troubleshooting)

---

## 🚀 Instalación

### 1. Requisitos

- **Linux** (probado en Ubuntu/Debian)
- **Python 3.10+** (conda recomendado)
- **SQLite 3** (`sqlite3 --version`)
- **git** (para versionado)
- **GPU Nvidia + CUDA 12.x** (opcional, para transcripción local)

### 2. Dependencias Python

```bash
conda activate base
pip install faster-whisper "av<19" yt-dlp
```

> ⚠️ **Importante**: `av<19` es obligatorio. La versión 19 de PyAV rompe `faster-whisper` con el error `metadata_errors`.

### 3. Estructura base

```bash
mkdir -p ~/oposicion/{bin,temario,supuestos,examenes,tests,export}
cd ~/oposicion
```

### 4. Copiar los scripts

Coloca en `~/oposicion/bin/`:

- `db.py` — Gestor de la base de datos
- `srs.py` — Curva del olvido
- `generar_simulacro.py` — Tests de práctica
- `ingesta_examen.py` — Importar exámenes oficiales
- `transcribir.py` — Utilidad de transcripción (opcional)

Y en `~/oposicion/`:

- `Makefile`
- `.gitignore`
- `README.md` (este archivo)

### 5. Permisos

```bash
chmod +x ~/oposicion/bin/*.py
```

### 6. Inicializar la base de datos

```bash
make init
```

### 7. Verificar el sistema

```bash
make check
```

---

## 📁 Estructura del proyecto

```text
~/oposicion/
├── README.md
├── Makefile
├── .gitignore
├── oposicion.db                 ← SQLite operativo (gitignored)
├── bin/
├── temario/
├── supuestos/
├── examenes/
├── tests/
└── export/
```

---

## 📖 Uso diario

### Rutina matutina

```bash
make hoy
make reconciliar
```

### Rutina semanal

```bash
make backup
make simulacro
make problematicos
```

---

## 📚 Comandos por fase

### Fase 0 — Ingesta de un tema

```bash
make migrar-tema T="tema-01-la-constitucion-espanola-de-1978"
make estado T="tema-01-la-constitucion-espanola-de-1978"
make reconciliar
```

### Fase 5 — Simulacros

```bash
make simulacro
make test-bloque B="bloque-iii"
make test-tema T="tema-15-modelado-de-datos"
```

---

## 🗂️ Estructura del temario

El temario TAI consta de **4 bloques** y **33 temas**:

| Bloque | Nombre | Temas |
|---|---|---|
| I | Organización del Estado y Administración electrónica | 1-8 |
| II | Administración Pública | 9-14 |
| III | Informática básica | 15-24 |
| IV | Sistemas y comunicaciones | 25-33 |

---

## 🔄 Flujo completo

```text
SETUP (una vez) → make init
POR TEMA        → ingesta + migrar-tema + reconciliar
DIARIO          → make hoy / responder
SEMANAL         → make simulacro / backup
```

---

## 🔧 Troubleshooting

### `sqlite3: command not found`

Este entorno no incluye el CLI de sqlite3; los targets del Makefile usan Python (`sqlite3` module) en su lugar.

### `Tema no encontrado en la BD`

Ejecuta `make init` primero.

---

## 🎯 Principios del sistema

1. Nunca inventar artículos, plazos, cifras o siglas.
2. La verificación final es humana.
3. Si BOE y manual discrepan, prevalece BOE.
4. SQLite operativo, JSON para git.
5. El SRS nunca modifica el contenido.

---

**¡Mucho ánimo con la oposición!** 🎓
