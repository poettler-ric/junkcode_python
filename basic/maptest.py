#!/usr/bin/python

def fact(a):
    if a < 0:
        raise ValueError("no negatives supported")

    if a <= 1:
        return 1
    return a * fact(a - 1)

if __name__ == '__main__':
    print(map(fact, range(10)))
