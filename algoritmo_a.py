"""
astar.py — Implementação do algoritmo A* para busca de caminho na grade do Snake.
"""

import heapq
from typing import Optional


def heuristica(a: tuple, b: tuple) -> int:
    """Distância Manhattan entre dois pontos."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def algoritmo_a(
    inicio: tuple,
    destino: tuple,
    tamanho_grade: int,
    obstaculos: set,
) -> Optional[list]:
    """
    Encontra o caminho mais curto de inicio até destino usando A*.

    Args:
        inicio: Coordenada (x, y) inicial.
        destino: Coordenada (x, y) de destino.
        tamanho_grade: Tamanho da grade (tamanho_grade × tamanho_grade).
        obstaculos: Conjunto de posições bloqueadas (corpo da cobra).

    Returns:
        Lista de coordenadas do caminho (excluindo inicio, incluindo destino),
        ou None se não houver caminho.
    """
    # Deslocamentos dos vizinhos: cima, baixo, esquerda, direita
    deslocamentos_vizinhos = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    # Fila de prioridade: (custo_f, contador, posicao)
    contador = 0
    conjunto_aberto = []
    heapq.heappush(conjunto_aberto, (heuristica(inicio, destino), contador, inicio))

    veio_de = {}
    custo_g = {inicio: 0}

    conjunto_fechado = set()

    while conjunto_aberto:
        _, _, atual = heapq.heappop(conjunto_aberto)

        if atual == destino:
            # Reconstrói o caminho
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

            # Verifica limites da grade
            if not (0 <= vizinho[0] < tamanho_grade and 0 <= vizinho[1] < tamanho_grade):
                continue

            # Verifica obstáculos
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
