from game import Game

MAX_DEPTH = 5
MAX_NODES = 20000


def evaluate(game, color):
    return (game.chips_on_board(color) - game.chips_on_board(3 - color)) * 1000 + len(game.get_all_possible_moves())


was_in = 0
max_depth = 0


def minimax(game, player, tokens=MAX_NODES, can_evaluate=True, depth=0):
    # if evaluate(game, player) >= 2:
    #     return 2, None
    # if evaluate(game, player) <= -2:
    #     return -2, None
    # if depth == MAX_DEPTH:
    #     return evaluate(game, player), None
    global was_in, max_depth
    was_in += 1
    tokens -= 1
    if tokens <= 0:
        return None, None
    if tokens == 1 and can_evaluate:
        return evaluate(game, player), None
    moves = game.get_all_possible_moves()
    if len(moves) == 0:
        return -100000, None
    best_move = None
    best_score = -1000000
    a = tokens // len(moves)
    b = tokens % len(moves)
    for i, move in enumerate(moves):
        new_game = game.copy()
        new_game.make_move(move)
        score, _ = minimax(new_game, 3 - player, a + int(i < b), not can_evaluate, depth+1)
        if score is None:
            if can_evaluate:
                return evaluate(game, player), None
            else:
                return None, None
        score = -score
        if score > best_score:
            best_score = score
            best_move = move
    max_depth = max(max_depth, depth)
    return best_score, best_move
