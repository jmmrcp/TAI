# Esquema: Flujo de trabajo en Git

```mermaid
flowchart LR
    WD[Directorio de trabajo<br/>(Working Directory)] -->|git add| ST[Index / Staging<br/>(preparado)]
    ST -->|git commit| LR[(Repositorio local)]
    LR -->|git push| RR[(Repositorio remoto)]
    RR -->|git fetch / git pull| LR
    LR -->|git checkout| WD
    LR -->|git tag| TG[Etiquetas<br/>(versiones)]
```

## Notas clave
- **git add**: prepara (stage) cambios para el próximo commit.
- **git commit**: guarda una instantánea del estado preparado en el historial local.
- **git push / pull / fetch**: sincronización con el repositorio remoto.
- **tag**: marca un punto concreto del historial (p. ej. una versión).
- **pull request**: propuesta de fusión de cambios entre ramas en plataformas colaborativas (GitHub/GitLab).
