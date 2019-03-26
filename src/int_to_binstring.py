def int_to_binstring(n):
    ''' Convert an integer to its corresponding binary string '''
    binstring = ''
    while n > 0:
        tmp = n % 2
        n = n // 2
        binstring += str(tmp)
    return binstring[::-1]
