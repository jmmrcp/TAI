# Esquema: DNIe: validez y zona de seguridad

```mermaid
flowchart LR
    A[Edad del titular] --> B{< 5 años?}
    B -- Sí --> C[Validez 2 años]
    B -- No --> D{5-30 años?}
    D -- Sí --> E[Validez 5 años]
    D -- No --> F{30-70 años?}
    F -- Sí --> G[Validez 10 años]
    F -- No --> H[Validez > 10 años<br/>fecha consignada]
    I[DNIe] --> J[Zona de seguridad<br/>lectura ciudadano]
    J --> K[Datos de filiación]
    J --> L[Fotografía]
    J --> M[Firma manuscrita]
```

## Notas clave
- **Validez DNI**: <5 años → 2; 5-30 → 5; 30-70 → 10; >70 → más de 10 (fecha consignada).
- **Certificados DNIe v3.0**: validez de 24 meses.
- **Legislación**: certificados electrónicos reconocidos del DNI no superarán 4 años (RD 1553/2005 mod. RD 414/2015).
```
