import random

class Moeda:

    def __init__ (self,Imagem, TELA):
        # armazena a tela

        self.Imagem = Imagem
        self.TELA = TELA

        self.tela = TELA.get_rect().size
        #posiçao do x e y da moeda
        self.x = None
        self.y = None
        # importar a imagem da moeda e seu tamanho

        self.tamanho = self.Imagem.get_rect().size

        self.tem_moeda = False
        
    def pos_aleatoria(self,nave):
        x_usuario = nave.x
        y_usuario = nave.y
        obj_size = self.tela
        p_size = nave.tamanho
        x_obj, y_obj = random.randint(0, obj_size[0] - self.tamanho[0]), random.randint(0, obj_size[1] - self.tamanho[1])
        while (x_usuario <= x_obj and x_obj <= x_usuario + p_size[0]) and (y_usuario <= y_obj and y_obj <= y_usuario + p_size[1]):
            # Fazendo que nao va nascer no lugar do usuario
            x_obj, y_obj = random.randint(0, obj_size[0] - self.tamanho[0]), random.randint(0, obj_size[1] - self.tamanho[1])

        self.x = x_obj
        self.y = y_obj

    def aparecer(self, tempo_jogo, FPS, nave):
        if tempo_jogo % (3*FPS) == 0:  # isso indica a cada 3 segundos(60 por segundo)
            self.tem_moeda = True
            self.pos_aleatoria(nave)
    def desenhar(self):
        if self.tem_moeda:
            self.TELA.blit(self.Imagem, (self.x, self.y))