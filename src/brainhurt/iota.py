
COUNTER = -1


def iota(reset=False):
    global COUNTER

    if reset:
        COUNTER = 0

    _temp = COUNTER
    COUNTER += 1

    return _temp

