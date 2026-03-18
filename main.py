import pygame
import sys
import time
from game import JogoCobra, EstadoJogo, Direcao
from ia_controller import ControladorIA

TAMANHO_GRADE = 30
TAMANHO_CELULA = 30
NUM_MOEDAS = 20
FPS = 12  # Quadros por segundo (velocidade da IA)

TAMANHO_JANELA = TAMANHO_GRADE * TAMANHO_CELULA
ALTURA_HUD = 60
LARGURA_TELA = TAMANHO_JANELA
ALTURA_TELA = TAMANHO_JANELA + ALTURA_HUD

COR_FUNDO = (18, 18, 24)
COR_GRADE = (30, 30, 42)
COR_COBRA_CABECA = (0, 230, 118)
COR_COBRA_CORPO = (0, 200, 83)
COR_COBRA_CORPO_ALT = (0, 180, 70)
COR_MOEDA = (255, 215, 0)
COR_MOEDA_BRILHO = (255, 235, 100)
COR_HUD_FUNDO = (25, 25, 35)
COR_TEXTO = (220, 220, 230)
COR_TEXTO_DESTAQUE = (0, 230, 118)
COR_FIM_DE_JOGO = (255, 82, 82)
COR_VITORIA = (0, 230, 118)
COR_CAMINHO = (70, 70, 120)

def desenhar_grade(tela):
    # Desenha as linhas da grade.
    for x in range(0, TAMANHO_JANELA, TAMANHO_CELULA):
        pygame.draw.line(tela, COR_GRADE, (x, ALTURA_HUD), (x, ALTURA_TELA))
    for y in range(ALTURA_HUD, ALTURA_TELA, TAMANHO_CELULA):
        pygame.draw.line(tela, COR_GRADE, (0, y), (TAMANHO_JANELA, y))


def desenhar_celula(tela, pos, cor, raio_borda=6):
    # Desenha uma célula na grade com bordas arredondadas.
    x, y = pos
    retangulo = pygame.Rect(
        x * TAMANHO_CELULA + 1,
        y * TAMANHO_CELULA + ALTURA_HUD + 1,
        TAMANHO_CELULA - 2,
        TAMANHO_CELULA - 2,
    )
    pygame.draw.rect(tela, cor, retangulo, border_radius=raio_borda)


def desenhar_cobra(tela, cobra):
    # Desenha a cobra com gradiente e destaque na cabeça.
    for i, segmento in enumerate(cobra):
        if i == 0:
            desenhar_celula(tela, segmento, COR_COBRA_CABECA, raio_borda=8)
            cx_cab, cy_cab = segmento
            cx = cx_cab * TAMANHO_CELULA + TAMANHO_CELULA // 2
            cy = cy_cab * TAMANHO_CELULA + ALTURA_HUD + TAMANHO_CELULA // 2
            pygame.draw.circle(tela, (255, 255, 255), (cx - 5, cy - 3), 4)
            pygame.draw.circle(tela, (255, 255, 255), (cx + 5, cy - 3), 4)
            pygame.draw.circle(tela, (0, 0, 0), (cx - 5, cy - 3), 2)
            pygame.draw.circle(tela, (0, 0, 0), (cx + 5, cy - 3), 2)
        else:
            cor = COR_COBRA_CORPO if i % 2 == 0 else COR_COBRA_CORPO_ALT
            desenhar_celula(tela, segmento, cor, raio_borda=5)


