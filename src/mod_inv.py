import sys

def mod_exp(x,d,n):
    ''' Fast modular exponentiation '''
    if d == 0:
        return 1
    if d % 2 == 0:
        z = mod_exp(x,d//2,n)
        return z**2 % n
    else:
        z = mod_exp(x,(d-1)//2,n)
        return ((z**2) * x) % n

def egcd(a, b, x, y):
    ''' Extended Euclidean Algorithm '''
    if a == 0:
        x = 0
        y = 1
        return [b, x, y]
    g, x1, y1 = egcd(b%a, a, x, y)
    x = y1 - int((b//a)) * x1
    y = x1
    return g, x, y

def mod_inv(k, prime):
    ''' Modular inverse of k mod prime '''
    x = 0
    y = 0
    g, x, y = egcd(k, prime, x, y)
    if g != 1:
        print('Cannot compute an inverse!')
        sys.exit(0)
    else:
        return ((x % prime) + prime) % prime
