import random


def one_max(vector):
    return sum(1 for bit in vector if bit == '1')


def generate_candidate(vector):
    candidate = {'bitstring': ''}
    for p in vector:
        candidate['bitstring'] += '1' if random.random() < p else '0'

    candidate['cost'] = one_max(candidate['bitstring'])
    return candidate


def update_vector(vector, winner, loser, pop_size):
    for i in range(len(vector)):
        if winner['bitstring'][i] != loser['bitstring'][i]:
            if winner['bitstring'][i] == '1':
                vector[i] += 1 / pop_size
            else:
                vector[i] -= 1 / pop_size


def search(num_bits, max_iter, population_size):
    vector = [0.5] * num_bits
    best = None

    for _ in range(max_iter):
        c1 = generate_candidate(vector)
        c2 = generate_candidate(vector)

        if c1['cost'] > c2['cost']:
            winner, loser = c1, c2
        else:
            winner, loser = c2, c1

        if best == None or winner['cost'] > best['cost']:
            best = winner

        update_vector(vector, winner, loser, population_size)

    return best


if __name__ == '__main__':
    num_bits = 32
    max_iter = 200
    population_size = 20

    best = search(num_bits, max_iter, population_size)
    print(
        f"done! Solution: f={best['cost']}/{num_bits}, s={best['bitstring']}")
