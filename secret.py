import sys
import binascii
import secrets

def find_field(n):
    ''' Find an appropriate field '''
    i = 2
    prime = 0
    while prime <= n:
        prime = (2**i)
        i += 1
    return prime

def gen_coeff(k, field):
    ''' Generate coefficients '''
    coeffs = []
    for i in range(k-1):
        coeffs.append(secrets.randbelow(field))
    return coeffs

def eval_poly(x, k, field, coeff, secret):
    ''' Evaluate the polynomial with Horner's method '''
    res = coeff[0]
    for i in range(1,k-1):
        res = (res * x + coeff[i]) % field
    return (res + secret) % field

def share(n, k, field, coeffs, secret):
    ''' Split message into shares '''
    shares = []
    for i in range(n):
        s = eval_poly(i, k, field, coeffs, secret)
        shares.append(s)
    return shares

def main():
    ''' Attempt to establish a sharing scheme '''
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

if __name__ == "__main__":
    main()
