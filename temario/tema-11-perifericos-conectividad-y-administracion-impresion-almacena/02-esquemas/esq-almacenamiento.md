# Esquema: Almacenamiento (HDD vs SSD)

```mermaid
flowchart LR
    A[Almacenamiento] --> HDD[Disco duro HDD\nmagnético, platos giratorios]
    A --> SSD[SSD\nmemoria flash NAND, sin partes móviles]
    HDD --> H1[Latencia rotacional\n60000/(2*RPM) ms]
    HDD --> H2[Interfaces: SATA, SAS]
    SSD --> S1[Interfaces: SATA, NVMe/PCIe, USB, TB]
    SSD --> S2[Formatos: 2.5\", M.2, mSATA, U.2, EDSFF]
    SSD --> S3[Mayor velocidad, menor consumo,\nsilencioso, resistente]
```

## Notas clave
- **SSD** (Solid State Drive): unidad de estado sólido basada en memoria flash, sin partes móviles.
- **Latencia rotacional** (HDD): tiempo medio de espera por rotación = 60000/(2·RPM) ms (≈4,17 ms a 7200 RPM).
- **SATA** es la tecnología de almacenamiento en disco mediante bus serie (Serial ATA).
- **NVMe** sobre PCIe ofrece el mayor rendimiento en SSD modernos.
- **M.2** es factor de forma, no protocolo (puede ser SATA o NVMe).
```