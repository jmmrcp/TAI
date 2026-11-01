# Esquema: Arquitectura Java EE / Jakarta EE

```mermaid
flowchart TB
    APP[Aplicación Jakarta EE] --> WEB[Capa Web<br/>Servlets / JSP / JSF]
    APP --> BIZ[Capa de negocio<br/>EJB (javax.ejb / jakarta.ejb)]
    APP --> PERS[Capa de persistencia<br/>JPA (jakarta.persistence)]
    WEB --> CONT[Contenedor Web]
    BIZ --> EJB_CONT[Contenedor EJB]
    PERS --> DB[(Base de datos)]
    CONT --> AS[Servidor de aplicaciones]
    EJB_CONT --> AS
    AS --> JVM[JVM (JIT / HotSpot)<br/>bytecode -> código máquina]
```

## Notas clave
- **Jakarta EE** (antes Java EE): plataforma empresarial con especificaciones (EJB, Servlet, JPA, JMS, JTA...).
- **EJB**: componentes de negocio del lado servidor; paquete `javax.ejb` / `jakarta.ejb`.
- **JPA**: especificación de persistencia; homóloga funcional a Entity Framework Core en .NET.
- **JVM**: máquina virtual que compila bytecode a código máquina en tiempo de ejecución (JIT).
- **Spring Boot**: framework Java para aplicaciones standalone con auto-configuración.
```