import random


def objective_function(vector):
    return sum([x**2 for x in vector])


def random_bit_string(num_bits):
    bit_string = ''
    for _ in range(num_bits):
        bit_string += random.choice(['0', '1'])
    return bit_string


def decode(bitstring, search_space, bits_per_parameter):
    vector = []
    for i, bounds in enumerate(search_space):
        offset_from_start = i*bits_per_parameter
        sum = 0
        param = list(
            reversed(bitstring[offset_from_start:offset_from_start+bits_per_parameter]))

        for i in range(len(param)):
            if param[i] == '1':
                sum += 2**i
        min, max = bounds
        vector.append(min + ((max-min) / ((2**bits_per_parameter)-1)) * sum)

    return vector


def calculate_fitness(candidate, search_space, bits_per_parameter):
    candidate['vector'] = decode(
        candidate['bitstring'], search_space, bits_per_parameter)
    candidate['fitness'] = objective_function(candidate['vector'])


def binary_tournament(population):
    i, j = random.randint(0, len(population) -
                          1), random.randint(0, len(population)-1)
    while j == i:
        j = random.randint(0, len(population)-1)
    return population[i] if population[i]['fitness'] < population[j]['fitness'] else population[j]


def point_mutation(bitstring, p_mutation=None):
    if p_mutation is None:
        p_mutation = 1/len(bitstring)
    mutated_child = ''

    for bit in bitstring:
        if random.random() < p_mutation:
            mutated_child += '1' if bit == '0' else '0'
        else:
            mutated_child += bit
    return mutated_child


def crossover(first_parent, second_parent, p_crossover):
    if random.random() > p_crossover:
        return first_parent

    child = ''
    for i in range(len(first_parent)):
        child += first_parent[i] if random.random() < 0.5 else second_parent[i]

    return child


def reproduce(selected, p_crossover, p_mutation):
    children = []

    for i, first_parent in enumerate(selected):
        if i == len(selected)-1:
            second_parent = selected[0]
        else:
            second_parent = selected[i + 1] if i % 2 == 0 else selected[i-1]
        child = {}
        child['bitstring'] = crossover(
            first_parent['bitstring'], second_parent['bitstring'], p_crossover)
        child['bitstring'] = point_mutation(child['bitstring'], p_mutation)
        children.append(child)

    return children


def bitclimber(child, search_space, p_mutation, max_local_generations, bits_per_parameter):
    current = child

    for _ in range(max_local_generations):
        candidate = {}
        candidate['bitstring'] = point_mutation(
            current['bitstring'], p_mutation)
        calculate_fitness(candidate, search_space, bits_per_parameter)
        if candidate['fitness'] <= current['fitness']:
            current = candidate

    return current


def search(max_gens, search_space, population_size, p_crossover, p_mutation, max_local_generations, p_perform_local_search, bits_per_parameter):
    population = [{'bitstring': random_bit_string(
        len(search_space)*bits_per_parameter)} for _ in range(population_size)]

    for individual in population:
        calculate_fitness(individual, search_space, bits_per_parameter)

    population = sorted(population, key=lambda x: x['fitness'])

    best = population[0]

    for _ in range(max_gens):
        selected = [binary_tournament(population)
                    for _ in range(population_size)]
        children = reproduce(selected, p_crossover, p_mutation)
        for child in children:
            calculate_fitness(child, search_space, bits_per_parameter)
        population.clear()
        for child in children:
            if random.random() < p_perform_local_search:
                child = bitclimber(child, search_space, p_mutation,
                                   max_local_generations, bits_per_parameter)

            population.append(child)

        population = sorted(population, key=lambda x: x['fitness'])

        if population[0]['fitness'] <= best['fitness']:
            best = population[0]
    return best


if __name__ == '__main__':
    problem_size = 3
    search_space = [[-5, 5] for _ in range(problem_size)]
    max_gens = 100
    population_size = 100
    p_crossover = 0.98
    bits_per_parameter = 16
    p_mutation = 1/(problem_size*bits_per_parameter)
    max_local_generations = 20
    p_perform_local_search = 0.5

    best = search(max_gens, search_space, population_size, p_crossover,
                  p_mutation, max_local_generations, p_perform_local_search, bits_per_parameter)

    print(
        f"done! Solution: f={best['fitness']}, b={best['bitstring']},v={best['vector']}")
