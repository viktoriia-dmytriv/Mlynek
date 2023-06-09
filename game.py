INDEX_TO_MODEL = [
    12, 13, 14,
    17, 20, 23,
    16, 19, 22,
    15, 18, 21,
    11, 10, 9,
    6, 3, 0,
    7, 4, 1,
    8, 5, 2,
]


class Game:
    def __init__(self):
        self.chips = [[0 for i in range(0, 3)] for j in range(0, 8)]
        self.chips_count = [0, 9, 9]
        self.turn = 1
        self.should_remove = False
        self.turns_without_mill = 0
        self.planes = {}
        self.last_turn = None
        self.last_removed = None
        self.tie = False
        self.end = False

    def copy(self):
        game = Game()
        game.chips = [[self.chips[i][j] for j in range(0, 3)] for i in range(0, 8)]
        game.chips_count = [self.chips_count[0], self.chips_count[1], self.chips_count[2]]
        game.turn = self.turn
        game.should_remove = self.should_remove
        game.turns_without_mill = self.turns_without_mill

        game.planes = {}
        for key in self.planes:
            game.planes[key] = self.planes[key]

        game.tie = self.tie
        game.end = self.end
        return game

    def chips_on_board(self, color):
        count = 0
        for i in range(0, 8):
            for j in range(0, 3):
                if self.chips[i][j] == color:
                    count += 1
        return count

    def can_move(self, color, pos1, pos2):
        if self.chips[pos1[0]][pos1[1]] != color:
            return False
        if self.chips[pos2[0]][pos2[1]] != 0:
            return False
        if self.chips_count[color] == 0 and self.chips_on_board(color) == 3:
            return True
        if self.chips_count[color] == 0:
            if pos1[0] == pos2[0]:
                if pos1[1] != pos2[1] and pos1[0] % 2 == 0 and abs(pos1[1] - pos2[1]) == 1:
                    return True
            if pos1[1] == pos2[1]:
                if (pos1[0] + 1) % 8 == pos2[0] or (pos1[0] - 1 + 8) % 8 == pos2[0]:
                    return True
        return False

    def can_put(self, color, pos):
        if self.chips[pos[0]][pos[1]] != 0:
            return False
        return self.chips_count[color] > 0

    def check_line(self, color, pos):
        if pos[0] % 2 == 0:
            if self.chips[pos[0]][pos[1]] \
                    and self.chips[pos[0]][(pos[1] + 1) % 3] == color \
                    and self.chips[pos[0]][(pos[1] + 2) % 3] == color:
                return True
        for i in range(-1, 2):
            if self.chips[(pos[0] + i - 1 + 8) % 8][pos[1]] == color \
                    and self.chips[(pos[0] + i) % 8][pos[1]] == color \
                    and self.chips[(pos[0] + i + 1) % 8][pos[1]] == color \
                    and (pos[0] + i) % 2 == 0:
                return True
        return False

    def can_remove(self, color, pos):
        if self.chips[pos[0]][pos[1]] != 3 - color:
            return False
        all_in_line = True
        for i in range(0, 8):
            for j in range(0, 3):
                if self.chips[i][j] == 3 - color and not self.check_line(3 - color, (i, j)):
                    all_in_line = False
        if self.check_line(3 - color, pos) and not all_in_line:
            return False
        return True

    def put_chip(self, color, pos):
        # if not self.can_put(color, pos):
        #     raise Exception("Can't put chip")
        self.chips[pos[0]][pos[1]] = color
        self.chips_count[color] -= 1
        self.last_turn = pos
        self.last_removed = None
        if self.check_line(color, pos):
            self.turns_without_mill = 0
            return True
        return False

    def remove_chip(self, color, pos):
        if not self.can_remove(color, pos):
            raise Exception("Can't remove chip")
        self.chips[pos[0]][pos[1]] = 0
        self.last_removed = pos

    def move_chip(self, color, pos1, pos2):
        if not self.can_move(color, pos1, pos2):
            raise Exception("Can't move chip")
        self.chips[pos1[0]][pos1[1]] = 0
        self.chips[pos2[0]][pos2[1]] = color
        self.last_turn = (pos1, pos2)
        self.last_removed = None
        if self.check_line(color, pos2):
            self.turns_without_mill = 0
            return True

    def end_turn(self):
        self.turn = 3 - self.turn
        self.turns_without_mill += 1
        if str(self.chips) in self.planes:
            self.planes[str(self.chips)] += 1
        else:
            self.planes[str(self.chips)] = 1
        if self.turns_without_mill >= 50 or self.planes[str(self.chips)] >= 3:
            self.tie = True
            self.end = True
        if self.check_win():
            self.end = True

    def check_possible_line(self, color, pos):
        self.chips[pos[0]][pos[1]] = color
        res = self.check_line(color, pos)
        self.chips[pos[0]][pos[1]] = 0
        return res

    def check_win(self):
        if self.chips_count[1] == 0 and self.chips_on_board(1) == 2:
            return 2
        if self.chips_count[2] == 0 and self.chips_on_board(2) == 2:
            return 1
        # check if person cant make a move
        can_move = self.chips_count[self.turn] > 0
        for i in range(0, 8):
            for j in range(0, 3):
                if self.chips[i][j] == self.turn:
                    for k in range(0, 8):
                        for l in range(0, 3):
                            if self.can_move(self.turn, (i, j), (k, l)):
                                can_move = True
        if not can_move:
            return 3 - self.turn
        return 0

    def check_tie(self):
        return self.tie

    def check_end(self):
        return self.end

    def get_configuration(self):
        res = [0] * 26
        for i in range(0, 8):
            for j in range(0, 3):
                res[i * 3 + j] = self.chips[i][j]
        res[24] = self.chips_count[1]
        res[25] = self.chips_count[2]
        return res

    @staticmethod
    def swap_players_in_configuration(configuration):
        res = [0] * 26
        for i in range(0, 24):
            res[i] = (3 - configuration[i]) % 3
        res[24] = configuration[25]
        res[25] = configuration[24]
        return res

    def get_all_possible_moves(self):
        res = []
        if self.chips_count[self.turn] > 0:
            for i in range(0, 8):
                for j in range(0, 3):
                    if self.can_put(self.turn, (i, j)):
                        if self.check_possible_line(self.turn, (i, j)):
                            for k in range(0, 8):
                                for l in range(0, 3):
                                    if self.can_remove(self.turn, (k, l)):
                                        res.append("pr" + str(i) + str(j) + str(k) + str(l))
                        else:
                            res.append("pn" + str(i) + str(j))
        else:
            for i in range(0, 8):
                for j in range(0, 3):
                    if self.chips[i][j] == self.turn:
                        for k in range(0, 8):
                            for l in range(0, 3):
                                if self.can_move(self.turn, (i, j), (k, l)):
                                    self.chips[i][j] = 0
                                    if self.check_possible_line(self.turn, (k, l)):
                                        # print("possible line")
                                        for m in range(0, 8):
                                            for n in range(0, 3):
                                                if self.can_remove(self.turn, (m, n)):
                                                    res.append("mr" + str(i) + str(j) + str(k) + str(l) + str(m) + str(n))
                                                    # print("remove")
                                    else:
                                        res.append("mn" + str(i) + str(j) + str(k) + str(l))
                                    self.chips[i][j] = self.turn
        return res

    def make_move(self, move):
        if move[0] == 'p':
            if move[1] == 'r':
                self.put_chip(self.turn, (int(move[2]), int(move[3])))
                self.remove_chip(self.turn, (int(move[4]), int(move[5])))
            else:
                self.put_chip(self.turn, (int(move[2]), int(move[3])))
        else:
            if move[1] == 'r':
                self.move_chip(self.turn, (int(move[2]), int(move[3])), (int(move[4]), int(move[5])))
                self.remove_chip(self.turn, (int(move[6]), int(move[7])))
            else:
                self.move_chip(self.turn, (int(move[2]), int(move[3])), (int(move[4]), int(move[5])))
        self.end_turn()

    def load_configuration(self, configuration):
        for i in range(0, 8):
            for j in range(0, 3):
                self.chips[i][j] = configuration[i * 3 + j]
        self.chips_count[1] = configuration[24]
        self.chips_count[2] = configuration[25]
