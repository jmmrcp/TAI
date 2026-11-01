# Esquema: Criptografía y firma digital

```mermaid
flowchart LR
    A[Documento original] --> B[Función hash]
    B --> C[Resumen (digest)]
    C --> D[Cifrado con clave privada]
    D --> E[Firma electrónica]
    E --> F[CAdES<br/>ficheros grandes]
    subgraph Algoritmos
        RSA[RSA: clave pública]
        ECDSA[ECDSA: firma digital]
        ElGamal[ElGamal: asimétrico]
        GOST[GOST: NO asimétrico]
    end
    subgraph Recomendaciones
        KE[Key Exchange >= 112 bits]
        MFA[MFA: factores de distinta categoría]
        PASS[Contraseña: frases cortas sin sentido]
    end
```

## Notas clave
- La firma digital crea un **resumen (hash)** del documento y lo **cifra con la clave privada**; no cifra el documento original (no garantiza confidencialidad).
- **CAdES** es apropiado para firmar ficheros grandes, especialmente si la firma contiene el documento original.
- **ECDSA** es un algoritmo de firma digital (no estándar de cableado ni protocolo de enlace).
- **RSA** es un criptosistema de clave pública; **ElGamal** es asimétrico; **GOST** no se considera asimétrico.
- CCN-CERT: key exchange con fortaleza mínima de 112 bits; MFA combina factores de categorías distintas; contraseñas robustas con frases cortas sin sentido.
