import sklearn


class Model:
    def __init__(self, class_weight = dict({1:0.9, 0:0.1}), n_estimators = 10, max_depth = 10, min_samples_split = 10):#后四个为随机森林超参
        '''
        对于任意一个model，输入的都是 Nxp 的已经处理过了的矩阵，可以直接套模型。
        所有模型都要记得进行中心化、标准化操作，尤其是PCA、Regression等
        在init里，主要是输入这个model的超参数，例如K、alpha等。
        '''
        self.class_weight = class_weight
        self.n_estimators = n_estimators 
        self.max_depth = max_depth 
        self.min_samples_split = min_samples_split
        

    def fit(self, X, y):
        '''
        fit 里输入 X 和 y 得到 model
        :param:
                X: X
                y：y
                *arg: 其他重要的东西继承下来
        '''
        from sklearn.ensemble import RandomForestClassifier
        self.clf = RandomForestClassifier(n_estimators = self.n_estimators,max_depth = self.max_depth,class_weight = self.class_weight,min_samples_split = self.min_samples_split)
        self.clf.fit(X, y)
        

    def predict(self, new_X):
        '''
        这个方程用来predict
        :param:
                new_X: 想要predict的X
        :return:
                predicted_y
        '''
        return self.clf.predict(new_X)

    def store(self, path):
        '''
        这个方程很重要，是用来存储我们训练过的model，
        之后用户使用我们的UI时只需要用这个pretrain model来做就可以了。
        可以用任何形式去存储这个model，比如json/npy等等，
        只要可以读取后复盘即可。
        '''
        from sklearn.externals import joblib#使用sklearn下的工具存储模型
        import os
        os.chdir(path)#调转路径
        joblib.dump(self.clf, "randomforest_model.m")
        
        #本地调回方法
        #clf = joblib.load("randomforest_model.m")