from neural_network import NeuralNetwork
from neural_network_utils import *
import random

model = NeuralNetwork([28, 100, 24 * 24 + 24], sigmoid, sigmoid_derivative)

EPOCHS = 3
LEARNING_RATE = 0.1

LIST_OF_POSITIONS = [
    "e4", "f4", "g4",
    "e3", "f2", "g1",
    "d3", "d2", "d1",
    "c3", "b2", "a1",
    "c4", "b4", "a4",
    "c5", "b6", "a7",
    "d5", "d6", "d7",
    "e5", "f6", "g7",
]

POS_TO_INDEX = {pos: i for i, pos in enumerate(LIST_OF_POSITIONS)}


def move_to_array(move):
    res = [0] * (24 * 24 + 24)
    if len(move) == 2:
        res[POS_TO_INDEX[move[0:2]] * (24 + 1)] = 1
    elif len(move) == 4:
        res[POS_TO_INDEX[move[0:2]] * 24 + POS_TO_INDEX[move[2:4]]] = 1
    else:
        res[POS_TO_INDEX[move[0:2]] * 24 + POS_TO_INDEX[move[2:4]]] = 1
        res[24 * 24 + POS_TO_INDEX[move[4:6]]] = 1
    return res


data = []
with open('dataset.data') as f:
    lines = f.readlines()
    for line in lines:
        x, y = line.strip().split('-')
        data.append((list(map(int, x.replace("O", "0").replace("M", "1").replace("E", "2"))), move_to_array(y)))

random.shuffle(data)
data = data[:10000]
train_data, test_data = data[:int(len(data) * 0.8)], data[int(len(data) * 0.8):]

for _ in range(EPOCHS):
    print(_)
    for data_line in train_data:
        model.fit(np.array(data_line[0]), np.array(data_line[1]), LEARNING_RATE)

accuracy = 0
for data_line in test_data:
    result = model.predict(np.array(data_line[0]))
    accuracy += np.argmax(result[:24 * 24]) == np.argmax(data_line[1][:24 * 24])
    if max(data_line[1][24 * 24:]) > 0:
        accuracy += np.argmax(result[24 * 24:]) == np.argmax(data_line[1][24 * 24:])
model.save("model")
print(f'Accuracy: {accuracy / len(test_data)}')
