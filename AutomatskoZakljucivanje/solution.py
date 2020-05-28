import sys
import re
import resolution
import cooking_assistant


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

    def __lt__(self, other):
        return len(self.literals) < len(other.literals)

    def __hash__(self):
        return hash(self.__key())


def parse_clauses_file(clauses_file):
    lines = open(clauses_file, 'r', encoding='utf-8').read().splitlines()

    clauses = dict()
    i = 1
    for line in lines:
        if line.startswith('#'):
            continue
        split = re.split("\\s+v\\s+", line.lower())
        literals = set()
        for part in split:
            neg_num = part.count('~')
            literals.add(Literal(part.replace('~', ''), neg_num % 2 == 1))

        clauses[i] = Clause(literals, -1)
        i += 1
    return clauses


def parse_user_commands_file(user_commands_file):
    lines = open(user_commands_file, 'r', encoding='utf-8').read().splitlines()
    commands = []
    for line in lines:
        if line.startswith('#'):
            continue
        commands.append(line.lower())
    return commands


def run_program(program, clauses, user_commands, verbose):
    if program == "resolution":
        goal_clause = clauses.pop(len(clauses))
        resolution.refutation_resolution(clauses, goal_clause, verbose)
    elif program == "cooking_interactive":
        cooking_assistant.run_cooking_interactive(clauses, verbose)
    elif program == "cooking_test":
        cooking_assistant.run_cooking_test(clauses, user_commands, verbose)


def main(argv):
    program = argv[0]
    clauses_file = argv[1]
    user_commands_file = None
    verbose = False
    if len(argv) == 3:
        if argv[2] != "verbose":
            user_commands_file = argv[2]
        else:
            verbose = argv[2]
    elif len(argv) == 4:
        user_commands_file = argv[2]
        verbose = True

    clauses = parse_clauses_file(clauses_file)

    user_commands = None
    if user_commands_file:
        user_commands = parse_user_commands_file(user_commands_file)

    run_program(program, clauses, user_commands, verbose)


if __name__ == "__main__":
    main(sys.argv[1:])
