import heapq
from solution import Literal
from solution import Clause
from time import time


def refutation_resolution(clauses: dict, goal_clause: Clause, verbose: bool):
    n = len(clauses) + 1
    sos_clauses = []
    print_arr = []
    for key, value in clauses.items():
        print_arr.append(f"{key}. {value}")
    print_arr.append("=============")

    for literal in goal_clause.literals:
        clause = Clause({Literal(literal.name, not literal.negation)}, 0)
        clauses[n] = clause
        sos_clauses.append(n)
        print_arr.append(f"{n}. {clause}")
        n += 1
    print_arr.append("=============")

    time1 = time()
    succ = pl_resolution(clauses, sos_clauses, print_arr, n)
    time2 = time()
    if verbose and succ:
        for s in print_arr:
            print(s)

    print(goal_clause, "is", "true" if succ else "unknown")
    if verbose:
        print(f"\nExecution time: {str(time2 - time1)}s")


def pl_resolution(clauses: dict, sos_clauses: list, print_arr: [], n: int):
    used_pairs = set()
    while True:
        new_clauses = []
        selected_clauses = select_clauses(clauses, sos_clauses, used_pairs)
        while selected_clauses:
            pair = heapq.heappop(selected_clauses)
            (i, j) = pair[2], pair[3]
            if i not in clauses.keys() or j not in clauses.keys():
                continue

            resolvents = pl_resolve(i, j, clauses)
            if not resolvents:
                print_arr.append(f"{n}. NIL {(i, j)}")
                print_arr.append("=============")
                return True

            if cannot_be_simplified(clauses, new_clauses, resolvents, sos_clauses):
                new_clauses.append(resolvents)

        if not new_clauses or new_clauses in [c.literals for c in clauses.values()]:
            return False
        n = add_to_dictionary(clauses, new_clauses, sos_clauses, print_arr, n)


def select_clauses(clauses, sos_clauses, used_pairs):
    selected_clauses = []
    heapq.heapify(selected_clauses)
    for i in reversed(sorted(list(clauses.keys()))):
        for j in reversed(sos_clauses):
            if i >= j or (i, j) in used_pairs:
                continue
            if contains_complementary_atom(clauses[i].literals, clauses[j].literals):
                heapq.heappush(selected_clauses, (clauses[i], clauses[j], i, j))
                used_pairs.add((i, j))

    return selected_clauses


def pl_resolve(i, j, clauses):
    c1 = list(clauses[i].literals)
    c2 = list(clauses[j].literals)
    literals = c1 + c2
    found_name = None
    for l1 in c1:
        for l2 in c2:
            if l1.name == l2.name and l1.negation != l2.negation:
                found_name = l1.name
                break

    if found_name:
        literals.remove(Literal(found_name, True))
        literals.remove(Literal(found_name, False))
    return Clause(set(literals), (i, j)) if len(literals) > 0 else None


def cannot_be_simplified(clauses, new_clauses, resolvents, sos_clauses):
    for literal in resolvents.literals:
        if Literal(literal.name, not literal.negation) in resolvents.literals:
            return False

    for index in list(clauses.keys()):
        if resolvents.literals.issuperset(clauses[index].literals):
            return False
        if clauses[index].literals.issuperset(resolvents.literals):
            del clauses[index]
            try:
                sos_clauses.remove(index)
            except ValueError:
                continue

    for clause in new_clauses.copy():
        if resolvents.literals.issuperset(clause.literals):
            return False
        if clause.literals.issuperset(resolvents.literals):
            new_clauses.remove(clause)

    return True


def contains_complementary_atom(literals_1, literals_2):
    for l1 in literals_1:
        if Literal(l1.name, not l1.negation) in literals_2:
            return True
    return False


def add_to_dictionary(clauses, new_clauses, sos_clauses, print_arr, n):
    for clause in new_clauses:
        sos_clauses.append(n)
        clauses[n] = clause
        print_arr.append(f"{n}. {clause} {clause.origin}")
        n += 1

    return n
