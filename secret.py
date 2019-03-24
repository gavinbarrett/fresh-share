import sys
import binascii
import secrets

def find_field(n):
    ''' Find an appropriate Galois field '''
    i = 2
    prime = 0
    while prime <= n:
        prime = (2**i)
        i += 1
    return prime

def gen_coeff(k, field):
    ''' Generate coefficients uniformly at random '''
    coeffs = []
    for i in range(k-1):
        coeffs.append(secrets.randbelow(field))
    return coeffs

def horners(x, k, field, coeff, secret):
    ''' Evaluate the polynomial with Horner's method '''
    res = coeff[0]
    for i in range(1,k-1):
        res = (res * x + coeff[i]) % field
    return (res + secret) % field

def share(n, k, field, coeffs, secret):
    ''' Split message into shares '''
    shares = []
    for i in range(n):
        s = horners(i, k, field, coeffs, secret)
        shares.append(s)
    return shares

def evaluatexs(x, xi, xs, field):
    ''' Evaluate x values for each y '''
    numer = 1
    denom = 1
    for i in range(len(xs)):
        if xi == xs[i]:
            continue
        numer = (numer * (x - xs[i]) % field) % field
        denom = (denom * (xi - xs[i]) % field) % field
    return numer / denom


def interpolate(x, xs, ys, field):
    ''' Use Lagrange interpolation to recover polynomial '''
    secret = 0
    for i in range(len(xs)-1):
        delta = ys[i] * evaluatexs(x, i, xs, field) % field
        secret += delta % field
    return secret

def main():
    ''' Attempt to establish a sharing scheme '''
    choice = input('Would you like to do?\n(1) Share a secret\n(2)Recover one\n')
    if choice == '1':    
        n = int(input('Enter the number of desired shares: '))
        k = int(input('\nEnter the number for the desired threshold\n(Mustn\'t exceed the number of shares!): '))
        if (k > n):
            print('\nThreshold above number of shares!\nAborting scheme!\n')
            sys.exit(0)
    
        # get the secret
        plaintext = input('\nEnter the secret you would like to share: ')
    
        # convert message to integer
        secret = int(binascii.hexlify(plaintext.encode('utf-8')),16)
   
        # generate a secure field
        field = find_field(secret)
    
        # generate array of randomly selected coefficients
        coeffs = gen_coeff(k, field)
   
        # split secret into shares
        shares = share(n, k, field, coeffs, secret)
    
        i = 1
        for s in shares:
            print('(' + str(i) + ',' + str(s) + ')')
            i += 1

    elif choice == '2':
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
                sys.exit(0)
        
        size = int(max(ys))
        field = find_field(size)

        secret = interpolate(0, xs, ys, field)
        print('The secret is: ' + str(secret))
    else:
        print('aborting')

if __name__ == "__main__":
    main()
# 1,17 2,23 3,29
