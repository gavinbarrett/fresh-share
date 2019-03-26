import sys
sys.path.append('../src/')
from mod_inv import egcd

def test():
    ''' Test some values, where egcd = 1, and where egcd = x '''
    a = egcd(3,7,0,0)
    b = egcd(5,11,0,0)
    c = egcd(2,128,0,0)
    d = egcd(3,30,0,0)
    e = egcd(4, 64, 0, 0)
    f = egcd(4, 17, 0, 0)
    g = egcd(5, 127, 0, 0)
    print('gcd(3,7) = ' + str(a[0]))
    print('gcd(5,11) = ' + str(b[0]))
    print('gcd(2,128) = ' + str(c[0]))
    print('gcd(3,30) = ' + str(d[0]))
    print('gcd(4,64) = ' + str(e[0]))
    print('gcd(4,17) = ' + str(f[0]))
    print('gcd(5,127) = ' + str(g[0]))

if __name__ == "__main__":
    test()
