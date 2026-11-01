# Esquema: Protocolos VPN por capa y cifrado

```mermaid
flowchart LR
    subgraph L2["VPN nivel de enlace (Capa 2)"]
        PPTP[PPTP<br/>MPPE débil]
        L2TP[L2TP<br/>sin cifrado propio]
    end
    subgraph L3["VPN nivel de red (Capa 3)"]
        IPSec[IPSec<br/>ESP cifrado]
        WG[WireGuard<br/>Noise / kernel Linux]
    end
    subgraph TLS["VPN basadas en TLS"]
        OpenVPN[OpenVPN<br/>TLS/OpenSSL]
    end
    L2TP -. se combina con .-> IPSec
```

## Notas clave
- **IPSec** opera en capa de red (nivel 3) y proporciona cifrado (ESP) y autenticación (IKE).
- **WireGuard** también opera en capa de red y se implementa como interfaz virtual en el kernel de Linux.
- **PPTP** (capa 2) usa MPPE y se considera obsoleto/inseguro.
- **L2TP** (capa 2) no cifra por sí solo; se combina con IPSec.
- **OpenVPN** usa TLS/OpenSSL y puede funcionar sobre UDP o TCP.
- VPN de nivel de enlace: protocolos como PPTP, L2TP, PPP; IPSec no es de nivel de enlace.
```
