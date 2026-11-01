# Esquema: Transacciones, JDBC y lenguajes de consulta

```mermaid
flowchart TD
    TX[Transacción] --> BEGIN[BEGIN TRANSACTION]
    BEGIN --> OP[Operaciones DML]
    OP --> SAVE[SAVEPOINT nombre]
    SAVE --> RB[ROLLBACK TO SAVEPOINT nombre]
    OP --> COMMIT[COMMIT]
    OP --> ROLLBACK[ROLLBACK]
    JDBC[JDBC] --> T1[Type 1: JDBC-ODBC]
    JDBC --> T2[Type 2: Native-API]
    JDBC --> T3[Type 3: Network protocol]
    JDBC --> T4[Type 4: Pure Java]
    JDBC --> PS[PreparedStatement / CallableStatement]
    LANG[Lenguajes] --> OQL[OQL: BD orientadas a objetos]
    LANG --> CYPHER[Cypher: Neo4j (grafos)]
```

## Notas clave
- **ROLLBACK** restituye modificaciones desde el inicio de la transacción o desde un savepoint.
- En Oracle, para establecer punto de recuperación dentro de una transacción: **SAVEPOINT nombre**.
- **JDBC**: Type 4 (puro Java) es el más usado; PreparedStatement precompila SQL con parámetros `?`.
- **OQL** es el lenguaje de consulta de bases de datos orientadas a objetos (estándar ODMG).
- **Cypher** es el lenguaje de consulta de Neo4j (bases de datos de grafos).
- Oracle INSTR: `SELECT INSTR('Corporate Floor','or',3,2) FROM DUAL;` devuelve **14**.
```