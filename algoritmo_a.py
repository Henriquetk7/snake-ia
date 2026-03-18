import heapq
from typing import Optional


def heuristica_manhattan(a: tuple, b: tuple) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def algoritmo_a(
    inicio: tuple,
    destino: tuple,
    tamanho_grade: int,
    obstaculos: set,
) -> Optional[list]:

    # Encontra o caminho mais curto de inicio até destino usando A*.

    movimentos_possiveis = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    contador = 0
    nos_aberto = []
    heapq.heappush(nos_aberto, (heuristica_manhattan(inicio, destino), contador, inicio))

    veio_de = {}
    custo = {inicio: 0}

    conjunto_fechado = set()

    while nos_aberto:
        _, _, atual = heapq.heappop(nos_aberto)

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

        for dx, dy in movimentos_possiveis:
            vizinho = (atual[0] + dx, atual[1] + dy)

            if not (0 <= vizinho[0] < tamanho_grade and 0 <= vizinho[1] < tamanho_grade):
                continue

            if vizinho in obstaculos:
                continue

            custo_tentativo = custo[atual] + 1

            if custo_tentativo < custo.get(vizinho, float("inf")):
                veio_de[vizinho] = atual
                custo[vizinho] = custo_tentativo
                custo_f = custo_tentativo + heuristica_manhattan(vizinho, destino)
                contador += 1
                heapq.heappush(nos_aberto, (custo_f, contador, vizinho))

    return None  # Caminho não encontrado
