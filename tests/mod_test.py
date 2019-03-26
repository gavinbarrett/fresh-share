import sys
sys.path.append('../src/')
from mod_inv import egcd
from mod_inv import mod_inv

def test():
    a = mod_inv(4,7)
    b = mod_inv(5,47)
    c = mod_inv(32,101)
    d = mod_inv(11,89)
    print('mod_inv(4,7) = ' + str(a))
    print('mod_inv(5,47) = ' + str(b))
    print('mod_inv(32,101) = ' + str(c))
    print('mod_inv(11,89) = ' + str(d))

if __name__ == "__main__":
    test()
