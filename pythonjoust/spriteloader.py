import os

import pygame


class Spriteloader(object):
    image_folder = os.path.join("pythonjoust", "images")
    alt_image_folder = os.path.join("pythonjoust", "alt_images")

    def __init__(self, game):
        self.game = game
        self.cached_slices = {}
        self.image_names = None
        self.images = None
        self.alt_image_names = None
        self.alt_images = None
        self.load_images()
        self.load_alt_images()

    def load_images(self):
        self.image_names = [
            image_name for image_name in os.listdir(self.image_folder)
            if image_name.endswith(".png")
        ]
        self.images = {
            image_name: pygame.image.load(os.path.join(self.image_folder, image_name)).convert_alpha()
            for image_name in self.image_names
        }

    def load_alt_images(self):
        if not self.game.options.use_alt_sprites:
            return

        self.alt_image_names = [
            image_name for image_name in os.listdir(self.alt_image_folder)
            if image_name.endswith(".png")
        ]
        self.alt_images = {
            image_name: pygame.image.load(os.path.join(self.alt_image_folder, image_name)).convert_alpha()
            for image_name in self.alt_image_names
        }

    def get_autosized_sliced_sprites(self, image_name, slice_number):
        if self.game.options.use_alt_sprites:
            master_image = self.alt_images.get(image_name, self.images.get(image_name))
        else:
            master_image = self.images.get(image_name)
        master_width, master_height = master_image.get_size()
        width = int(master_width / slice_number)
        height = master_height

        return self.get_sliced_sprites(width, height, image_name)

    def get_sliced_sprites(self, width, height, image_name):
        key = (width, height, image_name)
        cached_slices = self.cached_slices.get(key)
        if cached_slices is not None:
            return cached_slices

        if self.game.options.use_alt_sprites:
            # Substitute alternate images instead of original ones
            master_image = self.alt_images.get(image_name, self.images.get(image_name))
        else:
            master_image = self.images.get(image_name)

        # returns a list of image frames sliced from file
        master_width, master_height = master_image.get_size()
        image_slices = [master_image.subsurface((i * width, 0, width, height))
                        for i in range(int(master_width / width))]

        # Cache slices to avoid doing to work again
        self.cached_slices[key] = image_slices

        return image_slices

    def get_image(self, image_name):
        return self.images.get(image_name)
