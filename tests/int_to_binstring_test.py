import sys
sys.path.append('../src/')
from int_to_binstring import int_to_binstring as itb

def test():
    a = itb(5)
    b = itb(8)
    c = itb(256)
    d = itb(64)
    e = itb(10)
    f = itb(11)
    g = itb(32)
    h = itb(33)
    print('5 in binary is: ' + a)
    print('8 in binary is: ' + b)
    print('256 in binary is: ' + c)
    print('64 in binary is: ' + d)
    print('10 in binary is: ' + e)
    print('11 in binary is: ' + f)
    print('32 in binary is: ' + g)
    print('33 in binary is: ' + h)


if __name__ == "__main__":
    test()
