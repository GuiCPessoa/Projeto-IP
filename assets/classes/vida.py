import random
#Declara a vida que pode ser capturada pela nave , controlada pelo jogador. Atualmente a vida surge aleatoriamente na tela e fica parada. Caso tenha colisão com o jogador, deve ser contabilizado. Caso passe um tempo e o jogador n pegue a vida, **deve sumir e aparecer em outro lugar. 

class Vida:
    def __init__(self, imagem, tela):
        #ao inicializar a variável é necessário passar a largura e altura da tela e a posição inicial do jogador

        #salva a tela
        self.tela = tela
        self.tela_tamanho = tela.get_rect().size
        
        #determina o tamnho da imagem
        self.imagem = imagem
        self.tamanho = imagem.get_rect().size
        
        #posições iniciais
        self.x = None
        self.y = None
        #self.posicao = Vida.criar_posicao(player)

        self.aparecer = False

    def criar_posicao(self, nave):
        player_x = nave.x
        player_y = nave.y
        player_size = nave.tamanho
        #define uma posição aleatória para surgir o coração
        x = random.randint(0,self.tela_tamanho[0] - self.tamanho[0])
        y = random.randint(0,self.tela_tamanho[1] - self.tamanho[1])
        #chamar novamente se tiver junto do jogador
        if (player_x <= x and x <= player_x + player_size[0]) and (player_y<= y and y <= player_y + player_size[1]) :
            return self.criar_posicao(nave)
        else:
            self.x = x
            self.y = y 

    def sumir(self, tempo_decorrido, FPS):
        #se passou o tempo desejado (5s), mudar de posição
        if (tempo_decorrido % (10*FPS)) != 0 and (tempo_decorrido % (5*FPS)) == 0:
            #fazer a vida sumir ou mudar de posição
            #mudar de posição:
            self.aparecer = False          

    def surgir(self, tempo_decorrido, FPS, nave):
        if (tempo_decorrido % (10*FPS)) == 0 and (random.randint(1,100) <= 40):
            self.aparecer = True
            self.criar_posicao(nave)
 
    def desenhar(self):
        if self.aparecer:
            self.tela.blit(self.imagem, (self.x, self.y))