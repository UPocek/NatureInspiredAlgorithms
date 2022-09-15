import random
from math import sqrt


def random_vector(minmax):
    return [minmax[i][0] + ((minmax[i][1] - minmax[i][0]) * random.random()) for i in range(len(minmax))]


def initialize_vectors(domain, width, height):
    codebook_vectors = []
    for x in range(width):
        for y in range(height):
            codebook = {}
            codebook['vector'] = random_vector(domain)
            codebook['coord'] = [x, y]
            codebook_vectors.append(codebook)
    return codebook_vectors


def get_euclidean_distance(c1, c2):
    return sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)


def get_best_matching_unit(codebook_vectors, pattern):
    best, b_dist = None, None
    for codebook in codebook_vectors:
        dist = get_euclidean_distance(codebook['vector'], pattern)
        if b_dist is None or dist < b_dist:
            best, b_dist = codebook, dist
    return best, b_dist


def get_vectors_in_neighborhood(bmu, codebook_vectors, neighborhood_size):
    neighborhood = []
    for other in codebook_vectors:
        if get_euclidean_distance(bmu['coord'], other['coord']) <= neighborhood_size:
            neighborhood.append(other)
    return neighborhood


def update_codebook_vector(codebook, pattern, l_rate):
    for i in range(len(codebook['vector'])):
        error = pattern[i] - codebook['vector'][i]
        codebook['vector'][i] += l_rate * error


def train_network(vectors, shape, iterations, learning_rate, neighborhood_size):
    for iter in range(iterations):
        pattern = random_vector(shape)
        l_rate = learning_rate * (1 - (iter / iterations))
        neighborhood_size = neighborhood_size * (1 - (iter / iterations))
        bmu, dist = get_best_matching_unit(vectors, pattern)
        neighbors = get_vectors_in_neighborhood(
            bmu, vectors, neighborhood_size)
        for node in neighbors + [bmu]:
            update_codebook_vector(node, pattern, l_rate)
        print(f">training: neighbors={len(neighbors)}, bmu_dist={dist}")


def test_network(codebook_vectors, shape, num_trials=100):
    error = 0

    for _ in range(num_trials):
        pattern = random_vector(shape)
        _, dist = get_best_matching_unit(codebook_vectors, pattern)
        error += dist
    error /= num_trials
    print(f"Finished, average error={error}")
    return error


def execute(domain, shape, iterations, learning_rate, neighborhood_size, width, height):
    vectors = initialize_vectors(domain, width, height)
    train_network(vectors, shape, iterations, learning_rate, neighborhood_size)
    test_network(vectors, shape)
    return vectors


if __name__ == '__main__':
    domain = [[0.0, 1.0], [0.0, 1.0]]
    shape = [[0.3, 0.6], [0.3, 0.6]]
    iterations = 100
    learning_rate = 0.3
    neighborhood_size = 5
    width, height = 4, 5
    execute(domain, shape, iterations,
            learning_rate, neighborhood_size, width, height)
