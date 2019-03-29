from sys import exit
from binascii import hexlify
from secrets import randbelow

def _mod_exp(x,d,n):
    ''' Fast modular exponentiation '''
    if d == 0:
        return 1
    if d % 2 == 0:
        z = _mod_exp(x,d//2,n)
        return z**2 % n
    else:
        z = _mod_exp(x,(d-1)//2,n)
        return ((z**2) * x) % n

def _egcd(a, b, x, y):
    ''' Extended Euclidean Algorithm '''
    if a == 0:
        x = 0
        y = 1
        return [b, x, y]
    g, x1, y1 = _egcd(b%a, a, x, y)
    x = y1 - int((b//a)) * x1
    y = x1
    return g, x, y

def _mod_inv(k, prime):
    ''' Modular inverse of k mod prime '''
    x = 0
    y = 0
    g, x, y = _egcd(k, prime, x, y)
    if g != 1:
        print('Cannot compute an inverse!')
        sys.exit(0)
    else:
        return ((x % prime) + prime) % prime

def _pad(bstring):
    ''' Pad binary string to a multiple of 8 '''
    pad = 8 - (len(bstring) % 8)
    return '0'*pad + bstring

def _itb(n):
    ''' Convert an integer to its corresponding binary string '''
    binstring = ''
    while n > 0:
        tmp = n % 2
        n = n // 2
        binstring += str(tmp)
    return binstring[::-1]

def _bta(secretbin):
    ''' Convert a binary string to an ascii string '''
    n = 8
    if len(secretbin) % n != 0:
        secretbin = _pad(secretbin)
    byte = [secretbin[i:i+n] for i in range(0, len(secretbin), n)]
    secret = ''
    for b in byte:
        s = chr(int(b,2))
        secret += s
    return secret

def _find_field(n):
    ''' Calculate a Mersenne prime large enough '''
    mersenne = [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281, 3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701, 23209, 44497, 86243, 110503, 132049, 216091, 756839, 859433, 1257787]
    for i in range(len(mersenne)):
        prime = (2**mersenne[i]) - 1
        if prime > n:
            return prime
    print('Error 101: Could not find a prime sufficient to encode the secret!')
    exit(0)

def _gen_coeff(k, field):
    ''' Generate coefficients uniformly at random '''
    coeffs = []
    for i in range(k-1):
        r = 0
        while r == 0 or r in coeffs:
            r = randbelow(field)
        coeffs.append(r)
    return coeffs

def _horners(x, k, field, coeff, secret):
    ''' Evaluate the polynomial with Horner's method '''
    res = coeff[0]
    for i in range(1, k):
        res = ((res * x) % field + coeff[i]) % field
    return res

def _split_secret(n, k, field, coeffs, secret):
    ''' Split secret into shares '''
    shares = []
    s = 0
    for i in range(n):
        s = _horners(i+1, k, field, coeffs, secret)
        shares.append(s)
    return shares

def _encode_secret(plaintext):
    ''' Convert message to integer '''
    secret = int(hexlify(plaintext.encode('utf-8')),16)
    print('\nProcessing secret: ' + str(secret) + '\n')
    return secret

def _print_shares(shares):
    ''' Print out the shares '''
    i = 1
    for s in shares:
        print('Share ' + str(i) + ':')
        print('(' + str(i) + ', ' + str(s) + ')\n')
        i += 1

def _evaluate_poly(x, xi, xs, field):
    ''' Evaluate x values for each y '''
    numer = 1
    denom = 1
    for i in range(0, len(xs)):
        if xi == i:
            continue
        numer = numer * (x - xs[i]) % field
        denom = denom * (xs[xi] - xs[i]) % field
    return numer * _mod_inv(denom, field) % field

def _interpolate(x, xs, ys, field):
    ''' Use Lagrange interpolation to recover the f(x) value '''
    secret = 0
    for i in range(0, len(xs)):
        secret += (field + ys[i] * _evaluate_poly(x, i, xs, field)) % field
    return secret % field


class SecretSharer:


    def share(self, n, k, plaintext):
        ''' Split secret up into n shares '''
        
        # check that scheme is valid
        if (k > n):
            print('\nThreshold above number of shares!\nAborting scheme!\n')
            exit(0)

        # encode plaintext as an integer
        secret = _encode_secret(plaintext)

        # generate a secure field: # |Z_p| >= |M|
        field = _find_field(secret)

        # generate array of randomly selected coefficients
        coeffs = _gen_coeff(k, field)

        # add secret as coefficient 0
        coeffs = [secret] + coeffs

        # split secret into shares
        shares = _split_secret(n, k, field, coeffs[::-1], secret)
        
        # print out the shares
        _print_shares(shares)

    def recover(self, xs, ys):
        ''' Try to recover the secret given k shares '''
        
        # check that valid sets of shares were entered correctly
        if not xs or not ys or len(xs) != len(ys):
            raise Exception('Shares missing. Unable to process recovery')
        
        # find max y value    
        max_y = int(max(ys))
        
        # find an appropriately sized field
        field = _find_field(max_y)
    
        # perform polynomial interpolation to recover the secret
        secretint = _interpolate(0, xs, ys, field)
        
        # transform the integer into its corresponding binary
        secretbin = _itb(secretint)
        
        # interpret the binary string as an ascii string
        secret = _bta(secretbin)

        print('\nThe secret is: ' + secret + '\n')
