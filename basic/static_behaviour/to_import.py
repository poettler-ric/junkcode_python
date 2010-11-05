var = None

def get_var():
    return var

def set_var(value):
    """
    The global keyword is only needed in functions modifying this variable.
    """
    global var
    var = value
