import heapq
from typing import Optional


def heuristica(a: tuple, b: tuple) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def algoritmo_a(
    inicio: tuple,
    destino: tuple,
    tamanho_grade: int,
    obstaculos: set,
) -> Optional[list]:

    # Encontra o caminho mais curto de inicio até destino usando A*.

    deslocamentos_vizinhos = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    contador = 0
    conjunto_aberto = []
    heapq.heappush(conjunto_aberto, (heuristica(inicio, destino), contador, inicio))

    veio_de = {}
    custo_g = {inicio: 0}

    conjunto_fechado = set()

    while conjunto_aberto:
        _, _, atual = heapq.heappop(conjunto_aberto)

        if atual == destino:
            caminho = []
            while atual in veio_de:
                caminho.append(atual)
                atual = veio_de[atual]
            caminho.reverse()
            return caminho

        if atual in conjunto_fechado:
            continue
        conjunto_fechado.add(atual)

        for dx, dy in deslocamentos_vizinhos:
            vizinho = (atual[0] + dx, atual[1] + dy)

            if not (0 <= vizinho[0] < tamanho_grade and 0 <= vizinho[1] < tamanho_grade):
                continue

            if vizinho in obstaculos:
                continue

            custo_g_tentativo = custo_g[atual] + 1

            if custo_g_tentativo < custo_g.get(vizinho, float("inf")):
                veio_de[vizinho] = atual
                custo_g[vizinho] = custo_g_tentativo
                custo_f = custo_g_tentativo + heuristica(vizinho, destino)
                contador += 1
                heapq.heappush(conjunto_aberto, (custo_f, contador, vizinho))

    return None  # Caminho não encontrado
