# Esquema: Jerarquia de directorios en Linux/Unix

```mermaid
flowchart TD
    R[/] --> BIN[/bin Binarios esenciales]
    R --> ETC[/etc Configuracion]
    R --> HOME[/home Usuarios]
    R --> USR[/usr Programas de usuario]
    R --> VAR[/var Datos variables]
    R --> TMP[/tmp Temporales]
    R --> DEV[/dev Dispositivos]
    R --> PROC[/proc Procesos y kernel]
    R --> LIB[/lib Bibliotecas]
    R --> OPT[/opt Software opcional]
    R --> SBIN[/sbin Admin del sistema]
    R --> ROOT[/root Home de root]
```

## Notas clave
- **/etc** contiene la configuracion del sistema y de las aplicaciones instaladas.
- **/proc** expone informacion de procesos y del kernel como sistema de ficheros virtual.
- Permisos: `chmod 640` asigna `rw-r-----` (propietario lectura/escritura, grupo lectura, otros sin permisos).
- Para listar el contenido de `fichero.tar`: `tar -tf fichero.tar`.
- **BitLocker** (Windows) cifra volumenes; **sandboxing** (iOS) aísla apps y sus datos.
