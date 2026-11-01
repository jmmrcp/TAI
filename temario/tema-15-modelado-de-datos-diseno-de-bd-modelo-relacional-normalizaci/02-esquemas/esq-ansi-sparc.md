# Esquema: Arquitectura ANSI/SPARC y DFD (Métrica v3)

```mermaid
flowchart TD
    U[Usuarios / Aplicaciones] --> E[Nivel externo: vistas de usuario]
    E --> C[Nivel conceptual: esquema lógico global]
    C --> I[Nivel interno: almacenamiento físico]
    I --> D[(Disco / Estructuras físicas)]
    C --> DI[Independencia lógica]
    I --> DF[Independencia física]
    P[Proceso DFD] --> A[Almacén de datos]
    P --> F[Flujo de datos]
    EXT[Entidad externa] --> P
```

## Notas clave
- **ANSI/SPARC** define tres niveles de abstracción: externo (vistas), conceptual (esquema global) e interno (físico).
- **Independencia física**: cambios en el almacenamiento no afectan al esquema conceptual.
- **Independencia lógica**: cambios en el esquema conceptual no afectan a las vistas/programas.
- **DFD (Métrica v3)**: procesos, almacenes de datos, entidades externas y flujos de datos.
- En la **explosión** de un DFD debe mantenerse el **equilibrio** (balance) y la **conservación** de datos.
