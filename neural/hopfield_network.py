import random


def random_vector(minmax):
    return [minmax[i][0] + ((minmax[i][1] - minmax[i][0]) * random.random()) for i in range(len(minmax))]


def initialize_weights(problem_size):
    minmax = [[-0.5, 0.5] for _ in range(problem_size)]
    return random_vector(minmax)


def create_neuron(num_inputs):
    neuron = {}
    neuron['weights'] = initialize_weights(num_inputs)
    return neuron


def transfer(activation):
    return 1 if activation >= 0 else -1


def propagate_was_change(neurons):
    i = random.randint(0, len(neurons)-1)
    activation = 0
    for j, other in enumerate(neurons):
        if i != j:
            activation += other['weights'][i] * other['output']
    output = transfer(activation)
    change = output != neurons[i]['output']
    neurons[i]['output'] = output
    return change


def flatten_pattern(pattern):
    flatten = []
    for row in pattern:
        for x in row:
            flatten.append(x)
    return flatten


def get_output(neurons, perturbed_pattern, evals=100):
    vector = [x for x in perturbed_pattern]
    for i, neuron in enumerate(neurons):
        neuron['output'] = vector[i]
    for _ in range(evals):
        propagate_was_change(neurons)
    return [neurons[i]['output'] for i in range(len(neurons))]


def train_network(neurons, patterns):
    for i, neuron in enumerate(neurons):
        for j in range(i+1, len(neurons)):
            wij = 0
            for pattern in patterns:
                vector = flatten_pattern(pattern)
                wij += vector[i] * vector[j]
            neurons[i]['weights'][j] = wij
            neurons[j]['weights'][i] = wij


def to_binary(vector):
    return [1 if x > 0 else 0 for x in vector]


def print_pattern(provided, expected, actual):
    p, e, a = to_binary(provided), to_binary(expected), to_binary(actual)
    p1, p2, p3 = p[0:3], p[3:6], p[6:9]
    e1, e2, e3 = e[0:3], e[3:6], e[6:9]
    a1, a2, a3 = a[0:3], a[3:6], a[6:9]
    print('Provided  -  Expected  -  Got')
    print(f'{p1} - {e1} - {a1}')
    print(f'{p2} - {e2} - {a2}')
    print(f'{p3} - {e3} - {a3}')


def calculate_error(expected, actual):
    sum = 0
    for i in range(len(expected)):
        if expected[i] != actual[i]:
            sum += 1
    return sum


def perturb_pattern(vector, num_errors=2):
    perturbed = [el for el in vector]
    indicies = [random.randint(0, len(perturbed)-1)]
    while len(indicies) < num_errors:
        index = random.randint(0, len(perturbed)-1)
        if index not in indicies:
            indicies.append(index)
    for i in indicies:
        perturbed[i] = 1 if perturbed[i] == -1 else -1
    return perturbed


def test_network(neurons, patterns):
    error = 0
    for pattern in patterns:
        vector = flatten_pattern(pattern)
        perturbed = perturb_pattern(vector)
        output = get_output(neurons, perturbed)
        error += calculate_error(vector, output)
        print_pattern(perturbed, vector, output)
    error = error / len(patterns)
    print(f"Final Result: avg pattern error={error}")
    return error


def execute(patterns, num_inputs):
    neurons = [create_neuron(num_inputs) for _ in range(num_inputs)]
    train_network(neurons, patterns)
    test_network(neurons, patterns)
    return neurons


if __name__ == '__main__':
    num_inputs = 9
    p1 = [[1, 1, 1], [-1, 1, -1], [-1, 1, -1]]
    p2 = [[1, -1, 1], [1, -1, 1], [1, 1, 1]]
    patterns = [p1, p2]
    execute(patterns, num_inputs)
