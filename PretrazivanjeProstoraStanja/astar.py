from decimal import Decimal
from collections import deque
import heapq
import time

def a_star_search(init_state, transitions, goal_states, heuristicValues):
    # open: total heuristic value (cost + heuristic), state name, cost, parent node
    open_nodes = []
    heapq.heappush(open_nodes, (heuristicValues[init_state], init_state, 0, None))
    # dictionary: state => cost
    open_states_dict = {init_state: 0}
    closed_states_dict = dict()

    while open_nodes:
        node = heapq.heappop(open_nodes)
        parent_name = node[1]
        parent_cost = node[2]

        if parent_name in goal_states:
            return closed_states_dict, node

        closed_states_dict[parent_name] = parent_cost   
        for child in transitions[parent_name]:
            # child: name, cost
            child_name = child[0]
            child_cost = child[1] + parent_cost
            
            if child_name in open_states_dict:
                child_duplicate_cost = open_states_dict[child_name]
                if child_duplicate_cost <= child_cost:
                    continue
                else:
                    del open_states_dict[child_name]
                    try:
                        open_nodes.remove(child_name)
                    except ValueError:
                        pass
                    heapq.heapify(open_nodes)

            elif child_name in closed_states_dict:
                child_duplicate_cost = open_states_dict[child_name]
                if child_duplicate_cost <= child_cost:
                    continue
                else:
                    del closed_states_dict[child_name]

            child_tuple = (child_cost + heuristicValues[child_name], child_name, child_cost, node)
            heapq.heappush(open_nodes, child_tuple)
            open_states_dict[child_name] = child_cost
    
    return closed_states_dict, False

def get_transition_values(line):
    split = line.split(' ')
    values = list()
    for pair in split:
        tupleValues = pair.split(',') 
        values.append((tupleValues[0], Decimal(tupleValues[1])))
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
            goal_states = line.split(' ')
            i += 1
        else:
            split = line.split(': ')
            if len(split) != 2:
                transitions[split[0]] = []
            else:
                transitions[split[0]] = get_transition_values(split[1])

    return init_state, goal_states, transitions

def parse_heuristic_file(filepath):
    lines = open(filepath, 'r', encoding='utf-8').read().splitlines()
    
    heuristicValues = dict()
    for line in lines:
        if line.startswith('#'):
            continue
        split = line.split(': ')
        heuristicValues[split[0]] = Decimal(split[1])

    return heuristicValues

def reconstruct_path(leaf):
    if not leaf[3]:
        return [leaf]
    node = leaf
    path = deque()
    while node:
        path.appendleft(node[1])
        node = node[3]
    return path

def print_path(path):
    for p in path:
        if p == path[-1]:
            print(p)
        else:
            print(p, '=>')

def main():
    filepathStateSpace = "lab1_state_spaces_and_heuristics/3x3_puzzle.txt"
    filepathHeuristic = "lab1_state_spaces_and_heuristics/3x3_misplaced_heuristic.txt"

    init_state, goal_states, transitions = parse_state_space_file(filepathStateSpace)
    
    print("Start state:", init_state)
    print("End state(s):", goal_states)
    print("State space size:", len(transitions))
    print("Total transitions:", sum([len(transitions[x]) for x in transitions]))

    heuristicValues = parse_heuristic_file(filepathHeuristic)

    print("\nRunning A*:")
    start = time.time()
    visited, leaf = a_star_search(init_state, transitions, goal_states, heuristicValues)
    end = time.time()
    if not leaf:
        print("A* failed")
    else:
        print("States visited =", len(visited))
        path = reconstruct_path(leaf)
        print("Found path of length {0} with total cost {1}:".format(len(path), leaf[2]))
        print_path(path)
    print("\nA* execution time: %.4f seconds" % (end - start))

if __name__ == "__main__":
    main()
