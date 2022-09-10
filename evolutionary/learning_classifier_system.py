import random


def neg(bit):
    return 0 if bit == 1 else 1


def target_function(action):
    x0, x1, x2, x3, x4, x5 = [int(action[i]) for i in range(6)]
    return neg(x0)*neg(x1)*x2 + neg(x0)*x1*x3 + x0*neg(x1)*x4 + x0*x1*x5


def new_classifier(condition, action, genaration, prediction=10, error=0, fitness=10):
    individual = {}
    individual['condition'], individual['action'], individual['lasttime'] = condition, action, genaration
    individual['prediction'], individual['error'], individual['fitness'] = prediction, error, fitness
    individual['exp'], individual['setsize'], individual['num'] = 0, 1, 1
    return individual


def copy_classifier(parent):
    copy = {}
    for key, value in parent.items():
        copy[key] = value
    copy['num'], copy['exp'] = 1, 0
    return copy


def random_bitstring_from_simulated_envirement(size=6):
    bitstring = ''
    for _ in range(size):
        bitstring += '1' if random.random() < 0.5 else '0'
    return bitstring


def calculate_deletion_vote(classifier, population, delete_threashold, f_threashold=0.1):
    vote = classifier['setsize'] * classifier['num']
    total = 0
    for classifier in population:
        total += classifier['num']
    avg_fitness = 0
    for classifier in population:
        avg_fitness += classifier['fitness']
    avg_fitness /= total

    derated = classifier['fitness'] / classifier['num']

    if classifier['exp'] > delete_threashold and derated < (f_threashold*avg_fitness):
        return vote * (avg_fitness / derated)
    return vote


def delete_from_population(population, population_size, delete_threashold=None):
    if delete_threashold is None:
        delete_threashold = population_size * 0.1
    total = 0
    for individual in population:
        total += individual['num']

    if total <= population_size:
        return

    for individual in population:
        individual['dvote'] = calculate_deletion_vote(
            individual, population, delete_threashold)

    vote_sum = 0
    for individual in population:
        vote_sum += individual['dvote']

    point = random.random() * vote_sum
    vote_sum, index = 0, 0
    for i, individual in enumerate(population):
        vote_sum += individual['dvote']
        if vote_sum >= point:
            index = i
            break

    if population[index]['num'] > 1:
        population[index]['num'] -= 1
    else:
        population.pop(index)


def generate_random_classifier(input, remaining_actions, genaration, rate_for_hash=1/3):
    condition = ''
    for i in range(len(input)):
        condition += '#' if random.random() < rate_for_hash else input[i]

    action = remaining_actions[random.randint(0, len(remaining_actions)-1)]

    return new_classifier(condition, action, genaration)


def does_match(input, condition):
    for i in range(len(input)):
        if condition[i] != '#' and input[i] != condition[i]:
            return False
    return True


def get_actions(population):
    actions = []

    for individual in population:
        if not individual['action'] in actions:
            actions.append(individual['action'])

    return actions


def generate_match_set(input, population, all_actions, genaration, population_size):
    match_set = []

    for individual in population:
        if does_match(input, individual['condition']):
            match_set.append(individual)

    actions = get_actions(match_set)

    while len(actions) < len(all_actions):
        remaining = [action for action in all_actions if action not in actions]
        classifier = generate_random_classifier(input, remaining, genaration)
        population.append(classifier)
        match_set.append(classifier)
        delete_from_population(population, population_size)
        actions.append(classifier['action'])

    return match_set


def generate_prediction(match_set):
    prediction = {}

    for classifier in match_set:
        key = classifier['action']
        if prediction.get(key) == None:
            prediction[key] = {'sum': 0, 'count': 0, 'weight': 0}
        prediction[key]['sum'] += classifier['prediction'] * \
            classifier['fitness']
        prediction[key]['count'] += classifier['fitness']

    for key in prediction.keys():
        prediction[key]['weight'] = 0
        if prediction[key]['count'] > 0:
            prediction[key]['weight'] = prediction[key]['sum'] / \
                prediction[key]['count']

    return prediction


def select_action(predictions):
    possible_actions = list(predictions.keys())
    possible_actions = sorted(
        possible_actions, key=lambda x: predictions[x]['weight'], reverse=True)
    return possible_actions[0]


def update_set(action_set, reward, beta=0.2):
    sum = 0
    for other in action_set:
        sum += other['num']

    for action in action_set:
        action['exp'] += 1
        if action['exp'] < 1 / beta:
            action['error'] = (action['error'] * (action['exp']-1) +
                               abs(reward - action['prediction'])) / action['exp']
            action['prediction'] = (
                action['prediction'] * (action['exp'] - 1) + reward) / action['exp']
            action['setsize'] = (action['setsize'] *
                                 (action['exp'] - 1) + sum) / action['exp']
        else:
            action['error'] += beta * \
                (abs(reward - action['prediction']) - action['error'])
            action['prediction'] += beta * (reward - action['prediction'])
            action['setsize'] += beta * (sum - action['setsize'])


def update_fitness(action_set, min_error=10, l_rate=0.2, alpha=0.1, v=-5):
    sum = 0
    acc = [0] * len(action_set)

    for i, action in enumerate(action_set):
        acc[i] = 1 if action['error'] < min_error else alpha * \
            (action['error'] / min_error)**v

        sum += acc[i] * action['num']

    for i, action in enumerate(action_set):
        action['fitness'] += l_rate * \
            ((acc[i] * action['num']) / sum - action['fitness'])


