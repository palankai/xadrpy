
def is_method(func):
    return func.func_code.co_argcount >= 1 and func.func_code.co_varnames[0] == "self"
