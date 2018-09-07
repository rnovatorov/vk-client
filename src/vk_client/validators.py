from vk_client import utils


def negative(value):
    return utils.is_int(value) and value < 0


def positive(value):
    return utils.is_int(value) and value > 0


def not_zero(value):
    return utils.is_int(value) and value != 0
