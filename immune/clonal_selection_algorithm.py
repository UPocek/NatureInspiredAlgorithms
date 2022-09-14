import random
import math


def objective_function(vector):
    return sum([x**2 for x in vector])


def random_bitstring(bitstring_size):
    new_bitstring = ''
    for _ in range(bitstring_size):
        new_bitstring += random.choice(['0', '1'])
    return new_bitstring


def point_mutation(bitstring, mutation_rate=None):
    if mutation_rate is None:
        mutation_rate = 1/len(bitstring)
    mutated_child = ''

    for bit in bitstring:
        if random.random() < mutation_rate:
            mutated_child += '1' if bit == '0' else '0'
        else:
            mutated_child += bit
    return mutated_child


def decode(bitstring, search_space, bits_per_param):
    vector = []
    for i, bounds in enumerate(search_space):
        offset_from_start = i * bits_per_param
        sum = 0
        parameters = list(
            reversed(bitstring[offset_from_start:offset_from_start+bits_per_param]))
        for j in range(len(parameters)):
            if parameters[j] == '1':
                sum += 2 ** j
        min, max = bounds
        vector.append(min + ((max-min) / ((2**bits_per_param)-1)) * sum)

    return vector


def evalaute(population, search_space, bits_per_param):
    for antibody in population:
        antibody['vector'] = decode(
            antibody['bitstring'], search_space, bits_per_param)
        antibody['cost'] = objective_function(antibody['vector'])


def calculate_mutation_rate(antibody, mutate_factor=-2.5):
    return math.exp(mutate_factor * antibody['affinity'])


def calculate_number_of_clones(population_size, clone_factor):
    return math.floor(population_size * clone_factor)


def calculate_affinity(population):
    population = sorted(population, key=lambda x: x['cost'])
    range = population[-1]['cost'] - population[0]['cost']
    if range == 0:
        for antibody in population:
            antibody['affinity'] = 1
    else:
        for antibody in population:
            antibody['affinity'] = 1 - (antibody['cost'] / range)


def clone_and_hypermutate(population, clone_factor):
    clones = []
    number_of_clones = calculate_number_of_clones(
        len(population), clone_factor)
    calculate_affinity(population)
    for antibody in population:
        mutation_rate = calculate_mutation_rate(antibody)
        for _ in range(number_of_clones):
            clone = {}
            clone['bitstring'] = point_mutation(
                antibody['bitstring'], mutation_rate)
            clones.append(clone)
    return clones


def random_insertion(search_space, population, number_of_random_antibodies_to_create, bits_per_param):
    if number_of_random_antibodies_to_create == 0:
        return population

    random_antigens = [{'bitstring': random_bitstring(
        len(search_space) * bits_per_param)} for _ in range(number_of_random_antibodies_to_create)]

    evalaute(random_antigens, search_space, bits_per_param)
    return sorted(population+random_antigens, key=lambda x: x['cost'])[:len(population)]


def search(search_space, max_gens, population_size, clone_factor, number_of_random_antibodies_to_create, bits_per_param):
    population = [{'bitstring': random_bitstring(
        len(search_space) * bits_per_param)} for _ in range(population_size)]

    evalaute(population, search_space, bits_per_param)
    best = min(population, key=lambda x: x['cost'])
    for _ in range(max_gens):
        clones = clone_and_hypermutate(population, clone_factor)
        evalaute(clones, search_space, bits_per_param)
        population = sorted(population + clones,
                            key=lambda x: x['cost'])[:population_size]
        population = random_insertion(
            search_space, population, number_of_random_antibodies_to_create, bits_per_param)
        best = min(population + [best], key=lambda x: x['cost'])

    return best


if __name__ == '__main__':
    problem_size = 2
    search_space = [[-5, 5] for _ in range(problem_size)]
    max_gens = 100
    population_size = 100
    clone_factor = 0.1
    number_of_random_antibodies_to_create = 2
    bits_per_param = 16
    best = search(search_space, max_gens, population_size,
                  clone_factor, number_of_random_antibodies_to_create, bits_per_param)
    print(
        f"done! Solution: f={best['cost']}, s={best['bitstring']}, v={best['vector']}")
