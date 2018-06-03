import attr


@attr.s
class Model(object):

    _vk = attr.ib(repr=False)


@attr.s
class ModelManager(object):

    _model_class = NotImplemented

    _vk = attr.ib(repr=False)

    def __call__(self, *args, **kwargs):
        return self._model_class(self._vk, *args, **kwargs)
