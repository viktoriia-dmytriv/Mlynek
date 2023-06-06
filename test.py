import random

from neural_network import NeuralNetwork
from neural_network_utils import *

data = []
with open('phishing.data') as f:
    lines = f.readlines()
    random.shuffle(lines)
    for line in lines:
        data.append([int(x) for x in line.split(',')])

for data_line in data:
    data_line[-1] = (data_line[-1] + 1) // 2

train_data, test_data = data[:int(len(data) * 0.8)], data[int(len(data) * 0.8):]

nn = NeuralNetwork([30, 15, 1], sigmoid, sigmoid_derivative)

EPOCHS = 10
LEARNING_RATE = 0.1

for _ in range(EPOCHS):
    for data_line in train_data:
        nn.fit(np.array(data_line[:-1]), np.array([data_line[-1]]), LEARNING_RATE)

accuracy = 0
for data_line in test_data:
    print(nn.predict(np.array(data_line[:-1])), data_line[-1])
    result = nn.predict(np.array(data_line[:-1]))
    accuracy += (result > 0.5) == data_line[-1]
print(f'Accuracy: {accuracy / len(test_data)}')
