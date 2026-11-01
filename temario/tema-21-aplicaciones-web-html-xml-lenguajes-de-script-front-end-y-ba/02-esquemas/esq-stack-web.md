# Esquema: Stack web Front-end / Back-end y opciones móviles

```mermaid
flowchart LR
    U[Usuario / Navegador] --> FE[Front-end<br/>HTML CSS JS]
    FE --> FW[Frameworks SPA<br/>React Angular Vue]
    FE -->|HTTP/HTTPS| BE[Back-end<br/>Java Python PHP Ruby Node]
    BE --> DB[(Base de datos)]
    BE --> FWB[Frameworks<br/>Spring Django Laravel Rails Express]
    U --> MOB[App móvil]
    MOB --> NAT[Nativa]
    MOB --> HYB[Híbrida WebView]
    MOB --> PWA[PWA]
    MOB --> CP[Cross-platform<br/>Flutter React Native]
    MOTORES[Motores web] --> GECKO[Gecko Mozilla]
    MOTORES --> BLINK[Blink Chromium]
    MOTORES --> WEBKIT[WebKit Safari]
```

## Notas clave
- **Front-end**: HTML, CSS, JavaScript; frameworks SPA React/Angular/Vue.
- **Back-end**: Java, Python, PHP, Ruby, Node.js; frameworks Spring, Django, Laravel, Rails, Express.
- **Ruby on Rails**: framework MVC para Ruby en servidor.
- **JavaScript**: ECMAScript, débilmente tipado, orientado a prototipos, single-threaded con event loop; runtime servidor Node.js.
- **NO es framework JS**: Django, Laravel, Spring, Rails (back-end).
- **Motor Mozilla**: Gecko.
- **Apps móviles**: nativa, híbrida, PWA, cross-platform; una app de escritorio NO es opción móvil.
- **CSS3**: unidades relativas (em, rem, %, vw, vh...) vs absolutas (px, cm, pt...).
- **Eventos HTML**: onmouseover/mouseenter para efecto al situar puntero.
