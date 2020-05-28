from decimal import Decimal
from collections import deque
import heapq
import time

def check_heuristic_optimism(goal_states, transitions, heuristicValues):
    print("Checking if heuristic is optimistic.")
    optimistic = True

    for state in transitions:
        result = uniform_cost_search(state, transitions, goal_states)
        h_state = heuristicValues[state]
        if result[0] < h_state:
            optimistic = False
            print('  [ERR] h({0}) > h*: {1} > {2}'.format(state, h_state, result[0]))

    print('Heuristic is {:s}optimistic'.format("" if optimistic else "not "))

def uniform_cost_search(init_state, transitions, goal_states):
    # open: total cost, state name
    open_nodes = []
    heapq.heappush(open_nodes, (0, init_state))
    open_states_dict = {init_state: 0}
    visited_states_dict = dict()
    
    while open_nodes:
        node = heapq.heappop(open_nodes)
        parent_cost = node[0]
        parent_name = node[1]
        
        visited_states_dict[parent_name] = parent_cost  
        if parent_name in goal_states:
            return node

        for child in transitions[parent_name]:
            # child: name, cost
            child_name = child[0]
            child_cost = child[1] + parent_cost
            if child_name in open_states_dict:
                if open_states_dict[child_name] <= child_cost:
                    continue
                else:
                    del open_states_dict[child_name]
                    try:
                        open_nodes.remove(child_name)
                    except ValueError:
                        pass
                    heapq.heapify(open_nodes)

            if child_name in visited_states_dict:
                if visited_states_dict[child_name] <= child_cost:
                    continue
                else:
                    del visited_states_dict[child_name]
                
            heapq.heappush(open_nodes, (child_cost, child_name))
            open_states_dict[child_name] = child_cost
            
    return False

def check_heuristic_consistency(transitions, heuristicValues):
    print("Checking if heuristic is consistent.")
    consistent = True

    for key, values in transitions.items():
        h_parent = heuristicValues[key]
        for value in values:
            h_child = heuristicValues[value[0]]
            cost = value[1]
            if h_parent > h_child + cost:
                consistent = False
                print('  [ERR] h({0}) > h({1}) + c: {2} > {3} + {4}'.format(key, value[0], h_parent, h_child, cost))
            
    print('Heuristic is {:s}consistent'.format("" if consistent else "not "))

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
            i += 1
        elif i == 1:
            goal_states = line.split(' ')
            i += 1
        else:
            split = line.split(':')
            if not split[1]:
                transitions[split[0]] = []
            else:
                transitions[split[0]] = get_transition_values(split[1].strip())

    return goal_states, transitions

def parse_heuristic_file(filepath):
    lines = open(filepath, 'r', encoding='utf-8').read().splitlines()
    
    heuristicValues = dict()
    for line in lines:
        if line.startswith('#'):
            continue
        split = line.split(': ')
        heuristicValues[split[0]] = Decimal(split[1])

    return heuristicValues

def main():
    filepathStateSpace = "lab1_state_spaces_and_heuristics/istra.txt"
    filepathHeuristic = "lab1_state_spaces_and_heuristics/istra_heuristic.txt"

    goal_states, transitions = parse_state_space_file(filepathStateSpace)
    heuristicValues = parse_heuristic_file(filepathHeuristic)

    print("Checking heuristic")
    start = time.time()
    check_heuristic_optimism(goal_states, transitions, heuristicValues)
    check_heuristic_consistency(transitions, heuristicValues)
    end = time.time()
    print("\nEvaluating the heuristic function in: %.4f seconds" % (end - start))

if __name__ == "__main__":
    main()
