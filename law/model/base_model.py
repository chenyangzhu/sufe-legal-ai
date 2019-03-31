import sklearn


class Model:
    def __init__(self, *arg):
        '''
        对于任意一个model，输入的都是 Nxp 的已经处理过了的矩阵，可以直接套模型。

        所有模型都要记得进行中心化、标准化操作，尤其是PCA、Regression等

        在init里，主要是输入这个model的超参数，例如K、alpha等。
        '''

    def fit(self, X, y, *arg, **kwargs):
        '''
        fit 里输入 X 和 y 得到 model
        :param:
                X: X
                y：y
                *arg: 其他重要的东西继承下来
        '''
        pass

    def predict(self, new_X, *arg, **kwargs):
        '''
        这个方程用来predict
        :param:
                new_X: 想要predict的X
        :return:
                predicted_y
        '''
        pass

    def store(self, path='../.cache/'):
        '''
        这个方程很重要，是用来存储我们训练过的model，
        之后用户使用我们的UI时只需要用这个pretrain model来做就可以了。
        可以用任何形式去存储这个model，比如json/npy等等，
        只要可以读取后复盘即可。
        '''

        pass

    def read(self, dir='../.cache/xxx.m'):
        '''
        用这个function来读取我们训练过的model
        '''
        pass
