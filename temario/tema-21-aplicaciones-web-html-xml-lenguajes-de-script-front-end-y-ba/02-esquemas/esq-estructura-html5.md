# Esquema: Estructura de un documento HTML5

```mermaid
flowchart TD
    D[<!DOCTYPE html>] --> H[html]
    H --> HEAD[head]
    H --> BODY[body]
    HEAD --> META[meta charset / viewport]
    HEAD --> TITLE[title]
    HEAD --> LINK[link CSS]
    HEAD --> SCRIPT[script JS]
    BODY --> HEADER[header]
    BODY --> NAV[nav]
    BODY --> MAIN[main]
    BODY --> ASIDE[aside]
    BODY --> FOOTER[footer]
    MAIN --> ARTICLE[article]
    MAIN --> SECTION[section]
    ARTICLE --> FIGURE[figure + figcaption]
    ARTICLE --> VIDEO[video / audio]
    ARTICLE --> CANVAS[canvas]
```

## Notas clave
- **DOCTYPE** debe ser la primera línea del documento (HTML Living Standard WHATWG).
- **Semántica**: header, nav, main, article, section, aside, footer mejoran accesibilidad y SEO.
- **Multimedia nativa**: video, audio, canvas sin plugins externos.
- **Formularios**: datalist, output, progress, meter.
- **HTML vs XHTML**: HTML es SGML y más permisivo; XHTML es XML estricto (etiquetas en minúsculas, cerradas, atributos entre comillas).
