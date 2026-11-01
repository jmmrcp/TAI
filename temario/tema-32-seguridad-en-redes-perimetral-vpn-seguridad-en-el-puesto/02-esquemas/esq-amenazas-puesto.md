# Esquema: Amenazas al puesto del usuario

```mermaid
flowchart TB
    U[Usuario / Puesto] --> Phishing[Phishing: correo fraudulento]
    U --> Pharming[Pharming: redirección DNS/hosts]
    U --> Vishing[Vishing: llamadas telefónicas]
    U --> Smishing[Smishing: SMS fraudulento]
    U --> Clickjacking[Clickjacking: iframe invisible]
    Phishing --> Creds[Robo de credenciales]
    Pharming --> Creds
    Vishing --> Creds
    Smishing --> Creds
    Clickjacking --> Acciones[Acciones no deseadas]
```

## Notas clave
- **Pharming** obtiene credenciales de forma ilícita redirigiendo el tráfico a un sitio falso (manipulación de DNS/hosts).
- **Vishing** suplanta a una entidad legítima mediante llamadas telefónicas.
- **Clickjacking** superpone un iframe invisible para capturar clics del usuario.
- **MFA** y **formación** son medidas clave de mitigación.
- **Cookies seguras** (HttpOnly, Secure, SameSite) protegen la sesión frente a XSS/CSRF.
```
