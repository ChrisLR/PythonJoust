import os

import pygame


class Spriteloader(object):
    image_folder = os.path.join("pythonjoust", "images")

    def __init__(self):
        self.image_names = [
            image_name for image_name in os.listdir(self.image_folder)
            if image_name.endswith(".png")
        ]
        self.images = {
            image_name: pygame.image.load(os.path.join(self.image_folder, image_name))
            for image_name in self.image_names
        }
        self.cached_slices = {}

    def get_sliced_sprites(self, width, height, image_name):
        key = (width, height, image_name)
        cached_slices = self.cached_slices.get(key)
        if cached_slices is not None:
            return cached_slices

        # returns a list of image frames sliced from file
        master_image = self.images.get(image_name).convert_alpha()
        master_width, master_height = master_image.get_size()
        image_slices = [master_image.subsurface((i * width, 0, width, height))
                        for i in range(int(master_width / width))]

        # Cache slices to avoid doing to work again
        self.cached_slices[key] = image_slices

        return image_slices

    def get_image(self, image_name):
        return self.images.get(image_name)
