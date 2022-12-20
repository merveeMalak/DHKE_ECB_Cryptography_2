import argparse
import random
def get_info():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode')
    parser.add_argument("-a", help="a", type=int)
    parser.add_argument("-B", help="B", type=int)
    parser.add_argument("-p", help="p")   
    parser.add_argument("-g", help="g", type=int)
    parser.add_argument("-c", help="c")
    parser.add_argument("-k", help="key", type=int)
    args = parser.parse_args()
    return args.mode, args.a , args.B, args.p, args.g, args.c, args.k

#returns result base**power % mod
def modular_exponentiation(base, power, mod):
    if power == 0:
        return 1
    
    result = 0
    result = modular_exponentiation(base, power//2, mod)
    if power % 2 == 0: # power is even 
        return (result * result) % mod
    else: #power is odd
        return (result * result * base) % mod
        
#If the result returns true, the number may be prime,
# but if it returns false, the number is composite.
def primality_test_base(p):
    if (p==2):  #2 is prime
        return True
    a = random.randint(2, p-1) #a is random number 
    k = p-1 
    while k > 0:
        result = modular_exponentiation(a, k, p) #returns (a**k)%p
        if (result != 1) & (k < p-1) & (result != p-1): 
            return False
        elif result == p-1: #result == -1 
            return  True
        elif (result == 1) & (k % 2 != 0):
            return  True
        else:
            k = int(k/2)

#Even if the number is prime in the primality test,
#it can be strong liar, for this, 10 times are tested.
def primality_test(p):
    for i in range(0,10):
        if not primality_test_base(p):
            return False
    return True


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


#cheks g is a generator or not 
def generator_test(g,p): 
    prime_factor_list = prime_factor(p-1) #returns prime factors 
    for i in prime_factor_list:
        if (modular_exponentiation(g, (p-1)/i, p) == 1): 
            return False
    return True

def dhke_mode(a, B, p, g):
    CRED = '\033[91m'
    CEND = '\033[0m'
    p = int(p)
    if a != None and B != None and p != None:
        s = B ** a % p
        print(f"s = {CRED}{s}{CEND}")
        print("(This must be kept secret. However, Bob should be able to calculate this as well.)")
    elif p != None and g != None:
        if  not primality_test(p):
            print("p is not prime!")
            return
        print(f"p = {CRED}{p}{CEND} OK (This is a prime number.)")
        if not generator_test(g, p):
            print("g is not primitive root modulo p!")
            return 
        print(f"g = {CRED}{g}{CEND} OK (This is a primitive root modulo {p}.)")
        print("Alice and Bob publicly agree on the values of p and g.")
        print("However, it is advised to use any pair of p and g only once.")
        a =  4 #random.randint(100)
        print(f"a = {CRED}{a}{CEND} (This must be kept secret.)")
        A = modular_exponentiation(g, a, p)
        print(f"A = {CRED}{A}{CEND} (This can be sent to Bob.)")

def main():
    mode, a, B, p, g, c, k = get_info()
    #print(mode, a, B, p, g, c, k)
    if mode == "dhke":
        dhke_mode(a, B, p, g)

main()