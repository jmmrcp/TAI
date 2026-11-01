# Esquema: Normalización de bases de datos relacionales

```mermaid
flowchart TD
    R[Relación no normalizada] --> F1[1FN: atributos atómicos, sin grupos repetitivos]
    F1 --> F2[2FN: sin dependencias parciales de la PK]
    F2 --> F3[3FN: sin dependencias transitivas]
    F3 --> B[BCNF: todo determinante es superclave]
    B --> F4[4FN: sin dependencias multivaluadas]
    F4 --> F5[5FN: sin dependencias de join]
    F3 -. anomalías .-> A[Inserción / Actualización / Eliminación]
```

## Notas clave
- **1FN**: elimina grupos repetitivos; todos los valores son atómicos.
- **2FN**: elimina dependencias parciales cuando la PK es compuesta.
- **3FN**: elimina dependencias transitivas; todo atributo no clave depende directamente de la PK.
- **BCNF**: refuerza la 3FN exigiendo que todo determinante sea superclave.
- **4FN/5FN**: tratan dependencias multivaluadas y de join.
- Una relación con **descomposición sin pérdida** (lossless join) puede reconstruirse sin pérdida de información a partir de la join de sus proyecciones.
