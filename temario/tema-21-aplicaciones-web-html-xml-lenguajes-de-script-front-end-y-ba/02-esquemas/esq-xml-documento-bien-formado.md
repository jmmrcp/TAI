# Esquema: Documento XML bien formado y procesamiento

```mermaid
flowchart TD
    P[Prólogo opcional<br/><?xml version ...?>] --> R[Elemento raíz único]
    R --> E1[Elementos anidados<br/>correctamente cerrados]
    R --> A[Atributos<br/>entre comillas]
    R --> C[Comentarios<br/><!-- ... -->]
    R --> CD[Secciones CDATA]
    R --> V[Validación opcional]
    V --> DTD[DTD]
    V --> XSD[XML Schema XSD]
    PROC[APIs Java] --> DOM[DOM (árbol en memoria)]
    PROC --> SAX[SAX (eventos, streaming)]
    PROC --> STAX[StAX (pull parsing)]
    PROC --> JAXB[JAXB (binding a objetos)]
    BIN[Datos binarios] --> XOP[XOP / MTOM]
```

## Notas clave
- Un documento XML bien formado tiene **exactamente un elemento raíz**.
- **Case-sensitive**: distingue mayúsculas/minúsculas.
- **Comentarios**: `<!-- ... -->`.
- **Validación**: DTD o XML Schema (XSD).
- **APIs Java**: DOM, SAX, StAX, JAXB, JAXP.
- **XOP** (XML-binary Optimized Packaging) permite incluir datos binarios en mensajes SOAP; relacionado con MTOM.
