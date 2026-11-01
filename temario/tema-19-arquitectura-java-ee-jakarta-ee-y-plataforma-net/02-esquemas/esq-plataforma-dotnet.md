# Esquema: Plataforma .NET (CLR y componentes)

```mermaid
flowchart TB
    LANG[Lenguajes: C# / F# / VB.NET] --> COMP[Compilador]
    COMP --> CIL[CIL / MSIL<br/>código intermedio]
    CIL --> ASM[Ensamblado (Assembly)<br/>manifiesto + metadatos + CIL]
    ASM --> CLR[CLR (Common Language Runtime)]
    CLR --> JIT[JIT Compiler<br/>CIL -> código máquina]
    CLR --> GC[Garbage Collector]
    CLR --> EXH[Manejo de excepciones]
    CLR --> RT[Código máquina en ejecución]
    RT --> APP[Aplicación]
```

## Notas clave
- **CLR**: entorno de ejecución gestionado; responsable del manejo de excepciones y la recolección de basura.
- **JIT**: compila el código intermedio (CIL/MSIL) a código máquina en tiempo de ejecución.
- **Ensamblado**: unidad fundamental de implementación; contiene manifiesto, metadatos y CIL.
- **NuGet**: gestor de paquetes del ecosistema .NET.
- **Razor**: motor de vistas que combina HTML con C# en ASP.NET Core.
- **.NET MAUI**: framework multiplataforma para apps nativas (Android, iOS, macOS, Windows).
- **ADO.NET**: API de acceso a datos (no es un proveedor); proveedores: SqlClient, OleDb, Odbc.
- **EF Core**: ORM de .NET; homólogo funcional de JPA en Jakarta EE.
- **POCO**: Plain Old CLR Object; objeto simple sin dependencias del framework.
```