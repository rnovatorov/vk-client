import attr


@attr.s
class Model(object):

    _vk = attr.ib(repr=False)


def model_manager(model_class=None):

    @attr.s
    class ModelManager(object):

        _vk = attr.ib(repr=False)

        if model_class is not None:
            def __call__(self, *args, **kwargs):
                return model_class(self._vk, *args, **kwargs)

    return ModelManager
