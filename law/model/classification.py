import sklearn
from law.model.base_model import Model

class RandomForest(Model):
    def __init__(self, K):
        super().__init__()
        self.K = K