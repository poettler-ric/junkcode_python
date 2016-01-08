#!/usr/bin/python

"""Testing implementations of reversed."""


def reverse_list(l):
    result = list(l)
    # casting to int necessary for python3
    for i in range(int(len(result)/2)):
        result[i], result[-(i+1)] = result[-(i+1)], result[i]
    return result


def reverse_generator(l):
    for i in range(1, len(l) + 1):
        yield(l[-i])


def test_reverse(r):
    print("=== {} ===".format(r.__name__))
    print(r(range(1)))
    print(r(range(2)))
    print(r(range(3)))
    print(r(range(4)))
    print(r(range(5)))
    print("reverse: {}".format(r("meter")))
    print("reverse joined: {}".format("".join(r("meter"))))
    print("plain comparison: {}".format(r("meter") == "retem"))
    print("joined comparision: {}".format("".join(r("meter")) == "retem"))
    print()


if __name__ == '__main__':
    test_reverse(reversed)
    test_reverse(reverse_list)
    test_reverse(reverse_generator)
