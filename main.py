import pickle

import numpy as np
import pygame

import consts
from button_sprite import ButtonSprite
from chip_sprite import ChipSprite
from game import Game
import minimax
from round_sprite import RoundSprite
from simple_sprite import SimpleSprite

pygame.init()

window = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption('Młynek')

board = None
all_sprites = pygame.sprite.Group()
screen = None
game: Game = Game()
chips_positions = pygame.sprite.Group()
remaining_chips = pygame.sprite.Group()
chips = pygame.sprite.Group()
buttons = pygame.sprite.Group()


def refill_chips_positions():
    global chips_positions
    for chip in chips_positions:
        chip.kill()
    for i in range(0, 8):
        for j in range(0, 3):
            chips_positions.add(
                RoundSprite((0, 0, 0), consts.CHIP_RADIUS,
                            (consts.WIDTH / 2 + consts.CHIP_POSITIONS[i][j][0],
                             consts.HEIGHT / 2 + consts.CHIP_POSITIONS[i][j][1])))
    all_sprites.add(chips_positions)


def refill_remaining_chips():
    global remaining_chips
    for chip in remaining_chips:
        chip.kill()
    for i in range(1, 3):
        for j in range(0, 9):
            if i == 1 and game.chips_count[i] > 8 - j or i == 2 and game.chips_count[i] > j:
                remaining_chips.add(ChipSprite(i, (consts.WIDTH / 2 + consts.REMAINING_CHIPS_POSITIONS[i][j][0],
                                                   consts.HEIGHT / 2 + consts.REMAINING_CHIPS_POSITIONS[i][j][1]),
                                               consts.CHIP_RADIUS))
    all_sprites.add(remaining_chips)


def refill_chips():
    global chips, all_sprites
    for chip in chips:
        chip.kill()
    for i in range(0, 8):
        for j in range(0, 3):
            if game.get_configuration()[i * 3 + j] != 0:
                chips.add(ChipSprite(game.get_configuration()[i * 3 + j],
                                     chips_positions.sprites()[i * 3 + j].rect.center, consts.CHIP_RADIUS))
    all_sprites.add(chips)


def pos_on_window_to_pos_on_screen(pos, window):
    width = min(consts.WIDTH / consts.HEIGHT * window.get_height(), window.get_width())
    height = min(consts.HEIGHT / consts.WIDTH * window.get_width(), window.get_height())
    return (pos[0] - (window.get_width() - width) / 2) / width * consts.WIDTH, \
           (pos[1] - (window.get_height() - height) / 2) / height * consts.HEIGHT


def draw_borders(mouse_pos):
    for i in range(0, 8):
        for j in range(0, 3):
            if chips_positions.sprites()[i * 3 + j].rect.collidepoint(mouse_pos):
                pygame.draw.circle(screen, (0, 0, 0), chips_positions.sprites()[i * 3 + j].rect.center,
                                   chips_positions.sprites()[i * 3 + j].radius, 3)


dragging = False
dragging_chip = None
dragging_chip_pos = None
is_pressed = False
model = None
model_turns = []


def refill_buttons():
    global buttons, model_turns
    for button in buttons:
        button.kill()
    for i in range(1, 3):
        buttons.add(ButtonSprite(i, not (i in model_turns), (consts.WIDTH / 2 + consts.BUTTONS_POSITIONS[i][0],
                                                         consts.HEIGHT / 2 + consts.BUTTONS_POSITIONS[i][1]),
                                 consts.BUTTON_RADIUS))
    all_sprites.add(buttons)


def on_button_click(mouse_pos):
    global is_pressed, buttons, model_turns
    for button in buttons:
        if pygame.mouse.get_pressed()[0] and button.rect.collidepoint(mouse_pos) and not is_pressed:
            is_pressed = True
            if button.is_player:
                model_turns.append(button.player)
            else:
                model_turns.remove(button.player)
            button.is_player = not button.is_player
            refill_buttons()


def init():
    global board, all_sprites, screen, chips_positions, game, chips
    screen = pygame.Surface((consts.WIDTH, consts.HEIGHT))
    board_image = pygame.image.load("resources\\board.png")
    board_image = pygame.transform.scale(board_image, (consts.BOARD_WIDTH, consts.BOARD_HEIGHT))
    board = SimpleSprite(board_image, (consts.WIDTH / 2, consts.HEIGHT / 2))
    all_sprites = pygame.sprite.Group()
    all_sprites.add(board)
    refill_chips_positions()
    refill_remaining_chips()
    refill_chips()
    refill_buttons()
    game = Game()
    game.subscribe_on_change(refill_chips)
    game.subscribe_on_change(refill_remaining_chips)


