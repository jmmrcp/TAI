# Esquema: Prescripción de sanciones LOPDGDD

```mermaid
flowchart LR
    S[Sanción impuesta] --> A{Importe de la sanción}
    A -->|Igual o inferior a 40.000 €| P1[Prescribe en 1 año]
    A -->|De 40.001 a 300.000 €| P2[Prescribe en 2 años]
    A -->|Superior a 300.000 €| P3[Prescribe en 3 años]
    P1 --> I[Inicio: día siguiente a que sea ejecutable la resolución o transcurra el plazo para recurrirla]
    P2 --> I
    P3 --> I
```

## Notas clave
- **Art. 78 LOPDGDD**: la prescripción de las sanciones se determina por el importe de la sanción impuesta.
- **Art. 75 LOPDGDD**: la iniciación del procedimiento sancionador con conocimiento del interesado interrumpe la prescripción.
- Las infracciones prescriben por separado según su gravedad (muy graves 3 años, graves 2 años, leves 1 año) conforme al régimen general de la Ley 40/2015.
```