import pygame  # a biblioteca do pygame

# Os imports de pastas agora:
from assets.classes.enemyClass import *
from assets.classes.moeda import *
from assets.classes.vida import *
from assets.classes.nave import *
from assets.classes.inimigo2 import *
from assets.classes.game_text_menu import *

def dados_game(moeda_capturada, pontuacao, quantidade_vidas, tempo, VIDA, TELA_APP, FONTE):
    # Essa função serve para colocar os dados de coleta de moeda
    # Ou colisão com o inimigo, na tela

    message_coin = f'Moedas: {moeda_capturada}/99'
    formatted_text_coin = FONTE.render(message_coin, True, (255, 255, 255))

    message_enemy = f'Abates: {pontuacao}'
    formatted_text_enemy = FONTE.render(message_enemy, True, (255, 255, 255))

    message_time = f'Tempo: {tempo}s'
    formatted_text_time = FONTE.render(message_time, True, (255, 255, 255))

    TAM_VIDA = VIDA.get_rect().size
    for i in range(quantidade_vidas):
        TELA_APP.blit(VIDA, (i*TAM_VIDA[0], 0))

    TELA_APP.blit(formatted_text_coin, (770, 5))
    TELA_APP.blit(formatted_text_enemy, (370, 5))
    TELA_APP.blit(formatted_text_time, (560, 5))

#função de colisão com qualquer class
def colisao(x_a, y_a, tam_a, x_b, y_b, tam_b): # Checa se a e b colidem
    if (x_a <=  x_b + tam_b[0] and x_b <= x_a + tam_a[0]) and (y_a <=  y_b + tam_b[1] and y_b <= y_a + tam_a[1]):
        return True
    else:
        return False

LARGURA, ALTURA = 1000, 600  # Largura e altura da tela do aplicativo

TELA_APP = pygame.display.set_mode((LARGURA, ALTURA)) 
# Imagens
USUARIO = pygame.image.load("assets/imagens/ship.png")
INIMIGO1 = pygame.image.load("assets/imagens/ship_enemy_1.png")
INIMIGO2 = pygame.image.load("assets/imagens/ship_enemy_2.png") # Carrega a imagem do inimigo 1
MOEDA = pygame.image.load("assets/imagens/coin.png")
ATAQUE = pygame.image.load("assets/imagens/lazer.png")
VIDA = pygame.image.load("assets/imagens/health.png")
VIDA2 = pygame.image.load("assets/imagens/health2.png")
BACKGROUND = pygame.image.load("assets/imagens/galaxy_background.png") # Imagem do backgrond

pygame.init()
pygame.display.set_caption('The Galaxy War')

# pygame.mixer.init()
# musica_fundo = pygame.mixer.music.load('assets/sons/BoxCat Games - Mission.mp3')  # Buscando a música de fundo
# sound_effect_collect = pygame.mixer.Sound('assets/sons/smw_message_block.wav') # Coleta moeda
# sound_effect_lazer = pygame.mixer.Sound('assets/sons/Shofixti-Shot.wav') # atira com laser
# sound_effect_health = pygame.mixer.Sound('assets/sons/smw_kick.wav') #  pega vida
# pygame.mixer.music.play(-1) # Se passar menos -1 para a função, ela fica em Loop

pygame.font.init()  # Iniciando
FONTE_FILE = 'assets/8-BIT_WONDER.TTF'
FONTE = pygame.font.SysFont(FONTE_FILE, 35, True, True) 


FPS = 60
tempo_jogo = 0 
tempo_tela = 0  # O tempo que o app tá aberto
tela_aplicativo = 'tela_inicial' # Ela é dividida em: ['tela_inicial', 'jogo', 'pausa', 'tela_final']
app_fps = pygame.time.Clock()  

rodar_app = True  # Indica se o app tá rodando
jogo_text = Game_Text_and_Menu(rodar_app, tela_aplicativo == 'jogo', TELA_APP, FONTE_FILE)