init()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    screen = pygame.Surface((consts.WIDTH, consts.HEIGHT))
    screen.fill((255, 255, 255))
    all_sprites.update()
    all_sprites.draw(screen)

    # draw line of chips, representing number of chips left
    # for i in range(1, 3):
    #     for j in range(0, game.chips_count[i]):

    mouse_pos = pygame.mouse.get_pos()
    mouse_pos = pos_on_window_to_pos_on_screen(mouse_pos, window)
    draw_borders(mouse_pos)
    on_button_click(mouse_pos)

    if game.last_turn is not None:
        if isinstance(game.last_turn[0], tuple):
            print(game.last_turn)
            for i in range(0, 2):
                pygame.draw.circle(screen, consts.YELLOW, chips_positions.sprites()[
                    game.last_turn[i][0] * 3 + game.last_turn[i][1]].rect.center,
                                   chips_positions.sprites()[game.last_turn[i][0] * 3 + game.last_turn[i][1]].radius, 3)
        else:
            pygame.draw.circle(screen, consts.GREEN,
                               chips_positions.sprites()[game.last_turn[0] * 3 + game.last_turn[1]].rect.center,
                               chips_positions.sprites()[game.last_turn[0] * 3 + game.last_turn[1]].radius, 3)
    if game.last_removed is not None:
        pygame.draw.circle(screen, consts.RED,
                           chips_positions.sprites()[game.last_removed[0] * 3 + game.last_removed[1]].rect.center,
                           chips_positions.sprites()[game.last_removed[0] * 3 + game.last_removed[1]].radius, 3)


    if game.turn in model_turns:
        minimax.was_in = 0
        minimax.max_depth = 0
        score, move = minimax.minimax(game, game.turn)
        game.make_move(move)
    else:
        if dragging:
            dragging_chip.rect.center = mouse_pos

        if not pygame.mouse.get_pressed()[0]:
            is_pressed = False
            if dragging:
                dragging = False
                found = False
                for i in range(0, 8):
                    for j in range(0, 3):
                        if chips_positions.sprites()[i * 3 + j].rect.collidepoint(mouse_pos):
                            if game.can_move(game.turn, dragging_chip_pos, (i, j)):
                                dragging_chip.rect.center = chips_positions.sprites()[i * 3 + j].rect.center
                                game.should_remove = game.move_chip(game.turn, dragging_chip_pos, (i, j))
                                if not game.should_remove:
                                    game.end_turn()
                                found = True
                                break
                    if found:
                        break
                else:
                    dragging_chip.rect.center = chips_positions.sprites()[
                        dragging_chip_pos[0] * 3 + dragging_chip_pos[1]].rect.center
        if game.should_remove:
            if pygame.mouse.get_pressed()[0] and not is_pressed:
                is_pressed = True
                for i in range(0, 8):
                    for j in range(0, 3):
                        if chips_positions.sprites()[i * 3 + j].rect.collidepoint(mouse_pos):
                            if game.can_remove(game.turn, (i, j)):
                                game.should_remove = False
                                game.remove_chip(game.turn, (i, j))
                                game.end_turn()
                                break
        elif game.chips_count[game.turn] > 0:
            if pygame.mouse.get_pressed()[0] and not is_pressed:
                is_pressed = True
                for i in range(0, 8):
                    for j in range(0, 3):
                        if chips_positions.sprites()[i * 3 + j].rect.collidepoint(mouse_pos):
                            if game.can_put(game.turn, (i, j)):
                                game.should_remove = game.put_chip(game.turn, (i, j))
                                if not game.should_remove:
                                    game.end_turn()
                                break
        else:
            if pygame.mouse.get_pressed()[0] and not is_pressed:
                is_pressed = True
                for i in range(0, 8):
                    for j in range(0, 3):
                        if chips_positions.sprites()[i * 3 + j].rect.collidepoint(mouse_pos):
                            if game.chips[i][j] == game.turn:
                                dragging = True
                                for chip in chips.sprites():
                                    if chip.rect.collidepoint(chips_positions.sprites()[i * 3 + j].rect.center):
                                        dragging_chip = chip
                                        break
                                dragging_chip_pos = (i, j)
                                break

    if game.check_end():
        font = pygame.font.SysFont("comicsansms", 72)
        if game.check_win() != 0:
            text = font.render("Player " + str(game.check_win()) + " wins!", True, (0, 0, 0))
        else:
            text = font.render("Draw!", True, (0, 0, 0))
        screen.blit(text, (consts.WIDTH / 2 - text.get_width() / 2, consts.HEIGHT / 2 - text.get_height() / 2))

    width = min(consts.WIDTH / consts.HEIGHT * window.get_height(), window.get_width())
    height = min(consts.HEIGHT / consts.WIDTH * window.get_width(), window.get_height())
    window.fill((255, 255, 255))
    window.blit(
        pygame.transform.scale(screen, (width, height)),
        ((window.get_width() - width) / 2, (window.get_height() - height) / 2))
    pygame.display.flip()
