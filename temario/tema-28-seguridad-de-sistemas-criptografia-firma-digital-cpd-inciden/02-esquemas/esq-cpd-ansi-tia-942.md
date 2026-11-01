# Esquema: CPD según ANSI/TIA 942

```mermaid
flowchart TD
    CPD[Centro de Procesamiento de Datos] --> TIER[Niveles de disponibilidad]
    TIER --> T1[TIER I: menor disponibilidad]
    TIER --> T2[TIER II]
    TIER --> T3[TIER III: mantenimiento concurrente]
    TIER --> T4[TIER IV: mayor disponibilidad (tolerante a fallos)]
    CPD --> ZONAS[Zonas]
    ZONAS --> EDA[EDA: Equipment Distribution Area<br/>servidores, mainframes]
    CPD --> PLENUM[Plenum: compartimento de conductos de aire<br/>sistema de distribución del aire]
```

## Notas clave
- ANSI/TIA 942 establece **4 niveles TIER**: TIER I (menor) a TIER IV (mayor disponibilidad).
- **EDA (Equipment Distribution Area)**: zona donde se ubican elementos finales (servidor, mainframe).
- **Plenum**: compartimento donde se conectan conductos de aire; parte del sistema de distribución del aire.
