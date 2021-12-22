import random

class Inimigo2:
    def __init__(self, imagem, TELA):

        self.TELA = TELA
        self.tela = TELA.get_rect().size
        
        self.imagem = imagem
        self.tamanho = imagem.get_rect().size


        self.rect = self.imagem.get_rect(
            center=(
                self.tela[0] - self.tamanho[0] // 2,
                random.randint(0 + self.tamanho[1] // 2, self.tela[1] - self.tamanho[1] // 2)
            )
        )
        
        self.x = self.rect.left
        self.y = self.rect.top

        self.velocidade = [-5, -11]

        self.aparecer = True

    def update(self):
        self.rect = self.rect.move(self.velocidade)

        if self.rect.left < 0 or self.rect.right > self.tela[0]:
            self.velocidade[0] *= -1
        if self.rect.top < 0 or self.rect.bottom > self.tela[1]:
            self.velocidade[1] *= -1
        
        self.x = self.rect.left
        self.y = self.rect.top
    
    def desenhar(self):
        if self.aparecer:
            self.TELA.blit(self.imagem, (self.x, self.y))