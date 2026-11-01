# Esquema: Digitalización de la información y formatos

```mermaid
flowchart LR
    A[Señal analógica] --> M[Muestreo]
    M --> Q[Cuantificación]
    Q --> C[Codificación]
    C --> D[Datos digitales]
    D --> F{Formato de representación}
    F --> PDF[PDF / PDF/A / PDF/X]
    F --> IMG[JPEG (compresión con pérdida)]
    F --> TXT[CSV (RFC 4180) / JSON (RFC 8259)]
    F --> VID[AV1 (códec de vídeo)]
```

## Notas clave
- **Digitalización**: muestreo → cuantificación → codificación.
- **Unidades**: bit (0/1), byte (8 bits), y múltiplos (KB, MB, GB, TB…).
- **Sistemas de numeración**: decimal (10), binario (2), octal (8), hexadecimal (16: 0-9, A-F).
- **Funciones lógicas**: AND, OR, NOT, XOR, NAND, NOR, XNOR.
- **PDF**: ISO 32000; PDF/A archivado, PDF/X intercambio para impresión.
- **JPEG**: compresión con pérdida (DCT), 24 bits, sin transparencia original.
- **CSV (RFC 4180)**: comas, CRLF, campos entrecomillables.
- **JSON (RFC 8259)**: UTF-8, objetos/arrays, sin comentarios.
- **AV1**: códec de vídeo abierto y libre de royalties (AOMedia).
