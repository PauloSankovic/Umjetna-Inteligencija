class Example:
    def __init__(self, features: list, cls: str):
        self.features = features
        self.cls = cls

    def copy(self):
        return Example(self.features, self.cls)
