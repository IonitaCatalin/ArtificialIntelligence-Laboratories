"""
    Modelarea problemei:

    Variabile:WA,SA,NT
    Domeniu:red,green,blue

    Adiacenta:
        {WA-SA},{WA-NT},{SA,WA},{SA-NT},{NT,WA},{NT-SA}
    Culori:
        WA={red,green,blue}
        SA={red,green}
        NT={green}

    Modelare:
        [[X1,X2,...Xi],[[C11,C12,...,C1n],.....,[Ci1,Ci2,...Cin]],[[X1,Y1],....,[Xi,Yi]]]
    Constrangere:   Pentru orice [Xi,Yj] C(Xi)!=C(Xj)
"""

from collections import deque


def initialize_csp():
    return [["WA", "SA", "NT"], [["red", "green", "blue"], ["red", "green"], ["green"]],
            [["WA", "SA"], ["WA", "NT"], ["SA", "WA"], ["SA", "NT"], ["NT", "WA"], ["NT", "SA"]]]


def domain(region, csp):
    return csp[1][csp[0].index(region)]


def remove_inconst_values(x_i, x_j, csp):
    removed = False
    for x in domain(x_i, csp):
        if len([value for value in domain(x_j, csp) if x != value]) == 0:
            removed = True
            csp[1][csp[0].index(x_i)].remove(x)

    return removed


def neighbors(region, csp):
    return [value[1] for value in csp[2] if value[0] == region]


def arc_consistency(csp):
    queue = deque()
    for value in csp[2]:
        queue.append(value)
    while queue:
        current = queue.pop()
        if remove_inconst_values(current[0], current[1], csp):
            for index in neighbors(current[0], csp):
                queue.append([index, current[0]])
    return csp


if __name__ == '__main__':
    print(arc_consistency(initialize_csp()))
