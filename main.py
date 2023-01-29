import datetime as dt
import sys
from random import sample, choice  # Для выбора наборов карт

import pygame
from pygame import mixer

import best_combination
from globals import click_sound, full_deck, display_width, display_height, card_size
from globals import load_image


class Card(pygame.sprite.Sprite):
    """Класс для создания спрайта одной карты."""

    def __init__(self, *group, path, position, value, suit, screen, card_sizes=(225, 315)):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image(path), (card_sizes[0], card_sizes[1]))
        self.size = card_sizes
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.value = value
        self.suit = suit
        self.screen = screen

    def update(self, best_comb):
        """Отрисовка рамок у карт в комбинации, а также кикеров."""
        for card in best_comb[1]:
            value, suit = card[1], card[2]
            if self.value == value and self.suit == suit:
                size_percent = self.size[0] // 100
                stroke_pos = (self.rect.x - size_percent * 10,
                              self.rect.y - size_percent * 10,
                              self.size[0] + size_percent * 20,
                              self.size[1] + size_percent * 20)
                pygame.draw.rect(self.screen, (255, 0, 0), stroke_pos, size_percent * 5)
                break

        if best_comb[2]:
            for card in best_comb[2]:
                value, suit = card[1], card[2]
                if self.value == value and self.suit == suit:
                    size_percent = self.size[0] // 100
                    stroke_pos = (self.rect.x - size_percent * 10,
                                  self.rect.y - size_percent * 10,
                                  self.size[0] + size_percent * 20,
                                  self.size[1] + size_percent * 20)
                    pygame.draw.rect(self.screen, (0, 0, 0), stroke_pos, size_percent * 5)
                    break


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


def set_maker(game_set, player_set1, player_set2):
    """Функция подготовки данных для определения комбинации."""
    set1 = sorted(game_set + player_set1, key=lambda x: x[0])
    set1_values = [x[0] for x in set1]
    set1_suits = [x[1] for x in set1]

    set2 = sorted(game_set + player_set2, key=lambda x: x[0])
    set2_values = [x[0] for x in set2]
    set2_suits = [x[1] for x in set2]

    return (set1_values, set1_suits), (set2_values, set2_suits)


