# Esquema: Metodologías y gestión de servicios

```mermaid
flowchart LR
    S[Scrum] --> SM[Scrum Master]
    S --> PO[Product Owner]
    S --> DT[Development Team]
    I[ITIL] --> BP[Mejores prácticas de gestión de servicios TI]
    R[RACI] --> Resp[Responsible]
    R --> Acc[Accountable]
    R --> Cons[Consulted]
    R --> Inf[Informed]
    M[Métrica v3] --> PI[Pruebas de integración]
    M --> PR[Pruebas de rendimiento]
    M --> MU[Manuales de usuario (Equipo de Proyecto)]
    Q[SonarQube] --> QG[Quality Gates]
    Q --> ST[Análisis estático del código]
```

## Notas clave
- **Scrum**: roles del Equipo de Scrum según la Guía de Scrum (Scrum Master, Product Owner, Development Team).
- **ITIL**: colección de mejores prácticas de gestión de servicios de TI.
- **RACI**: Responsible, Accountable, Consulted, Informed.
- **Métrica v3**: metodología española; pruebas de integración y rendimiento; elaboración de manuales de usuario por el Equipo de Proyecto.
- **SonarQube**: análisis estático (no dinámico) del código; métricas, duplicación y Quality Gates.
