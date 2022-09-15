import random


def random_vector(minmax):
    return [minmax[i][0] + ((minmax[i][1] - minmax[i][0]) * random.random()) for i in range(len(minmax))]


def initialize_weights(problem_size):
    bias = 1
    minmax = [[0, 0.5] for _ in range(problem_size+bias)]
    return random_vector(minmax)


def update_weights(num_inputs, weights, input, actual, prediction, learning_rate):
    for i in range(num_inputs):
        weights[i] += learning_rate * (actual - prediction) * input[i]
    weights[num_inputs] += learning_rate * (actual - prediction) * 1


def activate(weights, vector):
    bias = weights[-1] * 1
    sum = 0
    for i, input in enumerate(vector):
        sum += weights[i] * input
    return sum + bias


def transfer(activation):
    return 1 if activation >= 0 else 0


def get_output(weights, vector):
    activation = activate(weights, vector)
    return transfer(activation)


def train_weights(weights, domain, num_inputs, iterations, learning_rate):
    for epoch in range(iterations):
        error = 0
        for pattern in domain:
            input = [pattern[k] for k in range(num_inputs)]
            prediction = get_output(weights, input)
            actual = pattern[-1]
            error += abs(prediction - actual)
            update_weights(num_inputs, weights, input,
                           actual, prediction, learning_rate)
        print(f'> epoch={epoch}, error={error}')


def test_weights(weights, domain, num_inputs):
    correct = 0
    random.shuffle(domain)
    for pattern in domain:
        input_vector = [pattern[k] for k in range(num_inputs)]
        prediction = get_output(weights, input_vector)
        if round(prediction) == pattern[-1]:
            correct += 1
    print(f"Finished test with a score of {correct}/{len(domain)}")
    return correct


def execute(domain, num_inputs, iterations, learning_rate):
    weights = initialize_weights(num_inputs)
    train_weights(weights, domain, num_inputs, iterations, learning_rate)
    test_weights(weights, domain, num_inputs)
    return weights


if __name__ == '__main__':
    or_problem = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
    inputs = 2
    iterations = 20
    learning_rate = 0.1
    execute(or_problem, inputs, iterations, learning_rate)
