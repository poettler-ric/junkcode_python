#!/usr/bin/python


def frange(*args):
    """range(...) yielding floats."""
    if len(args) == 1:
        return _frange(0, args[0], 1)
    if len(args) == 2:
        return _frange(args[0], args[1], 1)
    if len(args) == 3:
        return _frange(args[0], args[1], args[2])
    raise ValueError("frange is only defined for 1, 2 and 3 arguments")


def _frange(start, stop, step):
    """range(...) yielding floats."""
    cur = float(start)

    while cur < stop:
        yield cur
        cur += step

if __name__ == '__main__':
    print(" ".join("{:.1f}".format(n) for n in frange(10)))
    print(" ".join("{:.1f}".format(n) for n in frange(2, 10)))
    print(" ".join("{:.1f}".format(n) for n in frange(1, 2, .1)))
