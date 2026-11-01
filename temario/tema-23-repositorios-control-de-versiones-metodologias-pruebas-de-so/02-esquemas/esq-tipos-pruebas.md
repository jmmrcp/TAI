# Esquema: Tipos de pruebas de software

```mermaid
flowchart TD
    P[Pruebas de software] --> U[Pruebas unitarias<br/>(componentes aislados)]
    P --> I[Pruebas de integración<br/>(interfaces entre componentes)]
    P --> S[Pruebas del sistema<br/>(sistema completo)]
    P --> A[Pruebas de aceptación<br/>(validación del usuario)]
    P --> R[Pruebas de regresión<br/>(sin nuevos errores)]
    P --> REN[Pruebas de rendimiento<br/>(tiempos de respuesta)]
    P --> CE[Pruebas de carga/estrés<br/>(concurrencia de usuarios)]
    P --> CB[Pruebas caja negra / caja blanca]
```

## Notas clave
- **Integración**: verifica que los componentes/subsistemas interactúan correctamente a través de sus interfaces (Métrica v3).
- **Rendimiento**: comprueba que los tiempos de respuesta están dentro de los intervalos establecidos.
- **Regresión**: garantiza que los cambios no introducen errores en componentes no modificados.
- **Carga/estrés**: se simula con herramientas como JMeter.
- **Métrica v3**: contempla pruebas unitarias, de integración, del sistema y de aceptación, entre otras.
