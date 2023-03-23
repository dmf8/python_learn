from functools import wraps


def decorator(f):
    @wraps(f)
    def wrapFunc():
        print("wrap begin")
        f()
        print("wrap end")

    return wrapFunc


@decorator  # func = decorator(func)
def func():
    print("main func")


# func = decorator(func)
func()
print("func name "+func.__name__)
