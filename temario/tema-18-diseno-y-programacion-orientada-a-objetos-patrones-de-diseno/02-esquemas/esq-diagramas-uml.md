# Esquema: Diagramas UML 2.5

```mermaid
flowchart TD
    UML[UML 2.5] --> EST[Estructura]
    UML --> COMP[Comportamiento]
    EST --> E1[Clases]
    EST --> E2[Componentes]
    EST --> E3[Estructura compuesta]
    EST --> E4[Despliegue]
    EST --> E5[Objetos]
    EST --> E6[Paquetes]
    EST --> E7[Perfil]
    COMP --> C1[Actividad]
    COMP --> C2[Máquina de estados]
    COMP --> C3[Casos de uso]
    COMP --> INT[Interacción]
    INT --> I1[Secuencia]
    INT --> I2[Comunicación]
    INT --> I3[Panorama de interacción]
    INT --> I4[Tiempos]
```

## Notas clave
- **Diagramas de estructura** (7): Clases, Componentes, Estructura compuesta, Despliegue, Objetos, Paquetes, Perfil.
- **Diagramas de comportamiento** (4 + 4 de interacción): Actividad, Máquina de estados, Casos de uso e Interacción (Secuencia, Comunicación, Panorama, Tiempos).
- El **diagrama de secuencia** representa la interacción entre objetos/participantes mediante los mensajes que se intercambian; describe en detalle un escenario de un caso de uso (Métrica v3).
- Visibilidad UML: `+` público, `-` privado, `#` protegido, `~` paquete.
```

>