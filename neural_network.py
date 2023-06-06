import numpy as np


class NeuralNetwork:
    def __init__(self, layer_sizes, activation_function, activation_function_derivative):
        self.activation_function = activation_function
        self.activation_function_derivative = activation_function_derivative
        self.layers = len(layer_sizes)
        self.w = [np.random.randn(layer_sizes[i + 1], layer_sizes[i]) for i in range(self.layers - 1)]
        self.b = [np.random.randn(layer_sizes[i + 1]) for i in range(self.layers - 1)]
        self.out = [np.zeros(layer_sizes[i]) for i in range(self.layers)]

    def predict(self, x):
        self.out[0] = x
        for i in range(self.layers - 1):
            x = self.w[i] @ x + self.b[i]
            x = self.activation_function(x)
            self.out[i + 1] = x
        return x

    def fit(self, x, y, learning_rate=0.1):
        if not isinstance(x, np.ndarray) or x.ndim != 1:
            raise ValueError('x must be a 1D numpy array')
        if not isinstance(y, np.ndarray) or y.ndim != 1:
            raise ValueError('y must be a 1D numpy array')

        self.predict(x)

        d_error_over_d_out = (self.out[-1] - y)

        d_out_over_d_net = self.activation_function_derivative(self.out[-1])
        d_net_over_d_w = self.out[-2]
        d_net_over_d_b = 1

        self.w[-1] -= learning_rate * np.atleast_2d(d_error_over_d_out * d_out_over_d_net).T @ np.atleast_2d(d_net_over_d_w)
        self.b[-1] -= learning_rate * d_error_over_d_out * d_out_over_d_net * d_net_over_d_b

        d_total_error_over_d_net = d_error_over_d_out * d_out_over_d_net

        for i in range(self.layers - 2, 0, -1):
            d_total_error_over_d_out = self.w[i].T @ d_total_error_over_d_net
            d_out_over_d_net = self.activation_function_derivative(self.out[i])
            d_total_error_over_d_net = d_total_error_over_d_out * d_out_over_d_net
            d_net_over_d_w = self.out[i - 1]
            d_net_over_d_b = 1

            self.w[i - 1] -= learning_rate * np.atleast_2d(d_total_error_over_d_net * d_out_over_d_net).T @ np.atleast_2d(d_net_over_d_w)
            self.b[i - 1] -= learning_rate * d_total_error_over_d_net * d_out_over_d_net * d_net_over_d_b

