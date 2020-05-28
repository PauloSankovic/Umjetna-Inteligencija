from collections import deque
import time

def breadth_first_search(init_state, transitions, goal_statess):
    open_nodes = deque([(init_state, None)])
    open_states = set()
    visited_states = set()
    while open_nodes:
        node = open_nodes.popleft()
        parent = node[0]
        visited_states.add(parent)
        if parent in goal_statess:
            return visited_states, node
        for child in transitions[parent]: 
            if child not in visited_states and child not in open_states:
                open_nodes.append((child, node))
                open_states.add(child)    
    return visited_states, False

def get_transition_values(line):
    split = line.split(' ')
    values = list()
    for pair in split:
        values.append(pair.split(',')[0])
    return values

def parse_state_space_file(filepath):
    lines = open(filepath, 'r', encoding='utf-8').read().splitlines()

    i = 0
    transitions = dict()
    for line in lines:
        if line.startswith('#'): 
            continue
        if i == 0:
            init_state = line
            i += 1
        elif i == 1:
            goal_statess = line.split(' ')
            i += 1
        else:
            split = line.split(':')
            if not split[1]:
                transitions[split[0]] = []
            else:
                transitions[split[0]] = get_transition_values(split[1].strip())

    return init_state, goal_statess, transitions

def reconstruct_path(leaf):
    if not leaf[1]:
        return [leaf]
    node = leaf
    path = deque()
    while node:
        path.appendleft(node[0])
        node = node[1]
    return path

def print_path(path):
    for p in path:
        if p == path[-1]:
            print(p)
        else:
            print(p, '=>')

def main():
    filepath = "lab1_state_spaces_and_heuristics/ai.txt"

    init_state, goal_statess, transitions = parse_state_space_file(filepath)

    print("Start state:", init_state)
    print("End state(s):", goal_statess)
    print("State space size:", len(transitions))
    print("Total transitions:", sum([len(transitions[x]) for x in transitions]))

    print("\nRunning bfs:")
    start = time.time()
    visited, leaf = breadth_first_search(init_state, transitions, goal_statess)
    end = time.time()
    if not leaf:
        print("BFS failed")
    else:
        print("States visited =", len(visited))
        path = reconstruct_path(leaf)
        print("Found path of length {0}:".format(len(path)))
        print_path(path)
    print("\nBFS execution time: %.4f seconds" % (end - start))

if __name__ == "__main__":
    main()
