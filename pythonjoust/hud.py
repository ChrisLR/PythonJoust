class HUD(object):
    def __init__(self, game):
        self.game = game
        sprite_loader = game.sprite_loader
        self.life_image = sprite_loader.get_image("life.png")
        self.digits_image = sprite_loader.get_sliced_sprites(21, 21, "digits.png")

    def draw(self):
        lives = self.game.lives
        lives_2 = self.game.lives_2
        score = self.game.score
        score_2 = self.game.score_2
        screen = self.game.screen
        self._draw_lives(lives, screen, lives_2)
        self._draw_score(score, screen, score_2)

    def _draw_lives(self, lives, screen, lives_2):
        # TODO Must not copy pasta
        start_x = 375
        for num in range(lives):
            x = start_x + num * 20
            screen.blit(self.life_image, [x, 570])

        start_x = 600
        for num in range(lives_2):
            x = start_x + num * 20
            screen.blit(self.life_image, [x, 570])

    def _draw_score(self, score, screen, score_2):
        # TODO Must not copy pasta
        digits_image = self.digits_image
        screen.blit(digits_image[score % 10], [353, 570])
        screen.blit(digits_image[(score % 100) // 10], [335, 570])
        screen.blit(digits_image[(score % 1000) // 100], [317, 570])
        screen.blit(digits_image[(score % 10000) // 1000], [299, 570])
        screen.blit(digits_image[(score % 100000) // 10000], [281, 570])
        screen.blit(digits_image[(score % 1000000) // 100000], [263, 570])

        if self.game.two_players:
            screen.blit(digits_image[score_2 % 10], [577, 570])
            screen.blit(digits_image[(score_2 % 100) // 10], [559, 570])
            screen.blit(digits_image[(score_2 % 1000) // 100], [541, 570])
            screen.blit(digits_image[(score_2 % 10000) // 1000], [523, 570])
            screen.blit(digits_image[(score_2 % 100000) // 10000], [505, 570])
            screen.blit(digits_image[(score_2 % 1000000) // 100000], [487, 570])
