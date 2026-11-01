# Esquema: Jerarquía de Active Directory

```mermaid
flowchart TD
    F[Bosque (Forest)] --> T[Árbol (Tree)]
    T --> D[Dominio]
    D --> OU[Unidad Organizativa (OU)]
    OU --> O[Objetos<br/>(usuarios, equipos, grupos)]
    D --> PSO[PSO<br/>(Password Settings Object)]
    PSO --> U[Usuarios / grupos<br/>con política propia]
```

## Notas clave
- **Bosque (Forest)**: nivel superior; comparte esquema y catálogo global.
- **Árbol (Tree)**: dominios con espacio de nombres DNS contiguo.
- **Dominio**: unidad administrativa y de seguridad; límite de replicación.
- **OU**: contenedor para delegar administración y aplicar GPO.
- **Objetos**: usuarios, equipos, grupos, impresoras, etc.
- **AD DS**: servicio de directorio de Windows Server para autenticación/autorización.
- **PSO**: permite aplicar políticas de contraseña diferentes a usuarios o grupos específicos dentro de un mismo dominio (fine-grained password policies).
