# Esquema: PowerShell Core

```mermaid
flowchart LR
    P[PowerShell Core] --> B[Base: .NET Core/.NET]
    P --> M[Multiplataforma<br/>Windows/Linux/macOS]
    P --> O[Open source MIT]
    P --> C[Cmdlets<br/>verbo-sustantivo]
    P --> PL[Pipeline de objetos]
    P --> R[Remoting<br/>WinRM/SSH]
    P --> X[Coexiste con<br/>Windows PowerShell 5.1]
    C --> E[Ejemplos:<br/>Get-Service, Set-Location]
    PL --> F[Where-Object, Select-Object]
```

## Notas clave
- **PowerShell Core** (6+) es multiplataforma y open source, construido sobre .NET Core/.NET.
- **Cmdlets** usan nomenclatura verbo-sustantivo y operan sobre objetos .NET en el pipeline.
- **Pipeline de objetos** (no texto) permite filtrar/transformar con `Where-Object`, `Select-Object`.
- **Remoting** vía WinRM (Windows) o SSH (Linux/macOS).
- **Windows PowerShell 5.1** (.NET Framework, solo Windows) coexiste pero es edición distinta.
