from log_mod import egcd
from log_mod import mod_inv
import sys

def test():
    mersenne = [2,3,5,7,13,17,19,31,61,89,107,127,521,607,1279,2203]
    for i in range(len(mersenne)):
        print('m_prime: 2**' + str(mersenne[i]))
        for j in range(2**i):
            m = 2**mersenne[i]-1
            a,c,d = egcd(j,m,0,0)
            print('egcd(' + str(j) + ', 2**' + str(mersenne[i]) + ' = ' + str(a))
            b = mod_inv(j,m)
            print('mod_inv(' + str(j) + ', 2**' + str(mersenne[i]) + ' = ' + str(b))

def main():
    test()

if __name__ == "__main__":
    main()
