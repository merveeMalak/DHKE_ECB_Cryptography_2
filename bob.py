#STUDENT IDs: 280201089-260201043
#REFERENCES:
# https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal : print text with red color
# https://pycryptodome.readthedocs.io/en/latest/src/cipher/des.html : des algorithm
# lecture notes : generator and prime number test algoritm, diffie helman key exchange algorithm 

import argparse
import random
from Crypto.Cipher import DES
import base64  

#Use for red color
CRED = '\033[91m'
CEND = '\033[0m'

#gets and parse command line parameters
def get_info():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode')
    parser.add_argument("-A", help="A", type=int)
    parser.add_argument("-b", help="b", type=int)
    parser.add_argument("-p", help="p")   
    parser.add_argument("-g", help="g", type=int)
    parser.add_argument("-c", help="c")
    parser.add_argument("-k", help="key", type=int)
    args = parser.parse_args()
    return args.mode, args.A , args.b, args.p, args.g, args.c, args.k


#The prime number test algorithm we saw in the lesson was used!!!!
#Even if the number is prime in the primality test,
#it can be strong liar, for this, 10 times are tested.
def primality_test(p):
    #If the result returns true, the number may be prime,
    # but if it returns false, the number is composite.
    def primality_test_base(p):
        if (p==2):  #2 is prime
            return True
        a = random.randint(2, p-1) #a is random number 
        k = p-1 
        while k > 0:
            result = (a**k) %p  #returns (a**k)%p
            if (result != 1) & (k < p-1) & (result != p-1): 
                return False
            elif result == p-1: #result == -1 
                return  True
            elif (result == 1) & (k % 2 != 0):
                return  True
            else:
                k = int(k/2)
                
    for i in range(0,10):
        if not primality_test_base(p):
            return False
    return True


#The generator test algorithm we saw in the lesson was used!!!!
#cheks g is a generator or not 
def generator_test(g,p): 
    #returns prime factors of number
    def prime_factor(number):
        prime_factor_list = []
        while (number % 2 == 0): #number is even
            number /= 2
            prime_factor_list.append(2)
        for i in range(3, int(number**(0.5)), 2): #continues until the square root of the number 
            while (number % i == 0): #i is the multiplier of the number
                prime_factor_list.append(i)
                number /= i
        if number > 2:
            prime_factor_list.append(number)
        return set(prime_factor_list)
    
    prime_factor_list = prime_factor(p-1) #returns prime factors 
    for i in prime_factor_list:
        if (g ** ((p-1)/i ) % p) == 1: 
            return False
    return True


def dhke_mode(A, b, p, g):
    p = int(p)
    if A != None and b != None and p != None: #If the user inputs A, b and p
        s = A ** b % p # secret key is (A**b) p
        print(f"s = {CRED}{s}{CEND}")
        print("(This must be kept secret. However, Alice should be able to calculate this as well.)")
    elif p != None and g != None:   #If the user inputs p and g
        if  not primality_test(p):  #checks whether p is prime or not 
            print("p is not prime!")
            return
        print(f"p = {CRED}{p}{CEND} OK (This is a prime number.)")
        if not generator_test(g, p):  #checks whether g is primitive root modulo p or not
            print("g is not primitive root modulo p!")
            return 
        print(f"g = {CRED}{g}{CEND} OK (This is a primitive root modulo {p}.)")
        print("Alice and Bob publicly agree on the values of p and g.")
        print("However, it is advised to use any pair of p and g only once.")
        b =  random.randint(1,100) #3 #generates random private key  
        print(f"b = {CRED}{b}{CEND} (This must be kept secret.)")
        B = (g ** b) % p #calculates public key (g**b) % p
        print(f"B = {CRED}{B}{CEND} (This can be sent to Alice.)")

def des_mode(c, k):
    if c != None and k != None: #if user inputs c and k 
        c = base64.b64decode(c.encode('ascii'))  #ciphertext must be bytes form
        padding_size = len(c) % 8 #block size must be 8 bytes
        if ( padding_size != 0):
            c = c + (b' ' * (8 - padding_size))
        k = str(k).encode('ascii')  #type of key must be bytes
        if (len(k) > 8): #key length must 8 bytes if it larger than 8 bytes then finish the program
            print("Key length must be 8 bytes!")
            return
        k = (b'0'* (8 - (len(k)))) + k   #key length is smaller than 8 bytes
        des_cipher = DES.new(k, DES.MODE_ECB)
        plaintext = des_cipher.decrypt(c) #decrypt the ciphertext
        print("Decrypted plaintext:")
        print(f"{CRED}{plaintext.decode()}{CEND}")

    else:
        print("Please provide the plaintext and a key.")
        return 
    
def main():
    mode, A, b, p, g, c, k = get_info()
    #print(mode, a, B, p, g, c, k)
    if mode == "dhke":
        dhke_mode(A, b, p, g)
    elif mode == "des":
        des_mode(c,k)
    else:
        print("Mode must be dhke or des!!")
        return
main()