from decimal import Decimal

unit_prfixes = {
    "T": Decimal(12),
    "G": Decimal(9),
    "M": Decimal(6),
    "k": Decimal(3),
    "": Decimal(0),
    "m": Decimal(-3),
    "u": Decimal(-6),
    "n": Decimal(-9),
    "p": Decimal(-12),
    "f": Decimal(-15),
}


def convertToBaseUnits(input_value):
    if len(input_value) < 2:
        return Decimal(input_value)
    if input_value[-1] in unit_prfixes:
        unit = input_value[-1]
        value = Decimal(input_value[:-1])
        value *= 10 ** unit_prfixes[unit]
        return value
    return Decimal(input_value)


def convertToPrefix(input_value, unit=""):
    if input_value is None:
        return ""
    if input_value == 0:
        return "0" + unit
    if input_value < 0:
        input_value = -input_value
        sign = "-"
    else:
        sign = ""
    for prefix in unit_prfixes:
        if input_value >= 10 ** unit_prfixes[prefix]:
            return sign + str(input_value / 10 ** unit_prfixes[prefix]) + prefix + unit
    return sign + str(input_value) + unit


def convertToShorthandNotation(input_value:str):
    # convert from prefix to shorthand notation
    if len(input_value.strip()) < 2:
        return input_value
    # find the decimal point
    decimal_point = input_value.find(".")
    if decimal_point == -1:
        if input_value[-1] == "Ω":
            return input_value[:-1] + "R"
        return input_value[:-1]
    # find the unit prefix
    unit_prefix = input_value[-2]
    # replace the decimal point with the unit prefix
    input_value = input_value[:decimal_point] + unit_prefix + input_value[decimal_point+1:-1]
    return input_value[:-1]
