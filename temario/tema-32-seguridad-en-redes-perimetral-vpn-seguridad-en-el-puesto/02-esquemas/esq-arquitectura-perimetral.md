# Esquema: Arquitectura de seguridad perimetral

```mermaid
flowchart TB
    Internet((Internet)) --> FW[Firewall perimetral]
    FW --> DMZ[DMZ: servidores públicos]
    FW --> Internal[Red interna]
    DMZ -. aislamiento .-> Internal
    Honeypot[Honeypot / señuelo] -. monitorización .-> FW
    Portal[Portal cautivo] --> Internal
    EMMA[EMMA NAC CCN-CERT] -. visibilidad/control .-> Internal
```

## Notas clave
- **DMZ** aísla los servidores que ofrecen servicios al exterior, impidiendo que una intrusión en ellos comprometa la red interna.
- **Firewall** filtra tráfico entre zonas de seguridad (Internet, DMZ, red interna).
- **Honeypot** actúa como señuelo para atraer atacantes y estudiar sus técnicas.
- **Portal cautivo** exige autenticación/aceptación antes de conceder acceso a la red.
- **EMMA** (CCN-CERT) proporciona visibilidad y control sobre la red (NAC).
- **MACsec (IEEE 802.1AE)** protege datos en la capa de enlace Ethernet.
```
