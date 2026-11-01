# Esquema: Arquitectura de Kubernetes

```mermaid
flowchart TB
    subgraph CP["Plano de control (Control Plane)"]
        API[API Server]
        ETCD[(etcd)]
        SCHED[Scheduler]
        CM[Controller Manager]
    end
    subgraph N1["Nodo 1"]
        K1[Kubelet]
        KP1[Kube-proxy]
        P1[Pod]
        P2[Pod]
    end
    subgraph N2["Nodo 2"]
        K2[Kubelet]
        KP2[Kube-proxy]
        P3[Pod]
    end
    API <--> ETCD
    SCHED --> API
    CM --> API
    K1 --> API
    K2 --> API
    P1 & P2 -. ejecuta .-> K1
    P3 -. ejecuta .-> K2
```

## Notas clave
- **Scheduler**: asigna Pods a nodos según recursos disponibles.
- **etcd**: almacenamiento no volátil de toda la configuración del clúster.
- **Kubelet**: agente por nodo que garantiza que los contenedores estén en ejecución.
- **Objetos básicos**: Pod, Service, Volume, Namespace, ConfigMap, Secret.
- **Identificación única**: campo `metadata.name` (+ namespace).
