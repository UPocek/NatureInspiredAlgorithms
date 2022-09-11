import random


def objective_function(vector):
    return sum([x**2 for x in vector])


def random_within_search_space(lower_bound, upper_bound):
    return lower_bound + (upper_bound-lower_bound) * random.random()


def generate_random_vector(search_space):
    return [random_within_search_space(lower_bound, upper_bound) for lower_bound, upper_bound in search_space]


def generate_random_harmony(search_space):
    harmony = {}
    harmony['vector'] = generate_random_vector(search_space)
    harmony['fitness'] = objective_function(harmony['vector'])

    return harmony


def initialize_harmony_memory(search_space, memory_size, factor=3):
    memory = [generate_random_harmony(search_space)
              for _ in range(factor*memory_size)]

    memory = sorted(memory, key=lambda x: x['fitness'])
    return memory[:memory_size]


def generate_harmony(search_space, memory, memory_consideration_rate, adjust_rate, change_range):
    vector = [0] * len(search_space)

    for i in range(len(search_space)):
        if random.random() < memory_consideration_rate:
            value = memory[random.randint(0, len(memory)-1)]['vector'][i]
            if random.random() < adjust_rate:
                value = value + change_range * \
                    random_within_search_space(-1.0, 1.0)
            value = max(value, search_space[i][0])
            value = min(value, search_space[i][1])
            vector[i] = value
        else:
            vector[i] = random_within_search_space(
                search_space[i][0], search_space[i][1])

    return vector


def search(search_space, max_iter, memory_size, memory_cosideration_rate, adjust_rate, change_range):
    memory = initialize_harmony_memory(search_space, memory_size)
    best = memory[0]

    for _ in range(max_iter):
        harm = {}
        harm['vector'] = generate_harmony(
            search_space, memory, memory_cosideration_rate, adjust_rate, change_range)
        harm['fitness'] = objective_function(harm['vector'])

        if harm['fitness'] < best['fitness']:
            best = harm

        memory.append(harm)
        memory = sorted(memory, key=lambda x: x['fitness'])
        memory.pop(-1)

    return best


if __name__ == '__main__':
    problem_size = 3
    search_space = [[-5, 5] for _ in range(problem_size)]
    max_iter = 500
    memory_size = 20
    memory_cosideration_rate = 0.95
    adjust_rate = 0.7
    change_range = 0.05

    best = search(search_space, max_iter, memory_size,
                  memory_cosideration_rate, adjust_rate, change_range)
    print(f"done! Solution: f={best['fitness']}, s={best['vector']}")
