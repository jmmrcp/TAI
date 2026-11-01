# Esquema: Tipos, operadores y control de flujo

```mermaid
flowchart TB
    LP[Lenguajes de programación] --> T[Tipos de datos]
    LP --> O[Operadores]
    LP --> CF[Control de flujo]
    LP --> F[Funciones]
    T --> P[Primitivos: byte, short, int, long, float, double, char, boolean]
    T --> R[Referencia: String, arrays, objetos]
    O --> A[Aritméticos: + - * / % ^]
    O --> L[Lógicos: && || !]
    O --> C[Comparación: == != < >]
    O --> Te[Ternario: cond ? a : b]
    CF --> Cond[Condicionales: if/else, switch]
    CF --> Bucles[Bucles: while, do-while, for]
    CF --> Ind[Indentación en Python]
    F --> Func[Función: devuelve valor]
    F --> Proc[Procedimiento: void]
    F --> Sob[Sobrecarga: mismo nombre, distintos params]
```

## Notas clave
- **Tipos primitivos Java**: byte (8), short (16), int (32), long (64), float (32), double (64), char (16 Unicode), boolean (true/false).
- **^ en Java/C++** es XOR bit a bit, NO potencia (6^3 = 5).
- **==** compara valores en primitivos y referencias en objetos.
- **Python** delimita bloques por indentación; **Java/C++** usan llaves { }.
- **do...while** ejecuta el cuerpo al menos una vez (condición al final).
- **Python "*"** repite secuencias: "Java"*4 = "JavaJavaJavaJava".
- **Función** devuelve valor; **procedimiento** no devuelve (void).
- **Sobrecarga (overloading)**: varias funciones con el mismo nombre y distintos parámetros en el mismo ámbito (C++).
- Un bucle es infinito si su condición nunca se hace falsa (p. ej. incrementar y decrementar la misma variable).
