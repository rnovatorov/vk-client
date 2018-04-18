def negative(inst, attr, value):
    assert value < 0


def positive(inst, attr, value):
    assert value > 0


def not_zero(inst, attr, value):
    assert value != 0
