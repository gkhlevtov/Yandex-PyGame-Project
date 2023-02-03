import sys

import pygame
from pygame import mixer

import menu as menu
from globals import Button, ImageButton
from globals import fps, \
    click_sound, button_sound, \
    display_width, display_height, \
    w_percent, h_percent
from globals import load_image, RunWindow, read_data, write_data


def volume_up():
    """Функция повышения громкости."""
    values = read_data('settings_values.txt')
    current_volume = int(values[0])
    if current_volume < 100:
        current_volume += 1

    values[0] = current_volume

    write_data('settings_values.txt', values)


def volume_down():
    """Функция понижения громкости."""
    values = read_data('settings_values.txt')
    current_volume = int(values[0])
    if current_volume > 0:
        current_volume -= 1

    values[0] = current_volume

    write_data('settings_values.txt', values)


def custom_cursor():
    """Функция включения игрового курсора."""
    values = read_data('settings_values.txt')
    values[1] = 1

    write_data('settings_values.txt', values)


def default_cursor():
    """Функция включения стандартного курсора."""
    values = read_data('settings_values.txt')
    values[1] = 0

    write_data('settings_values.txt', values)


def show_volume(screen_size, screen):
    """Функция вывода текста настроек на экран."""

    values = read_data('settings_values.txt')

    current_volume, cursor = int(values[0]), values[1]

    if cursor == '0':
        cursor = 'стандартный'
    else:
        cursor = 'игровой'

    screen_width, screen_height = screen_size
    w_percent, h_percent = screen_width // 100, screen_height // 100
    font = pygame.font.Font('fonts/Intro.otf', screen_height // 100 * 7)
    text1 = font.render(f'Громкость музыки: {current_volume}', True, (250, 150, 0))
    text1_x = 25 * w_percent
    text1_y = 28 * h_percent

    screen.blit(text1, (text1_x, text1_y))

    text2 = font.render(f'Выбран курсор: {cursor}', True, (250, 150, 0))
    text2_x = 25 * w_percent
    text2_y = 60 * h_percent

    screen.blit(text2, (text2_x, text2_y))


def main():
    """Основная функция программы."""

    pygame.init()
    mixer.init()

    volume = int(read_data('settings_values.txt')[0])

    mixer.music.load('sounds/background_music_1.mp3')
    mixer.music.set_volume(volume / 100)
    mixer.music.play(-1)

    pygame.display.set_caption('Настройки игры')

    size = (display_width, display_height)

    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

    cursor_img = load_image("arrow.png")
    cursor_img = pygame.transform.scale(cursor_img, (36 * display_width // 1920, 63 * display_height // 1080))

    cursor_img_rect = cursor_img.get_rect()

    background_image = load_image('background_big.jpg')
    scaled_background = pygame.transform.scale(background_image, (display_width, display_height))

    buttons = pygame.sprite.Group()
    button_sizes = (w_percent * 15, h_percent * 10)

    go_back_button = Button((w_percent * 4, h_percent * 15), button_sizes[0], button_sizes[1], (255, 173, 64), 'Назад',
                            h_percent * 7,
                            (0, 0, 0))

    go_back_button.set_func(RunWindow(menu).run)
    buttons.add(go_back_button)

    arrow_up_button = ImageButton((w_percent * 80, h_percent * 15),
                                  w_percent * 7, w_percent * 7,
                                  (255, 173, 64), 'Увеличить',
                                  h_percent * 7, (0, 0, 0), 'arrow_up.png')

    arrow_up_button.set_func(volume_up)
    buttons.add(arrow_up_button)

    arrow_down_button = ImageButton((w_percent * 80, h_percent * 35),
                                    w_percent * 7, w_percent * 7,
                                    (255, 173, 64), 'Уменьшить',
                                    h_percent * 7, (0, 0, 0), 'arrow_down.png')

    arrow_down_button.set_func(volume_down)
    buttons.add(arrow_down_button)

    default_cursor_button = ImageButton((w_percent * 25, h_percent * 75),
                                        w_percent * 8, w_percent * 8,
                                        (255, 173, 64), 'Стандартный',
                                        h_percent * 7, (0, 0, 0), 'default_cursor.png')

    default_cursor_button.set_func(default_cursor)
    buttons.add(default_cursor_button)

    custom_cursor_button = ImageButton((w_percent * 40, h_percent * 75),
                                       w_percent * 5, w_percent * 7,
                                       (255, 173, 64), 'Кастомный',
                                       h_percent * 7, (0, 0, 0), 'arrow.png')

    custom_cursor_button.set_func(custom_cursor)
    buttons.add(custom_cursor_button)

    clock = pygame.time.Clock()

    running = True

    while running:
        screen.blit(scaled_background, (0, 0))
        use_custom_cursor = read_data('settings_values.txt')[1]

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
                        else:
                            button.action()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        show_volume(screen_size=size, screen=screen)

        buttons.update()
        buttons.draw(screen)

        if pygame.mouse.get_focused() and use_custom_cursor == '1':
            cursor_img_rect.center = pygame.mouse.get_pos()
            screen.blit(cursor_img, cursor_img_rect)

        clock.tick(fps)
        pygame.display.flip()


if __name__ == '__main__':
    sys.exit(main())
