import random
from math import sqrt


def random_vector(minmax):
    return [minmax[i][0] + ((minmax[i][1] - minmax[i][0]) * random.random()) for i in range(len(minmax))]


def generate_random_pattern(domain):
    classes = list(domain.keys())
    selected_class_index = random.randint(0, len(classes)-1)
    pattern = {'label': classes[selected_class_index]}
    pattern['vector'] = random_vector(domain[classes[selected_class_index]])
    return pattern


def initialize_vectors(domain, num_vectors):
    classes = list(domain.keys())
    codebook_vectors = []
    for _ in range(num_vectors):
        selected_class_index = random.randint(0, len(classes)-1)
        codebook = {}
        codebook['label'] = classes[selected_class_index]
        codebook['vector'] = random_vector([[0, 1], [0, 1]])
        codebook_vectors.append(codebook)
    return codebook_vectors


def get_euclidean_distance(c1, c2):
    return sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)


def get_best_matching_unit(codebook_vectors, pattern):
    best, b_dist = None, None
    for codebook in codebook_vectors:
        dist = get_euclidean_distance(codebook['vector'], pattern['vector'])
        if b_dist is None or dist < b_dist:
            best, b_dist = codebook, dist
    return best


def update_codebook_vector(best_matching_unit, pattern, l_rate):
    for i in range(len(best_matching_unit['vector'])):
        error = pattern['vector'][i] - best_matching_unit['vector'][i]
        if best_matching_unit['label'] == pattern['label']:
            best_matching_unit['vector'][i] += l_rate * error
        else:
            best_matching_unit['vector'][i] -= l_rate * error


def train_network(codebook_vectors, domain, iterations, learning_rate):
    for iter in range(iterations):
        pattern = generate_random_pattern(domain)
        best_matching_unit = get_best_matching_unit(codebook_vectors, pattern)
        l_rate = learning_rate * (1 - (iter / iterations))
        if iter % 10 == 0:
            print(
                f"> iter={iter}, got={best_matching_unit['label']}, exp={pattern['label']}")
        update_codebook_vector(best_matching_unit, pattern, l_rate)


def test_network(codebook_vectors, domain, num_trials=100):
    correct = 0
    for _ in range(num_trials):
        pattern = generate_random_pattern(domain)
        best_matching_unit = get_best_matching_unit(codebook_vectors, pattern)
        if best_matching_unit['label'] == pattern['label']:
            correct += 1
    print(f"Done. Score: {correct}/{num_trials}")
    return correct


def execute(domain, iterations, num_vectors, learning_rate):
    codebook_vectors = initialize_vectors(domain, num_vectors)
    train_network(codebook_vectors, domain, iterations, learning_rate)
    test_network(codebook_vectors, domain)
    return codebook_vectors


if __name__ == '__main__':
    domain = {'A': [[0, 0.4999999], [0, 0.4999999]], 'B': [[0.5, 1], [0.5, 1]]}
    learning_rate = 0.3
    iterations = 1000
    num_vectors = 20
    execute(domain, iterations, num_vectors, learning_rate)
