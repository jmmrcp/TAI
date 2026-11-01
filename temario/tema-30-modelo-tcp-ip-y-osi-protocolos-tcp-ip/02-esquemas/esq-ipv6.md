# Esquema: IPv6 y multicast

```mermaid
flowchart TB
    A[IPv6 128 bits] --> B[Unicast global 2000::/3]
    A --> C[ULA fc00::/7]
    A --> D[Link-local fe80::/10]
    A --> E[Multicast ff00::/8]
    A --> F[Loopback ::1/128]
    E --> G[ff02::1 todos los nodos]
    E --> H[ff02::2 todos los routers]
    A --> I[Hop Limit 8 bits: decrementa por salto, descarta si 0]
```

## Notas clave
- Prefijo multicast IPv6: **ff00::/8** (todo multicast comienza por ff).
- **Hop Limit** (RFC 8200): evita bucles; cada router lo decrementa; paquete descartado al llegar a 0.
- Multicast sustituye broadcast en IPv6.
- Link-local (fe80::/10) para autoconfiguración y descubrimiento de vecinos.
