import math
import heapq
import collections
from classes import Example


class Node:
    def __init__(self, v, subtrees: list, label: str):
        self.v = v
        self.subtrees = subtrees
        self.label = label


class Subtree:
    def __init__(self, v, node: Node):
        self.v = v
        self.node = node


class Leaf:
    def __init__(self, v):
        self.v = v


class ID3:
    def __init__(self, mode: str, max_depth: int):
        self.mode = mode
        self.max_depth = max_depth
        self.node = None

    def fit(self, td: list, X: list, y: set):
        feature_values = {}
        for i in range(len(X)):
            feature_values[X[i]] = set(map(lambda e: e.features[i], td))

        self.node = id3(td, td, X, y, feature_values, self.max_depth, 0, self.mode)

    def predict(self, test_dataset: list, X: list):
        predictions = []
        for test_case in test_dataset:
            predictions.append(id3_predict(self.node, test_case, X))

        return predictions

    def print_inner_nodes(self):
        print(f"{0}:{self.node.v}", end="")
        id3_print_inner_nodes(self.node, 0)


def id3(td: list, td_parent: list, X: list, y: set, feature_values: dict, max_depth: int, depth: int, mode):
    if len(td) == 0:
        label = most_frequent_label(td_parent)
        return Leaf(label)

    label = most_frequent_label(td)
    if len(X) == 0 or len(set(map(lambda e: e.cls, td))) == 1:
        return Leaf(label)

    if 0 <= max_depth <= depth:
        return Leaf(label)

    x = most_discriminative_feature(td, X, mode)
    if mode != 'test':
        print("Most discriminative feature:", x)
        print("======================================")

    subtrees = []
    index = X.index(x)
    X.remove(x)
    for v in feature_values[x]:
        td_copy = []
        for example in td:
            if example.features[index] == v:
                td_copy.append(Example(list(example.features[:index] + example.features[index + 1:]), example.cls))

        t = id3(td_copy, td, X.copy(), y.copy(), feature_values, max_depth, depth + 1, mode)
        subtrees.append(Subtree(v, t))

    return Node(x, subtrees, label)


def most_frequent_label(dataset):
    classes = list(map(lambda x: x.cls, dataset))
    counts = collections.Counter(classes)
    return sorted(classes, key=lambda x: (-counts[x], x))[0]


def most_discriminative_feature(dataset, X, mode):
    dataset_len = len(dataset)
    class_frequency = collections.Counter(list(map(lambda e: e.cls, dataset)))

    # entropy of the initial dataset
    id_entropy = 0
    for item in class_frequency.values():
        tmp = item / dataset_len
        id_entropy += tmp * math.log2(tmp)

    id_entropy *= -1
    if mode != 'test':
        print(f"Initial dataset entropy: {id_entropy}")

    information_gain = []
    heapq.heapify(information_gain)
    for i in range(len(X)):
        class_frequency = {}
        for example in dataset:
            values, cls = example.features, example.cls
            classes = class_frequency.get(values[i], {})
            freq = classes.get(cls, 0)
            classes[cls] = freq + 1
            class_frequency[values[i]] = classes

        # expected entropy
        expected_entropy = id_entropy
        for value in class_frequency.values():
            classes_len = 0
            for v in value.values():
                classes_len += v

            tmp_entropy = 0
            for v in value.values():
                tmp = v / classes_len
                tmp_entropy += tmp * math.log2(tmp)
            tmp_entropy *= -1

            expected_entropy -= classes_len / dataset_len * tmp_entropy

        if mode != 'test':
            print("IG({:s})={:.4f}".format(X[i], expected_entropy))
        heapq.heappush(information_gain, (expected_entropy * -1, X[i]))

    return heapq.heappop(information_gain)[1]


def id3_predict(parent, test_case, X):
    if isinstance(parent, Leaf):
        return parent.v

    index = X.index(parent.v)
    value = test_case[index]
    for subtree in parent.subtrees:
        if subtree.v == value:
            if isinstance(subtree.node, Node):
                return id3_predict(subtree.node, test_case, X)
            else:
                return subtree.node.v

    return parent.label


def id3_print_inner_nodes(parent: Node, index: int):
    if index != 0:
        print(f", {index}:{parent.v}", end="")
    for subtree in parent.subtrees:
        if isinstance(subtree.node, Node):
            id3_print_inner_nodes(subtree.node, index + 1)
