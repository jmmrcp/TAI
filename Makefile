# ============================================================
# Makefile — Atajos para el sistema TAI Oposición
# ============================================================
# Uso: make <comando>
# ============================================================

ROOT := /root/.dsh/oposicion
PY := python3
DB := $(ROOT)/oposicion.db
EXPORT_DIR := $(ROOT)/export
TESTS_DIR := $(ROOT)/tests

# ============================================================
# Ayuda
# ============================================================

.PHONY: help
help:
	@echo "════════════════════════════════════════════════════════"
	@echo "  SISTEMA TAI OPOSICIÓN — Comandos disponibles"
	@echo "════════════════════════════════════════════════════════"
	@echo ""
	@echo "  📦 SETUP"
	@echo "    make init           Crear la BD (bloques + 33 temas vacíos)"
	@echo "    make check          Verificar el estado del sistema"
	@echo ""
	@echo "  📚 CONTENIDO"
	@echo "    make migrar         Importar todos los temas (JSON → SQLite)"
	@echo "    make migrar-tema T=  Importar un tema concreto"
	@echo "    make exportar       Exportar todo a JSON (backup git)"
	@echo "    make backup         Exportar + commit git automático"
	@echo ""
	@echo "  📖 ESTUDIO DIARIO"
	@echo "    make reconciliar    Sincronizar SRS con el contenido"
	@echo "    make hoy            Ver qué toca repasar hoy"
	@echo "    make hoy-tema T=    Ver qué toca de un tema"
	@echo "    make estado T=      Estado de un tema"
	@echo "    make bloque B=      Estado de un bloque"
	@echo ""
	@echo "  📝 PRÁCTICA"
	@echo "    make simulacro      Simulacro global (80 preguntas)"
	@echo "    make test-bloque B= Test de un bloque"
	@echo "    make test-tema T=   Test de un tema"
	@echo "    make problematicos  Ver ítems leech"
	@echo ""
	@echo "  🔧 UTILIDADES"
	@echo "    make stats          Estadísticas globales"
	@echo "    make pendientes     Preguntas pendientes de verificar"
	@echo "    make conceptos-shared  Conceptos compartidos entre temas"
	@echo "    make limpiar-tests  Borrar tests antiguos"
	@echo ""
	@echo "════════════════════════════════════════════════════════"
	@echo "  Variables: T=tema, B=bloque (ej. make estado T=tema-01)"
	@echo "════════════════════════════════════════════════════════"

# ============================================================
# SETUP
# ============================================================

.PHONY: init
init:
	@echo "📦 Creando base de datos..."
	$(PY) $(ROOT)/bin/db.py init --root $(ROOT)

.PHONY: init-force
init-force:
	@echo "⚠️  Forzando recreación de la BD (se perderán datos)..."
	@read -p "¿Estás seguro? [y/N] " resp; \
	if [ "$$resp" = "y" ]; then \
		$(PY) $(ROOT)/bin/db.py init --root $(ROOT) --force; \
	else \
		echo "Cancelado"; \
	fi

.PHONY: check
check:
	@echo "🔍 Estado del sistema:"
	@echo ""
	@echo "  BD:"
	@if [ -f "$(DB)" ]; then \
		echo "    ✅ oposicion.db ($(shell du -h $(DB) 2>/dev/null | cut -f1))"; \
		$(PY) -c "import sqlite3; c=sqlite3.connect('$(DB)'); print('    bloques:', c.execute('SELECT COUNT(*) FROM bloques').fetchone()[0]); print('    temas:', c.execute('SELECT COUNT(*) FROM temas').fetchone()[0]); print('    conceptos:', c.execute('SELECT COUNT(*) FROM conceptos').fetchone()[0]); print('    preguntas:', c.execute('SELECT COUNT(*) FROM preguntas').fetchone()[0])"; \
	else \
		echo "    ❌ No existe. Ejecuta: make init"; \
	fi

.PHONY: migrar
migrar:
	@echo "📚 Migrando todos los temas..."
	$(PY) $(ROOT)/bin/db.py migrar --root $(ROOT)

.PHONY: migrar-dry
migrar-dry:
	@echo "🔍 Simulando migración (sin escribir)..."
	$(PY) $(ROOT)/bin/db.py migrar --root $(ROOT) --dry-run

.PHONY: migrar-tema
migrar-tema:
	@if [ -z "$(T)" ]; then echo "❌ Falta T=<tema_id>"; exit 1; fi
	$(PY) $(ROOT)/bin/db.py migrar --root $(ROOT) --tema $(T)

