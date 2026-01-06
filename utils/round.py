import math


def round_to_tick(price, tick):
    return round(round(price / tick) * tick, 8)


def round_down(price, tick):
    return math.floor(price / tick) * tick


def round_up(price, tick):
    return math.ceil(price / tick) * tick
