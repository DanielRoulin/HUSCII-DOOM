def lerp(x1, x2, percentage):
    """Linear interpolation implementation."""
    return (1- percentage)*x1 + percentage*x2

# TODO: Use f.__annotations to determine wanted type
def round_inputs(f):
    """Decorator, rounds all float functions parameters to int."""
    def wrapper(*args, **kwargs):
        r_args = []
        for arg in args:
            if isinstance(arg, float):
                arg = round(arg)
            r_args.append(arg)

        r_kwargs = {}
        for key, arg in kwargs.items():
            if isinstance(arg, float):
                arg = round(arg)
            r_kwargs[key] = arg

        f(*r_args, **r_kwargs)
    return wrapper