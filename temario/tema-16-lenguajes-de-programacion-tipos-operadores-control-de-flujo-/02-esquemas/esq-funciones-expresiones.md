# Esquema: Funciones, parámetros y expresiones

```mermaid
flowchart LR
    F[Funciones] --> VP[Por valor: copia, no modifica original]
    F --> VR[Por referencia: modifica original]
    F --> Rec[Recursión: se llama a sí misma]
    F --> Lam[Lambda / anónima]
    F --> Sob[Sobrecarga]
    Expr[Expresiones de examen] --> Xor["Java: 6^3 = 5 (XOR)"]
    Expr --> Py["Python: \"Java\"*4+\"Linux\""]
    Expr --> JS["JS: ternario (a+b>c)?a:(b+c)"]
    Expr --> Inf["Bucle infinito: x+1 luego x-1"]
```

## Notas clave
- **Paso por valor**: se copia el argumento; el original no cambia (Java primitivos).
- **Paso por referencia**: se pasa la dirección; modifica el original (C++ con &).
- **Recursión**: caso base + caso recursivo; riesgo de stack overflow.
- **Funciones de orden superior / lambda**: funciones anónimas inline (JS arrow functions).
- **Expresiones típicas de examen**: XOR (^) no es potencia; "*" repite en Python; ternario condicional; bucles infinitos por cancelación de incremento.
- **Librerías Apache en Java**: no son parte del JDK estándar (p. ej. Commons, Log4j, HttpClient).
- **JavaScript**: distingue tipos primitivos (number, string, boolean, null, undefined, symbol, bigint) y objetos.
