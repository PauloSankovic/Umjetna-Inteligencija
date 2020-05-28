import re
import resolution


class Literal:
    def __init__(self, name: str, negation: bool):
        self.name = name
        self.negation = negation

    def negate(self):
        self.negation = not self.negation

    def __key(self):
        return self.name, self.negation

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __hash__(self):
        return hash(self.__key())

    def __str__(self):
        return "{0}{1}".format('~' if self.negation else '', self.name)

    def __repr__(self):
        return "{0}{1}".format('~' if self.negation else '', self.name)


class Clause:
    def __init__(self, literals: set, origin):
        self.literals = literals
        self.origin = origin

    def __repr__(self):
        rez = ""
        i = len(self.literals)
        for literal in self.literals:
            rez += literal.__repr__()
            if i - 1 > 0:
                rez += " v "
                i -= 1
        return rez

    def __key(self):
        return self.literals, self.literals

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __hash__(self):
        return hash(self.__key())


def run_cooking_interactive(clauses: dict, verbose: bool):
    print("Testing cooking assistant with standard resolution")
    print("Constructed with knowledge:")
    for clause in clauses.values():
        print(f"> {clause}")
    print()

    while True:
        query = input("Please enter your query\n> ").lower().strip()
        if query == "exit":
            print("-> exiting...")
            break

        if query == "print":
            for clause in clauses.values():
                print(f"-> {clause}")
            print()
            continue

        clause_str = query[:-1].strip()
        if not clause_str:
            print("Invalid query\n")
            continue

        clause = parse_clause(clause_str)
        option = query[-1]
        if option == '?':
            resolution.refutation_resolution(clauses.copy(), clause, verbose)
        elif option == '+':
            add_clause(clause, clauses)
            print("-> added:", clause)

        elif option == '-':
            for key in list(clauses):
                if clauses[key] == clause:
                    print("-> deleted:", clauses[key])
                    del clauses[key]

        else:
            print("Invalid query")
        print()


def run_cooking_test(clauses: dict, user_commands: list, verbose: bool):
    for query in user_commands:
        clause = parse_clause(query[:-1].strip())
        option = query[-1]
        if option == '?':
            resolution.refutation_resolution(clauses.copy(), clause, verbose)
        elif option == '+':
            add_clause(clause, clauses)
        elif option == '-':
            for key in list(clauses):
                if clauses[key] == clause:
                    del clauses[key]
                #GREŠKA
                    # del key
        else:
            print("Invalid operator")


def parse_clause(string):
    split = re.split("\\s+v\\s+", string)
    literals = set()
    for part in split:
        neg_num = part.count('~')
        literals.add(Literal(part.replace('~', ''), neg_num % 2 == 1))

    return Clause(literals, -1)


def add_clause(clause, clauses):
    i = 1
    while True:
        if i in clauses.keys():
            i += 1
            continue
        clauses[i] = clause
        return
