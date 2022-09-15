import random
import math


def random_vector(minmax):
    return [minmax[i][0] + ((minmax[i][1] - minmax[i][0]) * random.random()) for i in range(len(minmax))]


def initialize_weights(problem_size):
    minmax = [[-random.random(), random.random()]
              for _ in range(problem_size)]
    return random_vector(minmax)


def activate(weights, vector):
    sum = weights[-1] * 1
    for i, x in enumerate(vector):
        sum += weights[i] * x
    return sum


def transfer(activation):
    return 1 / (1 + math.exp(-activation))


def transfer_derivative(output):
    return output * (1 - output)


def forward_propagate(net, vector):
    for i, layer in enumerate(net):
        if i == 0:
            input = vector
        else:
            input = [net[i-1][k]['output'] for k in range(len(net[i-1]))]
        for neuron in layer:
            neuron['activation'] = activate(neuron['weights'], input)
            neuron['output'] = transfer(neuron['activation'])
    return net[-1][0]['output']


def backward_propagate_error(network, expected_output):
    for n in range(len(network)):
        layer_index = len(network) - 1 - n
        if layer_index == len(network)-1:
            neuron = network[layer_index][0]
            error = expected_output - neuron['output']
            neuron['delta'] = error * transfer_derivative(neuron['output'])
        else:
            for k, neuron in enumerate(network[layer_index]):
                sum = 0
                for next_neuron in network[layer_index + 1]:
                    sum += next_neuron['weights'][k] * next_neuron['delta']
                neuron['delta'] = sum * transfer_derivative(neuron['output'])


def calculate_error_derivatives_for_weights(net, vector):
    for i, layer in enumerate(net):
        if i == 0:
            input = vector
        else:
            input = [net[i-1][k]['output'] for k in range(len(net[i-1]))]

        for neuron in layer:
            for j, signal in enumerate(input):
                neuron['deriv'][j] += neuron['delta'] * signal
            neuron['deriv'][-1] += neuron['delta'] * 1


def update_weights(network, l_rate, momentum=0.8):
    for layer in network:
        for neuron in layer:
            for j, w in enumerate(neuron['weights']):
                delta = (l_rate * neuron['deriv'][j]) + \
                    (neuron['last_delta'][j] * momentum)
                neuron['weights'][j] += delta
                neuron['last_delta'][j] = delta
                neuron['deriv'][j] = 0


def train_network(network, domain, number_of_inputs, iterations, l_rate):
    correct = 0
    for epoch in range(iterations):
        for pattern in domain:
            vector, expected = [pattern[k]
                                for k in range(number_of_inputs)], pattern[-1]
            output = forward_propagate(network, vector)
            if round(output) == expected:
                correct += 1
            backward_propagate_error(network, expected)
            calculate_error_derivatives_for_weights(network, vector)
        update_weights(network, l_rate)
        if epoch+1 % 100 == 0:
            print(f'> epoch={epoch+1}, Correct={correct}/{100*len(domain)}')
            correct = 0


def test_network(network, domain, number_of_inputs):
    correct = 0
    for pattern in domain:
        input_vector = [pattern[k]
                        for k in range(number_of_inputs)]
        output = forward_propagate(network, input_vector)
        if round(output) == pattern[-1]:
            correct += 1
    print(f"Finished test with a score of {correct}/{len(domain)}")
    return correct


def create_neuron(number_of_inputs):
    bias = 1
    return {'weights': initialize_weights(number_of_inputs + bias), 'last_delta': [0] * (number_of_inputs + bias), 'deriv': [0] * (number_of_inputs + bias)}


def execute(domain, number_of_inputs, iterations, num_hidden_nodes, l_rate):
    network = []
    network.append([create_neuron(number_of_inputs)
                   for _ in range(num_hidden_nodes)])
    network.append([create_neuron(len(network[-1]))])
    train_network(network, domain, number_of_inputs, iterations, l_rate)
    test_network(network, domain, number_of_inputs)
    return network


if __name__ == '__main__':
    xor_problem = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
    inputs = 2
    iterations = 2000
    learning_rate = 0.3
    num_hidden_nodes = 4
    execute(xor_problem, inputs, iterations, num_hidden_nodes, learning_rate)
