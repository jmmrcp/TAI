# Esquema: Arquitectura SNMP (gestor, agente, MIB)

```mermaid
flowchart LR
    M[Gestor SNMP<br/>(NMS)] -->|GET / GETNEXT / GETBULK| A[Agente SNMP<br/>(dispositivo)]
    M -->|SET| A
    A -->|RESPONSE| M
    A -.->|TRAP / INFORM<br/>(no solicitado)| M
    A --> MIB[(MIB<br/>base de información)]
    M --> MIB
```

## Notas clave
- **SNMP** (Simple Network Management Protocol): protocolo estándar para administrar dispositivos de red.
- **Gestor (NMS)**: estación de administración que consulta y configura agentes.
- **Agente**: proceso en el dispositivo gestionado que mantiene la MIB.
- **MIB** (Management Information Base): base de datos jerárquica de variables (OIDs) del dispositivo.
- **TRAP**: notificación no solicitada por el gestor ante eventos inesperados (sin confirmación).
- **INFORM**: notificación con acuse de recibo.
- **GETBULK**: comando para recuperar datos voluminosos de una tabla MIB grande.
- **Versiones**: v1 y v2c usan community string; **v3** es la última y añade seguridad (USM/VACM, autenticación y cifrado).
