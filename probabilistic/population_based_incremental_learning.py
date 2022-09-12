import random


def one_max(vector):
    return sum(1 for bit in vector if bit == '1')


def generate_candidate(vector):
    candidate = {'bitstring': ''}
    for p in vector:
        candidate['bitstring'] += '1' if random.random() < p else '0'
    return candidate


def update_vector(vector, current, learning_rate):
    for i, p in enumerate(vector):
        vector[i] = p*(1-learning_rate) + \
            int(current['bitstring'][i])*learning_rate


def mutate_vector(vector, mutation_factor, p_mutate):
    for i, p in enumerate(vector):
        if random.random() < p_mutate:
            vector[i] = p * (1 - mutation_factor) + \
                random.random() * mutation_factor


def search(number_of_bits, max_iter, number_of_samples, p_mutate, mutation_factor, learning_rate):
    vector = [0.5] * number_of_bits
    best = None

    for _ in range(max_iter):
        this_iter_best_candidate = None
        for _ in range(number_of_samples):
            candidate = generate_candidate(vector)
            candidate['cost'] = one_max(candidate['bitstring'])
            if this_iter_best_candidate == None or candidate['cost'] > this_iter_best_candidate['cost']:
                this_iter_best_candidate = candidate
            if best == None or candidate['cost'] > best['cost']:
                best = candidate

        update_vector(vector, this_iter_best_candidate, learning_rate)
        mutate_vector(vector, mutation_factor, p_mutate)

    return best


if __name__ == '__main__':
    number_of_bits = 64
    max_iter = 100
    number_of_samples = 100
    p_mutate = 1 / number_of_bits
    mutation_factor = 0.05
    learning_rate = 0.1

    best = search(number_of_bits, max_iter, number_of_samples,
                  p_mutate, mutation_factor, learning_rate)
    print(
        f"done! Solution: f={best['cost']}/{number_of_bits}, s={best['bitstring']}")