while rodar_app:
    app_fps.tick(FPS)
    TELA_APP.fill((0, 0, 0))
    TELA_APP.blit(BACKGROUND, (0,0))

    if tela_aplicativo == 'tela_inicial':
        jogo_text.curr_menu.display_menu()

        if jogo_text.running == False:
            rodar_app = False
        
        if jogo_text.playing == True:
            tela_aplicativo = 'jogo'
            tempo_jogo = 0
            
    elif tela_aplicativo == 'jogo':
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodar_app = False

            if event.type == pygame.KEYDOWN: 
                if event.key == ord('p'):
                    tela_aplicativo = 'pausa'
                    jogo_text.paused = True
                    jogo_text.curr_menu = jogo_text.pause

        if tempo_jogo == 0:
            player = Nave(USUARIO, TELA_APP, ATAQUE)
            vida = Vida(VIDA, TELA_APP)
            moeda = Moeda(MOEDA, TELA_APP)
            lista_inimigos = []
            tempo_respawn = 3
            lista_inimigos.append(Enemy(INIMIGO1, TELA_APP))
        
        # Enquanto estiver no jogo, o tempo de jogo será contado (o tempo atual é (tempo_jogo - 1)/60 segundos)
        tempo_jogo += 1

        # Os controles dos tempos de Respawn dos inimigos
        if tempo_jogo % (int(round(tempo_respawn*FPS, 0))) == 0:
            lista_inimigos.append(Enemy(INIMIGO1, TELA_APP))

        if tempo_jogo//FPS >= 60 and (tempo_jogo % (10*FPS) == 0):
            lista_inimigos.append(Inimigo2(INIMIGO2, TELA_APP))

        if (tempo_jogo % (10*FPS) == 0) and tempo_respawn > 0.2:
            tempo_respawn = round(tempo_respawn - 0.1, 1)

        #surgir a vida
        vida.surgir(tempo_jogo, FPS, player)
        vida.sumir(tempo_jogo, FPS)


        #surgir moeda
        if player.moedas < 99:
            moeda.aparecer(tempo_jogo, FPS, player)
        elif player.moedas >= 99:
            tela_aplicativo = 'tela_final'

        if player.vida <= 0:
            tela_aplicativo = 'tela_final'
            jogo_text.playing = False

        # Checar colisão com a moeda
        if moeda.tem_moeda == True and colisao(player.x, player.y, player.tamanho, moeda.x, moeda.y, moeda.tamanho):
            player.moedas += 1
            moeda.tem_moeda = False  
            # sound_effect_collect.play()
        
        # Checar colisão com a vida
        if vida.aparecer == True and player.vida < 10 and colisao(player.x, player.y, player.tamanho, vida.x, vida.y, vida.tamanho):
            player.vida += 1
            vida.aparecer = False
            # sound_effect_health.play()

        # Checar colisão do inimigo com o player ou com o laser
        for i in range(len(lista_inimigos)):
            if colisao(player.x, player.y, player.tamanho, lista_inimigos[i].rect[0], lista_inimigos[i].rect[1], lista_inimigos[i].tamanho):
                player.vida -= 1
                lista_inimigos[i].aparecer = False 

            if player.tiro == True and colisao(player.tiroX, player.tiroY, player.tiroTamanho, lista_inimigos[i].rect[0], lista_inimigos[i].rect[1], lista_inimigos[i].tamanho):
                player.inimigos += 1
                player.tiro = False
                lista_inimigos[i].aparecer = False 

        # Fazer o movimento do player
        keys = pygame.key.get_pressed()

        # Efeito sonoro do tiro
        # if keys[pygame.K_SPACE] and not player.tiro: 
        #     sound_effect_lazer.play()

        #conrola o movimento do jogador
        player.controle(keys)

        # Fazer o movimento do inimigo
        for i in range(len(lista_inimigos)):
            lista_inimigos[i].update()

        # Remover o inimigo da lista de inimigos caso ele tenha sido destruído
        for inimigo in lista_inimigos:
            if inimigo.aparecer == False:
                lista_inimigos.remove(inimigo)

        # Mostra os dados de Coleta Moeda e Abates na tela
        dados_game(player.moedas, player.inimigos, player.vida, tempo_jogo//FPS,  VIDA2, TELA_APP, FONTE)

        # Desenhar a vida, a moeda os inimigos e o player
        vida.desenhar()
        moeda.desenhar()
        for inimigo in lista_inimigos:
            inimigo.desenhar()

        player.desenhar()

    # Desenha a tela caso o jogo esteja pausado
    elif tela_aplicativo == 'pausa':
        
        dados_game(player.moedas, player.inimigos, player.vida, tempo_jogo//FPS,  VIDA2, TELA_APP, FONTE)
        vida.desenhar()
        moeda.desenhar()
        for inimigo in lista_inimigos:
            inimigo.desenhar()
        player.desenhar()

        jogo_text.curr_menu.display_menu()
        
        if jogo_text.paused == False:
            tela_aplicativo = 'jogo'

        if jogo_text.playing == False:
            tela_aplicativo = 'tela_inicial'

    # Desenha a tela de final do jogo
    elif tela_aplicativo == 'tela_final':
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodar_app = False
                        
            if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        jogo_text.playing = False
                        jogo_text.paused = False
                        tela_aplicativo = 'tela_inicial'

        dados_game(player.moedas, player.inimigos, player.vida, tempo_jogo//FPS,  VIDA2, TELA_APP, FONTE)

        vida.desenhar()
        moeda.desenhar()
        for inimigo in lista_inimigos:
            inimigo.desenhar()

        player.desenhar()

        
        tempo_tela += 1

        if player.moedas < 99:
            jogo_text.draw_text('Obrigado por jogar', 40,
                            LARGURA//2, ALTURA//2)

            if (tempo_tela//(FPS//1.5)) % 2 == 0:
                jogo_text.draw_text('Aperte espaco para voltar ao Menu Inicial', 20,
                                LARGURA//2, ALTURA//2 + 50)
        else:
            jogo_text.draw_text('Parabens voce venceu', 40,
                            LARGURA//2, ALTURA//2 - 45)
            jogo_text.draw_text('Quanta habilidade', 20,
                            LARGURA//2, ALTURA//2 + 0)
            jogo_text.draw_text('Quanta superacao', 20,
                            LARGURA//2, ALTURA//2 + 25)
            jogo_text.draw_text('Voce esta de parabens', 20,
                            LARGURA//2, ALTURA//2 + 50)

            if (tempo_tela//(FPS//1.5)) % 2 == 0:
                jogo_text.draw_text('Aperte espaco para voltar ao Menu Inicial', 20,
                                LARGURA//2, ALTURA//2 + 90)
    
    # Aqui atualiza a tela inserindo todos os desenhos realizados pelo blit a cada rodar_app do while
    pygame.display.flip()


pygame.quit()
