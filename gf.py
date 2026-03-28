x = 2

def outer():
    y = 0

    def inner():
        global x
        nonlocal y
        x += 1
        y += 1

    inner()