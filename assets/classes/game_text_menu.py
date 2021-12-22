# Importações
import pygame
from assets.classes.menu import *

class Game_Text_and_Menu():
    def __init__(self, running, playing, TELA, FONTE_FILE):
        pygame.init()

        self.running = running  # Será verdadeira quando o jogo estiver ligado
        self.playing = playing  # Quando o jogador estiver jogando
        self.paused = False

        # Iteração através do menu
        # A ideia é que quando o jogador soltar uma dessas teclas, elas vão ser definidas como verdadeiras
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

        # Largura e Altura de exibição
        self.DISPLAY_W, self.DISPLAY_H = TELA.get_rect().size

        # Criando o display de acordo com o tamanho que escolhemos
        self.display = TELA

        # Fonte
        self.font_name = FONTE_FILE

        # Color
        self.WHITE = (255, 255, 255)

        # Só pra referenciar, não vai ser alterado
        self.main_menu = MainMenu(self)
        self.credits = CreditsMenu(self)
        self.pause = MenuPause(self)
        # Permite que essa variável do menu atual, mude dependendo do menu em q ela estiver
        self.curr_menu = self.main_menu

    def check_eventos(self):  # Verificando as entradas do jogador
        for event in pygame.event.get():  # Percorre uma lista de tudo oq o jogador pode fazer

            # Verificando tecla a tecla
            if event.type == pygame.QUIT:  # Verificando se o jogador clicou no X, no topo da tela
                self.running, self.playing = False, False
                # Vai impedir de qualquer menu que esteja em execução, seja executado
                self.curr_menu.run_display = False

            if event.type == pygame.KEYDOWN:  # Verificando se aquelas teclas foram pressionadas
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self.START_KEY = True
                if event.key == pygame.K_ESCAPE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def restart_keys(self):  # Voltando todas para False, só será verdadeira quando entrar no loop
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    # Só serve pra desenhar na tela, sem isso fica tudo preto
    def draw_text(self, text, size, x, y):
        # Paramentros, texto, tamanho, e uma posição X/Y para desenhar em relação à tela
        fonte = pygame.font.Font(self.font_name, size)

        # Imagem retangular do texto
        texto_superfice = fonte.render(text, True, self.WHITE)

        # Paramentros de tamanho e posição na tela
        texto_rect = texto_superfice.get_rect()

        texto_rect.center = (x, y)  # Centraliza de acordo com a posição

        # Colocando o texto na tela
        self.display.blit(texto_superfice, texto_rect)