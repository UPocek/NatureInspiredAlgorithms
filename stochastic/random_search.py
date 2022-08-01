import random


def objective_function(vector):
    return sum([x**2 for x in vector])


def random_vector(search_space):
    return [random.randint(lower_bound, upper_bound) for lower_bound, upper_bound in search_space]


def random_search(search_space, max_iter):
    best = None

    for _ in range(max_iter):
        candidate = {}
        candidate['vector'] = random_vector(search_space)
        candidate['cost'] = objective_function(candidate['vector'])
        if best is None or candidate['cost'] < best['cost']:
            best = candidate

    return best


if __name__ == '__main__':

    # f = sum(xi**2), i = {1,2...n}, -5 <= xi <= 5

    problem_size = 2
    search_space = [[-5, 5] for _ in range(problem_size)]
    max_iter = 100

    best = random_search(search_space, max_iter)
    print(f"Done. Best Solution: c={best['cost']}, v={best['vector']}")
