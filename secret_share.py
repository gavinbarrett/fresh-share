from sys import exit
from binascii import hexlify
from secrets import randbelow
from src.mod_inv import mod_inv

def pad(bstring):
    ''' Pad binary string to a multiple of 8 '''
    pad = 8 - (len(bstring) % 8)
    return '0'*pad + bstring

def itb(n):
    ''' Convert an integer to its corresponding binary string '''
    binstring = ''
    while n > 0:
        tmp = n % 2
        n = n // 2
        binstring += str(tmp)
    return binstring[::-1]

def bta(secretbin):
    ''' Convert a binary string to an ascii string '''
    n = 8
    if len(secretbin) % n != 0:
        secretbin = pad(secretbin)
    byte = [secretbin[i:i+n] for i in range(0, len(secretbin), n)]
    secret = ''
    for b in byte:
        s = chr(int(b,2))
        secret += s
    return secret

def find_field(n):
    ''' Calculate a Mersenne prime large enough '''
    mersenne = [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281, 3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701, 23209, 44497, 86243, 110503, 132049, 216091, 756839, 859433, 1257787]
    for i in range(len(mersenne)):
        prime = (2**mersenne[i]) - 1
        if prime > n:
            return prime
    print('Could not find a large enough prime')
    exit(0)

def gen_coeff(k, field):
    ''' Generate coefficients uniformly at random '''
    coeffs = []
    for i in range(k-1):
        r = 0
        while r == 0 or r in coeffs:
            r = randbelow(field)
        coeffs.append(r)
    return coeffs

def horners(x, k, field, coeff, secret):
    ''' Evaluate the polynomial with Horner's method '''
    res = coeff[0]
    for i in range(1, k):
        res = ((res * x) % field + coeff[i]) % field
    return res

def split_secret(n, k, field, coeffs, secret):
    ''' Split secret into shares '''
    shares = []
    s = 0
    for i in range(n):
        s = horners(i+1, k, field, coeffs, secret)
        shares.append(s)
    return shares

def evaluate_poly(x, xi, xs, field):
    ''' Evaluate x values for each y '''
    numer = 1
    denom = 1
    for i in range(0, len(xs)):
        if xi == i:
            continue
        numer = numer * (x - xs[i]) % field
        denom = denom * (xs[xi] - xs[i]) % field
    return numer * mod_inv(denom, field) % field

def interpolate(x, xs, ys, field):
    ''' Use Lagrange interpolation to recover the f(x) value '''
    secret = 0
    for i in range(0, len(xs)):
        secret += (field + ys[i] * evaluate_poly(x, i, xs, field)) % field
    return secret % field

def share():
    ''' Split secret up into n shares '''
    n = int(input('Enter the number of desired shares: '))
    k = int(input('\nEnter the number for the desired threshold\n(Mustn\'t exceed the number of shares!): '))
    if (k > n):
        print('\nThreshold above number of shares!\nAborting scheme!\n')
        exit(0)
    
    # get the secret
    plaintext = input('\nEnter the secret you would like to share: ')
    
    # convert message to integer
    secret = int(hexlify(plaintext.encode('utf-8')),16)
    print('Processing secret: ' + str(secret) + '\n')

    # generate a secure field: # |Z_p| >= |M|
    field = find_field(secret)
    # generate array of randomly selected coefficients
    coeffs = gen_coeff(k, field)

    # add secret as coefficient 0
    coeffs = [secret] + coeffs

    # split secret into shares
    shares = split_secret(n, k, field, coeffs[::-1], secret)
    
    # print shares
    i = 1
    for s in shares:
        print('(' + str(i) + ',' + str(s) + ')\n')
        i += 1

def recover():
    ''' Try to recover the secret given k shares '''
    xs = []
    ys = []
    share_no = int(input('How many shares do you have? '))
    for i in range(share_no):
        try:
            x, y = input("Please enter your share: ").split(' ')
            xs.append(int(x))
            ys.append(int(y))
        except:
            print('Please enter x and y share values, seperated by a space.')
            print('Exiting scheme')
            exit(0)
    # find max y value    
    max_y = int(max(ys))
    # find an appropriately sized field
    field = find_field(max_y)
    
    # perform polynomial interpolation to recover the secret
    secretint = interpolate(0, xs, ys, field)
    # transform the integer into its corresponding binary
    secretbin = itb(secretint)
    # interpret the binary string as an ascii string
    secret = bta(secretbin)

    print('\nThe secret is: ' + secret + '\n')


def main():
    ''' Attempt to establish a sharing scheme '''
    choice = input('What would you like to do?\n(1) Share a secret\n(2) Recover one\n')
    if choice == '1':    
        share()
    elif choice == '2':
        recover()
    else:
        print('Invalid input; exiting program')


if __name__ == "__main__":
    main()
