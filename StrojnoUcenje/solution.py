import sys


def parse_train_set(file):
    lines = open(file, 'r', encoding='utf-8').read().splitlines()

    i = 0
    train_dataset = {}
    header = []
    for line in lines:
        if i == 0:
            header = line.split(',')
            i += 1
        else:
            parts = line.split(',')
            train_dataset[tuple(parts[:len(header) - 1])] = list(parts[len(header) - 1:])

    return header, train_dataset


def parse_test_set(file):
    lines = open(file, 'r', encoding='utf-8').read().splitlines()

    i = 0
    test_dataset = []
    results = []
    header = []
    for line in lines:
        if i == 0:
            header = line.split(',')
            i += 1
        else:
            parts = line.split(',')
            test_dataset.append(tuple(parts[:len(header) - 1]))
            results.append(parts[len(header) - 1:])

    return test_dataset, results


def parse_config_file(file):
    lines = open(file, 'r', encoding='utf-8').read().splitlines()

    config = {'max_depth': float('Inf'), 'num_trees': int(1), 'feature_ratio': float(1), 'example_ratio': float(1)}
    for line in lines:
        parts = line.split('=')
        if parts[0] == 'max_depth' or parts[0] == 'num_trees':
            config[parts[0]] = int(parts[1])
        elif parts[0] == 'feature_ratio' or parts[0] == 'example_ratio':
            config[parts[0]] = float(parts[1])
        else:
            config[parts[0]] = parts[1]

    return config


def main(argv):
    header, train_dataset = parse_train_set(argv[0])
    test_dataset, results = parse_test_set(argv[1])
    config = parse_config_file(argv[2])


if __name__ == "__main__":
    if len(sys.argv) != 4:
        exit("Invalid number of parameters (3)")
    main(sys.argv[1:])
