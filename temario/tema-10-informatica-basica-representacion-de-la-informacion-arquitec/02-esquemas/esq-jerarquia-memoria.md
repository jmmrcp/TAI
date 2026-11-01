# Esquema: Jerarquía de memoria

```mermaid
flowchart TB
    R[Registros de CPU] --> L1[(Caché L1)]
    L1 --> L2[(Caché L2)]
    L2 --> L3[(Caché L3)]
    L3 --> RAM[(Memoria principal RAM)]
    RAM --> DISK[(Almacenamiento secundario: SSD/HDD)]
    R -. más rápida / menor capacidad .-> DISK
```

## Notas clave
- **Registros**: más rápidos, dentro de la CPU, capacidad mínima.
- **Caché L1**: integrada en el núcleo, más rápida, menor capacidad.
- **Caché L2/L3**: mayor capacidad, algo más lentas.
- **RAM**: memoria principal volátil.
- **Almacenamiento secundario**: persistente, mayor capacidad, más lento.
- **Placa base**: socket CPU, chipset, BIOS/UEFI, ranuras DIMM, PCIe, puertos E/S, batería CMOS.
