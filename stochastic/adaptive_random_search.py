import random


def objective_function(vector):
    return sum([x**2 for x in vector])


def random_from_bounds(lower_bound, upper_bound):
    return lower_bound + (upper_bound-lower_bound) * random.random()


def random_vector(search_space):
    return [random_from_bounds(lower_bound, upper_bound) for lower_bound, upper_bound in search_space]


def take_step(search_space, current_position, step_size):
    finish_position = [0] * len(current_position)
    for i in range(len(finish_position)):
        position_min = max(search_space[i][0], current_position[i] - step_size)
        position_max = min(search_space[i][1], current_position[i] + step_size)
        finish_position[i] = position_min + \
            (position_max - position_min) * random.random()
    return finish_position


def get_new_big_step_size(iter, step_size, small_step_size_factor, large_step_size_factor, enlarge_factor):
    if iter > 0 and iter % enlarge_factor == 0:
        return step_size * large_step_size_factor
    return step_size * small_step_size_factor


def take_steps(search_space, current, step_size, big_step_size):
    state_after_regular_step = take_regular_step(
        search_space, current, step_size)
    state_after_big_step = take_big_step(search_space, current, big_step_size)

    return state_after_regular_step, state_after_big_step


def take_regular_step(search_space, current, step_size):
    step_state = {}
    step_state['vector'] = take_step(
        search_space, current['vector'], step_size)
    step_state['cost'] = objective_function(step_state['vector'])

    return step_state


def take_big_step(search_space, current, big_step_size):
    big_step_state = {}
    big_step_state['vector'] = take_step(
        search_space, current['vector'], big_step_size)
    big_step_state['cost'] = objective_function(big_step_state['vector'])

    return big_step_state


def adaptive_random_search(max_iter, search_space, initial_step_size_factor, small_step_size_factor, large_step_size_factor, enlarge_factor, max_number_of_iterations_to_wait_for_improvement):
    current_state = {}
    count = 0
    step_size = sum((upper_bound - lower_bound)
                    for lower_bound, upper_bound in search_space) / len(search_space) * initial_step_size_factor

    current_state['vector'] = random_vector(search_space)
    current_state['cost'] = objective_function(current_state['vector'])

    for i in range(max_iter):
        big_step_size = get_new_big_step_size(
            i, step_size, small_step_size_factor, large_step_size_factor, enlarge_factor)
        state_after_regular_step, state_after_big_step = take_steps(
            search_space, current_state, step_size, big_step_size)

        if state_after_regular_step['cost'] <= current_state['cost'] or state_after_big_step['cost'] <= current_state['cost']:
            if state_after_big_step['cost'] <= state_after_regular_step['cost']:
                step_size, current_state = big_step_size, state_after_big_step
            else:
                current_state = state_after_regular_step
            count = 0
        else:
            count += 1
            if count >= max_number_of_iterations_to_wait_for_improvement:
                count, step_size = 0, (step_size/large_step_size_factor)

    return current_state


if __name__ == '__main__':

    # f = sum(xi**2), i = {1,2...n}, -5 <= xi <= 5

    problem_size = 2
    search_space = [[-5, 5] for _ in range(problem_size)]
    max_iter = 100
    initial_step_size_factor = 0.05
    small_step_size_factor = 1.2
    large_step_size_factor = 2.0
    enlarge_factor = 10
    max_number_of_iterations_to_wait_for_improvement = 30

    best = adaptive_random_search(
        max_iter, search_space, initial_step_size_factor, small_step_size_factor, large_step_size_factor, enlarge_factor, max_number_of_iterations_to_wait_for_improvement)

    print(f"Done. Best Solution: c={best['cost']}, v={best['vector']}")
