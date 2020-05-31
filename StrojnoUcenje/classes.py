class Example:
    def __init__(self, features: list, cls: str):
        self.features = features
        self.cls = cls

    def get_all_by_indexes(self, indexes):
        result = []
        for i in indexes:
            result.append(self.features[i])
        return Example(result, self.cls)
