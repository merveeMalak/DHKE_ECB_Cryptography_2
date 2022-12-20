# DHKE_ECB_Cryptography_2
Please write 2 Python scripts named alice.py, which represents the sender, and bob.py which
represents the receiver. These scripts take the inputs in the form of command-line arguments (For
this, simply use sys.argv1 or rely on the more advanced argparse2 module from the standard library).
Both of these scripts can fulfill two tasks: Diffie-Hellman Key Exchange (dhke) and Data Encryption
Standard (des). In dhke part, please do not depend on any package outside the standard library. In des
part, please use DES from Crypto.Cipher package3. You can install this package using the following
command: pip install pycryptodome. Run the algorithm in the Electronic CodeBook (ECB) mode.
The scripts shall be implemented in accordance with the following specification:

alice.py

● dhke mode

○ If a, B and p are given (They can be given in any order; for example p, B and A):

i. Calculates s.

○ Else if p and g are given (They can be given in the reversed order):

i. Checks whether p is a prime number (If not, the program is terminated here).

ii. Checks whether g is a primitive root modulo p (If not, the program is terminated
here).

iii. Randomly generates a.

iv. Calculates A.

○ Otherwise:

i. Displays an error (A message such as “Please provide p and g to initialize the key
exchange or provide a, B and p to calculate the key.”).

● des mode

○ If p (plaintext; different than p in the dhke mode) and k (key; corresponds to s in the dhke
mode) are given (They can be given in the reversed order as well):

i. If the plaintext is not valid, adds the minimum number of trailing spaces to make
it valid.

ii. If the key is not valid, adds the minimum number of leading zeros to make it
valid.

iii. Calculates ciphertext (Both the bytes and the corresponding readable text. Refer
to the examples below.).

○ Otherwise:

i. Displays an error (A message such as “Please provide the plaintext and a key.”).
bob.py is very similar to alice.py. In dhke mode, Bob produces b and B instead of a and A, and
consumes b and A instead of a and B. In des mode, Bob consumes c (ciphertext) instead of p
(plaintext) and produces plaintext instead of ciphertext. See the given examples below.

A successful scenario is given below. It is okay if the format of your outputs slightly differs from
these. However make sure that you display all of the calculated values (mind the red color). Note that
dhke and des are “positional arguments”.

Initialization of the key exchange

dell:~$ python3 alice.py dhke -p 23 -g 5

p = 23 OK (This is a prime number.)

g = 5 OK (This is a primitive root modulo 23.)

Alice and Bob publicly agree on the values of p and g.

However, it is advised to use any pair of p and g only once.

a = 4 (This must be kept secret.)

A = 4 (This can be sent to Bob.)

dell:~$ python3 bob.py dhke -g 5 -p 23

p = 23 OK (This is a prime number.)

g = 5 OK (This is a primitive root modulo 23.)

Alice and Bob publicly agree on the values of p and g.

However, it is advised to use any pair of p and g only once.

b = 3 (This must be kept secret.)

B = 10 (This can be sent to Alice.)

Finalization of the key exchange

dell:~$ python3 alice.py dhke -a 4 -B 10 -p 23

s = 18

(This must be kept secret. However, Bob should be able to calculate this as well.)

dell:~$ python3 bob.py dhke -b 3 -A 4 -p 23

s = 18

(This must be kept secret. However, Alice should be able to calculate this as well.)

Encryption and decryption of a single message

dell:~$ python3 alice.py des -p 'This is the secret message.' -k 18

Raw ciphertext (Normally this is sent to Bob over a network):
b"\xd55\xc3d\x9d\xf4\x11y\x10\\\x81\xd1\x88n\xdc\xc2\xbb\xed2R\x81'\x8a\xf4\x91g\x90\x18\x
a49\\\xbd"

Readable ciphertext (For the sake of simplicity, we will send this to Bob. This can also
be used if we use pen and paper to deliver the message.):

1TXDZJ30EXkQXIHRiG7cwrvtMlKBJ4r0kWeQGKQ5XL0=

dell:~$ python3 bob.py des -c '1TXDZJ30EXkQXIHRiG7cwrvtMlKBJ4r0kWeQGKQ5XL0='-k 18

Decrypted plaintext:

This is the secret message.
