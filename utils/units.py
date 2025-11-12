from decimal import Decimal

unit_prfixes = {
    "T": Decimal(12),
    "G": Decimal(9),
    "M": Decimal(6),
    "k": Decimal(3),
    "": Decimal(0),
    "m": Decimal(-3),
    "u": Decimal(-6),
    "μ": Decimal(-6),  # Greek mu character
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


def convertToShorthandNotation(input_value: str):
    # convert from prefix to shorthand notation
    if not input_value:
        return ""
    # divice the input value to value and unit
    lastnum = -1
    input_value = input_value.strip()
    for i in range(len(input_value)):
        if input_value[len(input_value) - i - 1].isdigit():
            lastnum = len(input_value) - i
            break
    if lastnum == -1:
        return input_value

    value = input_value[:lastnum]
    unit = input_value[lastnum:]
    decimal_point = value.find(".")
    if unit[0] in unit_prfixes:
        unit = unit[0]
    elif unit[0] == "Ω":
        unit = "R"
    else:
        return input_value

    if decimal_point == -1:
        return value + unit
    return value[:decimal_point] + unit + value[decimal_point + 1:]
