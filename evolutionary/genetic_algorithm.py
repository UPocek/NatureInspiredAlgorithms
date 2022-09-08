import random


def one_max(bitstring):
    sum = 0
    for el in bitstring:
        if el == '1':
            sum += 1
    return sum


def random_bitstring(bitstring_size):
    new_bitstring = ''
    for _ in range(bitstring_size):
        new_bitstring += random.choice(['0', '1'])
    return new_bitstring


def binary_tournament(population):
    i, j = random.randint(0, len(population) - 1), random.randint(
        0, len(population) - 1)
    while i == j:
        j = random.randint(0, len(population) - 1)
    return population[i] if population[i]['fitness'] > population[j]['fitness'] else population[j]


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


def crossover(parent1_bitstring, parent2_bitstring, breading_rate):
    if random.random() > breading_rate:
        return parent1_bitstring
    boundary = 1 + random.randint(0, len(parent1_bitstring) - 2)
    return parent1_bitstring[:boundary] + parent2_bitstring[boundary:]


def reproduce(selected, population_size, p_crossover, p_mutation):
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


def search(number_of_generations, bitstring_size, population_size, p_crossover, p_mutation):
    population = [{'bitstring': random_bitstring(
        bitstring_size)} for _ in range(population_size)]
    for i, genom in enumerate(population):
        population[i]['fitness'] = one_max(genom['bitstring'])

    best = sorted(population, key=lambda x: x['fitness'], reverse=True)[0]

    for _ in range(number_of_generations):
        selected = []
        for _ in range(population_size):
            selected.append(binary_tournament(population))

        children = reproduce(selected, population_size,
                             p_crossover, p_mutation)
        for i, genom in enumerate(children):
            children[i]['fitness'] = one_max(genom['bitstring'])

        children = sorted(children, key=lambda x: x['fitness'], reverse=True)

        if children[0]['fitness'] >= best['fitness']:
            best = children[0]

        new_population = []

        for i, genom in enumerate(population):
            if genom['fitness'] > children[0]['fitness']:
                new_population.append(genom)
            else:
                break
        new_population.extend(children[:len(children) - i])

        population = new_population

        if best['fitness'] == bitstring_size:
            break

    return best


if __name__ == '__main__':
    bitstring_size = 64
    number_of_generations = 100
    population_size = 100
    p_crossover = 0.98
    p_mutation = 1 / bitstring_size

    best = search(number_of_generations, bitstring_size,
                  population_size, p_crossover, p_mutation)
    print(f"Done! Solution: f={best['fitness']}, s={best['bitstring']}")
