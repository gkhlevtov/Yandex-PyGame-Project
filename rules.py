import sys

import pygame
from pygame import mixer

import menu as menu
from globals import Button
from globals import fps, \
    click_sound, button_sound, \
    display_width, display_height, \
    w_percent, h_percent, card_size
from globals import load_image, RunWindow, read_data, read_rules


def show_rules(screen_size, screen, number=1, card_sizes=(225, 315)):
    """Функция вывода текста правил на экран."""

    rules = read_rules('rules.txt')
    size_percent = card_sizes[0] // 100
    card_sizes = (card_sizes[0] - size_percent * 30, card_sizes[1] - size_percent * 30)

    screen_width, screen_height = screen_size
    w_percent, h_percent = screen_width // 100, screen_height // 100
    font = pygame.font.Font('fonts/FiraSans-Bold.otf', screen_height // 100 * 5)

    text_x = 20 * w_percent

    if number == 1:
        text_y = -2 * h_percent

        for i in range(2):
            text_y += 5 * h_percent
            text = font.render(rules[i], True, (250, 150, 0))
            screen.blit(text, (text_x, text_y))

        text_y += 3 * h_percent

        text_x = 2 * w_percent
        for i in range(2, 7):
            text_y += 5 * h_percent
            text = font.render(rules[i], True, (250, 150, 0))
            screen.blit(text, (text_x, text_y))

        text_y += 3 * h_percent

        for i in range(7, 10):
            text_y += 5 * h_percent
            text = font.render(rules[i], True, (250, 150, 0))
            screen.blit(text, (text_x, text_y))

        text_y += 10 * h_percent
        for i in ['01', '52', '28', '17', '09']:
            image = pygame.transform.scale(load_image(f'card_{i}.png'), card_sizes)
            screen.blit(image, (text_x, text_y))
            text_x += 15 * w_percent

    elif number == 2:
        text_y = -2 * h_percent

        for i in range(10, 12):
            text_y += 5 * h_percent
            text = font.render(rules[i], True, (250, 150, 0))
            screen.blit(text, (text_x, text_y))

        text_y += 3 * h_percent
        text_x = 2 * w_percent

        for i in range(12, 22):
            text_y += 5 * h_percent
            text = font.render(rules[i], True, (250, 150, 0))
            screen.blit(text, (text_x, text_y))

        text_y += 3 * h_percent

        for i in range(22, 24):
            text_y += 5 * h_percent
            text = font.render(rules[i], True, (250, 150, 0))
            screen.blit(text, (text_x, text_y))

        text_y += 3 * h_percent

        for i in range(24, 27):
            text_y += 5 * h_percent
            text = font.render(rules[i], True, (250, 150, 0))
            screen.blit(text, (text_x, text_y))

    elif number == 3:
        text_y = -2 * h_percent

        for i in range(27, 29):
            text_y += 5 * h_percent
            text = font.render(rules[i], True, (250, 150, 0))
            screen.blit(text, (text_x, text_y))

        text_x = 2 * w_percent
        text_y += 3 * h_percent

        for i in range(29, 33):
            text_y += 5 * h_percent
            text = font.render(rules[i], True, (250, 150, 0))
            screen.blit(text, (text_x, text_y))

        text_y += 3 * h_percent

        for i in range(33, 36):
            text_y += 5 * h_percent
            text = font.render(rules[i], True, (250, 150, 0))
            screen.blit(text, (text_x, text_y))

        text_y += 3 * h_percent

        for i in range(36, 38):
            text_y += 5 * h_percent
            text = font.render(rules[i], True, (250, 150, 0))
            screen.blit(text, (text_x, text_y))


def go_to_page1():
    """Функция выбора первой страницы правил."""
    return 1


def go_to_page2():
    """Функция выбора второй страницы правил."""
    return 2


def go_to_page3():
    """Функция выбора третьей страницы правил."""
    return 3


def main():
    """Основная функция программы."""

    pygame.init()
    mixer.init()

    pygame.display.set_caption('Настройки игры')

    size = (display_width, display_height)

    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

    cursor_img = load_image("arrow.png")
    cursor_img = pygame.transform.scale(cursor_img, (36 * display_width // 1920, 63 * display_height // 1080))

    cursor_img_rect = cursor_img.get_rect()

    background_image = load_image('background_big.jpg')
    scaled_background = pygame.transform.scale(background_image, (display_width, display_height))

    current_page = 1

    buttons = pygame.sprite.Group()
    button_sizes = (w_percent * 15, h_percent * 10)

    go_back_button = Button((w_percent * 2, h_percent * 4), button_sizes[0], button_sizes[1], (255, 173, 64), 'Назад',
                            h_percent * 7,
                            (0, 0, 0))

    go_back_button.set_func(RunWindow(menu).run)
    buttons.add(go_back_button)

    page_1_button = Button((w_percent * 95, h_percent * 5), 5 * w_percent, 5 * w_percent, (255, 173, 64), '1',
                           h_percent * 7,
                           (0, 0, 0))
    page_1_button.set_func(go_to_page1)
    buttons.add(page_1_button)

    page_2_button = Button((w_percent * 95, h_percent * 20), 5 * w_percent, 5 * w_percent, (255, 173, 64), '2',
                           h_percent * 7,
                           (0, 0, 0))

    page_2_button.set_func(go_to_page2)
    buttons.add(page_2_button)

    page_3_button = Button((w_percent * 95, h_percent * 35), 5 * w_percent, 5 * w_percent, (255, 173, 64), '3',
                           h_percent * 7,
                           (0, 0, 0))

    page_3_button.set_func(go_to_page3)
    buttons.add(page_3_button)

    clock = pygame.time.Clock()

    running = True
    use_custom_cursor = read_data('settings_values.txt')[1]

    while running:
        screen.blit(scaled_background, (0, 0))

        if use_custom_cursor == '1':
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.check_mouse_position((pos[0], pos[1])):
                        button.set_color(True)
                        break
                    else:
                        button.set_color(False)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                click_pos = pygame.mouse.get_pos()

                for button in buttons:
                    if button.check_mouse_position(click_pos):
                        button_sound.play()
                        if button.func is None:
                            print('Nothing happened')
                        if button.func in [go_to_page1, go_to_page2, go_to_page3]:
                            current_page = button.action()
                        else:
                            button.action()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        show_rules(screen_size=size, screen=screen, number=current_page, card_sizes=card_size)
        buttons.update()
        buttons.draw(screen)

        if pygame.mouse.get_focused() and use_custom_cursor == '1':
            cursor_img_rect.center = pygame.mouse.get_pos()
            screen.blit(cursor_img, cursor_img_rect)

        clock.tick(fps)
        pygame.display.flip()


if __name__ == '__main__':
    sys.exit(main())
