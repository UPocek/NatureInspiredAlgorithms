import random
from math import sqrt


def random_from_bounds(lower_bound, upper_bound):
    return lower_bound + (upper_bound-lower_bound) * random.random()


def random_vector(search_space):
    return [random_from_bounds(lower_bound, upper_bound) for lower_bound, upper_bound in search_space]


def get_euclidean_distance(city_from, city_to):
    return sqrt((city_from[0] - city_to[0])**2 + (city_from[1] - city_to[1])**2)


def contains(vector, space):
    for i, x in enumerate(vector):
        if x < space[i][0] or x > space[i][1]:
            return False
    return True


def matches(vector, dataset, minimum_distance):
    for pattern in dataset:
        dist = get_euclidean_distance(vector, pattern['vector'])
        if dist <= minimum_distance:
            return True
    return False


def generate_detectors(number_of_detectors, search_space, self_dataset, minimum_distance):
    detectors = []
    while True:
        detector = {'vector': random_vector(search_space)}
        if not matches(detector['vector'], self_dataset, minimum_distance):
            if not matches(detector['vector'], detectors, 0):
                detectors.append(detector)
        if len(detectors) >= number_of_detectors:
            break
    return detectors


def generate_self_dataset(num_records, self_space, search_space):
    self_dataset = []
    while True:
        pattern = {}
        pattern['vector'] = random_vector(search_space)
        if matches(pattern['vector'], self_dataset, 0):
            continue
        if contains(pattern['vector'], self_space):
            self_dataset.append(pattern)
        if len(self_dataset) >= num_records:
            break
    return self_dataset


def apply_detectors(detectors, search_space, self_dataset, minimum_distance, test_dataset_size):
    correct = 0
    test_dataset = [random_vector(search_space)
                    for _ in range(test_dataset_size)]
    for input in test_dataset:
        predicted = 'N' if matches(
            input, detectors, minimum_distance) else 'S'
        expected = 'S' if matches(
            input, self_dataset, minimum_distance) else 'N'
        if expected == predicted:
            correct += 1
    return correct


def execute(search_space, self_space, number_of_detectors, self_dataset_size, minimum_distance, test_dataset_size):
    self_dataset = generate_self_dataset(
        self_dataset_size, self_space, search_space)
    print(f"Done: prepared {len(self_dataset)} self patterns.")
    detectors = generate_detectors(
        number_of_detectors, search_space, self_dataset, minimum_distance)
    print(f"Done: prepared #{len(detectors)} detectors.")
    correct = apply_detectors(detectors, search_space,
                              self_dataset, minimum_distance, test_dataset_size)
    return correct


if __name__ == '__main__':

    # two-class classification problem where samples are drawn from a domain, where xi ∈ [0, 1]. Those samples in 1.0 > xi > 0.5 are classified as self and the rest of the space belongs to the non-self class.

    problem_size = 2
    search_space = [[0, 1] for _ in range(problem_size)]
    self_space = [[0.5, 1] for _ in range(problem_size)]
    self_dataset_size = 150
    max_detectors = 300
    min_dist = 0.05
    test_dataset_size = 50
    correct = execute(search_space, self_space,
                      max_detectors, self_dataset_size, min_dist, test_dataset_size)
    print(f"done! Correct: f={correct}")
