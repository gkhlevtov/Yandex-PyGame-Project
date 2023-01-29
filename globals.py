import os
import sys

import pygame
import pygame.mixer as mixer

pygame.init()
mixer.init()


def load_image(filename, color_key=None):
    """Функция загрузки изображения в pygame."""

    fullname = os.path.join('images', filename)

    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)

    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


click_sound = mixer.Sound('sounds/click.mp3')

display_info = pygame.display.Info()
display_width, display_height = display_info.current_w, display_info.current_h

card_size = 225 * display_width // 1920, 315 * display_height // 1080

# Полная колода карт
full_deck = (
    [14, 'C', 'card_40.png'], [14, 'D', 'card_27.png'], [14, 'H', 'card_01.png'], [14, 'S', 'card_14.png'],
    [13, 'C', 'card_52.png'], [13, 'D', 'card_39.png'], [13, 'H', 'card_13.png'], [13, 'S', 'card_26.png'],
    [12, 'C', 'card_51.png'], [12, 'D', 'card_38.png'], [12, 'H', 'card_12.png'], [12, 'S', 'card_25.png'],
    [11, 'C', 'card_50.png'], [11, 'D', 'card_37.png'], [11, 'H', 'card_11.png'], [11, 'S', 'card_24.png'],
    [10, 'C', 'card_49.png'], [10, 'D', 'card_36.png'], [10, 'H', 'card_10.png'], [10, 'S', 'card_23.png'],
    [9, 'C', 'card_48.png'], [9, 'D', 'card_35.png'], [9, 'H', 'card_09.png'], [9, 'S', 'card_22.png'],
    [8, 'C', 'card_47.png'], [8, 'D', 'card_34.png'], [8, 'H', 'card_08.png'], [8, 'S', 'card_21.png'],
    [7, 'C', 'card_46.png'], [7, 'D', 'card_33.png'], [7, 'H', 'card_07.png'], [7, 'S', 'card_20.png'],
    [6, 'C', 'card_45.png'], [6, 'D', 'card_32.png'], [6, 'H', 'card_06.png'], [6, 'S', 'card_19.png'],
    [5, 'C', 'card_44.png'], [5, 'D', 'card_31.png'], [5, 'H', 'card_05.png'], [5, 'S', 'card_18.png'],
    [4, 'C', 'card_43.png'], [4, 'D', 'card_30.png'], [4, 'H', 'card_04.png'], [4, 'S', 'card_17.png'],
    [3, 'C', 'card_42.png'], [3, 'D', 'card_29.png'], [3, 'H', 'card_03.png'], [3, 'S', 'card_16.png'],
    [2, 'C', 'card_41.png'], [2, 'D', 'card_28.png'], [2, 'H', 'card_02.png'], [2, 'S', 'card_15.png']
)
