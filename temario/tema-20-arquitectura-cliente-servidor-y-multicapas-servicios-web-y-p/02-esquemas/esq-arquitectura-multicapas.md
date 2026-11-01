# Esquema: Arquitectura cliente/servidor y multicapas

```mermaid
flowchart TB
    C[Cliente] -->|HTTP/HTTPS| W[Capa Web / Presentación]
    W --> A[Capa de Aplicación / Negocio]
    A --> D[(Capa de Datos / BD)]
    subgraph "2 capas"
        C2[Cliente] --> S2[Servidor]
    end
    subgraph "3 capas"
        P3[Presentación] --> N3[Negocio] --> D3[(Datos)]
    end
    subgraph "n capas"
        Pn[Presentación] --> Wn[Web] --> Bn[Negocio] --> In[Integración] --> Dn[(Datos)]
    end
```

## Notas clave
- **Cliente/servidor**: el cliente solicita servicios; el servidor los proporciona.
- **2 capas**: cliente + servidor; lógica repartida; acoplamiento alto.
- **3 capas**: separación presentación / negocio / datos; escalabilidad.
- **n capas (multicapas)**: especialización por capas; balanceo y caché.
- **Sistemas distribuidos**: escalabilidad, transparencia, heterogeneidad y tolerancia a fallos.
