class HUD(object):
    def __init__(self, game):
        self.game = game
        sprite_loader = game.sprite_loader
        self.life_image = sprite_loader.get_image("life.png")
        self.digits_image = sprite_loader.get_sliced_sprites(21, 21, "digits.png")

    def draw(self):
        screen = self.game.screen
        for i, player in enumerate(self.game.players):
            lives = player.lives
            score = player.score
            self._draw_lives(lives, screen, i)
            self._draw_score(score, screen, i)

    def _draw_lives(self, lives, screen, player_no=0):
        # TODO Could support more than two players
        start_x = 375 if player_no == 0 else 615
        for num in range(lives):
            x = start_x + num * 20
            screen.blit(self.life_image, [x, 570])

    def _draw_score(self, score, screen, player_no=0):
        start_x = 353 if player_no == 0 else 590
        # TODO Could support more than two players
        digits_image = self.digits_image
        screen.blit(digits_image[score % 10], [start_x, 570])
        screen.blit(digits_image[(score % 100) // 10], [start_x - 20, 570])
        screen.blit(digits_image[(score % 1000) // 100], [start_x - 40, 570])
        screen.blit(digits_image[(score % 10000) // 1000], [start_x - 60, 570])
        screen.blit(digits_image[(score % 100000) // 10000], [start_x - 80, 570])
        screen.blit(digits_image[(score % 1000000) // 100000], [start_x - 100, 570])
