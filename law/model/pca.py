import numpy as np
import numpy.linalg as la
import pandas as pd
from sklearn import linear_model

from law.model.base_model import Model
from sklearn.externals import joblib


class Pca(Model):
    def __init__(self, score=0.95, minpca=2, maxpca=10):
        super().__init__()
        self.score = score
        self.maxpca = 10 
        self.reg = linear_model.LogisticRegression()
        
        '''
        选择a个主成分使得这些主成分包含原数据95%的信息
        取2-10个主成分
        在该背景下一般第一个主成分即包含足够信息


    def fit(self, X, y):
        covx = X.cov()
        u,v = la.eig(covx)
        
        if np.sum(u[0:self.maxpca]/np.sum(u)) < self.score:
            a = self.maxpca
        
        elif np.sum(u[0:self.minpca]/np.sum(u)) > self.score:
            a = self.minpca
            
        else:
            a = 0
            i = 0
            while(a/np.sum(u) < self.score):
                a+=u[i]
                i+=1
        
        newx = X.dot(v[0:a].T.real)
        self.reg.fit(newx, y)

    def predict(self, new_X):
        return self.reg.predict(new_X)

    def store(self, path="../.cache"):
        joblib.dump(self.reg, path + "/pca_model.m")


class Pretrained_Pca(Pca, Model):
    def __init__(self, dir="../.cache/pca_model.m"):
        super().__init__()
        self.pca = joblib.load(dir)
