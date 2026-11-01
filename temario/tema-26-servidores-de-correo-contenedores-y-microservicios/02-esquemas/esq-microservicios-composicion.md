# Esquema: Composición de microservicios

```mermaid
flowchart LR
    subgraph ORQ["Orquestación (centralizado)"]
        O[Orquestador]
        O --> A1[Servicio A]
        O --> B1[Servicio B]
        O --> C1[Servicio C]
    end
    subgraph COR["Coreografía (descentralizado)"]
        EA[Servicio A] -- evento --> EB[Servicio B]
        EB -- evento --> EC[Servicio C]
        EC -- evento --> EA
    end
```

## Notas clave
- **Orquestación**: un controlador central dirige el flujo y las llamadas.
- **Coreografía**: los servicios se coordinan mediante eventos, sin controlador central.
