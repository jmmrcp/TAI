# Esquema: Equivalencias Jakarta EE ↔ .NET

```mermaid
flowchart LR
    subgraph Jakarta["Jakarta EE"]
        JPA[JPA<br/>persistencia]
        EJB[EJB<br/>negocio]
        SERV[Servlets/JSP<br/>web]
        JVM[JVM JIT<br/>ejecución]
    end
    subgraph DotNet[".NET"]
        EF[Entity Framework Core]
        SVC[Servicios / componentes]
        ASP[ASP.NET Core (Razor)]
        CLR[CLR JIT]
    end
    JPA <--> EF
    EJB <--> SVC
    SERV <--> ASP
    JVM <--> CLR
```

## Notas clave
- **JPA ↔ EF Core**: gestión de persistencia / ORM.
- **EJB ↔ servicios de negocio**: componentes del lado servidor.
- **Servlets/JSP ↔ ASP.NET Core (Razor)**: componentes web y vistas.
- **JVM (JIT) ↔ CLR (JIT)**: compilación en tiempo de ejecución de código intermedio.
```