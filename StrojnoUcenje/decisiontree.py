import math
import heapq


class Node:
    def __init__(self, v, subtrees: list):
        self.v = v
        self.subtrees = subtrees


class Subtree:
    def __init__(self, v, node: Node):
        self.v = v
        self.node = node


class Leaf:
    def __init__(self, v):
        self.v = v


class ID3:
    def __init__(self, hyper_parameter=()):
        self.hyper_parameter = hyper_parameter
        self.node = None

    def fit(self, td: dict, td_parent: dict, X: list, y: set):
        self.node = id3(td, td_parent, X, y)

    def predict(self, test_dataset: list, X: list):
        predictions = []
        for test_case in test_dataset:
            predictions.append(id3_predict(self.node, test_case, X))

        return predictions

    def print(self):
        print_nodes(self.node, 0)


def id3_predict(parent: Node, test_case, X):
    index = X.index(parent.v)
    value = test_case[index]
    for subtree in parent.subtrees:
        if subtree.v == value:
            if isinstance(subtree.node, Node):
                return id3_predict(subtree.node, test_case, X)
            else:
                return subtree.node.v

    return 'maybe'


def print_nodes(parent: Node, index: int):
    print(f"{index}:{parent.v}", end=", ")
    for subtree in parent.subtrees:
        if isinstance(subtree.node, Node):
            print_nodes(subtree.node, index + 1)


def id3(td: dict, td_parent: dict, X: list, y: set):
    if len(td) == 0:
        v = most_frequent_label(td_parent)
        return Leaf(v)

    v = most_frequent_label(td)
    if len(X) == 0 or len(set(td.values())) == 1:
        return Leaf(v)

    x = most_discriminative_feature(td, X)
    print("Most discriminative feature:", x)

    subtrees = []
    index = X.index(x)
    X.remove(x)
    for v in set(i[index] for i in td):
        td_copy = {}
        for item, value in td.items():
            if item[index] == v:
                td_copy[item[:index] + item[index + 1:]] = value

        t = id3(td_copy, td, X, y)
        subtrees.append(Subtree(v, t))

    return Node(x, subtrees)


def most_frequent_label(dataset):
    return max(set(dataset.values()), key=list(dataset.values()).count)


def most_discriminative_feature(dataset, X):
    class_frequency = {}
    dataset_len = len(dataset)
    for item in dataset.values():
        v = class_frequency.get(item, 0)
        class_frequency[item] = v + 1

    # entropy of the initial dataset
    id_entropy = 0
    for item in class_frequency.values():
        tmp = item / dataset_len
        id_entropy += tmp * math.log2(tmp)

    id_entropy *= -1

    information_gain = []
    heapq.heapify(information_gain)
    for i in range(len(X)):
        class_frequency = {}
        for values, cls in dataset.items():
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

        print("IG({:s})={:.4f}".format(X[i], expected_entropy))
        heapq.heappush(information_gain, (expected_entropy * -1, X[i]))

    return heapq.heappop(information_gain)[1]
