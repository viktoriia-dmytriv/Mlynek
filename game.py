class Game:
    def __init__(self):
        self.chips = [[0 for i in range(0, 3)] for j in range(0, 8)]
        self.chips_count = [0, 9, 9]
        self.turn = 1
        self.turns_without_mill = 0
        self.planes = {}
        self.tie = False

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
                if pos1[1] != pos2[1] and pos1[0] % 2 == 0 and (
                        (pos1[1] + 1) % 3 == pos2[1] or (pos1[1] - 1 + 3) % 3 == pos2[1]):
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
        if self.check_line(color, pos):
            self.turns_without_mill = 0
            return True
        return False

    def remove_chip(self, color, pos):
        if not self.can_remove(color, pos):
            raise Exception("Can't remove chip")
        self.chips[pos[0]][pos[1]] = 0

    def move_chip(self, color, pos1, pos2):
        if not self.can_move(color, pos1, pos2):
            raise Exception("Can't move chip")
        self.chips[pos1[0]][pos1[1]] = 0
        self.chips[pos2[0]][pos2[1]] = color
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
            print("Tie")
            self.tie = True

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
            res[i] = configuration[i]
        res[24] = configuration[25]
        res[25] = configuration[24]
        return res

    def get_all_possible_configurations(self):
        # return array of all possible configurations after one move
        res = []
        if self.chips_count[self.turn] > 0:
            for i in range(0, 8):
                for j in range(0, 3):
                    if self.can_put(self.turn, (i, j)):
                        config = self.get_configuration()
                        new_game = Game()
                        new_game.load_configuration(config)
                        new_game.put_chip(self.turn, (i, j))
                        res.append(new_game.get_configuration())
        else:
            for i in range(0, 8):
                for j in range(0, 3):
                    if self.chips[i][j] == self.turn:
                        for k in range(0, 8):
                            for l in range(0, 3):
                                if self.can_move(self.turn, (i, j), (k, l)):
                                    config = self.get_configuration()
                                    new_game = Game()
                                    new_game.load_configuration(config)
                                    new_game.move_chip(self.turn, (i, j), (k, l))
                                    res.append(new_game.get_configuration())
        return res

    def load_configuration(self, configuration):
        for i in range(0, 8):
            for j in range(0, 3):
                self.chips[i][j] = configuration[i * 3 + j]
        self.chips_count[1] = configuration[24]
        self.chips_count[2] = configuration[25]
