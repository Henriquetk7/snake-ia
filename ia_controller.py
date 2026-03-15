"""
ai_controller.py — Controlador de IA que usa A* para jogar Snake.
"""

from game import Direcao, JogoCobra
from algoritmo_a import algoritmo_a
from typing import Optional


class ControladorIA:
    """
    IA que controla a cobra usando o algoritmo A*.

    Estratégia principal: buscar a moeda mais próxima via A*.
    Fallback: se o caminho direto não existe, tenta seguir a própria cauda
    (modo de sobrevivência) para ganhar espaço e tentar novamente.
    """

    def __init__(self, jogo: JogoCobra):
        self.jogo = jogo

    def obter_direcao_do_caminho(self, caminho: list) -> Optional[Direcao]:
        """Converte o primeiro passo de um caminho em uma direção."""
        if not caminho:
            return None

        cabeca = self.jogo.cabeca
        proxima_pos = caminho[0]
        dx = proxima_pos[0] - cabeca[0]
        dy = proxima_pos[1] - cabeca[1]

        mapa_direcao = {
            (0, -1): Direcao.CIMA,
            (0, 1): Direcao.BAIXO,
            (-1, 0): Direcao.ESQUERDA,
            (1, 0): Direcao.DIREITA,
        }
        return mapa_direcao.get((dx, dy))

    def buscar_caminho_ate_moeda(self) -> Optional[list]:
        """Busca caminho A* até a moeda mais próxima."""
        moeda = self.jogo.obter_moeda_mais_proxima()
        if moeda is None:
            return None

        obstaculos = self.jogo.obter_obstaculos()
        return algoritmo_a(self.jogo.cabeca, moeda, self.jogo.tamanho_grade, obstaculos)

    def buscar_caminho_ate_cauda(self) -> Optional[list]:
        """Busca caminho A* até a própria cauda (modo de sobrevivência)."""
        cauda = self.jogo.cobra[-1]
        obstaculos = set(self.jogo.cobra[1:-1])  # Exclui cauda como obstáculo
        return algoritmo_a(self.jogo.cabeca, cauda, self.jogo.tamanho_grade, obstaculos)

    def buscar_movimento_seguro(self) -> Optional[Direcao]:
        """Encontra qualquer movimento seguro como último recurso."""
        cabeca = self.jogo.cabeca
        conjunto_corpo = set(self.jogo.cobra)

        for direcao in Direcao:
            dx, dy = direcao.value
            nx, ny = cabeca[0] + dx, cabeca[1] + dy
            if (
                0 <= nx < self.jogo.tamanho_grade
                and 0 <= ny < self.jogo.tamanho_grade
                and (nx, ny) not in conjunto_corpo
            ):
                return direcao
        return None

    def proximo_movimento(self) -> Optional[Direcao]:
        """
        Decide o próximo movimento da cobra.

        Prioridade:
        1. Caminho A* até a moeda mais próxima
        2. Caminho A* até a própria cauda (sobrevivência)
        3. Qualquer movimento seguro
        """
        # Tenta ir até a moeda
        caminho = self.buscar_caminho_ate_moeda()
        if caminho:
            # Verifica se após seguir o caminho, a cobra ainda terá escape
            direcao = self.obter_direcao_do_caminho(caminho)
            if direcao:
                # Simula se o caminho é seguro: verifica se após comer
                # a moeda, existe caminho até a cauda
                if self._caminho_e_seguro(caminho):
                    return direcao

        # Fallback: segue a cauda para ganhar espaço
        caminho_cauda = self.buscar_caminho_ate_cauda()
        if caminho_cauda:
            direcao = self.obter_direcao_do_caminho(caminho_cauda)
            if direcao:
                return direcao

        # Último recurso: qualquer movimento seguro
        return self.buscar_movimento_seguro()

    def _caminho_e_seguro(self, caminho: list) -> bool:
        """
        Verifica se seguir o caminho até a moeda não deixa a cobra presa.
        Simula o movimento e verifica se haverá caminho de volta à cauda.
        """
        if len(caminho) <= 1:
            return True

        # Simula a cobra após percorrer todo o caminho
        cobra_simulada = list(self.jogo.cobra)
        posicoes_moedas = set(tuple(m) for m in self.jogo.moedas)

        for pos in caminho:
            cobra_simulada.insert(0, pos)
            if pos in posicoes_moedas:
                posicoes_moedas.discard(pos)
            else:
                cobra_simulada.pop()

        # Verifica se existe caminho da nova cabeça até a cauda simulada
        cabeca_sim = cobra_simulada[0]
        cauda_sim = cobra_simulada[-1]
        obstaculos_sim = set(cobra_simulada[1:-1])

        caminho_cauda = algoritmo_a(cabeca_sim, cauda_sim, self.jogo.tamanho_grade, obstaculos_sim)
        return caminho_cauda is not None
