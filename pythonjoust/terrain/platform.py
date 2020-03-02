import pygame


class Platform(pygame.sprite.Sprite):
    render_priority = 1

    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)
        self.right = self.rect.right
        self.top = self.rect.top


class Bridge(pygame.sprite.Sprite):
    render_priority = 1

    def __init__(self, image, rect):
        super().__init__()
        self.image = pygame.transform.scale(image, (rect.width, rect.height))
        self.rect = rect
        self.x = rect.x
        self.y = rect.y
        self.right = self.rect.right
        self.top = self.rect.top
