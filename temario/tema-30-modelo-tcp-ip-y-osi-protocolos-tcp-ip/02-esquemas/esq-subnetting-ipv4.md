# Esquema: Subnetting IPv4

```mermaid
flowchart LR
    A[Red base / Prefijo] --> B[Bits necesarios para N subredes: 2^k >= N]
    B --> C[Nuevo prefijo = prefijo base + k]
    C --> D[Máscara de subred resultante]
    D --> E[Hosts por subred = 2^h - 2]
    E --> F[Red y broadcast no asignables]
```

## Notas clave
- Ejemplo: 10.0.0.0/8 con 600 subredes → k=10 (2^10=1024≥600) → /18 → máscara 255.255.192.0.
- Hosts por subred con /18: 2^14 - 2 = 16382.
- Dirección de red (host todo 0) y broadcast (host todo 1) no asignables a hosts.
- Clase A: 1-126, /8; Clase B: 128-191, /16; Clase C: 192-223, /24.
