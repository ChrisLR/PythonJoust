class HUD(object):
    def __init__(self, game):
        self.game = game
        sprite_loader = game.sprite_loader
        self.life_image = sprite_loader.get_image("life.png")
        self.digits_image = sprite_loader.get_sliced_sprites(21, 21, "digits.png")

    def draw(self):
        lives = self.game.lives
        score = self.game.score
        screen = self.game.screen
        self._draw_lives(lives, screen)
        self._draw_score(score, screen)

    def _draw_lives(self, lives, screen):
        start_x = 375
        for num in range(lives):
            x = start_x + num * 20
            screen.blit(self.life_image, [x, 570])

    def _draw_score(self, score, screen):
        digits_image = self.digits_image
        screen.blit(digits_image[score % 10], [353, 570])
        screen.blit(digits_image[(score % 100) // 10], [335, 570])
        screen.blit(digits_image[(score % 1000) // 100], [317, 570])
        screen.blit(digits_image[(score % 10000) // 1000], [299, 570])
        screen.blit(digits_image[(score % 100000) // 10000], [281, 570])
        screen.blit(digits_image[(score % 1000000) // 100000], [263, 570])
