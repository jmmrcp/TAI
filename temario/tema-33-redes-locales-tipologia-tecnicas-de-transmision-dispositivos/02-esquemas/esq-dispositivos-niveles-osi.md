# Esquema: Dispositivos de interconexión por nivel OSI

```mermaid
flowchart TB
    L1[Nivel 1 - Físico] --> H[Hub / Repetidor / Media converter]
    L2[Nivel 2 - Enlace] --> S[Switch / Bridge]
    L3[Nivel 3 - Red] --> R[Router]
    L7[Nivel 7 - Aplicación] --> G[Gateway]
    H -->|repite señal| S
    S -->|filtra por MAC| R
    R -->|encamina por IP / tablas de encaminamiento| G
    G -->|traduce protocolos| NET[Redes heterogéneas]
```

## Notas clave
- **Hub**: nivel 1, repite la señal a todos los puertos; dominio de colisión compartido.
- **Switch/Bridge**: nivel 2, filtran/conmutan por dirección MAC.
- **Router**: nivel 3, utiliza tablas de encaminamiento para interconectar redes.
- **Gateway**: traduce protocolos entre redes distintas (ej. coaxial a Ethernet).
- **Repetidor/Media converter**: nivel 1, regeneran señal o convierten medios.