def can_run_genetic_algorithm(action_set, genaration, batch_size):
    if len(action_set) <= 2:
        return False

    total = 0
    sum = 0
    for action in action_set:
        total += action['lasttime'] * action['num']
        sum += action['num']

    if genaration - (total / sum) > batch_size:
        return True
    return False


def binary_tournament(population):
    i, j = random.randint(0, len(population) -
                          1), random.randint(0, len(population)-1)
    while j == i:
        j = random.randint(0, len(population)-1)
    return population[i] if population[i]['fitness'] < population[j]['fitness'] else population[j]


def mutation(classifier, action_set, input, mutation_rate=0.04):
    for i in range(len(classifier['condition'])-1):
        if random.random() < mutation_rate:
            if classifier['condition'][i] == '#':
                classifier['condition'] = classifier['condition'][:i] + \
                    input[i] + classifier['condition'][i + 1:]
            else:
                classifier['condition'] = classifier['condition'][:i] + \
                    '#' + classifier['condition'][i + 1:]
    if random.random() < mutation_rate:
        subset = [
            action for action in action_set if action not in classifier['action']]
        classifier['action'] = subset[random.randint(0, len(subset)-1)]


def uniform_crossover(parent1, parent2):
    child = ''
    for i in range(len(parent1)):
        child += parent1[i] if random.random() < 0.5 else parent2[i]

    return child


def insert_in_population(classifier, population):
    for individual in population:
        if classifier['condition'] == individual['condition'] and classifier['action'] == individual['action']:
            individual['num'] += 1
            return

    population.append(classifier)


def crossover(c1, c2, parent1, parent2):
    c1['condition'] = uniform_crossover(
        parent1['condition'], parent2['condition'])
    c2['condition'] = uniform_crossover(
        parent1['condition'], parent2['condition'])
    c2['prediction'] = c1['prediction'] = (
        parent1['prediction']+parent2['prediction'])/2
    c2['error'] = c1['error'] = (parent1['error']+parent2['error'])/2
    c2['fitness'] = c1['fitness'] = (parent1['fitness']+parent2['fitness'])/2


def calculate_populations_num(population):
    sum = 0
    for individual in population:
        sum += individual['num']
    return sum


def run_algorithm(all_actions, population, action_set, input, population_size, crossover_rate=0.8):
    parent1, parent2 = binary_tournament(
        action_set), binary_tournament(action_set)
    child1, child2 = copy_classifier(parent1), copy_classifier(parent2)
    if random.random() < crossover_rate:
        crossover(child1, child2, parent1, parent2)

    for clasifier in [child1, child2]:
        mutation(clasifier, all_actions, input)
        insert_in_population(clasifier, population)

    sum = calculate_populations_num(population)

    while sum > population_size:
        delete_from_population(population, population_size)
        sum = calculate_populations_num(population)


def train_model(max_population_size, max_gens, all_actions, batch_size, report_frequency):
    population, progress_tracker = [], []
    for current_generation in range(max_gens):
        explore = current_generation % 2 == 0
        input = random_bitstring_from_simulated_envirement()
        match_set = generate_match_set(
            input, population, all_actions, current_generation, max_population_size)
        predictions_array = generate_prediction(match_set)
        action = select_action(predictions_array)
        reward = 1000 if target_function(input) == int(action) else 0
        if explore:
            action_set = []
            for classifiers in match_set:
                if classifiers['action'] == action:
                    action_set.append(classifiers)
            update_set(action_set, reward)
            update_fitness(action_set)
            if can_run_genetic_algorithm(action_set, current_generation, batch_size):
                for individual in action_set:
                    individual['lasttime'] = current_generation
                run_algorithm(all_actions, population, action_set,
                              input, max_population_size)
        else:
            e = abs(predictions_array[action]['weight']-reward)
            a = 1 if reward > 0 else 0
            progress_tracker.append({'error': e, 'correct': a})
            if len(progress_tracker) >= report_frequency:
                s = 0
                for p in progress_tracker:
                    s += p['error']
                err = s / len(progress_tracker)
                s = 0
                for p in progress_tracker:
                    s += p['correct']
                acc = s / len(progress_tracker)
                print(
                    f"> iter={current_generation+1} size={len(population)}, error={err}, acc={acc}")
                progress_tracker = []
    return population


def test_model(system, num_trials=50):
    correct = 0
    for _ in range(num_trials):
        input = random_bitstring_from_simulated_envirement()
        match_set = []
        for s in system:
            if does_match(input, s['condition']):
                match_set.append(s)
        pred_array = generate_prediction(match_set)
        action = select_action(pred_array)
        correct += 1 if target_function(input) == int(action) else 0

    print(f"Done! classified correctly={correct}/{num_trials}")
    return correct


def execute(max_population_size, max_gens, all_actions, batch_size, report_frequency):
    system = train_model(max_population_size, max_gens, all_actions,
                         batch_size, report_frequency)
    test_model(system)
    return system


if __name__ == '__main__':
    all_actions = ['0', '1']
    max_gens, max_population_size = 5000, 200
    batch_size = 25
    report_frequency = 500
    model = execute(max_population_size, max_gens, all_actions,
                    batch_size, report_frequency)
