# Esquema: Dimensiones y marcos de seguridad del ENS

```mermaid
flowchart LR
  subgraph Dimensiones["Dimensiones de seguridad (Anexo I)"]
    C[Confidencialidad (C)]
    I[Integridad (I)]
    T[Trazabilidad (T)]
    A[Autenticidad (A)]
    D[Disponibilidad (D)]
  end
  subgraph Marcos["Marcos de medidas (Anexo II)"]
    O[Marco organizativo]
    OP[Marco operacional]
    P[Medidas de protección]
  end
  Dimensiones --> N[Nivel de seguridad: BAJO / MEDIO / ALTO]
  Marcos --> N
  N --> R[Responsables: información, servicio, seguridad, sistema (Art. 13.2)]
```
