# Esquema: Arquitectura de un ordenador

```mermaid
flowchart TB
    subgraph CPU["CPU"]
        UC[Unidad de Control]
        ALU[ALU]
        REG[Registros: PC, IR, MAR, MDR]
        L1[(Caché L1)]
    end
    L2[(Caché L2)]
    L3[(Caché L3)]
    RAM[(Memoria principal RAM)]
    IO[Periféricos / E/S]
    UC --> ALU
    UC --> REG
    CPU --> L1
    L1 --> L2 --> L3 --> RAM
    CPU <-->|Bus de datos| RAM
    CPU -->|Bus de direcciones| RAM
    CPU -->|Bus de control| RAM
    CPU <--> IO
```

## Notas clave
- **ALU**: operaciones aritméticas y lógicas; parte de la CPU.
- **Unidad de Control**: decodifica instrucciones y coordina.
- **IR**: instrucción en ejecución; **PC**: siguiente instrucción.
- **Buses**: datos, direcciones y control.
- **Caché**: L1 (en núcleo, más rápida/menor), L2, L3 (compartida).
- **Harvard**: memorias/buses separados para instrucciones y datos.
- **CISC vs RISC**: instrucciones complejas vs simples; **ARM**: RISC de bajo consumo.
- **Taxonomía de Flynn**: SISD, SIMD, MISD, MIMD.
