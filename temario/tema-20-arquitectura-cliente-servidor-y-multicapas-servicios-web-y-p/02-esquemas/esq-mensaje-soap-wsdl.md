# Esquema: Mensaje SOAP y operaciones WSDL

```mermaid
flowchart TB
    E[Envelope] --> H[Header opcional]
    E --> B[Body]
    B --> P[Petición/Respuesta]
    B --> F[Fault opcional]
    W[WSDL 2.0] --> O1[One-way]
    W --> O2[Request-Response]
    W --> O3[Solicit-Response]
    W --> O4[Notification]
```

## Notas clave
- **Envelope**: elemento raíz obligatorio del mensaje SOAP.
- **Header**: metadatos opcionales (seguridad, transacciones).
- **Body**: carga útil obligatoria.
- **Fault**: error dentro del Body.
- **WSDL 2.0**: lenguaje XML para describir servicios web a partir de un modelo abstracto.
- **SOAP última versión**: 1.2.
