from backpropcore.model._model import CyModel

class Model:

    def __init__(self):
        self.layer = None
        self.optimizer = None
        self.obj = CyModel()

    def train(self):
        pass

    def build(self, ipt):
        self.obj.build(ipt)

    def backprop(self):
        pass


