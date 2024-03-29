import pygame
import random
import menu
import os
import sys

def sp_play_game(size):

    pygame.init()

    width, height = size[0], size[1]
    block_size = 20

    black = (0, 0, 0)
    red = (230, 20, 20)
    green = (0, 255, 0)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('SinglePlayer Snake Game')


    main_theme = pygame.mixer.Sound(os.getcwd() + '\\sounds\\sound_track.mp3')
    channel0 = pygame.mixer.Channel(0)
    channel0.play(main_theme, loops=-1)

    get_point = pygame.mixer.Sound(os.getcwd() + '\\sounds\\get_point.mp3')
    channel1 = pygame.mixer.Channel(1)

    clock = pygame.time.Clock()

    def pause_game(current_direction):
        paused = True
        pause_font = pygame.font.Font(None, 72)
        toggle_text = True

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False

            clock.tick(5)
            pause_text = pause_font.render("GAME PAUSED", True, black)
            screen.blit(pause_text,
                        (width // 2 - pause_text.get_width() // 2, height // 2 - pause_text.get_height() // 2))

            if toggle_text:
                pause_text = pause_font.render("GAME PAUSED", True, green)
                screen.blit(pause_text,
                            (width // 2 - pause_text.get_width() // 2, height // 2 - pause_text.get_height() // 2))

            toggle_text = not toggle_text

            pygame.display.update()

        return paused, current_direction

    def display_points(points,color):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(f"Points: {points}", True, color)
        text_rect = text_surface.get_rect(topleft=(10, 10))
        screen.blit(text_surface, text_rect)

    def generate_food_position(snake_list):
        while True:
            food_x = round(random.randrange(0, width - block_size) / 20.0) * 20.0
            food_y = round(random.randrange(0, height - block_size) / 20.0) * 20.0
            if [food_x, food_y] not in snake_list:
                return food_x, food_y
    def gameLoop():
        fps = 12
        game_over = False
        game_paused = False
        first_move = True
        x, y = width / 2, height / 2
        x_change, y_change = 0, 0

        snake_list = []
        length_of_snake = 1

        food_x, food_y = generate_food_position(snake_list)

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_paused, last_direction = pause_game((x_change, y_change))

                    if not game_paused:
                        if first_move:
                            if event.key == pygame.K_UP:
                                x_change, y_change = 0, -block_size
                                first_move = False
                            elif event.key == pygame.K_DOWN:
                                x_change, y_change = 0, block_size
                                first_move = False
                            elif event.key == pygame.K_LEFT:
                                x_change, y_change = -block_size, 0
                                first_move = False
                            elif event.key == pygame.K_RIGHT:
                                x_change, y_change = block_size, 0
                                first_move = False
                        else:
                            if event.key == pygame.K_UP and (x_change != 0 and y_change != -block_size):
                                x_change, y_change = 0, -block_size
                            elif event.key == pygame.K_DOWN and (x_change != 0 and y_change != block_size):
                                x_change, y_change = 0, block_size
                            elif event.key == pygame.K_LEFT and (x_change != -block_size and y_change != 0):
                                x_change, y_change = -block_size, 0
                            elif event.key == pygame.K_RIGHT and (x_change != block_size and y_change != 0):
                                x_change, y_change = block_size, 0

            if not game_paused:
                x += x_change
                y += y_change

            if x >= width or x < 0 or y >= height or y < 0:
                game_over = True

            screen.fill(black)
            pygame.draw.rect(screen, red, [food_x, food_y, block_size, block_size])

            snake_head = [x, y]
            snake_list.append(snake_head)

            if len(snake_list) > length_of_snake:
                del snake_list[0]

            for segment in snake_list[:-1]:
                if segment == snake_head:
                    game_over = True

            for segment in snake_list:
                pygame.draw.rect(screen, green, [segment[0], segment[1], block_size, block_size])
                pygame.draw.rect(screen, black, [segment[0], segment[1], block_size, block_size], 1)

            display_points(length_of_snake - 1,green)

            pygame.display.update()

            if x == food_x and y == food_y:
                food_x, food_y = generate_food_position(snake_list)
                length_of_snake += 1
                channel1.play(get_point)
                if fps < 20:
                    fps += 2

            clock.tick(fps)
            pygame.display.update()

        menu.end_game('single', length_of_snake - 1, 0,size)
        pygame.quit()
        sys.exit()

    gameLoop()
