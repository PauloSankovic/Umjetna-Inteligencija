import sys
from decisiontree import ID3
from randomforest import RL


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
            train_dataset[tuple(parts[:-1])] = parts[-1]

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
            results.append(parts[-1])

    return test_dataset, results


def parse_config_file(file) -> dict:
    lines = open(file, 'r', encoding='utf-8').read().splitlines()

    config = {'max_depth': int(-1), 'num_trees': int(1), 'feature_ratio': float(1), 'example_ratio': float(1)}
    for line in lines:
        parts = line.split('=')
        if parts[0] == 'max_depth' or parts[0] == 'num_trees':
            config[parts[0]] = int(parts[1])
        elif parts[0] == 'feature_ratio' or parts[0] == 'example_ratio':
            config[parts[0]] = float(parts[1])
        else:
            config[parts[0]] = parts[1]

    return config


def get_accuracy(predictions: list, results: list) -> float:
    count = 0
    for i in range(len(results)):
        if predictions[i] == results[i]:
            count += 1

    return count / len(results)


def confusion_matrix(predictions: list, results: list, classes: list):
    n = len(classes)
    matrix = [[0 for x in range(n)] for y in range(n)]
    for i in range(n):
        indexes = []
        for index in range(len(results)):
            if results[index] == classes[i]:
                indexes.append(index)

        for j in range(len(classes)):
            count = 0
            for index in indexes:
                if predictions[index] == classes[j]:
                    count += 1
            matrix[i][j] = count

    return matrix


def main(argv):
    header, train_dataset = parse_train_set(argv[0])
    test_dataset, results = parse_test_set(argv[1])
    config = parse_config_file(argv[2])

    if config['model'] == 'ID3':
        model = ID3(config['max_depth'])
        model.fit(train_dataset, header[:-1], set(train_dataset.values()))
        model.print()
        print()
        predictions = model.predict(test_dataset, header[:-1])

    elif config['model'] == 'RF':
        model = RL(config['num_trees'], config['max_depth'], config['example_ratio'], config['feature_ratio'])
        model.fit(train_dataset, header[:-1], set(train_dataset.values()))
        predictions = model.predict(test_dataset, header[:-1])

    else:
        exit("Non implemented model")

    print(predictions[0], end="")
    for i in range(1, len(predictions)):
        print(f" {predictions[i]}", end="")
    print()

    print("{:.5f}".format(get_accuracy(predictions, results)))

    matrix = confusion_matrix(predictions, results, list(set(train_dataset.values())))
    for x in matrix:
        for y in x:
            print(y, end=" ")
        print()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        exit("Invalid number of parameters (3)")
    main(sys.argv[1:])
