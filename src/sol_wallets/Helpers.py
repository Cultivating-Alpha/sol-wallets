from decimal import Decimal as D
from typing import Union
import math


def normalize_fraction(decim: D) -> D:
    normalized = decim.normalize()
    sign, digit, exponent = normalized.as_tuple()
    return normalized if exponent <= 0 else normalized.quantize(1)


def decimal_from_value(value: Union[str, int, float]) -> D:
    return normalize_fraction(D(str(value)))


def round_value(_value: str | float, _step: float, how: str = "down") -> float:
    step = decimal_from_value(_step)
    value = decimal_from_value(_value)
    if how == "down":
        return float(value // step * step)
    elif how == "up":
        return float(math.ceil(value / step) * step)
    else:
        return float(round(value / step) * step)
