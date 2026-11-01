# Esquema: Algoritmos de ordenación, grafos y organización de ficheros

```mermaid
flowchart LR
    ALG[Algoritmos] --> ORD[Ordenación]
    ALG --> GRA[Grafos]
    ORD --> CMP[Por comparación O(n log n): Merge, Quick, Heap]
    ORD --> LIN[Lineales: Counting, Radix, Bucket]
    GRA --> BFSDFS[BFS / DFS]
    GRA --> DIJ[Dijkstra (pesos no negativos)]
    GRA --> BF[Bellman-Ford (pesos negativos)]
    GRA --> FW[Floyd-Warshall (todos los pares)]
    GRA --> MST[Kruskal / Prim (MST)]
    FIC[Organización de ficheros] --> SEQ[Secuencial]
    FIC --> HASH[Directa / hash]
    FIC --> ISAM[ISAM]
    FIC --> BTREE[Árbol B / B+]
    FIC --> HEAPF[Heap de fichero]
    FIC --> INV[Invertida]
```

## Notas clave
- **Ordenación por comparación**: límite inferior Ω(n log n); Merge (estable), Quick (in-place, peor O(n²)), Heap (no estable).
- **Ordenación lineal**: Counting O(n+k), Radix O(d(n+k)), Bucket O(n+k) caso medio; requieren rango conocido.
- **Grafos**: BFS (anchura, cola) y DFS (profundidad, pila/recursión) en O(V+E).
- **Camino mínimo**: Dijkstra (sin pesos negativos), Bellman-Ford (permite negativos), Floyd-Warshall (todos los pares).
- **MST**: Kruskal (unión-búsqueda) y Prim (cola de prioridad).
- **Ficheros**: secuencial, directa/hash, ISAM, árbol B/B+, heap e invertida según patrón de acceso.
- **Dijkstra** es el algoritmo de camino más corto desde un origen en grafo con pesos en aristas.
