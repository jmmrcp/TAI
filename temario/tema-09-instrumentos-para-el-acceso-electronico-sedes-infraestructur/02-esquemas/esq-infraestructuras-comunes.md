# Esquema: Infraestructuras y servicios comunes del sector público

```mermaid
flowchart TD
    A[Administración electrónica] --> B[Infraestructuras comunes]
    A --> C[Servicios comunes]
    B --> D[DIR3<br/>Inventario de unidades orgánicas]
    B --> E[Port@firmas AGE<br/>Firma CAdES/XAdES/PAdES]
    B --> F[eVisor<br/>Copia auténtica en papel]
    B --> G[Nodo eIDAS<br/>SAML 2.0]
    B --> H[SCSPv3<br/>Librerías / Cliente Ligero / SCSP-WS]
    B --> I[PID<br/>Verificación y consulta de datos]
    B --> J[Carpeta Ciudadana<br/>Área personalizada PAGe]
    B --> K[RFH<br/>Funcionarios habilitados]
    C --> L[NEDAES<br/>Gestión de nómina]
    C --> M[SERVINOMINA<br/>Visualización de nóminas]
    C --> N[CIRCAB<br/>Trabajo colaborativo]
    C --> O[ENVIA<br/>Ficheros de gran volumen]
```

## Notas clave
- **DIR3** proporciona un inventario unificado y común de las unidades orgánicas y oficinas asociadas.
- **Port@firmas AGE** incorpora la firma electrónica en los flujos de trabajo; se integra vía servicios web.
- **eVisor** genera copia auténtica en papel de documentos con firma electrónica y justificantes de firma.
- **Nodo eIDAS** intercambia mensajes conforme a SAML 2.0; las AAPP españolas se integran a través de Cl@ve.
- **SCSPv3** sustituye certificados en soporte papel; SCSP-SOAP no es un producto del portfolio.
- **PID** permite la intermediación de datos entre AAPP (verificación y consulta).
- **RFH** es interoperable con sistemas equivalentes de CC.AA. y entidades locales.
- **NEDAES** gestiona la nómina de empleados públicos; **SERVINOMINA** solo la visualiza.
