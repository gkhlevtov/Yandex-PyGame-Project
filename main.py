import os
import sys
from random import sample, choice  # Для выбора наборов карт

import pygame

# Полная колода карт
full_deck = (
    ['A', 'C', 'card_40.png'], ['A', 'D', 'card_27.png'], ['A', 'H', 'card_01.png'], ['A', 'S', 'card_14.png'],
    ['K', 'C', 'card_52.png'], ['K', 'D', 'card_39.png'], ['K', 'H', 'card_13.png'], ['K', 'S', 'card_26.png'],
    ['Q', 'C', 'card_51.png'], ['Q', 'D', 'card_38.png'], ['Q', 'H', 'card_12.png'], ['Q', 'S', 'card_25.png'],
    ['J', 'C', 'card_50.png'], ['J', 'D', 'card_37.png'], ['J', 'H', 'card_11.png'], ['J', 'S', 'card_24.png'],
    ['10', 'C', 'card_49.png'], ['10', 'D', 'card_36.png'], ['10', 'H', 'card_10.png'], ['10', 'S', 'card_23.png'],
    ['9', 'C', 'card_48.png'], ['9', 'D', 'card_35.png'], ['9', 'H', 'card_09.png'], ['9', 'S', 'card_22.png'],
    ['8', 'C', 'card_47.png'], ['8', 'D', 'card_34.png'], ['8', 'H', 'card_08.png'], ['8', 'S', 'card_21.png'],
    ['7', 'C', 'card_46.png'], ['7', 'D', 'card_33.png'], ['7', 'H', 'card_07.png'], ['7', 'S', 'card_20.png'],
    ['6', 'C', 'card_45.png'], ['6', 'D', 'card_32.png'], ['6', 'H', 'card_06.png'], ['6', 'S', 'card_19.png'],
    ['5', 'C', 'card_44.png'], ['5', 'D', 'card_31.png'], ['5', 'H', 'card_05.png'], ['5', 'S', 'card_18.png'],
    ['4', 'C', 'card_43.png'], ['4', 'D', 'card_30.png'], ['4', 'H', 'card_04.png'], ['4', 'S', 'card_17.png'],
    ['3', 'C', 'card_42.png'], ['3', 'D', 'card_29.png'], ['3', 'H', 'card_03.png'], ['3', 'S', 'card_16.png'],
    ['2', 'C', 'card_41.png'], ['2', 'D', 'card_28.png'], ['2', 'H', 'card_02.png'], ['2', 'S', 'card_15.png']
)


class Card(pygame.sprite.Sprite):
    """Класс для создания спрайта одной карты."""

    def __init__(self, *group, path, position, card_size=(225, 315)):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image(path), (card_size[0], card_size[1]))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    def update(self):
        """
        self.rect = self.rect.move(random.randrange(3) - 1,
                                   random.randrange(3) - 1)
        """


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


def update_sets(deck):
    """Функция обновления наборов карт."""

    game_set = sample(deck, k=5)

    player_set1 = []
    player_set2 = []

    while True:
        card = choice(deck)
        if card not in player_set1 and card not in game_set:
            player_set1.append(card)

        if len(player_set1) == 2:
            break

    while True:
        card = choice(deck)
        if card not in player_set1 and card not in player_set2 and card not in game_set:
            player_set2.append(card)

        if len(player_set2) == 2:
            break

    game_set_images = [x[2] for x in game_set]
    player_set1_images = [x[2] for x in player_set1]
    player_set2_images = [x[2] for x in player_set2]

    images = [game_set_images, player_set1_images, player_set2_images]

    return game_set, player_set1, player_set2, images


def draw_cards(screen, sprite_group, images, screen_size, card_size=(225, 315)):
    """Функция создания и отрисовки спрайтов карт."""

    screen_width, screen_height = screen_size
    w_percent, h_percent = screen_width // 100, screen_height // 100
    card_width, card_height = card_size
    center = (screen_width // 2, screen_height // 2)

    center_card_pos = center[0] - 6 * w_percent, center[1] - 40 * h_percent
    right_card1_pos = center_card_pos[0] - 36 * w_percent, center_card_pos[1]
    right_card2_pos = center_card_pos[0] - 18 * w_percent, center_card_pos[1]
    left_card1_pos = center_card_pos[0] + 18 * w_percent, center_card_pos[1]
    left_card2_pos = center_card_pos[0] + 36 * w_percent, center_card_pos[1]

    Card(sprite_group, path=images[0][0], position=right_card1_pos, card_size=card_size)
    Card(sprite_group, path=images[0][1], position=right_card2_pos, card_size=card_size)
    Card(sprite_group, path=images[0][2], position=center_card_pos, card_size=card_size)
    Card(sprite_group, path=images[0][3], position=left_card1_pos, card_size=card_size)
    Card(sprite_group, path=images[0][4], position=left_card2_pos, card_size=card_size)

    player_set_y = center[1] + 15 * h_percent
    set1_x = center[0] - 38 * w_percent
    set2_x = center[0] + 8 * w_percent
    indent = card_width + 6 * w_percent

    Card(sprite_group, path=images[1][0], position=(set1_x, player_set_y), card_size=card_size)
    Card(sprite_group, path=images[1][1], position=(set1_x + indent, player_set_y), card_size=card_size)
    Card(sprite_group, path=images[2][0], position=(set2_x, player_set_y), card_size=card_size)
    Card(sprite_group, path=images[2][1], position=(set2_x + indent, player_set_y), card_size=card_size)

    sprite_group.draw(screen)
    sprite_group.update()


def main():
    """Основная функция программы."""

    pygame.init()
    pygame.display.set_caption('GG Покерок')

    display_info = pygame.display.Info()
    display_width, display_height = display_info.current_w, display_info.current_h
    size = (display_width, display_height)

    print(display_width, display_height)

    card_width, card_height = 225 * display_width // 1920, 315 * display_height // 1080

    print(card_width, card_height)

    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

    background_image = load_image('background_big.jpg')
    scaled_background = pygame.transform.scale(background_image, (display_width, display_height))

    all_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    fps = 50
    running = True

    game_set, player_set1, player_set2, images = update_sets(full_deck)

    draw_cards(screen=screen, sprite_group=all_sprites, images=images, screen_size=size,
               card_size=(card_width, card_height))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_set, player_set1, player_set2, images = update_sets(full_deck)
                    draw_cards(screen=screen, sprite_group=all_sprites, images=images, screen_size=size,
                               card_size=(card_width, card_height))
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.blit(scaled_background, (0, 0))
        all_sprites.draw(screen)
        all_sprites.update()

        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
