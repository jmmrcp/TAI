# Esquema: Redes inalámbricas y estándares

```mermaid
flowchart LR
    W[Redes inalámbricas] --> WIFI[Wi-Fi IEEE 802.11]
    W --> BT[Bluetooth IEEE 802.15.1]
    WIFI --> WIFI6[Wi-Fi 6 = 802.11ax]
    WIFI --> SEC[Seguridad: WEP < WPA2; WPA3 tras KRACK]
    WIFI --> BAND[Bandas: 2.4 GHz / 5 GHz]
    WIFI --> WPS[WPS: PIN, PBC, NFC, USB]
    BT --> PICO[Piconet: 1 maestro + hasta 7 esclavos]
    BT --> SCAT[Scatternet: grupo de piconets]
    BT --> BLE[BLE Extended Advertising: 40 canales]
```

## Notas clave
- **Wi-Fi 6** se corresponde con **IEEE 802.11ax**.
- **WEP** es inferior a **WPA2**; **WPA3** mejora WPA2-PSK (AES) tras el ataque KRACK.
- **2,4 GHz** tiene mayor alcance e interferencias (Bluetooth); **5 GHz** menor alcance.
- **WPS** admite PIN, PBC, NFC y USB.
- **Bluetooth**: piconet y scatternet; BLE Extended Advertising usa 40 canales.
- **SOHO**: Small Office, Home Office.
