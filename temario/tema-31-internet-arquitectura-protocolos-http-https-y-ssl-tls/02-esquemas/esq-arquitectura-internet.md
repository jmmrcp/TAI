# Esquema: Arquitectura de Internet

```mermaid
flowchart LR
    C[Cliente / Navegador] -->|DNS (UDP 53)| DNS[Servidor DNS]
    C -->|HTTP/HTTPS (TCP 80/443)| ISP[ISP / Red de acceso]
    ISP --> BB[Backbone de Internet]
    BB --> S[Servidor web]
    S --> DB[(Servicios / Datos)]
    C -. TLS handshake .-> S
```

## Notas clave
- **IETF** (Internet Engineering Task Force): organismo creador de estándares de Internet (RFCs: HTTP, TLS, TCP/IP).
- **ICANN/IANA**: gestión de nombres de dominio, direcciones IP y parámetros de protocolo.
- **DNS**: resuelve nombres de dominio a direcciones IP; registro **SOA** describe la zona (serial, refresh, retry, expire, minimum).
- **HTTP/HTTPS**: protocolo de aplicación cliente-servidor; HTTPS añade TLS sobre TCP 443.
- **TLS 1.3** (RFC 8446): última versión estable; handshake en 1-RTT y cifrados modernos.
