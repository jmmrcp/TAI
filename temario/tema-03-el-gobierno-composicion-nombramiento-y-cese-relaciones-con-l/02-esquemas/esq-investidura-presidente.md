# Esquema: Investidura del Presidente del Gobierno

```mermaid
flowchart TD
    R[Rey consulta grupos parlamentarios] --> P[Propone candidato<br/>(art. 99.1 CE)]
    P --> D[Debate en el Congreso<br/>Programa político]
    D --> V1{Primera votación}
    V1 -->|Mayoría absoluta| OK[Investidura concedida]
    V1 -->|No mayoría absoluta| V2{Segunda votación<br/>48 h después}
    V2 -->|Mayoría simple| OK
    V2 -->|No mayoría simple| S[Sucesivas propuestas]
    S --> PLAZO{¿2 meses desde<br/>primera votación?}
    PLAZO -->|Sí, sin investidura| DIS[Rey disuelve Cortes<br/>y convoca elecciones]
    PLAZO -->|No| P
    OK --> NOM[Rey nombra Presidente<br/>(art. 99.6 CE)]
```

## Notas clave
- Primera votación: **mayoría absoluta** del Congreso (art. 99 CE).
- Segunda votación (48 h después): **mayoría simple**.
- Si transcurridos **dos meses** desde la primera votación no hay investidura, el Rey **disuelve las Cortes** y convoca elecciones.
- Tras la investidura, el Rey **nombra** al candidato Presidente del Gobierno.
- El Presidente del Gobierno es nombrado y cesa conforme a la Constitución (art. 98.2 CE).