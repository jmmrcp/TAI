# Esquema: Administración de impresión (IPP)

```mermaid
flowchart LR
    C[Cliente] -->|IPP/HTTP :631| S[Servidor de impresión\n(CUPS / Spooler)]
    S --> Q[(Cola de impresión)]
    Q --> D[Driver / Controlador]
    D --> P[Impresora]
    P -->|Estado/feedback| S
    S -->|IPP gestión remota| C
```

## Notas clave
- **IPP** (Internet Printing Protocol): protocolo estándar basado en HTTP para imprimir y gestionar trabajos vía red.
- **Spooler**: servicio que almacena temporalmente los trabajos y los envía a la impresora.
- **Cola de impresión**: lista de trabajos pendientes (FIFO/prioridades).
- **Driver/Controlador de dispositivo**: software que permite al SO comunicarse con la impresora.
- **CUPS** es el sistema de impresión estándar en Linux/Unix (usa IPP).
- Lenguajes de página: **PCL** (HP) y **PostScript** (Adobe).
```