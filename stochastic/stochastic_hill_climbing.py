import random


def one_max(vector):
    return sum(1 for bit in vector if bit == '1')


def random_bit_string(num_bits):
    bit_string = ''
    for _ in range(num_bits):
        bit_string += random.choice(['0', '1'])
    return bit_string


def random_neighbor(bit_string):
    position_to_mutate = random.randint(0, len(bit_string)-1)

    mutant = ''
    for i, bit in enumerate(bit_string):
        if i == position_to_mutate:
            mutant += '1' if bit == '0' else '0'
        else:
            mutant += bit

    return mutant


def stochastic_hill_climbing_search(max_iter, num_bits):
    candidate = {}
    candidate['vector'] = random_bit_string(num_bits)
    candidate['cost'] = one_max(candidate['vector'])

    for _ in range(max_iter):
        neighbor = {}
        neighbor['vector'] = random_neighbor(candidate['vector'])
        neighbor['cost'] = one_max(neighbor['vector'])

        if neighbor['cost'] >= candidate['cost']:
            candidate = neighbor

        if candidate['cost'] == num_bits:
            break

    return candidate


if __name__ == '__main__':

    # Max One Problem (https://github.com/Oddsor/EvolAlgo/wiki/Max-One-Problem) - target: 111111111111111111111111111111111

    max_iter = 100
    num_bits = 64
    best = stochastic_hill_climbing_search(max_iter, num_bits)

    print(f"Done. Best Solution: c={best['cost']}, v={best['vector']}")
