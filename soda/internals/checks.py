
def IsNumber(obj):
    return hasattr(obj, "is_signed_integer") or \
           hasattr(obj, "is_unsigned_integer") or \
           hasattr(obj, "is_floating_point")


def IsFloat(obj):
    return hasattr(obj, "is_floating_point")


def IsBool(obj):
    return hasattr(obj, "is_bool_type")


def FindUnusedParameters(state):
    for var in state.defined_variables:
        if not state.defined_variables[var].isUsed():
            state.warning_handler("Unused parameter.", state.defined_variables[var].getSpan())