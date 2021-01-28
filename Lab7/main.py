import random
from math import exp


def read_from_file(file):
    file_desc = open(file, 'r')
    content = file_desc.read()

    splitted = content.split('\n')
    first = splitted[0]
    second = splitted[1]
    third = splitted[2:]

    return first, second, third


def init_neural_network(inputs_count, hidden_count, output_counts):
    neural_network = list()
    hidden = [[random.uniform(0, 1) for i in range(inputs_count)] for i in range(hidden_count)]
    output = [[random.uniform(0, 1) for i in range(hidden_count)] for i in range(output_counts)]
    for i in range(len(hidden)):
        hidden[i].append(0.0)
        hidden[i].append(0.0)
    for i in range(len(output)):
        output[i].append(0.0)
        output[i].append(0.0)
    neural_network.append(hidden)
    neural_network.append(output)

    return neural_network


def activate(weights, inputs):
    neuron_activation = -1
    for i in range(len(weights) - 1):
        neuron_activation += weights[i] * inputs[i]
    return neuron_activation


def sigmoid_function_derived(x):
    return x * (1 - x)


def sigmoid_function(x):
    return 1.0 / (1.0 + exp(-x))


def propagate_forward(neural_network, inputs):
    forward = inputs
    for layer in neural_network:
        new_inputs = list()
        for neuron in layer:
            activation = activate(neuron[0:len(neuron) - 2], inputs)
            transfer = sigmoid_function(activation)
            neuron[len(neuron) - 2] = transfer
            new_inputs.append(neuron[-2])
        forward = new_inputs
    return forward


def backward_propagate_error(neural_network, expected):
    for i in reversed(range(len(neural_network))):
        layer = neural_network[i]
        errors = list()
        if i != len(neural_network) - 1:
            for j in range(len(layer)):
                error = 0.0
                for neuron in neural_network[i + 1]:
                    error += sum(
                        [neuron[index] * neuron[len(neuron) - 1] for index in range(0, 2)]) * sigmoid_function_derived(
                        error)
                errors.append(error)
        else:
            for j in range(len(layer)):
                neuron = layer[j]
                errors.append(expected[j] - neuron[len(neuron) - 2])
        for j in range(len(layer)):
            neuron = layer[j]
            neuron[len(neuron) - 1] = errors[j] * sigmoid_function_derived(neuron[len(neuron) - 2])


def correct_weights(neural_network, inputs, rate):
    for i in range(len(neural_network)):
        if i != 0:
            correction_input = [neuron[len(neuron) - 2] for neuron in neural_network[i - 1]]
            for neuron in neural_network[i]:
                for index in range(len(correction_input)):
                    neuron[index] = neuron[index] + rate * neuron[len(neuron) - 1] * correction_input[index]
                neuron[-1] = neuron[-1] + rate * neuron[len(neuron) - 1]
        else:
            correction_input = inputs
            for neuron in neural_network[i]:
                for index in range(0, len(neuron) - 2):
                    neuron[index] = neuron[index] + rate * correction_input[index] * neuron[len(neuron) - 2]


def mean_square_error(expected, outputs):
    return [expected[i] - outputs[i] for i in range(len(expected))]


def train_neural_network(neural_network, train_data_input, train_data_output, rate, epochs_count):
    neural_final = None
    for epoch in range(epochs_count):
        counter = 0
        for row in train_data_input:
            forward_output = propagate_forward(neural_network, row)
            expected_output = [train_data_output[counter]]
            mse = mean_square_error(expected_output, forward_output)
            mse_final = mse
            backward_propagate_error(neural_network, expected_output)
            correct_weights(neural_network, row, rate)
            neural_final = neural_network
            counter = counter + 1

    print(mse_final, neural_final)


if __name__ == '__main__':
    epochs, learning_rate, function = read_from_file('input.in')
    training_data_string = [value[0:3].split(' ') for value in function]
    training_data_output = [int(value[3:]) for value in function]
    training_data_int = list()
    for sub_list in training_data_string:
        convert = list()
        for character in sub_list:
            convert.append(int(character))
        training_data_int.append(convert)

    train_neural_network(init_neural_network(2, 2, 1), training_data_int, training_data_output, 0.01, 10000)
