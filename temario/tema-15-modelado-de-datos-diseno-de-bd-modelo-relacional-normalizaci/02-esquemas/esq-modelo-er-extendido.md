# Esquema: Modelo Entidad/Relación Extendido (Métrica v3)

```mermaid
flowchart TD
    E[Entidad] --> A[Atributo]
    E --> K[Clave]
    R[Relación] --> C[Cardinalidad 1:1 / 1:N / N:M]
    R --> P[Participación total/parcial]
    R --> Rol[Rol]
    E -.generalización.-> S[Supertipo/Subtipo]
    E -.categoría (unión).-> Cat[Categoría]
    R -.agregación.-> Agg[Relación como entidad]
    A --> Ac[Atributo compuesto]
    A --> Am[Atributo multivaluado]
    A --> Ad[Atributo derivado]
```

## Notas clave
- **Entidad**: conjunto de objetos del dominio con propiedades comunes; se representa con rectángulo.
- **Relación**: asociación entre entidades; rombo. Se define por nombre, tipo, cardinalidad y participación.
- **Cardinalidad**: número de instancias asociadas (1:1, 1:N, N:M).
- **Participación**: total (obligatoria, línea doble) o parcial (opcional).
- **Atributo derivado**: elipse discontinua; su valor se calcula, no se almacena.
- **Categoría (unión)**: relaciona entidades de dominios independientes que coyunturalmente se asocian.
- **Agregación**: trata una relación como entidad para que participe en otra relación.
