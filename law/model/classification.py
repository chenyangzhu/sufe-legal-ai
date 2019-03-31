from sklearn.ensemble import RandomForestClassifier
from law.model.base_model import Model
from sklearn.externals import joblib  # 使用sklearn下的工具存储模型


class RandomForest(Model):
    def __init__(self, class_weight={1: 0.9, 0: 0.1}, n_estimators=10,
                 max_depth=10, min_samples_split=10):
        super().__init__()
        self.class_weight = class_weight
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.clf = RandomForestClassifier(n_estimators=self.n_estimators,
                                          max_depth=self.max_depth,
                                          class_weight=self.class_weight,
                                          min_samples_split=self.min_samples_split)

    def fit(self, X, y):
        self.clf.fit(X, y)

    def predict(self, new_X):
        return self.clf.predict(new_X)

    def store(self, path="../.cache"):
        joblib.dump(self.clf, path + "/randomforest_model.m")


class Pretrained_RandomForest(RandomForest, Model):
    def __init__(self, dir="../.cache/andomforest_model.m"):
        super().__init__()
        self.clf = joblib.load(dir)
