# Esquema: Virtualizacion de sistemas y almacenamiento

```mermaid
flowchart LR
    HW[Hardware fisico] --> HV1[Hipervisor Tipo 1<br/>bare-metal<br/>ESXi, Xen, Hyper-V, KVM]
    OS[SO anfitrion] --> HV2[Hipervisor Tipo 2<br/>hosted<br/>VirtualBox, Workstation]
    HV1 --> VM[Maquinas virtuales]
    HV2 --> VM
    VM --> VDI[VDI<br/>Escritorios centralizados]
    VM --> TP[Thin Provisioning<br/>Asignacion virtual]
    ST[Almacenamiento] --> SAN[SAN<br/>bloque: FC, iSCSI]
    ST --> NAS[NAS<br/>archivo: SMB, NFS]
```

## Notas clave
- **Hipervisor tipo 1**: se ejecuta directamente sobre el hardware; mayor rendimiento; usado en servidores.
- **Hipervisor tipo 2**: se ejecuta sobre un SO anfitrion; orientado a escritorio/pruebas.
- **VDI**: centraliza escritorios en el datacenter; acceso remoto mediante thin clients.
- **Thin provisioning**: sobreasigna espacio virtual; reserva bloques fisicos al escribir.
- **SAN**: acceso a nivel de bloque; alto rendimiento; NAS: acceso a nivel de archivo compartido en LAN.
