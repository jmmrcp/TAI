# Esquema: Handshake TLS 1.3 y conexión HTTPS

```mermaid
sequenceDiagram
    participant C as Cliente
    participant S as Servidor
    C->>S: ClientHello (cipher suites, key share)
    S->>C: ServerHello (key share)
    S->>C: EncryptedExtensions
    S->>C: Certificate (clave pública)
    S->>C: CertificateVerify
    S->>C: Finished
    C->>S: Finished
    Note over C,S: Canal seguro establecido (1-RTT)
    C->>S: HTTP Request (GET /)
    S->>C: HTTP Response (200 OK)
```

## Notas clave
- **TLS 1.3** negocia parámetros mediante **ClientHello, ServerHello, HelloRetryRequest** (entre otros); **HelloRequest no existe en TLS 1.3** (era de TLS 1.2).
- El navegador necesita la **clave pública del certificado del sitio** para establecer HTTPS; la clave privada permanece en el servidor.
- Ventaja principal frente a TLS 1.2: handshake en **un solo viaje de ida y vuelta (1-RTT)**, reduciendo latencia.
- Certificados digitales siguen siendo necesarios (no se eliminan en TLS 1.3).
