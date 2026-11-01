# Esquema: Clasificación de SGBD

```mermaid
flowchart TD
    SGBD[Sistema Gestor de Bases de Datos] --> R[Relacional]
    SGBD --> OO[Orientado a Objetos]
    SGBD --> NO[NoSQL]
    R --> ACID[Propiedades ACID]
    R --> SQL[SQL / ANSI]
    OO --> OID[OID único]
    OO --> COL[Colecciones: Array, Lista, Bolsa]
    OO --> OQL[OQL]
    NO --> KV[Clave-valor]
    NO --> DOC[Documental]
    NO --> G[Grafos]
    NO --> COLU[Columnar]
```

## Notas clave
- **Relacional**: tablas, SQL, propiedades ACID, niveles de aislamiento.
- **Orientado a objetos**: objetos con OID, herencia, colecciones; OQL como lenguaje de consulta; ejemplo de SGBDOO: Matisse.
- **NoSQL**: modelos no relacionales; tipos clave-valor, documental, grafos y columnar; ejemplos: Redis, MongoDB, JanusGraph, HBase.
- **Oracle**: tablespace (lógico), datafile (físico), segmento, extensión.