.PHONY: exportar
exportar:
	@echo "💾 Exportando a JSON..."
	$(PY) $(ROOT)/bin/db.py exportar --root $(ROOT) \
		--output $(EXPORT_DIR) --srs --supuestos --examenes

.PHONY: backup
backup: exportar
	@echo ""
	@echo "📦 Haciendo backup en git..."
	@cd $(ROOT) && \
		git add export/ 2>/dev/null && \
		git commit -m "backup: $(shell date +%Y-%m-%d)" 2>/dev/null && \
		echo "    ✅ Commit creado" || \
		echo "    ⚠️  Sin cambios para commitear o git no configurado"

.PHONY: reconciliar
reconciliar:
	@echo "🔄 Reconciliando SRS con contenido..."
	$(PY) $(ROOT)/bin/srs.py reconciliar --root $(ROOT) --verbose

.PHONY: hoy
hoy:
	@$(PY) $(ROOT)/bin/srs.py hoy --root $(ROOT)

.PHONY: estado
estado:
	@if [ -z "$(T)" ]; then echo "❌ Falta T=<tema_id>"; exit 1; fi
	$(PY) $(ROOT)/bin/srs.py estado $(T) --root $(ROOT)

.PHONY: bloque
bloque:
	@if [ -z "$(B)" ]; then echo "❌ Falta B=<bloque_id>"; exit 1; fi
	$(PY) $(ROOT)/bin/srs.py bloque $(B) --root $(ROOT)

.PHONY: simulacro
simulacro:
	@echo "📝 Generando simulacro global (80 preguntas)..."
	$(PY) $(ROOT)/bin/generar_simulacro.py --root $(ROOT) \
		--tipo global --output $(TESTS_DIR)

.PHONY: test-bloque
test-bloque:
	@if [ -z "$(B)" ]; then echo "❌ Falta B=<bloque_id>"; exit 1; fi
	$(PY) $(ROOT)/bin/generar_simulacro.py --root $(ROOT) \
		--tipo bloque --scope $(B) --n 25 --output $(TESTS_DIR)

.PHONY: test-tema
test-tema:
	@if [ -z "$(T)" ]; then echo "❌ Falta T=<tema_id>"; exit 1; fi
	$(PY) $(ROOT)/bin/generar_simulacro.py --root $(ROOT) \
		--tipo tema --scope $(T) --n 15 --output $(TESTS_DIR)

.PHONY: problematicos
problematicos:
	@$(PY) $(ROOT)/bin/srs.py problematicos --root $(ROOT)

.PHONY: stats
stats:
	@echo "📊 Estadísticas globales"
	@$(PY) -c "import sqlite3; c=sqlite3.connect('$(DB)'); \
print('  preguntas:', c.execute('SELECT COUNT(*) FROM preguntas').fetchone()[0]); \
print('  conceptos:', c.execute('SELECT COUNT(*) FROM conceptos').fetchone()[0]); \
print('  flashcards:', c.execute('SELECT COUNT(*) FROM flashcards').fetchone()[0])"

.PHONY: pendientes
pendientes:
	@$(PY) -c "import sqlite3; c=sqlite3.connect('$(DB)'); print(c.execute('SELECT COUNT(*) FROM preguntas WHERE verificado=0').fetchone()[0], 'preguntas sin verificar')"

.PHONY: temas
temas:
	@$(PY) -c "import sqlite3; c=sqlite3.connect('$(DB)'); [print(r[0], r[1], r[2]) for r in c.execute('SELECT numero,titulo,estado_ingesta FROM temas WHERE estado_ingesta!=\"pendiente\" ORDER BY numero')]"

.PHONY: temas-pendientes
temas-pendientes:
	@$(PY) -c "import sqlite3; c=sqlite3.connect('$(DB)'); [print(r[0], r[1]) for r in c.execute('SELECT numero,titulo FROM temas WHERE estado_ingesta=\"pendiente\" ORDER BY numero')]"

.PHONY: exportar-tema
exportar-tema:
	@if [ -z "$(T)" ]; then echo "❌ Falta T=<tema_id>"; exit 1; fi
	$(PY) $(ROOT)/bin/db.py exportar --root $(ROOT) \
		--tema $(T) --output $(EXPORT_DIR) --srs

.PHONY: d
d: hoy

.PHONY: e
e: estado

.PHONY: b
b: backup

.PHONY: s
s: simulacro
