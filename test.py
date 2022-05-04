def plus():
    global a, b
    return a + b


def plus2():
    a = 10
    b = 20
    return plus()

plus2()