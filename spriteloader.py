import pygame
import os


class Spriteloader(object):
    def __init__(self):
        self.image_names = [image_name for image_name in os.listdir("images")
                            if image_name.endswith(".png")]
        self.images = {image_name: pygame.image.load(os.path.join("images", image_name))
                       for image_name in self.image_names}

    def get_sliced_sprites(self, width, height, image_name):
        # returns a list of image frames sliced from file
        master_image = self.images.get(image_name)
        master_image = master_image.convert_alpha()
        master_width, master_height = master_image.get_size()
        sub_images = [master_image.subsurface((i * width, 0, width, height))
                      for i in range(int(master_width / width))]

        return sub_images

    def get_image(self, image_name):
        return self.images.get(image_name)
