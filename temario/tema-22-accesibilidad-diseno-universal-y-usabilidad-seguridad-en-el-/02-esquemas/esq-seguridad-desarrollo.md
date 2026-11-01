# Esquema: Seguridad en el desarrollo de software

```mermaid
flowchart LR
    SDLC[Ciclo de vida seguro] --> SAST[SAST<br/>Análisis estático]
    SDLC --> DAST[DAST<br/>Análisis dinámico]
    SDLC --> SCA[SCA<br/>Composición de software]
    SDLC --> IAST[IAST<br/>Análisis interactivo]
    SDLC --> REV[Revisión de código]
    SDLC --> PRAC[Prácticas anti-inyección]
    PRAC --> VAL[Validación y saneamiento<br/>de entradas]
    PRAC --> PARAM[Consultas<br/>parametrizadas]
    PRAC --> ESC[Codificación de salida<br/>(escaping)]
```

## Notas clave
- **SAST**: analiza el código fuente sin ejecutarlo para detectar vulnerabilidades.
- **DAST**: prueba la aplicación en ejecución simulando ataques externos.
- **SCA**: detecta vulnerabilidades en dependencias y librerías de terceros.
- La práctica que previene de forma directa vulnerabilidades de inyección (SQLi, XSS) es la **validación y saneamiento de las entradas de usuario**.
- Complementar con consultas parametrizadas (anti-SQLi) y codificación de salida (anti-XSS).
