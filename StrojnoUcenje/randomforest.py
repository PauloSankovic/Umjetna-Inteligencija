import random
from decisiontree import ID3


class RL:
    def __init__(self, mode: str, num_trees: int, max_depth: int, example_ratio: float, feature_ratio: float):
        self.mode = mode
        self.num_trees = num_trees
        self.max_depth = max_depth
        self.example_ratio = example_ratio
        self.feature_ratio = feature_ratio
        self.trees = []

    def add_tree(self, tree: ID3):
        self.trees.append(tree)

    def fit(self, td: dict, X: list, y: set):
        instance_subset = round(self.example_ratio * len(td))
        feature_subset = round(self.feature_ratio * len(X))

        for i in range(self.num_trees):
            tree = ID3(self.mode, self.max_depth)

            indexes = []
            instances = list(td.keys())
            td_new = {}
            for j in range(instance_subset):
                index = random.randint(0, len(td) - 1)
                indexes.append(index)
                td_new[instances[index]] = td[instances[index]]

            features = []
            for j in range(feature_subset):
                index = random.randint(0, len(X) - 1)
                features.append(X[index])

            for feature in features:
                print(feature, end=" ")
            print()

            for index in indexes:
                print(index, end=" ")
            print()

            tree.fit(td_new, features, y)
            self.add_tree(tree)

    def predict(self, test_dataset: list, X: list):
        predictions = []
        for tree in self.trees:
            predictions.append(tree.predict(test_dataset, X))

        results = []
        for i in range(len(test_dataset)):
            classes = {}
            for prediction in predictions:
                count = classes.get(prediction[i], 0)
                classes[prediction[i]] = count + 1

            results.append([v[0] for v in sorted(classes.items(), key=lambda kv: (-kv[1], kv[0]))][0])

        return results
