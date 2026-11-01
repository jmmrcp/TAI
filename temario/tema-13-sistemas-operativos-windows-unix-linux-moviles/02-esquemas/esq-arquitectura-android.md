# Esquema: Arquitectura en capas de Android

```mermaid
flowchart TB
    A[Aplicaciones] --> B[Framework Java API]
    B --> C[Bibliotecas nativas]
    B --> D[Android Runtime ART]
    C --> E[HAL Hardware Abstraction Layer]
    D --> E
    E --> F[Linux Kernel]
    F --> G[Hardware]
    E -. Wi-Fi HALs .-> H[Vendor HAL]
    E -. Wi-Fi HALs .-> I[Supplicant HAL]
    E -. Wi-Fi HALs .-> J[Hostapd HAL]
```

## Notas clave
- Android se basa en el **kernel de Linux**.
- **ART** ejecuta aplicaciones a partir de bytecode `.dex`.
- **HAL** abstrae el hardware; en Wi-Fi (Android 14+) destacan Vendor, Supplicant y Hostapd HAL.
- **Android NDK** permite desarrollar en C/C++ nativo, pero no sustituye al SDK.
- Las versiones de Android se identifican por nombre en clave y nivel API (Pie = Android 9, API 28).
