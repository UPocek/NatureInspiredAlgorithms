import random


def one_max(vector):
    return sum(1 for bit in vector if bit == '1')


def random_bit_string(number_of_bits):
    bitstring = ''
    for _ in range(number_of_bits):
        bitstring += random.choice(['0', '1'])
    return bitstring


def binary_tournament(population):
    i, j = random.randint(0, len(population) -
                          1), random.randint(0, len(population)-1)
    while j == i:
        j = random.randint(0, len(population)-1)
    return population[i] if population[i]['fitness'] > population[j]['fitness'] else population[j]


def calculate_bit_probabilities(selected):
    vector = [0] * len(selected[0]['bitstring'])

    for member in selected:
        for i, bit in enumerate(member['bitstring']):
            vector[i] += int(bit)

    for i, bit in enumerate(vector):
        vector[i] = bit / len(selected)

    return vector


def generate_candidate(vector):
    candidate = {'bitstring': ''}
    for p in vector:
        candidate['bitstring'] += '1' if random.random() < p else '0'
    return candidate


def search(number_of_bits, max_iter, population_size, select_size):
    population = [{'bitstring': random_bit_string(
        number_of_bits)} for _ in range(population_size)]

    for member in population:
        member['fitness'] = one_max(member['bitstring'])
    population = sorted(population, key=lambda x: x['fitness'], reverse=True)

    best = population[0]

    for _ in range(max_iter):
        selected = [binary_tournament(population) for _ in range(select_size)]
        vector = calculate_bit_probabilities(selected)
        samples = [generate_candidate(vector) for _ in range(population_size)]
        for sample in samples:
            sample['fitness'] = one_max(sample['bitstring'])

        samples = sorted(samples, key=lambda x: x['fitness'], reverse=True)

        if samples[0]['fitness'] > best['fitness']:
            best = samples[0]

        population = samples

    return best


if __name__ == '__main__':
    number_of_bits = 64
    max_iter = 200
    population_size = 100
    select_size = 30

    best = search(number_of_bits, max_iter, population_size, select_size)
    print(
        f"done! Solution: f={best['fitness']}/{number_of_bits}, s={best['bitstring']}")
