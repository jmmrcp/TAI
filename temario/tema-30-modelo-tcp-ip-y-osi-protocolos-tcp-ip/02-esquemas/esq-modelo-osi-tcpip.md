# Esquema: Modelos OSI y TCP/IP

```mermaid
flowchart TB
    subgraph OSI["Modelo OSI (7 capas)"]
        O7[7 Aplicación]
        O6[6 Presentación]
        O5[5 Sesión]
        O4[4 Transporte]
        O3[3 Red]
        O2[2 Enlace de datos]
        O1[1 Física]
    end
    subgraph TCP["Modelo TCP/IP (4 capas)"]
        T4[Aplicación]
        T3[Transporte]
        T2[Internet]
        T1[Acceso a red]
    end
    O7 --> T4
    O6 --> T4
    O5 --> T4
    O4 --> T3
    O3 --> T2
    O2 --> T1
    O1 --> T1
```

## Notas clave
- **Presentación (capa 6)**: negociación de sintaxis de transferencia y transformaciones de datos (cifrado, compresión).
- **TCP/IP** agrupa las capas 5-7 de OSI en "Aplicación" y las capas 1-2 en "Acceso a red".
- **Transporte**: TCP (fiable, orientado a conexión) y UDP (datagramas, no fiable).
- **Internet**: IP, ICMP, IGMP; direccionamiento lógico y enrutamiento.
