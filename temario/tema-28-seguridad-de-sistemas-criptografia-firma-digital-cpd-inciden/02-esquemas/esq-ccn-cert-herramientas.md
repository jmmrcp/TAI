# Esquema: Herramientas y soluciones del CCN-CERT

```mermaid
flowchart TD
    CCN[CCN-CERT] --> H[Herramientas]
    CCN --> S[Soluciones de ciberseguridad]
    H --> MARTA[MARTA<br/>Análisis automatizado de ficheros maliciosos]
    H --> MARIA[MARIA<br/>Análisis estático multi-motor AV/antimalware]
    H --> LUCIA[LUCIA<br/>Ticketing de incidentes ENS]
    S --> ELENA[ELENA<br/>Simulador de técnicas de cibervigilancia]
    S --> NVD[NVD<br/>Base de datos de vulnerabilidades]
    S --> DD[Datadog<br/>Monitorización y seguridad (APM)]
```

## Notas clave
- **MARTA**: análisis automatizado de ficheros con posible comportamiento malicioso.
- **MARIA**: análisis estático de código dañino mediante múltiples motores antivirus/antimalware (Windows y Linux).
- **LUCIA**: herramienta de ticketing para la gestión de incidentes de seguridad en entidades del ENS.
- **ELENA**: solución del CCN (simulador de técnicas de cibervigilancia).
- **NVD**: base de datos de vulnerabilidades de referencia.
- **Datadog**: plataforma integrada de monitorización y seguridad con APM.
