def fit_decorator(func):
    """Decorator to access the transformed input
    Args:
        func (function): fit
    Return (wrapper)
    """
    def fit_wrapper(*args, **kwargs):
        setattr(args[0], 'x_input', args[1])
        if len(args) > 2:
            setattr(args[0], 'y_input', args[2])
        return func(*args, **kwargs)
    return fit_wrapper
