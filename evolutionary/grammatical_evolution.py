import random
import re


def random_bitstring(num_bits):
    bitstring = ''
    for _ in range(num_bits):
        bitstring += random.choice(['0', '1'])
    return bitstring


def binary_tournament(population):
    i, j = random.randint(0, len(population) -
                          1), random.randint(0, len(population)-1)
    while j == i:
        j = random.randint(0, len(population)-1)
    return population[i] if population[i]['fitness'] < population[j]['fitness'] else population[j]


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


def one_point_crossover(parent1_bitstring, parent2_bitstring, number_of_bits_in_codon, p_crossover=0.3):
    if random.random() > p_crossover:
        return parent1_bitstring

    cut = random.randint(0, min(len(parent1_bitstring), len(parent2_bitstring)) //
                         number_of_bits_in_codon)
    cut *= number_of_bits_in_codon
    return parent1_bitstring[:cut] + parent2_bitstring[cut:]


def codon_duplication(bitstring, number_of_bits_in_codon, duplication_rate=None):
    if duplication_rate is None:
        duplication_rate = 1/number_of_bits_in_codon

    if random.random() > duplication_rate:
        return bitstring

    codons = len(bitstring)//number_of_bits_in_codon
    selected_codon_start = random.randint(
        0, codons-1) * number_of_bits_in_codon
    return bitstring + bitstring[selected_codon_start:selected_codon_start+number_of_bits_in_codon]


def codon_deletion(bitstring, number_of_bits_in_codon, deletion_rate=None):
    if deletion_rate is None:
        deletion_rate = 0.5/number_of_bits_in_codon

    if random.random() > deletion_rate:
        return bitstring

    codons = len(bitstring)//number_of_bits_in_codon
    offset_from_start = random.randint(0, codons) * number_of_bits_in_codon
    return bitstring[:offset_from_start] + bitstring[offset_from_start+number_of_bits_in_codon:]


def reproduce(selected, p_crossoverover, number_of_bits_in_codon):
    children = []

    for i, parent1 in enumerate(selected):
        if i == len(selected)-1:
            parent2 = selected[0]
        else:
            parent2 = selected[i + 1] if i % 2 == 0 else selected[i-1]

        child = {}
        child['bitstring'] = one_point_crossover(
            parent1['bitstring'], parent2['bitstring'], number_of_bits_in_codon, p_crossoverover)
        child['bitstring'] = codon_deletion(
            child['bitstring'], number_of_bits_in_codon)
        child['bitstring'] = codon_duplication(
            child['bitstring'], number_of_bits_in_codon)
        child['bitstring'] = point_mutation(child['bitstring'])
        children.append(child)

    return children


def decode_integers(bitstring, number_of_bits_in_codon):
    integers = []
    for current_offset in range(len(bitstring) // number_of_bits_in_codon):
        codon = bitstring[current_offset *
                          number_of_bits_in_codon:current_offset * number_of_bits_in_codon + number_of_bits_in_codon]
        sum = 0
        for i in range(len(codon)):
            if codon[i] == '1':
                sum += 2**i
        integers.append(sum)
    return integers


def map(grammar, integers, max_depth):
    done, offset, current_depth = False, 0, 0
    symbolic_string = grammar['START']

    while True:
        done = True
        for key in grammar.keys():
            occurences = re.findall(key, symbolic_string)
            for occurence in occurences:
                done = False
                if occurence == 'EXP' and current_depth >= max_depth - 1:
                    set = grammar['VAR']
                else:
                    set = grammar[occurence]
                integer = integers[offset] % len(set)
                offset = 0 if offset == len(integers) - 1 else offset + 1
                symbolic_string = symbolic_string.replace(
                    occurence, set[integer], 1)
        current_depth += 1
        if done:
            break

    return symbolic_string


def target_function(x):
    return x**4 + x**3 + x**2 + x


def random_in_search_space(min_bound, max_bound):
    return min_bound + (max_bound - min_bound) * random.random()


def cost(program, search_space, num_trials=30):
    if program.strip() == 'X':
        return 9999999
    sum_error = 0
    for _ in range(num_trials):
        x = random_in_search_space(search_space[0], search_space[1])
        expression = re.sub('X', str(x), program)
        try:
            score = eval(expression)
        except Exception:
            return 9999999

        sum_error += abs(score - target_function(x))

    return sum_error / num_trials


def evaluate(candidate, number_of_bits_in_codon, grammer, max_depth, search_space):
    candidate['integers'] = decode_integers(
        candidate['bitstring'], number_of_bits_in_codon)
    candidate['program'] = map(grammer, candidate['integers'], max_depth)
    candidate['fitness'] = cost(candidate['program'], search_space)


def search(max_gens, population_size, number_of_bits_in_codon, num_bits, p_crossover, grammar, max_depth, search_space):
    population = [{'bitstring': random_bitstring(
        num_bits)} for _ in range(population_size)]

    for individual in population:
        evaluate(individual, number_of_bits_in_codon,
                 grammar, max_depth, search_space)

    population = sorted(population, key=lambda x: x['fitness'])
    best = population[0]

    for _ in range(max_gens):
        selected = [binary_tournament(population)
                    for _ in range(population_size)]
        children = reproduce(selected,
                             p_crossover, number_of_bits_in_codon)
        for child in children:
            evaluate(child, number_of_bits_in_codon,
                     grammar, max_depth, search_space)
        children = sorted(children, key=lambda x: x['fitness'])

        if children[0]['fitness'] < best['fitness']:
            best = children[0]

        union = sorted(population + children, key=lambda x: x['fitness'])

        population = union[:population_size]

    return best


if __name__ == '__main__':
    grammar = {'START': 'EXP', 'EXP': [' EXP BINARY EXP ', ' (EXP BINARY EXP) ', ' VAR '], 'BINARY': [
        '+', '-', '/', '*'], 'VAR': ['X', '1.0']}
    search_space = [1, 10]
    max_depth = 7
    max_gens = 50
    population_size = 100
    number_of_bits_in_codon = 4
    num_bits = 10 * number_of_bits_in_codon
    p_crossover = 0.3
    best = search(max_gens, population_size, number_of_bits_in_codon,
                  num_bits, p_crossover, grammar, max_depth, search_space)
    print(f"done! Solution: f={best['fitness']}, s={best['program']}")
