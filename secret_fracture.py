#!/usr/bin/env python3
from src.secretshare import SecretSharer

def main():
    
    # instantiate a secret sharer
    s = SecretSharer()
    
    choice = input('What would you like to do?\n(1) Share a secret\n(2) Recover one\n')
    
    if choice == '1':
        n = int(input('\nEnter the number of desired shares: '))
        k = int(input('\nEnter the number for the desired threshold: '))
        plaintext = input('\nEnter the secret you would like to share: ')
        
        # share the secret
        s.share(n,k,plaintext)

    elif choice == '2':
        xs = []
        ys = []
        share_num = int(input('\nHow many shares do you have? '))
        for i in range(share_num):
            try:
                x, y = input("\nPlease enter your share: ").split(' ')
                xs.append(int(x))
                ys.append(int(y))
            except:
                print('Please enter x and y share values, seperated by a space.')
                print('Usage: <share_number share value> e.g. 4 56789')
                print('Exiting scheme')
                exit(0)
        
        # recover the secret
        s.recover(xs, ys, share_num)

    else:
        print('Invalid input; exiting program')


if __name__ == "__main__":
    main()
