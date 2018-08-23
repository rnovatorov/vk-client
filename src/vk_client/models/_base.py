class Model(object):

    def __init__(self, vk):
        self._vk = vk


class ModelManager(Model):

    _model = NotImplemented

    def __call__(self, *args, **kwargs):
        return self._model(self._vk, *args, **kwargs)
