"""
game.py — Lógica central do jogo Snake.
"""

import random
from enum import Enum
from typing import Optional


class Direcao(Enum):
    CIMA = (0, -1)
    BAIXO = (0, 1)
    ESQUERDA = (-1, 0)
    DIREITA = (1, 0)


class EstadoJogo(Enum):
    JOGANDO = "jogando"
    VITORIA = "vitoria"
    FIM_DE_JOGO = "fim_de_jogo"


class JogoCobra:
    """Jogo Snake com grade, cobra, moedas e detecção de colisão."""

    def __init__(self, tamanho_grade: int = 20, num_moedas: int = 10):
        self.tamanho_grade = tamanho_grade
        self.num_moedas = num_moedas
        self.reiniciar()

    def reiniciar(self):
        """Reinicia o jogo para o estado inicial."""
        meio = self.tamanho_grade // 2
        self.cobra = [(meio, meio), (meio - 1, meio), (meio - 2, meio)]
        self.direcao = Direcao.DIREITA
        self.estado = EstadoJogo.JOGANDO
        self.pontuacao = 0
        self.total_moedas = self.num_moedas
        self.moedas = []
        self._posicionar_moedas()

    def _posicionar_moedas(self):
        """Posiciona moedas em posições aleatórias livres na grade."""
        ocupadas = set(self.cobra)
        livres = [
            (x, y)
            for x in range(self.tamanho_grade)
            for y in range(self.tamanho_grade)
            if (x, y) not in ocupadas
        ]
        random.shuffle(livres)
        self.moedas = livres[: self.num_moedas]

    @property
    def cabeca(self):
        """Retorna a posição da cabeça da cobra."""
        return self.cobra[0]

    def obter_obstaculos(self) -> set:
        """Retorna o conjunto de posições ocupadas pelo corpo da cobra (exceto cabeça)."""
        return set(self.cobra[1:])

    def definir_direcao(self, direcao: Direcao):
        """Define a direção de movimento (impede inversão de 180°)."""
        oposta = {
            Direcao.CIMA: Direcao.BAIXO,
            Direcao.BAIXO: Direcao.CIMA,
            Direcao.ESQUERDA: Direcao.DIREITA,
            Direcao.DIREITA: Direcao.ESQUERDA,
        }
        if direcao != oposta.get(self.direcao):
            self.direcao = direcao

    def passo(self) -> EstadoJogo:
        """Executa um passo do jogo: move a cobra, verifica colisões e coleta moedas."""
        if self.estado != EstadoJogo.JOGANDO:
            return self.estado

        # Calcula nova posição da cabeça
        dx, dy = self.direcao.value
        nova_cabeca = (self.cabeca[0] + dx, self.cabeca[1] + dy)

        # Verifica colisão com paredes
        if not (0 <= nova_cabeca[0] < self.tamanho_grade and 0 <= nova_cabeca[1] < self.tamanho_grade):
            self.estado = EstadoJogo.FIM_DE_JOGO
            return self.estado

        # Verifica colisão consigo mesma
        if nova_cabeca in self.cobra[:-1]:
            self.estado = EstadoJogo.FIM_DE_JOGO
            return self.estado

        # Move a cobra
        self.cobra.insert(0, nova_cabeca)

        # Verifica coleta de moeda
        if nova_cabeca in self.moedas:
            self.moedas.remove(nova_cabeca)
            self.pontuacao += 1
            # Verifica vitória
            if not self.moedas:
                self.estado = EstadoJogo.VITORIA
        else:
            self.cobra.pop()  # Remove a cauda se não coletou moeda

        return self.estado

    def obter_moeda_mais_proxima(self) -> Optional[tuple]:
        """Retorna a moeda mais próxima da cabeça usando distância Manhattan."""
        if not self.moedas:
            return None
        return min(
            self.moedas,
            key=lambda m: abs(m[0] - self.cabeca[0]) + abs(m[1] - self.cabeca[1]),
        )