def draw_cards(screen, sprite_group, images, screen_size, game_set, player_set1, player_set2, card_sizes=(225, 315)):
    """Функция создания и отрисовки спрайтов карт."""

    all_cards = game_set + player_set1 + player_set2
    values = [x[0] for x in all_cards]
    suits = [x[1] for x in all_cards]

    screen_width, screen_height = screen_size
    w_percent, h_percent = screen_width // 100, screen_height // 100
    card_width, card_height = card_sizes
    center = (screen_width // 2, screen_height // 2)

    center_card_pos = center[0] - 6 * w_percent, center[1] - 40 * h_percent
    right_card1_pos = center_card_pos[0] - 36 * w_percent, center_card_pos[1]
    right_card2_pos = center_card_pos[0] - 18 * w_percent, center_card_pos[1]
    left_card1_pos = center_card_pos[0] + 18 * w_percent, center_card_pos[1]
    left_card2_pos = center_card_pos[0] + 36 * w_percent, center_card_pos[1]

    positions = [right_card1_pos, right_card2_pos, center_card_pos, left_card1_pos, left_card2_pos]
    for i in range(5):
        Card(sprite_group, path=images[0][i], position=positions[i], card_sizes=card_sizes,
             value=values[i], suit=suits[i], screen=screen)

    player_set_y = center[1] + 15 * h_percent
    set1_x = center[0] - 38 * w_percent
    set2_x = center[0] + 8 * w_percent
    indent = card_width + 6 * w_percent

    Card(sprite_group, path=images[1][0], position=(set1_x, player_set_y), card_sizes=card_sizes,
         value=values[5], suit=suits[5], screen=screen)
    Card(sprite_group, path=images[1][1], position=(set1_x + indent, player_set_y), card_sizes=card_sizes,
         value=values[6], suit=suits[6], screen=screen)
    Card(sprite_group, path=images[2][0], position=(set2_x, player_set_y), card_sizes=card_sizes,
         value=values[7], suit=suits[7], screen=screen)
    Card(sprite_group, path=images[2][1], position=(set2_x + indent, player_set_y), card_sizes=card_sizes,
         value=values[8], suit=suits[8], screen=screen)


def show_combination(comb, screen_size, screen):
    """Функция вывода названия лучшей комбинации на экран."""
    screen_width, screen_height = screen_size
    h_percent = screen_height // 100

    font = pygame.font.Font('fonts/Intro_Inline.otf', screen_height // 100 * 15)
    text = font.render(comb, True, (250, 150, 0))
    text_w = text.get_width()
    text_h = text.get_height()
    text_x = screen_width // 2 - text_w // 2
    text_y = screen_height // 2 - text_h // 2 + 5 * h_percent

    screen.blit(text, (text_x, text_y))


def show_score(score, screen_size, screen):
    """Функция вывода счёта на экран во время игры."""
    screen_width, screen_height = screen_size
    w_percent, h_percent = screen_width // 100, screen_height // 100

    font = pygame.font.Font('fonts/Intro.otf', screen_height // 100 * 7)
    text = font.render(f'Счёт: {score}', True, (250, 150, 0))
    text_x = 2 * w_percent
    text_y = 1 * h_percent

    screen.blit(text, (text_x, text_y))


def show_time(current_time, screen_size, screen):
    """Функция отрисовки таймера со временем"""
    screen_width, screen_height = screen_size
    w_percent, h_percent = screen_width // 100, screen_height // 100

    font = pygame.font.Font('fonts/Intro.otf', screen_height // 100 * 7)
    text = font.render(current_time, True, (250, 150, 0))
    text_x = 90 * w_percent
    text_y = 1 * h_percent

    screen.blit(text, (text_x, text_y))


def get_sets_positions(screen_size, card_sizes):
    """Функция определения координат позиций наборов карт."""
    screen_width, screen_height = screen_size
    w_percent, h_percent = screen_width // 100, screen_height // 100
    card_width, card_height = card_sizes
    center = (screen_width // 2, screen_height // 2)

    player_set_y = center[1] + 15 * h_percent
    set1_x = center[0] - 38 * w_percent
    set2_x = center[0] + 8 * w_percent
    indent = card_width + 6 * w_percent

    set1_up_pos = set1_x - 3 * w_percent, player_set_y - 3 * h_percent
    set2_up_pos = set2_x - 3 * w_percent, player_set_y - 3 * h_percent

    set1_down_pos = set1_x + indent + card_width + 3 * w_percent, player_set_y + card_height + 3 * h_percent
    set2_down_pos = set2_x + indent + card_width + 3 * w_percent, player_set_y + card_height + 3 * h_percent

    return set1_up_pos, set1_down_pos, set2_up_pos, set2_down_pos


def get_screen_zone(pos, sets_pos):
    """Функция определения нахождения курсора в игровых зонах."""
    zone = 0  # зона стола
    x, y = pos[0], pos[1]

    set1_up_pos, set1_down_pos, set2_up_pos, set2_down_pos = sets_pos

    if (set1_up_pos[0] <= x <= set1_down_pos[0]) and (set1_up_pos[1] <= y <= set1_down_pos[1]):
        zone = 1  # зона 1-ого набора
    elif (set2_up_pos[0] <= x <= set2_down_pos[0]) and (set2_up_pos[1] <= y <= set2_down_pos[1]):
        zone = 2  # зона 2-ого набора
    return zone


def draw_zone_border(zone, sets_pos, screen_size, card_sizes, screen):
    """Функция отрисовки обводки зон с наборами карт."""
    if zone != 0:
        screen_width, screen_height = screen_size
        w_percent, h_percent = screen_width // 100, screen_height // 100
        card_width, card_height = card_sizes
        size_percent = card_width // 100
        indent = card_width + 6 * w_percent

        set1_up_pos, set1_down_pos, set2_up_pos, set2_down_pos = sets_pos

        if zone == 1:
            pygame.draw.rect(screen, (255, 255, 255),
                             (set1_up_pos[0], set1_up_pos[1],
                              card_width + indent + 6 * w_percent, card_height + 6 * h_percent),
                             size_percent * 5)
        else:
            pygame.draw.rect(screen, (255, 255, 255),
                             (set2_up_pos[0], set2_up_pos[1],
                              card_width + indent + 6 * w_percent, card_height + 6 * h_percent),
                             size_percent * 5)


def draw_game_over_screen(score, screen_size, screen):
    """Функция отрисовки экрана окончания игры."""
    screen_width, screen_height = screen_size
    w_percent, h_percent = screen_width // 100, screen_height // 100

    font = pygame.font.Font('fonts/FiraSans-Bold.otf', screen_height // 100 * 20)
    line1 = font.render(f'Игра', True, (250, 150, 0))
    line2 = font.render(f'окончена', True, (250, 150, 0))
    line3 = font.render(f'Ваш счёт: {score}', True, (250, 150, 0))

    lines = [line1, line2, line3]

    for i in range(len(lines)):
        line = lines[i]
        text_w = line.get_width()
        text_h = line.get_height()
        text_x = screen_width // 2 - text_w // 2
        text_y = screen_height // 2 - text_h // 2 - 30 * h_percent + 25 * i * h_percent
        if i == 2:
            text_y += 5 * h_percent

        screen.blit(line, (text_x, text_y))


def draw_compare(win_comb, screen_size, screen):
    """Функция отрисовки сравнения комбинаций на столе"""
    screen_width, screen_height = screen_size
    w_percent, h_percent = screen_width // 100, screen_height // 100

    if win_comb == 'draw':
        symbol = '='
    elif win_comb == '1':
        symbol = '>'
    else:
        symbol = '<'

    font = pygame.font.Font('fonts/FiraSans-Bold.otf', screen_height // 100 * 25)
    text = font.render(symbol, True, (250, 150, 0))
    text_w = text.get_width()
    text_h = text.get_height()
    text_x = screen_width // 2 - text_w // 2
    text_y = screen_height // 2 - text_h // 2 + 30 * h_percent

    screen.blit(text, (text_x, text_y))


def get_best_combination(game_set, player_set1, player_set2):
    """
    Функция определения выигрышной комбинации из двух наборов
    с использованием функций best_combinations.
    """
    full_set1, full_set2 = set_maker(game_set, player_set1, player_set2)

    comb1 = best_combination.comb(*full_set1)
    comb2 = best_combination.comb(*full_set2)

    print(*comb1, sep='\t')
    print(*comb2, sep='\t', end='\n\n')

    best = best_combination.best_comb(*comb1, *comb2)
    if best == '1':
        win_comb = best_combination.output(*comb1)
        print('Первая выигрышная')

    elif best == '0':
        win_comb = best_combination.output(*comb2)
        print('Вторая выигрышная')
    else:
        best1 = best_combination.output(*comb1)
        best2 = best_combination.output(*comb2)
        win_comb = (best1[0], best1[1] + best2[1], best1[2] + best2[2])
        print('Ничья')

    print(win_comb)

    return win_comb, best


def main():
    """Основная функция программы."""

    pygame.init()
    mixer.init()

    cards_sound = mixer.Sound('sounds/mb_card_clear_04.mp3')
    time_over_sound = mixer.Sound('sounds/time_is_over.mp3')
    point_sound = mixer.Sound('sounds/point_plus.mp3')
    point_sound.set_volume(0.5)

    mixer.music.load('sounds/background_music_1.mp3')
    mixer.music.set_volume(0.1)
    mixer.music.play(-1)

    pygame.display.set_caption('GG Покерок')

    size = (display_width, display_height)

    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

    cursor_img = load_image("arrow.png")
    cursor_img = pygame.transform.scale(cursor_img, (40 * display_width // 1920, 70 * display_height // 1080))

    background_image = load_image('background_big.jpg')
    scaled_background = pygame.transform.scale(background_image, (display_width, display_height))

    cursor_img_rect = cursor_img.get_rect()

    sets_pos = get_sets_positions(size, card_size)

    start_time = dt.datetime.now()

    cards_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    fps = 60
    current_zone = 0
    running = True
    use_custom_cursor = True

    focused = False
    on_pause = True
    wait = False
    game_is_over = False

    current_score = 0
    table_zone = 0
    draw_border = False

    print('')
    print('=' * 100)

    game_set, player_set1, player_set2, images = update_sets(full_deck)

    cards_sound.play()

    draw_cards(screen=screen, sprite_group=cards_sprites, images=images,
               screen_size=size, card_sizes=card_size,
               game_set=game_set, player_set1=player_set1, player_set2=player_set2)

    win_comb = get_best_combination(game_set, player_set1, player_set2)
    best_set = win_comb[1]
    show_combination(win_comb[0][0], screen_size=size, screen=screen)
    show_score(current_score, screen_size=size, screen=screen)

    while running:
        if use_custom_cursor:
            pygame.mouse.set_visible(False)
            if pygame.mouse.get_focused():
                cursor_img_rect.center = pygame.mouse.get_pos()
                screen.blit(cursor_img, cursor_img_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                click_pos = pygame.mouse.get_pos()
                table_zone = get_screen_zone(click_pos, sets_pos)

                if on_pause:
                    on_pause = False
                else:
                    if wait:
                        cards_sound.play()
                        cards_sprites = pygame.sprite.Group()
                        game_set, player_set1, player_set2, images = update_sets(full_deck)

                        print(f'Текущие очки: {current_score}', end='\n\n')
                        print('=' * 100)

                        win_comb = get_best_combination(game_set, player_set1, player_set2)
                        best_set = win_comb[1]

                        draw_cards(screen=screen, sprite_group=cards_sprites, images=images,
                                   screen_size=size, card_sizes=card_size,
                                   game_set=game_set, player_set1=player_set1, player_set2=player_set2)

                        wait = False
                    if focused and table_zone != 0 and current_zone == table_zone:

                        wait = True
                        if best_set == 'draw':
                            current_score += 1
                            point_sound.play()

                        elif (best_set == '1' and table_zone == 1) or (best_set == '0' and table_zone == 2):
                            current_score += 1
                            point_sound.play()

                        else:
                            game_is_over = True

                        focused = False
                        draw_border = False

                    elif focused and table_zone == 0:
                        focused = False
                        draw_border = False
                    elif table_zone != 0:
                        focused = True
                        draw_border = True

                    current_zone = table_zone

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.blit(scaled_background, (0, 0))

        if game_is_over:
            screen.blit(scaled_background, (0, 0))
            mixer.music.fadeout(1000)
            break

        cards_sprites.draw(screen)

        if on_pause:
            start_time = dt.datetime.now()
            show_time('1:00', screen_size=size, screen=screen)
        else:
            current_date = dt.datetime.now()
            diff = current_date - start_time

            seconds = abs(diff.seconds - 59) % 60
            if seconds == 0:
                game_is_over = True
                time_over_sound.play()

            if len(str(seconds)) == 1:
                zero = '0'
            else:
                zero = ''

            show_time(str(f'0:{zero}{seconds}'), screen_size=size, screen=screen)

            if wait:
                show_combination(win_comb[0][0], screen_size=size, screen=screen)
                cards_sprites.update(win_comb[0])
                draw_compare(best_set, screen_size=size, screen=screen)

        show_score(current_score, screen_size=size, screen=screen)

        if draw_border:
            draw_zone_border(table_zone, sets_pos, screen_size=size, card_sizes=card_size, screen=screen)

        if use_custom_cursor:
            screen.blit(cursor_img, cursor_img_rect)

        clock.tick(fps)
        pygame.display.flip()

    print(f'Итоговый счёт: {current_score}')

    while running:
        screen.blit(scaled_background, (0, 0))
        draw_game_over_screen(current_score, screen_size=size, screen=screen)
        if use_custom_cursor:
            pygame.mouse.set_visible(False)
            if pygame.mouse.get_focused():
                cursor_img_rect.center = pygame.mouse.get_pos()
                screen.blit(cursor_img, cursor_img_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                sys.exit()

        clock.tick(fps)
        pygame.display.flip()


if __name__ == '__main__':
    main()