def desenhar_moedas(tela, moedas, contador_quadros):
    pulso = abs((contador_quadros % 40) - 20) / 20.0
    for moeda in moedas:
        cx = moeda[0] * TAMANHO_CELULA + TAMANHO_CELULA // 2
        cy = moeda[1] * TAMANHO_CELULA + ALTURA_HUD + TAMANHO_CELULA // 2

        raio_brilho = int(TAMANHO_CELULA * 0.5 + pulso * 3)
        superficie_brilho = pygame.Surface((raio_brilho * 2, raio_brilho * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            superficie_brilho,
            (*COR_MOEDA_BRILHO, int(40 + pulso * 30)),
            (raio_brilho, raio_brilho),
            raio_brilho,
        )
        tela.blit(superficie_brilho, (cx - raio_brilho, cy - raio_brilho))

        raio = int(TAMANHO_CELULA * 0.35)
        pygame.draw.circle(tela, COR_MOEDA, (cx, cy), raio)
        pygame.draw.circle(tela, (200, 170, 0), (cx, cy), raio, 2)

        fonte_pequena = pygame.font.SysFont("Arial", 12, bold=True)
        simbolo = fonte_pequena.render("$", True, (150, 120, 0))
        tela.blit(simbolo, (cx - simbolo.get_width() // 2, cy - simbolo.get_height() // 2))


def desenhar_caminho(tela, caminho):
    # Desenha o caminho que a IA está seguindo.
    for pos in caminho:
        cx = pos[0] * TAMANHO_CELULA + TAMANHO_CELULA // 2
        cy = pos[1] * TAMANHO_CELULA + ALTURA_HUD + TAMANHO_CELULA // 2
        pygame.draw.circle(tela, COR_CAMINHO, (cx, cy), 3)


def desenhar_hud(tela, pontuacao, total, estado):
    retangulo_hud = pygame.Rect(0, 0, LARGURA_TELA, ALTURA_HUD)
    pygame.draw.rect(tela, COR_HUD_FUNDO, retangulo_hud)
    pygame.draw.line(tela, COR_GRADE, (0, ALTURA_HUD), (LARGURA_TELA, ALTURA_HUD), 2)

    fonte_titulo = pygame.font.SysFont("Consolas", 22, bold=True)
    fonte_info = pygame.font.SysFont("Consolas", 16)

    titulo = fonte_titulo.render("SNAKE IA — A*", True, COR_TEXTO_DESTAQUE)
    tela.blit(titulo, (15, 8))

    texto_placar = fonte_info.render(f"Moedas: {pontuacao}/{total}", True, COR_TEXTO)
    tela.blit(texto_placar, (15, 35))

    if estado == EstadoJogo.JOGANDO:
        cor_status = COR_TEXTO_DESTAQUE
        status = "● IA jogando..."
    elif estado == EstadoJogo.VITORIA:
        cor_status = COR_VITORIA
        status = "★ VITÓRIA!"
    else:
        cor_status = COR_FIM_DE_JOGO
        status = "✖ GAME OVER"

    texto_status = fonte_info.render(status, True, cor_status)
    tela.blit(texto_status, (LARGURA_TELA - texto_status.get_width() - 15, 35))

    texto_FPS = fonte_info.render(f"Vel: {FPS} FPS", True, (100, 100, 120))
    tela.blit(texto_FPS, (LARGURA_TELA - texto_FPS.get_width() - 15, 10))


def desenhar_sobreposicao(tela, texto, cor):
    sobreposicao = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
    sobreposicao.fill((0, 0, 0, 160))
    tela.blit(sobreposicao, (0, 0))

    fonte_grande = pygame.font.SysFont("Consolas", 48, bold=True)
    fonte_pequena = pygame.font.SysFont("Consolas", 20)

    superficie_texto = fonte_grande.render(texto, True, cor)
    tela.blit(
        superficie_texto,
        (
            LARGURA_TELA // 2 - superficie_texto.get_width() // 2,
            ALTURA_TELA // 2 - 40,
        ),
    )

    texto_reiniciar = fonte_pequena.render("Pressione [R] para reiniciar ou [ESC] para sair", True, COR_TEXTO)
    tela.blit(
        texto_reiniciar,
        (
            LARGURA_TELA // 2 - texto_reiniciar.get_width() // 2,
            ALTURA_TELA // 2 + 25,
        ),
    )


def principal():
    global FPS

    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Snake IA — Algoritmo A*")
    relogio = pygame.time.Clock()

    jogo = JogoCobra(tamanho_grade=TAMANHO_GRADE, num_moedas=NUM_MOEDAS)
    ia = ControladorIA(jogo)
    contador_quadros = 0
    caminho_atual = []

    executando = True
    while executando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    executando = False
                elif evento.key == pygame.K_r:
                    jogo.reiniciar()
                    ia = ControladorIA(jogo)
                    caminho_atual = []
                elif evento.key == pygame.K_UP:
                    FPS = min(FPS + 2, 60)
                elif evento.key == pygame.K_DOWN:
                    FPS = max(FPS - 2, 2)

        if jogo.estado == EstadoJogo.JOGANDO:
            direcao = ia.proximo_movimento()
            if direcao:
                jogo.definir_direcao(direcao)
                caminho = ia.buscar_caminho_ate_moeda()
                caminho_atual = caminho if caminho else []
            jogo.passo()

        tela.fill(COR_FUNDO)
        desenhar_grade(tela)

        if caminho_atual and jogo.estado == EstadoJogo.JOGANDO:
            desenhar_caminho(tela, caminho_atual)

        desenhar_moedas(tela, jogo.moedas, contador_quadros)
        desenhar_cobra(tela, jogo.cobra)
        desenhar_hud(tela, jogo.pontuacao, jogo.total_moedas, jogo.estado)

        if jogo.estado == EstadoJogo.FIM_DE_JOGO:
            desenhar_sobreposicao(tela, "GAME OVER", COR_FIM_DE_JOGO)
        elif jogo.estado == EstadoJogo.VITORIA:
            desenhar_sobreposicao(tela, "VITÓRIA!", COR_VITORIA)

        pygame.display.flip()
        relogio.tick(FPS)
        contador_quadros += 1

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    principal()
