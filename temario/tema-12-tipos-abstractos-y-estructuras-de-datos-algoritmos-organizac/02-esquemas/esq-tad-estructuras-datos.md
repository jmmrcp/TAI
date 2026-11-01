# Esquema: Tipos abstractos de datos (TAD) y estructuras de datos

```mermaid
flowchart TB
    TAD[Tipos Abstractos de Datos] --> Pila[Pila (Stack) - LIFO]
    TAD --> Cola[Cola (Queue) - FIFO]
    TAD --> Lista[Lista lineal]
    TAD --> Conjunto[Conjunto (Set)]
    TAD --> Mapa[Mapa / Diccionario]
    TAD --> Arbol[Árbol]
    TAD --> Grafo[Grafo]
    Arbol --> BST[Árbol de búsqueda (BST)]
    Arbol --> Heap[Montículo (Heap)]
    Arbol --> AVL[Árbol balanceado (AVL/rojo-negro)]
    Grafo --> Dirigido[Dirigido / No dirigido]
    Grafo --> Ponderado[Ponderado / No ponderado]
```

## Notas clave
- Un **TAD** define la interfaz (operaciones) independientemente de la implementación.
- **Pila**: LIFO; operaciones push/pop/top. **Cola**: FIFO; enqueue/dequeue/front.
- **Lista**: secuencia ordenada; implementación con arrays o listas enlazadas.
- **Conjunto**: elementos únicos; operaciones de unión, intersección y diferencia.
- **Mapa/Diccionario**: asociación clave-valor; implementación con tabla hash o árbol.
- **Árbol**: estructura jerárquica; BST mantiene orden; heaps para colas de prioridad.
- **Grafo**: vértices y aristas; puede ser dirigido/no dirigido y ponderado.
- **JSON (RFC 8259)**: formato de intercambio de datos; valores: object, array, string, number, true, false, null; codificación UTF-8.
