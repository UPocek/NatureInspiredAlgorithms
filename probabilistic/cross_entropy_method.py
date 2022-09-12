import random
import math


def objective_function(vector):
    return sum([x**2 for x in vector])


def random_from_bounds(lower_bound, upper_bound):
    return lower_bound + (upper_bound-lower_bound) * random.random()


def random_gaussian(mean=0.0, std=1.0):
    u1 = u2 = w = 0

    while True:
        u1 = 2 * random.random() - 1
        u2 = 2 * random.random() - 1
        w = u1 ** 2 + u2 ** 2
        if w < 1:
            break

    w = math.sqrt((-2 * math.log(w)) / w)

    return mean + (u2 * w) * std


def generate_sample(search_space, means, stdevs):
    vector = [0] * len(search_space)
    for i in range(len(search_space)):
        vector[i] = random_gaussian(means[i], stdevs[i])
        vector[i] = max(vector[i], search_space[i][0])
        vector[i] = min(vector[i], search_space[i][1])
    return {'vector': vector}


def mean_attr(samples, i):
    sum = 0
    for sample in samples:
        sum += sample['vector'][i]
    return sum / len(samples)


def stdev_attr(samples, mean, i):
    sum = 0
    for sample in samples:
        sum += (sample['vector'][i] - mean)**2

    return math.sqrt(sum / len(sample))


def update_distribution(samples, learning_rate, means, stdevs):
    for i in range(len(means)):
        means[i] = learning_rate * means[i] + \
            ((1-learning_rate) * mean_attr(samples, i))
        stdevs[i] = learning_rate * stdevs[i] + \
            ((1-learning_rate) * stdev_attr(samples, means[i], i))


def search(search_space, max_iter, num_samples, num_update, learning_rate):
    means = [random_from_bounds(search_space[i][0], search_space[i][1])
             for i in range(len(search_space))]
    stdevs = [search_space[i][1]-search_space[i][0]
              for i in range(len(search_space))]
    best = None

    for _ in range(max_iter):
        samples = [generate_sample(search_space, means, stdevs)
                   for _ in range(num_samples)]
        for sample in samples:
            sample['cost'] = objective_function(sample['vector'])

        samples = sorted(samples, key=lambda x: x['cost'])
        if best is None or samples[0]['cost'] < best['cost']:
            best = samples[0]
        selected = samples[:num_update]
        update_distribution(selected, learning_rate, means, stdevs)

    return best


if __name__ == '__main__':
    problem_size = 3
    search_space = [[-5, 5] for _ in range(problem_size)]
    max_iter = 100
    num_samples = 50
    num_update = 5
    learning_rate = 0.7

    best = search(search_space, max_iter, num_samples,
                  num_update, learning_rate)
    print(f"done! Solution: f={best['cost']}, s={best['vector']}")
