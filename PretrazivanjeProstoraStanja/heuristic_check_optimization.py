from decimal import Decimal
from collections import deque
import math
import heapq
import time

def check_heuristic_optimism(init_states, goal_states, transitions, heuristicValues):
    print("Checking if heuristic is optimistic.")

    fail = 0
    distance = dijkstra(goal_states, transitions, init_states)

    for state, cost in distance.items():
        h_value = heuristicValues[state]
        if cost < h_value:
            fail += 1

    if fail > 0:
        print('  [ERR]', fail ,'errors, omitting output.') 
    print('Heuristic is {:s}optimistic'.format("" if fail == 0 else "not "))

def dijkstra(init_states, transitions, goal_state):
    distance = dict()
    process_states = list()
    for state in transitions:
        if state in init_states:
            distance[state] = 0
            process_states.append((0, state))
        else:
            distance[state] = float("inf")
    distance[goal_state] = float("inf")

    heapq.heapify(process_states)
    visited_states = set()
    while process_states:
        parent = heapq.heappop(process_states)
        parent_distance = parent[0]
        parent_name = parent[1]

        visited_states.add(parent_name)
        if parent_name in transitions:
            for child_distance, child_name in transitions[parent_name]:
                if child_name in visited_states:
                    continue
                total_distance = parent_distance + child_distance 
                if not math.isinf(distance[child_name]) or distance[child_name] <= total_distance:
                    continue
                else:
                    distance[child_name] =  total_distance
                    heapq.heappush(process_states, (total_distance, child_name))

    return distance

def check_heuristic_consistency(transitions, heuristicValues):
    print("Checking if heuristic is consistent.")

    fail = 0
    for key, values in transitions.items():
        h_parent = heuristicValues[key]
        for value in values:
            h_child = heuristicValues[value[0]]
            cost = value[1]
            if h_parent > h_child + cost:
                fail += 1

    if fail > 0:
        print('  [ERR]', fail ,'errors, omitting output.')    
    print('Heuristic is {:s}consistent'.format("" if fail == 0 else "not "))

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
            split = line.split(':')
            if not split[1]:
                transitions[split[0]] = []
            else:
                transitions[split[0]] = get_transition_values(split[1].strip())

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

def reverse_transitions(transitions):
    reversed = dict()

    for parent_name, values in transitions.items():
        # values: list of tuples => (name, cost)
        for child_name, cost in values:
            if child_name not in reversed:
                list_of_parents = list()
            else:
                list_of_parents = reversed[child_name]
            list_of_parents.append((cost, parent_name))
            reversed[child_name] = list_of_parents

    return reversed

def main():
    filepathStateSpace = "lab1_state_spaces_and_heuristics/3x3_puzzle.txt"
    filepathHeuristic = "lab1_state_spaces_and_heuristics/3x3_misplaced_heuristic.txt"

    init_state, goal_states, transitions = parse_state_space_file(filepathStateSpace)
    heuristicValues = parse_heuristic_file(filepathHeuristic)

    rev_transitions = reverse_transitions(transitions)

    print("Checking heuristic")
    start = time.time()
    check_heuristic_consistency(transitions, heuristicValues)
    check_heuristic_optimism(init_state, goal_states, rev_transitions, heuristicValues)
    end = time.time()
    print("\nEvaluating the heuristic function in: %.4f seconds" % (end - start))

if __name__ == "__main__":
    main()
