# Esquema: Transacciones y niveles de aislamiento

```mermaid
flowchart LR
    T[Transacción] --> A[Atomicidad]
    T --> C[Consistencia]
    T --> I[Aislamiento]
    T --> D[Durabilidad]
    I --> U[READ UNCOMMITTED]
    I --> Cm[READ COMMITTED]
    I --> R[REPEATABLE READ]
    I --> S[SERIALIZABLE]
    U --> A1[Sin protección]
    Cm --> A2[Protege lectura sucia]
    R --> A3[Protege sucia + no repetible]
    S --> A4[Protege todas las anomalías]
```

## Notas clave
- **ACID**: Atomicidad, Consistencia, Aislamiento, Durabilidad.
- **READ UNCOMMITTED**: no protege ninguna anomalía.
- **READ COMMITTED**: protege lectura sucia.
- **REPEATABLE READ**: protege lectura sucia y no repetible, no la fantasma.
- **SERIALIZABLE**: máximo aislamiento, protege todas las anomalías.
