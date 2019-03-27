import sys
def egcd(a, b, x, y):
    if a == 0:
        x = 0
        y = 1
        return [b, x, y]
    g, x1, y1 = egcd(b%a, a, x, y)
    x = y1 - int((b//a)) * x1
    y = x1
    return g, x, y

def mod_inv(k, prime):
    x = 0
    y = 0
    g, x, y = egcd(k, prime, x, y)
    if g != 1:
        print('Cannot compute an inverse!')
        sys.exit(0)
    else:
        return ((x % prime) + prime) % prime
