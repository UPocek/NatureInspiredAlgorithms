import random


def one_max(vector):
    return sum(vector)


def random_bit_string(number_of_bits):
    bitstring = []
    for _ in range(number_of_bits):
        if random.random() < 0.5:
            bitstring.append(1)
        else:
            bitstring.append(0)
    return bitstring


def path_exists(i, j, graph):
    visited, stack = [], [i]

    while len(stack) != 0:
        if j in stack:
            return True
        k = stack.pop(0)
        if k in visited:
            continue
        visited.append(k)
        for m in graph[k]['out']:
            if m not in visited:
                stack.append(m)
    return False


def can_add_edge(i, j, graph):
    return j not in graph[i]['out'] and not path_exists(j, i, graph)


def get_viable_parents(node_index, graph):
    viable = []
    for index in range(len(graph)):
        if node_index != index and can_add_edge(node_index, index, graph):
            viable.append(index)
    return viable


def compute_count_for_edges(selected, indexes):
    counts = [0] * (2**len(indexes))
    for member in selected:
        index = 0
        indexes_r = list(reversed(indexes))
        for i, v in enumerate(indexes_r):
            if member['bitstring'][v] == '1':
                index += 2**i
        counts[index] += 1
    return counts


def fact(v):
    return 1 if v <= 1 else v * fact(v-1)


def k2equation(node_index, candidates, selected):
    counts = compute_count_for_edges(selected, [node_index]+candidates)
    total = None
    for i in range(len(counts)//2):
        a1, a2 = counts[i*2], counts[i*2+1]
        rs = (1/fact(a1+a2+1)) * fact(a1) * fact(a2)
        if total is None:
            total = rs
        else:
            total = total * rs
    return total


def compute_gains(node, graph, selected, max=2):
    viable = get_viable_parents(node['num'], graph)
    gains = [-1] * len(graph)
    for i in range(len(gains)):
        if len(graph[i]['in']) < max and i in viable:
            gains[i] = k2equation(node['num'], node['in']+[i], selected)
    return gains


def construct_network(selected, num_bits, max_edges=None):
    if max_edges is None:
        max_edges = 3 * len(selected)

    graph = [{'out': [], 'in':[], 'num':i} for i in range(num_bits)]
    gains = [0] * num_bits

    for i in range(max_edges):
        max, from_i, to_i = -1, None, None
        for i, node in enumerate(graph):
            gains[i] = compute_gains(node, graph, selected)
            for gains_i, v in enumerate(gains[i]):
                if v > max:
                    from_i, to_i, max = i, gains_i, v
        if max <= 0:
            break
        graph[from_i]['out'].append(to_i)
        graph[to_i]['in'].append(from_i)

    return graph


def topological_ordering(graph):
    for node in graph:
        node['count'] = len(node['in'])
    ordered = []
    stack = [node for node in graph if node['count'] == 0]
    while len(ordered) < len(graph):
        current = stack.pop(0)
        for egde_index in current['out']:
            for n in graph:
                if n['num'] == egde_index:
                    node = n

            node['count'] -= 1
            if node['count'] <= 0:
                stack.append(node)
        ordered.append(current)
    return ordered


def marginal_probability(i, population):
    s = 0
    for x in population:
        s += x['bitstring'][i]

    return s / len(population)


def calculate_probability(node, bitstring, population):
    if len(node['in']) == 0:
        return marginal_probability(node['num'], population)
    counts = compute_count_for_edges(population, [node['num']] + node['in'])
    index = 0
    in_r = list(reversed(node['in']))

    for i, v in enumerate(in_r):
        if bitstring[v] == 1:
            index += 2**i

    i1 = index + (1*2**(len(node['in'])))
    i2 = index + (0*2**(len(node['in'])))
    a1, a2 = counts[i1], counts[i2]
    try:
        return a1/(a1+a2)
    except Exception:
        return 1


def probabilistic_logic_sample(graph, population):
    bitstring = [0] * len(graph)
    for node in graph:
        prob = calculate_probability(node, bitstring, graph, population)
        bitstring[node['num']] = 1 if random.random() < prob else 0
    return {'bitstring': bitstring}


def sample_from_network(population, graph, num_samples):
    ordered = topological_ordering(graph)
    samples = [probabilistic_logic_sample(
        ordered, population) for _ in range(num_samples)]
    return samples


def search(num_bits, max_iter, population_size, select_size, num_children):
    population = [{'bitstring': random_bit_string(
        num_bits)} for _ in range(population_size)]
    for member in population:
        member['cost'] = one_max(member['bitstring'])

    population = sorted(population, key=lambda x: x['cost'], reverse=True)
    best = population[0]

    for _ in range(max_iter):
        selected = population[:select_size]
        network = construct_network(selected, num_bits)
        children = sample_from_network(selected, network, num_children)
        for child in children:
            child['cost'] = one_max(child['bitstring'])

        population = population[0:(population_size-select_size)] + children
        population = sorted(population, key=lambda x: x['cost'], reverse=True)
        if population[0]['cost'] >= best['cost']:
            best = population[0]
    return best


if __name__ == '__main__':
    num_bits = 20
    max_iter = 100
    population_size = 50
    select_size = 15
    num_children = 25

    best = search(num_bits, max_iter, population_size,
                  select_size, num_children)
    print(
        f"done! Solution: f={best['cost']}/{num_bits}, s={best['bitstring']}")
