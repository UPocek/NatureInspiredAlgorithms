import random


def random_in_bounds(min_bound, max_bound):
    return min_bound + (max_bound - min_bound) * random.random()


def print_program(node):
    if not (type(node) is tuple):
        return node
    return f"({node[0]} {print_program(node[1])} {print_program(node[2])})"


def generate_random_program(max_depth, functions, terms, current_depth=0):
    if current_depth >= max_depth - 1 or (current_depth > 1 and random.random() < 0.1):
        t = terms[random.randint(0, len(terms)-1)]
        return (random_in_bounds(-5.0, 5.0) if t == 'R' else t)
    current_depth += 1
    arg1 = generate_random_program(max_depth, functions, terms, current_depth)
    arg2 = generate_random_program(max_depth, functions, terms, current_depth)
    return functions[random.randint(0, len(functions)-1)], arg1, arg2


def evaluate_program(node, node_type_map):
    if not (type(node) is tuple):
        if node_type_map.get(node) is not None:
            return node_type_map[node]
        return node
    arg1, arg2 = evaluate_program(
        node[1], node_type_map), evaluate_program(node[2], node_type_map)
    if node[0] == '/' and arg2 == 0.0:
        return 1

    if node[0] == '+':
        return arg1 + arg2
    elif node[0] == '-':
        return arg1 - arg2
    elif node[0] == '*':
        return arg1 * arg2
    elif node[0] == '/':
        return arg1 / arg2


def count_nodes(node):
    if not (type(node) is tuple):
        return 1
    a1 = count_nodes(node[1])
    a2 = count_nodes(node[2])
    return a1+a2+1


def target_function(x):
    return x**2 + x + 1


def fitness(program, num_trials=20):
    sum_error = 0

    for _ in range(num_trials):
        x = random_in_bounds(-1.0, 1.0)
        error = evaluate_program(program, {'X': x}) - target_function(x)
        sum_error += abs(error)

    return sum_error / num_trials


def tournament_selection(population, number_of_individuals_to_compare):
    selected = [population[random.randint(
        0, len(population) - 1)] for _ in range(number_of_individuals_to_compare)]
    selected = sorted(selected, key=lambda x: x['fitness'])
    return selected[0]


def replace_node(node, replacement, replacement_node_depth, current_depth=0):
    if current_depth == replacement_node_depth:
        return replacement, current_depth + 1
    current_depth += 1
    if not (type(node) is tuple):
        return (node, current_depth)
    a1, current_depth = replace_node(
        node[1], replacement, replacement_node_depth, current_depth)
    a2, current_depth = replace_node(
        node[2], replacement, replacement_node_depth, current_depth)
    return (node[0], a1, a2), current_depth


def get_node(node, depth_of_wanted_node, current_depth=0):
    if current_depth == depth_of_wanted_node:
        return node, current_depth + 1
    current_depth += 1
    if not (type(node) is tuple):
        return None, current_depth
    a1, current_depth = get_node(node[1], depth_of_wanted_node, current_depth)
    if a1 is not None:
        return a1, current_depth
    a2, current_depth = get_node(node[2], depth_of_wanted_node, current_depth)
    if a2 is not None:
        return a2, current_depth
    return None, current_depth


def prune(node, max_depth, terms, current_depth=0):
    if current_depth == max_depth - 1:
        t = terms[random.randint(0, len(terms)-1)]
        return random_in_bounds(-5.0, 5.0) if t == 'R' else t
    current_depth += 1
    if not (type(node) is tuple):
        return node

    a1 = prune(node[1], max_depth, terms, current_depth)
    a2 = prune(node[2], max_depth, terms, current_depth)
    return node[0], a1, a2


def crossover(parent1, parent2, max_depth, terms):
    point1, point2 = random.randint(0, count_nodes(
        parent1)-1), random.randint(0, count_nodes(parent2)-1)
    tree1, _ = get_node(parent1, point1)
    tree2, _ = get_node(parent2, point2)
    child1, _ = replace_node(parent1, tree2, point1)
    child1 = prune(child1, max_depth, terms)
    child2, _ = replace_node(parent2, tree1, point2)
    child2 = prune(child2, max_depth, terms)
    return child1, child2


def mutation(parent, max_depth, functions, terms):
    random_tree = generate_random_program(max_depth/2, functions, terms)
    point = random.randint(0, count_nodes(parent))
    child, _ = replace_node(parent, random_tree, point)
    child = prune(child, max_depth, terms)
    return child


def search(max_gens, population_size, max_depth, number_of_individuals_to_compare, p_reproduction, p_crossover, p_mutation,
           functions, terms):
    population = [
        {'program': generate_random_program(max_depth, functions, terms)} for _ in range(population_size)]

    for i in range(population_size):
        population[i]['fitness'] = fitness(population[i]['program'])

    population = sorted(population, key=lambda x: x['fitness'])
    best = population[0]

    for _ in range(max_gens):
        children = []
        while len(children) < population_size:
            p_operation = random.random()
            first_parent = tournament_selection(
                population, number_of_individuals_to_compare)
            child1 = {}

            if p_operation < p_reproduction:
                child1['program'] = first_parent['program']
            elif p_operation < p_reproduction + p_crossover:
                second_parent = tournament_selection(
                    population, number_of_individuals_to_compare)
                child2 = {}
                child1['program'], child2['program'] = crossover(
                    first_parent['program'], second_parent['program'], max_depth, terms)
                children.append(child2)
            elif p_operation < p_reproduction + p_crossover + p_mutation:
                child1['program'] = mutation(
                    first_parent['program'], max_depth, functions, terms)

            if len(children) < population_size:
                children.append(child1)

        for i in range(population_size):
            children[i]['fitness'] = fitness(population[i]['program'])

        population = children
        population = sorted(
            population, key=lambda x: x['fitness'])
        if population[0]['fitness'] < best['fitness'] or (population[0]['fitness'] == best['fitness'] and len(population[0]['program']) < len(best['program'])):
            best = population[0]

    return best


if __name__ == "__main__":
    terms = ['X', 'R']
    functions = ['+', '-', '*', '/']

    max_gens = 100
    max_depth = 7
    population_size = 100
    number_of_individuals_to_compare = 5
    p_reproduction = 0.08
    p_crossover = 0.9
    p_mutation = 0.02
    best = search(max_gens, population_size, max_depth, number_of_individuals_to_compare,
                  p_reproduction, p_crossover, p_mutation, functions, terms)

    print(
        f"done! Solution: f={best['fitness']}, {print_program(best['program'])}")
