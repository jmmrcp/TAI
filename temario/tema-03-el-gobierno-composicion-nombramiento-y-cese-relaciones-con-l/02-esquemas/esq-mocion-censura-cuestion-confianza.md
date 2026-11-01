# Esquema: Moción de censura y cuestión de confianza

```mermaid
flowchart TD
    A[Relaciones Gobierno-Cortes] --> MC[Moción de censura<br/>(art. 113 CE)]
    A --> CC[Cuestión de confianza<br/>(art. 112 CE)]
    A --> DIS[Disolución de Cortes<br/>(art. 115 CE)]
    MC --> P1[Propuesta: ≥ 1/10 diputados<br/>con candidato a Presidente]
    P1 --> DEB[Debate tras 5 días]
    DEB --> VOT{Votación}
    VOT -->|Mayoría absoluta| EF1[Gobierno dimite;<br/>Rey nombra candidato]
    VOT -->|No aprobada| EF2[No se puede presentar<br/>otra en el mismo período]
    CC --> P2[Presidente plantea<br/>(previa deliberación CM)]
    P2 --> VOT2{Votación}
    VOT2 -->|Mayoría simple| OK2[Confianza otorgada]
    VOT2 -->|No obtenida| DIM[Gobierno dimite]
    DIS --> P3[Presidente propone<br/>(previa deliberación CM)]
    P3 --> REY[Rey disuelve]
```

## Notas clave
- **Moción de censura**: propuesta por al menos una décima parte de los diputados e incluye candidato a la Presidencia; votación por mayoría absoluta tras 5 días (art. 113 CE).
- **Cuestión de confianza**: la plantea el Presidente del Gobierno; se otorga por mayoría simple (art. 112 CE).
- Si no se obtiene la confianza o se aprueba la moción, el **Gobierno dimite**.
- La **disolución** de las Cortes la propone el Presidente previa deliberación del Consejo de Ministros (art. 2.2.c Ley 50/1997; art. 115 CE).
- El Gobierno responde **solidariamente** ante el Congreso (art. 108 CE).