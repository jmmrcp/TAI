# Esquema: Estrategia de backup y snapshots

```mermaid
flowchart TD
    B[Backup completo] --> D[Backup diferencial<br/>cambios desde full]
    B --> I[Backup incremental<br/>cambios desde ultimo backup]
    SNAP[Snapshot<br/>imagen instantanea] -. no es backup independiente .-> B
    R[Regla 3-2-1] --> R3[3 copias]
    R --> R2[2 soportes distintos]
    R --> R1[1 copia offsite]
```

## Notas clave
- **Completo**: copia de todos los datos; base de referencia.
- **Diferencial**: cambios desde el ultimo backup completo.
- **Incremental**: cambios desde el ultimo backup (completo o incremental).
- **Snapshot**: imagen puntual (copy-on-write); depende del volumen original; no sustituye al backup.
- **Regla 3-2-1**: 3 copias, en 2 soportes distintos, 1 copia fuera de sitio (offsite).
