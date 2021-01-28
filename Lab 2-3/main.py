"""
    Stare a problemei: [[Xc,Yc],[Xf,Yf],[[Xs,Ys]......[Xc-1,Yc-1]]]
    Matrice: [[X1i.......X1m][X2i.....X2m].......[Xni......Xnm]] i=1,n
    Stare initiala: [[Xs,Ys],[Xf,Yf],[[]]
    Starea finala: [[Xc,Yc],[Xf,Xf],[[Xs,Ys]......[Xc-1,Yc-1]]]

"""
from collections import deque
from copy import deepcopy
import math

matrix = list(list())


def get_binary_matrix():
    with open('lab.in', 'r') as f:
        line = [[int(num) for num in line.split(',')] for line in f]
    return line


def initialize_problem(init_x, init_y, final_x, final_y):
    return [[init_x, init_y], [final_x, final_y], []]


def check_is_final(state):
    if state[0] == state[1]:
        return True
    else:
        return False


def check_valid_move(move_x, move_y, matx, current_x, current_y):
    directions = [[current_x + 1, current_y],
                  [current_x, current_y + 1],
                  [current_x - 1, current_y],
                  [current_x, current_y - 1]]

    if move_x >= len(matrix) or move_x < 0 or move_y >= len(matrix[0]) or move_y < 0:
        return False
    if [move_x, move_y] in directions and matx[move_x][move_y] == 0:
        return True
    return False


def state_transition(state, move_x, move_y):
    global matrix
    if check_valid_move(move_x, move_y, matrix, state[0][0], state[0][1]):
        transition = deepcopy(state)
        transition[0][0] = move_x
        transition[0][1] = move_y
        transition[2].append([state[0][0], state[0][1]])
        return transition
    else:
        return None


def available_states(state):
    neighbours = list()
    current_x = state[0][0]
    current_y = state[0][1]

    down = state_transition(state, current_x + 1, current_y)
    right = state_transition(state, current_x, current_y + 1)
    up = state_transition(state, current_x - 1, current_y)
    left = state_transition(state, current_x, current_y - 1)

    if up is not None:
        neighbours.append(up)
    if down is not None:
        neighbours.append(down)
    if left is not None:
        neighbours.append(left)
    if right is not None:
        neighbours.append(right)

    return neighbours


def solve_bfs_strategy(state):
    queue_states = deque()
    discovered = list()
    #road = list()
    discovered.append(state)
    queue_states.append(state)
    reached = False

    while queue_states and not reached:
        current_state = queue_states.popleft()
        for visitable in available_states(current_state):
            if len([item for item in discovered if
                    (item[0][0], item[0][1]) == (visitable[0][0], visitable[0][1])]) == 0:
                if (visitable[0][0], visitable[0][1]) == (visitable[1][0], visitable[1][1]):
                    reached = True
                    discovered.append(visitable)
                    break
                discovered.append(visitable)
                queue_states.append(visitable)
    # road.append(discovered[-1][2][-1])
    # while road[-1] != state[0]:
    #     road.append([item[2][-1] for item in discovered if road[-1] == item[0]][0])
    # return road[::-1]
    if discovered[-1][2] is not []:
        return discovered[-1]
    else:
        return []


def solve_backtracking_strategy(state):
    stack = [[state, 0]]
    directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]

    while stack:
        current = stack[-1]
        current[1] = current[1] + 1
        if current[0][0] == current[0][1]:
            break
        if current[1] == 5:
            stack.pop()
        else:
            orientation = current[1] - 1
            transition = state_transition(current[0],
                                          current[0][0][0] + directions[orientation][0],
                                          current[0][0][1] + directions[orientation][1])
            if transition is not None and len([item for item in stack if transition[0] == item[0][0]]) == 0:
                stack.append([transition, 0])

    if stack:
        return stack[-1][0][2]
    else:
        return []


def solve_hillclimbing_strategy(state):
    adjacent = list()
    discovered = list()
    road = list()
    discovered.append(state[0])
    next_state = deepcopy(state)
    road.append(next_state[0])
    while True:
        minimum = math.sqrt(len(matrix) * len(matrix) + len(matrix[0]) * len(matrix[0]))
        for iterator in available_states(next_state):
            if iterator[0] not in discovered:
                adjacent.append(iterator)
        if not adjacent:
            break
        for iterator in adjacent:
            x = state[1][0] - iterator[0][0]
            y = state[1][1] - iterator[0][1]
            distance = math.sqrt(x * x + y * y)
            if distance < minimum:
                minimum = distance
                next_state = deepcopy(iterator)
                road.append(next_state[0])
                if iterator[0] not in discovered:
                    if iterator[0][0] == state[1][0] and iterator[0][1] == state[1][1]:
                        break
                    discovered.append(iterator[0])
        adjacent.clear()
    return road


if __name__ == '__main__':
    matrix = get_binary_matrix()
    print("DFS=", solve_bfs_strategy(initialize_problem(1, 9, 27, 6)))
    print("Backtracking=", solve_backtracking_strategy(initialize_problem(1, 9, 27, 6)))
    print("Hillclimbing=", solve_hillclimbing_strategy(initialize_problem(1, 9, 27, 6)))
