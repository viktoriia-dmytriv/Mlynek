import pygame

import globals
from game import Game
from round_sprite import RoundSprite
from simple_sprite import SimpleSprite

pygame.init()

window = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption('Młynek')

board = None
all_sprites = None
screen = None
game = None
chips_positions = None
chips = None


def refill_chips_positions():
    global chips_positions
    chips_positions = pygame.sprite.Group()
    for i in range(0, 8):
        for j in range(0, 3):
            chips_positions.add(
                RoundSprite((0, 0, 0), 20,
                            (globals.WIDTH / 2 + globals.CHIP_POSITIONS[i][j][0] * globals.BOARD_WIDTH / 2,
                             globals.HEIGHT / 2 + globals.CHIP_POSITIONS[i][j][1] * globals.BOARD_HEIGHT / 2)))


def init():
    global board, all_sprites, screen, chips_positions, game, chips
    screen = pygame.Surface((globals.WIDTH, globals.HEIGHT))
    board_image = pygame.image.load("resources\Board.png")
    board_image = pygame.transform.scale(board_image, (globals.BOARD_WIDTH, globals.BOARD_HEIGHT))
    board = SimpleSprite(board_image, (globals.WIDTH / 2, globals.HEIGHT / 2))
    all_sprites = pygame.sprite.Group()
    all_sprites.add(board)
    refill_chips_positions()
    all_sprites.add(chips_positions)
    chips = pygame.sprite.Group()
    game = Game()


def pos_on_window_to_pos_on_screen(pos, window):
    width = min(globals.WIDTH / globals.HEIGHT * window.get_height(), window.get_width())
    height = min(globals.HEIGHT / globals.WIDTH * window.get_width(), window.get_height())
    return (pos[0] - (window.get_width() - width) / 2) / width * globals.WIDTH, \
           (pos[1] - (window.get_height() - height) / 2) / height * globals.HEIGHT


init()
dragging = False
dragging_chip = None
dragging_chip_pos = None
should_remove = False
is_pressed = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    screen = pygame.Surface((globals.WIDTH, globals.HEIGHT))
    screen.fill((255, 255, 255))
    all_sprites.update()
    all_sprites.draw(screen)

    mouse_pos = pygame.mouse.get_pos()
    mouse_pos = pos_on_window_to_pos_on_screen(mouse_pos, window)
    for i in range(0, 8):
        for j in range(0, 3):
            if chips_positions.sprites()[i * 3 + j].rect.collidepoint(mouse_pos):
                pygame.draw.circle(screen, (0, 0, 0), chips_positions.sprites()[i * 3 + j].rect.center,
                                   chips_positions.sprites()[i * 3 + j].radius, 3)

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
                            should_remove = game.move_chip(game.turn, dragging_chip_pos, (i, j))
                            if not should_remove:
                                game.end_turn()
                            found = True
                            break
                if found:
                    break
            else:
                dragging_chip.rect.center = chips_positions.sprites()[
                    dragging_chip_pos[0] * 3 + dragging_chip_pos[1]].rect.center
                print("can't move" + dragging_chip.rect.center.__str__())
    if should_remove:
        if pygame.mouse.get_pressed()[0] and not is_pressed:
            is_pressed = True
            for i in range(0, 8):
                for j in range(0, 3):
                    if chips_positions.sprites()[i * 3 + j].rect.collidepoint(mouse_pos):
                        print("remove chip" + str((i, j)))
                        if game.can_remove(game.turn, (i, j)):
                            print("can remove")
                            for chip in chips.sprites():
                                if chip.rect.collidepoint(chips_positions.sprites()[i * 3 + j].rect.center):
                                    chip.kill()
                            should_remove = False
                            game.remove_chip(game.turn, (i, j))
                            game.end_turn()
                            break
    elif game.chips_count[game.turn] > 0:
        if pygame.mouse.get_pressed()[0] and not is_pressed:
            is_pressed = True
            for i in range(0, 8):
                for j in range(0, 3):
                    if chips_positions.sprites()[i * 3 + j].rect.collidepoint(mouse_pos):
                        print("put chip" + str((i, j)))
                        if game.can_put(game.turn, (i, j)):
                            print("can put")
                            # add chip to sprites and game
                            chip = RoundSprite(globals.PLAYER_COLORS[game.turn], 20,
                                               chips_positions.sprites()[i * 3 + j].rect.center)
                            chips.add(chip)
                            all_sprites.add(chip)
                            should_remove = game.put_chip(game.turn, (i, j))
                            if not should_remove:
                                game.end_turn()
                            if should_remove:
                                print("should remove")
                            break
    else:
        if pygame.mouse.get_pressed()[0] and not is_pressed:
            is_pressed = True
            for i in range(0, 8):
                for j in range(0, 3):
                    if chips_positions.sprites()[i * 3 + j].rect.collidepoint(mouse_pos):
                        if game.chips[i][j] == game.turn:
                            dragging = True
                            # find chip
                            for chip in chips.sprites():
                                if chip.rect.collidepoint(chips_positions.sprites()[i * 3 + j].rect.center):
                                    dragging_chip = chip
                                    break
                            dragging_chip_pos = (i, j)
                            break

    if game.check_win() != 0:
        font = pygame.font.SysFont("comicsansms", 72)
        text = font.render("Player " + str(game.check_win()) + " wins!", True, (0, 0, 0))
        screen.blit(text, (globals.WIDTH / 2 - text.get_width() / 2, globals.HEIGHT / 2 - text.get_height() / 2))
    elif game.check_tie():
        font = pygame.font.SysFont("comicsansms", 72)
        text = font.render("Draw!", True, (0, 0, 0))
        screen.blit(text, (globals.WIDTH / 2 - text.get_width() / 2, globals.HEIGHT / 2 - text.get_height() / 2))

    width = min(globals.WIDTH / globals.HEIGHT * window.get_height(), window.get_width())
    height = min(globals.HEIGHT / globals.WIDTH * window.get_width(), window.get_height())
    window.blit(
        pygame.transform.scale(screen, (width, height)),
        ((window.get_width() - width) / 2, (window.get_height() - height) / 2))
    pygame.display.flip()
