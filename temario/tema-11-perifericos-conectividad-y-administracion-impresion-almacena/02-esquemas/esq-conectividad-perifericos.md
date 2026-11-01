# Esquema: Conectividad de periféricos

```mermaid
flowchart TD
    PC[Equipo / Host] --> USB[USB\n1.0 1.5Mbps / 2.0 480Mbps / 3.x 5-20Gbps / 4 40Gbps]
    PC --> TB[Thunderbolt 3/4\n40 Gbps]
    PC --> HDMI[HDMI 2.1\n48 Gbps]
    PC --> DP[DisplayPort 2.x\n80 Gbps]
    PC --> VGA[VGA analógico]
    PC --> DVI[DVI digital]
    PC --> SATA[SATA III\n6 Gbps]
    PC --> NVMe[NVMe / PCIe\nSSD alto rendimiento]
    PC --> LIGHT[Lightning\nApple carga+datos]
    USB --> SSDext[SSD externo]
    NVMe --> SSDint[SSD interno M.2/U.2]
    SATA --> HDD[HDD / SSD 2.5]
    HDMI --> MON[Monitor]
    DP --> MON
```

## Notas clave
- **USB4** alcanza 40 Gbps; **Thunderbolt 3/4** también 40 Gbps.
- **HDMI 2.1** ofrece hasta 48 Gbps de ancho de banda.
- **DisplayPort 2.x** hasta 80 Gbps.
- **Lightning** es el conector creado por Apple para carga y datos.
- **IDE/PATA** NO es una interfaz válida para SSD modernos.
- **NVMe** es el protocolo de alto rendimiento para SSD sobre PCIe.
```