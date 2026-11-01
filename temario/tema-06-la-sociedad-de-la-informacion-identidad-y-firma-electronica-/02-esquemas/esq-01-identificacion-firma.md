# Esquema: Identificación y firma electrónica (DNIe, Cl@ve, eIDAS)

```mermaid
flowchart TD
    U[Usuario] --> DNIe[DNIe v3.0<br/>chip contacto+NFC]
    U --> CLAVE[Cl@ve<br/>PIN / Permanente]
    DNIe --> CERTS[Certificados<br/>autenticación + firma<br/>validez 24 meses]
    CLAVE --> REG[Registro<br/>Básico / Avanzado]
    CERTS --> eIDAS[eIDAS<br/>niveles: bajo / substancial / alto]
    eIDAS --> FE[Firma electrónica<br/>básica / avanzada / cualificada]
    FE --> FORMATOS[Formatos: CAdES, XAdES, PAdES, ASiC]
    FORMATOS --> LTV[LTV: certificados + revocación<br/>validación a largo plazo]
```

## Notas clave
- **DNIe v3.0**: RSA 2048, SHA-256, Triple DES y AES; certificados con validez de 24 meses.
- **Cl@ve**: dos modalidades (PIN y Permanente) y niveles de registro Básico/Avanzado.
- **eIDAS**: tres niveles de aseguramiento (bajo, substancial, alto).
- **Ley 6/2020**: certificados cualificados con vigencia máxima de 5 años; pseudónimo permitido en certificados de firma y autenticación web.
```
