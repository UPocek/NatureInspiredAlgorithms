import random
from math import sqrt


def random_from_bounds(lower_bound, upper_bound):
    return lower_bound + (upper_bound-lower_bound) * random.random()


def random_vector(search_space):
    return [random_from_bounds(lower_bound, upper_bound) for lower_bound, upper_bound in search_space]


def generate_random_pattern(domain):
    class_label = list(domain.keys())[random.randint(0, len(domain.keys())-1)]
    pattern = {'label': class_label}
    pattern['vector'] = random_vector(domain[class_label])
    return pattern


def create_cell(vector, class_label):
    return {'label': class_label, 'vector': vector}


def initialize_cells(domain):
    memory_cells = []
    for class_label in domain:
        memory_cells.append(create_cell(
            random_vector([[0, 1], [0, 1]]), class_label))
    return memory_cells


def get_euclidean_distance(city_from, city_to):
    return sqrt((city_from[0] - city_to[0])**2 + (city_from[1] - city_to[1])**2)


def stimulate(memory_cells, pattern):
    range = get_euclidean_distance([0.0, 0.0], [1.0, 1.0])
    for cell in memory_cells:
        cell['affinity'] = get_euclidean_distance(
            cell['vector'], pattern['vector']) / range
        cell['stimulation'] = 1 - cell['affinity']


def get_most_stimulated_cell(memory_cells, pattern):
    stimulate(memory_cells, pattern)
    return sorted(memory_cells, key=lambda x: x['stimulation'], reverse=True)[0]


def mutate_cell(cell, best_match):
    range = 1 - best_match['stimulation']
    for i, x in enumerate(cell['vector']):
        min_i = max(x - range / 2, 0)
        max_i = min(x + range / 2, 1)
        cell['vector'][i] = min_i + ((max_i-min_i) * random.random())
    return cell


def create_arb_pool(best_match, clone_rate, mutate_rate):
    pool = []
    pool.append(create_cell(best_match['vector'], best_match['label']))
    num_clones = round(best_match['stimulation'] * clone_rate * mutate_rate)
    for _ in range(num_clones):
        cell = create_cell(best_match['vector'], best_match['label'])
        pool.append(mutate_cell(cell, best_match))
    return pool


def compatetion_from_resources(pool, clone_rate, max_resources):
    for cell in pool:
        cell['resources'] = cell['stimulation'] * clone_rate

    total_resources = 0
    for cell in pool:
        total_resources += cell['resources']

    while total_resources > max_resources:
        cell = pool.pop(-1)
        total_resources -= cell['resources']


def refine_arb_pool(pool, pattern, stimulation_threashold, clone_rate, max_resources):
    mean_stimulation, candidate = 0, None

    while True:
        stimulate(pool, pattern)
        candidate = sorted(
            pool, key=lambda x: x['stimulation'], reverse=True)[0]
        mean_stimulation = 0
        for cell in pool:
            mean_stimulation += cell['stimulation']
        mean_stimulation = mean_stimulation / len(pool)
        if mean_stimulation < stimulation_threashold:
            compatetion_from_resources(
                pool, clone_rate, max_resources)
            for i in range(len(pool)):
                cell = create_cell(pool[i]['vector'], pool[i]['label'])
                mutate_cell(cell, pool[i])
                pool.append(cell)
        if mean_stimulation >= stimulation_threashold:
            break
    return candidate


def add_candidate_to_memory_cells(candidate, best_match, memory_cells):
    if candidate['stimulation'] > best_match['stimulation']:
        memory_cells.append(candidate)


def classify_pattern(memory_cells, pattern):
    stimulate(memory_cells, pattern)
    return sorted(memory_cells, key=lambda x: x['stimulation'], reverse=True)[0]


def train_system(memory_cells, domain, num_patterns, clone_rate, mutate_rate, stimulation_threashold, max_resources):
    for _ in range(num_patterns):
        pattern = generate_random_pattern(domain)
        best_match = get_most_stimulated_cell(memory_cells, pattern)
        if best_match['label'] != pattern['label']:
            memory_cells.append(create_cell(
                pattern['vector'], pattern['label']))
        else:
            pool = create_arb_pool(best_match,
                                   clone_rate, mutate_rate)
            cand = refine_arb_pool(
                pool, pattern, stimulation_threashold, clone_rate, max_resources)
            add_candidate_to_memory_cells(cand, best_match, memory_cells)


def test_system(memory_cells, domain, num_trials=50):
    correct = 0
    for _ in range(num_trials):
        pattern = generate_random_pattern(domain)
        best = classify_pattern(memory_cells, pattern)
        if best['label'] == pattern['label']:
            correct += 1
    return correct


def execute(domain, num_patterns, clone_rate, mutate_rate, stimulation_threashold, max_resources, test_dataset_size):
    memory_cells = initialize_cells(domain)
    train_system(memory_cells, domain, num_patterns, clone_rate,
                 mutate_rate, stimulation_threashold, max_resources)
    correct = test_system(memory_cells, domain, test_dataset_size)
    return correct


if __name__ == '__main__':
    domain = {'A': [[0, 0.4999999], [0, 0.4999999]], 'B': [[0.5, 1], [0.5, 1]]}
    num_patterns = 50
    clone_rate = 10
    mutate_rate = 2
    stimulation_threashold = 0.9
    max_resources = 150
    test_dataset_size = 50
    correct = execute(domain, num_patterns, clone_rate,
                      mutate_rate, stimulation_threashold, max_resources, test_dataset_size)
    print(f"done! Correct: f= {correct} / {test_dataset_size}")
