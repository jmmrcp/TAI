# Esquema: Comandos de administración del SO (Windows vs Linux)

```mermaid
flowchart TD
    A[Administración del SO] --> W[Windows]
    A --> L[Linux / Debian]
    W --> W1[sfc /scannow<br/>Reparar archivos de sistema]
    W --> W2[net user pepe *<br/>Cambiar contraseña]
    W --> W3[sc query / Get-Service<br/>Listar servicios]
    W --> W4[tasklist /svc<br/>Procesos y servicios]
    W --> W5[DISM /RestoreHealth<br/>Reparar imagen]
    L --> L1[uname -a / lsb_release<br/>Versión del SO]
    L --> L2[mv PAGOS RECIBOS<br/>Renombrar archivo]
    L --> L3[tail -f fichero.log<br/>Log en tiempo real]
    L --> L4[apt-get update<br/>Descargar info paquetes]
    L --> L5[systemctl status<br/>Gestionar servicios]
    L --> L6[crontab -e<br/>Tareas programadas]
```

## Notas clave
- **Windows**: `sfc /scannow` repara archivos de sistema protegidos; complementar con `DISM /Online /Cleanup-Image /RestoreHealth`.
- **Cambio de contraseña**: `net user <usuario> *` solicita la nueva contraseña de forma interactiva (requiere privilegios).
- **Servicios en Windows**: `sc query`, `Get-Service` (PowerShell) y `tasklist /svc` muestran servicios/procesos.
- **Linux/Debian**: `uname -a`/`lsb_release -a`/`/etc/os-release` para la versión; `mv` renombra; `tail -f` sigue logs.
- **Paquetes Debian**: `apt-get update` descarga índices (no instala); `apt-get upgrade` actualiza paquetes instalados.
- **Servicios Linux**: gestión con `systemctl`; tareas programadas con `crontab -e`.
