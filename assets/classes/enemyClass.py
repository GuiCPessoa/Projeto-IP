import random


class Enemy:

    def __init__(self, image, TELA):
        self.aparecer = True
        self.image = image
        self.tamanho = self.image.get_rect().size
        self.TELA = TELA
        self.tela = TELA.get_rect().size
        self.rect = self.image.get_rect(
            center=(
                self.tela[0] - self.tamanho[0] // 2,
                random.randint(0 + self.tamanho[1] // 2, self.tela[1] - self.tamanho[1] // 2)
            )
        )

        self.speed = random.randint(3, 10)

    def update(self):
        self.rect.left -= self.speed
        if self.rect.left < 0:
            self.aparecer = False

    def desenhar(self):
        self.TELA.blit(self.image, (self.rect.left, self.rect.top))
