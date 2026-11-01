# Esquema: Flujo de correo electrónico (SMTP / POP3 / IMAP)

```mermaid
flowchart LR
    U1[Cliente de correo<br/>origen] -->|SMTP :25/:587| MTA1[Servidor SMTP<br/>saliente (MTA)]
    MTA1 -->|SMTP :25| MTA2[Servidor SMTP<br/>destino (MTA/MDA)]
    MTA2 --> MB[(Buzón del<br/>destinatario)]
    MB -->|POP3 :110/:995| U2[Cliente de correo<br/>destino]
    MB -->|IMAP :143/:993| U2
    U2 -. sincronización .-> MB
```

## Notas clave
- **SMTP** (Simple Mail Transfer Protocol): envío y retransmisión entre servidores (puerto 25 estándar, 465/587 con TLS).
- **POP3**: descarga al cliente; típicamente borra del servidor (puerto 110 / 995 TLS).
- **IMAP**: acceso y sincronización en servidor; ideal multi-dispositivo (puerto 143 / 993 TLS).
- **Exchange ActiveSync**: sincronización de correo/contactos/calendario en móviles vía HTTPS (443).
