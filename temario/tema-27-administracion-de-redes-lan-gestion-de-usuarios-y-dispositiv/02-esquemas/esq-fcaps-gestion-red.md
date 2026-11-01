# Esquema: FCAPS y gestión de red

```mermaid
flowchart TD
    G[Gestión de red<br/>(modelo OSI)] --> F[Fault<br/>(Fallos)]
    G --> C[Configuration<br/>(Configuración)]
    G --> A[Accounting<br/>(Contabilidad)]
    G --> P[Performance<br/>(Rendimiento)]
    G --> S[Security<br/>(Seguridad)]
    F --> F1[Detección / diagnóstico / corrección]
    C --> C1[Inventario / configuración / cambios]
    A --> A1[Uso de recursos / facturación]
    P --> P1[Monitorización / optimización]
    S --> S1[Control de acceso / políticas]
```

## Notas clave
- **FCAPS**: acrónimo de las cinco áreas funcionales de gestión de redes según ISO/OSI: Fault, Configuration, Accounting, Performance, Security.
- **Gestión de fallos**: detectar, aislar y corregir incidencias para mantener la disponibilidad.
- **Gestión de configuración**: mantener inventario y controlar cambios de dispositivos.
- **Gestión contable**: medir uso de recursos para asignación de costes.
- **Gestión de rendimiento**: monitorizar y optimizar capacidad y respuesta.
- **Gestión de seguridad**: proteger la red mediante políticas y control de acceso.
