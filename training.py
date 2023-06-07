# train model to play mlynek
from random import random

from game import Game
from neural_network import NeuralNetwork
from neural_network_utils import *

# make two models play against each other
# next generation is made from statistics of the previous generation

# data is list of tuples (board, winrate)

EPOCHS = 10
LEARNING_RATE = 0.1
GAMES_IN_GENERATION = 1000
GENERATIONS = 30
model = [NeuralNetwork([26, 15, 1], sigmoid, sigmoid_derivative) for _ in range(2)]


def pick_best_configuration(model: NeuralNetwork, data):
    #pick best configuration with random coefficient
    sum = 0
    for data_line in data:
        sum += model.predict(np.array(data_line))[0]
    random_number = random() * sum
    for data_line in data:
        random_number -= model.predict(np.array(data_line))[0]
        if random_number <= 0:
            return data_line


for gen in range(GENERATIONS):
    data = []
    with open('positions.data') as f:
        lines = f.readlines()
        for line in lines:
            data.append([float(x) for x in line.split(',')])

    for i in range(2):
        for _ in range(EPOCHS):
            for data_line in data:
                model[i].fit(np.array(data_line[:-1]), np.array([data_line[-1]]), LEARNING_RATE)

    new_data = {}
    for game_num in range(GAMES_IN_GENERATION):
        print(f'Generation {gen}, game {game_num}')
        game = Game()
        turn = 1
        #collect data about winrate of each configuration
        models_configurations = [[], []]
        while not game.check_win() and not game.check_tie():
            # print(game.get_configuration())
            configurations = game.get_all_possible_configurations()
            if turn == 2:
                for i in range(len(configurations)):
                    configurations[i] = Game.swap_players_in_configuration(configurations[i])
            best_conf = pick_best_configuration(model[turn - 1], configurations)
            models_configurations[turn - 1].append(best_conf)
            game.load_configuration(best_conf)
            game.end_turn()
            turn = 3 - turn
        if game.check_win():
            print(f'Player {game.check_win()} won')
            winner = game.check_win()
            for conf in models_configurations[winner - 1]:
                if tuple(conf) in new_data:
                    new_data[tuple(conf)] += 1
                else:
                    new_data[tuple(conf)] = 1
        else:
            for conf in models_configurations[0]:
                if tuple(conf) in new_data:
                    new_data[tuple(conf)] += 0.5
                else:
                    new_data[tuple(conf)] = 0.5
    #rewrite data
    with open('positions.data', 'w') as f:
        for key in new_data:
            f.write(','.join([str(x) for x in key]) + ',' + str(new_data[key]) + '\n')
    print(f'Generation {gen} done')
