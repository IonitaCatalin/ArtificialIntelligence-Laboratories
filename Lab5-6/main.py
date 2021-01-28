"""
    Stare:
        [[[Coordonate piese player],[Coordonate piese calculator]],[[Stare finala om],[Stare finala calculator]]]
"""
from copy import deepcopy

directions = [[0, 1], [0, -1], [-1, 0], [-1, 1], [-1, -1], [1, 0], [1, 1], [1, -1]]


def get_initial_state():
    return [[[[0, 0], [0, 1], [0, 2], [0, 3]], [[3, 0], [3, 1], [3, 2], [3, 3]]],
            [[[3, 0], [3, 1], [3, 2], [3, 3]], [[0, 0], [0, 1], [0, 2], [0, 3]]]]


def check_final_state(state):
    final_state_player = True
    final_state_computer = True
    for index in state[0][0]:
        if index not in state[1][0]:
            final_state_player = False
    for index in state[0][1]:
        if index not in state[1][1]:
            final_state_computer = False
    if final_state_computer or final_state_player:
        return True
    else:
        return False


def get_final_state_player():
    return [[[[3, 0], [3, 1], [3, 2], [3, 3]], [[3, 0], [3, 1], [3, 2], [3, 3]]],
            [[[3, 0], [3, 1], [3, 2], [3, 3]], [[0, 0], [0, 1], [0, 2], [0, 3]]]]


def get_final_state_ai():
    return [[[[0, 0], [0, 1], [0, 2], [0, 3]], [[0, 0], [0, 1], [0, 2], [0, 3]]],
            [[[3, 0], [3, 1], [3, 2], [3, 3]], [[0, 0], [0, 1], [0, 2], [0, 3]]]]


def is_valid_move(state, move_x, move_y, current_x, current_y):
    if move_x > 3 or move_y > 3 or move_x < 0 or move_y < 0:
        return False
    for i in range(0, 8):
        if current_x + directions[i][0] == move_x and current_y + directions[i][1] == move_y:
            if [move_x, move_y] not in state[0][0]:
                if [move_x, move_y] not in state[0][1]:
                    return True
    return False


def evaluate_state_score(state):
    computer_sum = 0
    opponent_sum = 0
    for index in range(0, 4):
        computer_sum += state[0][1][index][1]
    for index in range(0, 4):
        opponent_sum += state[0][0][index][1]

    return 12 - computer_sum - opponent_sum


def transition_to_state(current_state, move_x, move_y, current_x, current_y):
    if is_valid_move(current_state, move_x, move_y, current_x, current_y):
        transition = deepcopy(current_state)
        if [current_x, current_y] in transition[0][0]:
            found = transition[0][0].index([current_x, current_y])
            transition[0][0][found][0] = move_x
            transition[0][0][found][1] = move_y
        else:
            return None
        return transition


def transition_to_state_ai(current_state, move_x, move_y, current_x, current_y):
    if is_valid_move(current_state, move_x, move_y, current_x, current_y):
        transition = deepcopy(current_state)
        if [current_x, current_y] in transition[0][1]:
            found = transition[0][1].index([current_x, current_y])
            transition[0][1][found][0] = move_x
            transition[0][1][found][1] = move_y
        else:
            return None
        return transition


def generate_next_best_state(state):
    best_score = 0
    best_state = list(list())

    for opponent_coord in state[0][1]:
        for move in range(0, 8):
            if is_valid_move(state, opponent_coord[0] + directions[move][0], opponent_coord[1] + directions[move][1],
                             opponent_coord[0], opponent_coord[1]):
                transition = deepcopy(state)
                found = transition[0][1].index(opponent_coord)
                transition[0][1][found][0] = opponent_coord[0] + directions[move][0]
                transition[0][1][found][1] = opponent_coord[1] + directions[move][1]
                score = evaluate_state_score(transition)
                if score > best_score:
                    best_state = deepcopy(transition)
                    best_score = score
    return best_state


def display_table(state):
    table = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for i in range(0, 4):
        table[state[0][0][i][0]][state[0][0][i][1]] = 'P'
        table[state[0][1][i][0]][state[0][1][i][1]] = 'C'
    for i in range(4):
        for j in range(4):
            print(table[i][j], ' ', end='')
        print()
    print()


def generate_next_best_minimax(current_depth, max_depth, is_maximization_level, state, alpha_value, beta_value):
    if current_depth == max_depth:
        return state

    if is_maximization_level:
        best_value = -1000000
        best_state = state
        for player_move in state[0][0]:
            for direction in directions:
                to_state = transition_to_state(state,
                                               player_move[0] + direction[0],
                                               player_move[1] + direction[1],
                                               player_move[0], player_move[1])

                if to_state is not None:
                    value = generate_next_best_minimax(current_depth + 1,
                                                       max_depth, False,
                                                       to_state, alpha_value,
                                                       beta_value)

                    if evaluate_state_score(value) > best_value:
                        best_value = evaluate_state_score(value)
                        best_state = value
                    alpha_value = max(alpha_value, best_value)
                    if beta_value <= alpha_value:
                        break
        return best_state
    else:
        best_value = 1000000
        best_state = state
        for ai_move in state[0][1]:
            for direction in directions:
                to_state = transition_to_state_ai(state,
                                                  ai_move[0] + direction[0],
                                                  ai_move[1] + direction[1],
                                                  ai_move[0], ai_move[1])

                if to_state is not None:
                    value = generate_next_best_minimax(current_depth + 1, max_depth,
                                                       True, to_state, alpha_value,
                                                       beta_value)

                    if evaluate_state_score(value) < best_value:
                        best_value = evaluate_state_score(value)
                        best_state = value
                    beta_value = min(beta_value, best_value)
                    if beta_value <= alpha_value:
                        break
        return best_state


if __name__ == '__main__':

    current_state = get_initial_state()
    display_table(current_state)

    while check_final_state(current_state) is False:

        ideal = generate_next_best_minimax(0, 2, True, current_state, -1000000, 1000000)
        ideal[0][0] = current_state[0][0]
        current_state = ideal
        print("AI moved!It's player turn!")
        display_table(current_state)
        while True:
            player_position_x = int(input('Input the x of the piece you wish to move:'))
            player_position_y = int(input('Input the y of the piece you wish to move:'))
            player_move_x = int(input('Input the x of where you wish to move:'))
            player_move_y = int(input('Input the y of where you wish to move:'))
            transition = transition_to_state(current_state, player_move_x, player_move_y, player_position_x,
                                             player_position_y)
            if transition is not None:
                current_state = deepcopy(transition)
                print("Player moved!")
                display_table(current_state)
                break
            else:
                print("Invalid move,please try again!")
                display_table(current_state)
        if check_final_state(current_state):
            print('Game ended!There is a winner!')
            break
