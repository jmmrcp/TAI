# Esquema: Niveles RAID y tolerancia a fallos

```mermaid
flowchart TD
    RAID[RAID] --> R0[RAID 0<br/>Striping<br/>0 fallos, min 2 discos]
    RAID --> R1[RAID 1<br/>Mirroring<br/>1 fallo, min 2 discos]
    RAID --> R5[RAID 5<br/>Paridad distribuida<br/>1 fallo, min 3 discos]
    RAID --> R6[RAID 6<br/>Doble paridad<br/>2 fallos, min 4 discos]
    RAID --> R10[RAID 10<br/>Mirror + Stripe<br/>1 por mirror, min 4 discos]
```

## Notas clave
- **RAID 5**: striping con paridad distribuida; acceso independiente; tolera 1 fallo.
- **RAID 6**: tolera 2 fallos simultaneos gracias a doble paridad.
- **RAID 0**: sin redundancia; mejora rendimiento pero no tolera fallos.
- **RAID 1**: espejo; tolera fallo de un disco (o n-1 en mirror).
- **RAID 10**: combina mirroring y striping; alto rendimiento y redundancia.
