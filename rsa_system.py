import random
import math
import os
from bitarray.util import int2ba

# Python 3.9
# Author: Sean Taylor Thomas
# 4/22
# Implementation of an RSA Cryptosystem


def is_coprime(a, b):
    """ check if integers a and b are co-prime"""
    return math.gcd(a, b) == 1


def generate_e(p, q):
    """ generate e and make sure e and (p-1)(q-1) are co-prime"""
    e = 2 ** 16 + 1
    if is_coprime(e, (p - 1) * (q - 1)):
        return e
    else:  # generate an e relatively prime to (p-1)(q-1)
        e = generate_large_prime(17, 228)
        while not is_coprime(e, (p - 1) * (q - 1)):
            e = generate_large_prime()
        return e


def generate_large_int(min_bits=333, max_bits=1200, p=-1):
    """
    returns: rand_int (random integer with k bits)
    optional argument: p, an int where |rand_int - p| > 10^95
    minimum k: 333 (2^333>10^100)
    """

    # if we already have first prime, make sure difference btwn primes is large
    if p != -1:
        ks = [-1, -1]  # k's generated from 2 intervals (higher and lower than p)

        p_bits = p.bit_length()
        valid_bits_interval = [min_bits, p_bits - 316, p_bits + 316, max_bits]  # min1, max1, min2, max2
        # make sure range is valid
        if valid_bits_interval[1] - valid_bits_interval[0] > 0 and valid_bits_interval[3] - valid_bits_interval[2] > 0:
            ks[0] = random.randint(valid_bits_interval[0], valid_bits_interval[1])
            ks[1] = random.randint(valid_bits_interval[2], valid_bits_interval[3])
            k = random.choice(ks)  # choose random k
        elif valid_bits_interval[1] - valid_bits_interval[0] > 0:  # higher interval invalid
            ks[0] = random.randint(valid_bits_interval[0], valid_bits_interval[1])
            k = ks[0]  # choose lower interval k
        else:  # lower interval invalid
            ks[1] = random.randint(valid_bits_interval[2], valid_bits_interval[3])
            k = ks[1]  # choose higher interval k
        rand_int = random.getrandbits(k)  # calculate random int
        return rand_int

    # no optional 'p' argument provided
    k = random.randint(min_bits, max_bits)  # get random # of bits
    rand_int = random.getrandbits(k)  # calculate random int
    return rand_int


def primality_test(n):
    """
    takes in large integer
    returns: whether the int passes the primality test
    """
    a = random.randint(1, n)

    return modular_exponentiation(a, n - 1, n) == 1


def generate_large_prime(min_bits=333, max_bits=1200, p=-1):
    """
    gets large integer and checks if it passes the primality test
    returns: (probably) prime int
    """
    rand_int = generate_large_int(min_bits=min_bits, max_bits=max_bits, p=p)
    passes_test = primality_test(rand_int)
    while not passes_test:
        rand_int = generate_large_int(min_bits=min_bits, max_bits=max_bits, p=p)
        passes_test = primality_test(rand_int)
    return rand_int


def modular_exponentiation(x, y, n):
    """
    recursive modular exponentiation
    arguments: x, y, n such that 0 <= x, y, <= n-1
    returns result of x^y (mod n)
    """
    y_bits = int2ba(y)  # convert y into bit representation
    y_bits.reverse()  # reverse this bit representation
    z = 1
    for i in reversed(range(len(y_bits))):
        z = z * z % n
        if y_bits[i] == 1:
            z = z * x % n
    return z


def eea(e, n):
    """
    recursive implementation of extended euclid algorithm
    arguments: [ e*x + n*y = gcd(e, n) ]
    1) e
    2) n
    returns: (gcd, x, y)
    """
    if e == 0:
        return n, 0, 1
    else:
        gcd, x, y = eea(n % e, e)
        return gcd, y - (n // e) * x, x


def get_positive_x(x, e, n):
    while x < 0:
        x += n
    for i in range(random.randint(0, 12)):
        x += n
    return x


def write_to_file(text="nothing to write", filename="default.txt"):
    """ arguments:
        1) text: text to write to file
        2) filename: name of file to write to
        """
    if os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write(text)
    else:  # if file doesn't  exist, make a new file w/ this name
        with open(filename, 'x') as f:
            f.write(text)


def read_file(filename):
    """
    arguments:
    1) filename (str) : what file to read from
    returns: the contents of the file (str)
    """
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return f.read()
    else:
        print("Sorry, ", filename, " doesn't exist in this directory.")


class rsa_system:

    def __init__(self):
        self.public_key = ""
        self.private_key = ""
        self.p = -1
        self.q = -1
        self.n = -1
        self.e = -1
        self.d = -1

    def generate_keys(self):
        print("Keys being generated")


        # generate public_key and write to file
        print("_" * 100)
        self.generate_public_key()
        print("_" * 100)
        print()

        # generate private_key an write to file
        print("_" * 100)
        self.generate_private_key()
        print("_" * 100)

    def generate_public_key(self):
        print("Generating Public Key..")
        self.p = generate_large_prime()
        print("p generated: ", self.p)
        self.q = generate_large_prime(p=self.p)

        # make sure difference btwn p and q is large
        valid_q = abs(self.p - self.q) > 10 ** 95
        while not valid_q:
            print("L")
            self.q = generate_large_prime(self.p)
            valid_q = abs(self.p - self.q) > 10 ** 95
        print("q generated: ", self.q)

        # calculate n and generate e
        self.n = self.p * self.q
        self.e = generate_e(self.p, self.q)
        print("e generated: ", self.e)
        self.public_key = str(self.n) + "\n" + str(self.e)
        print("Public Key: (", self.n, ", ", self.e, ")")
        write_to_file(text=self.public_key, filename="public_key.txt")

    def generate_private_key(self):
        """
        Generates a private key from the given public key information
        """
        print("Generating Private Key..")
        gcd, x, y = eea(self.e, ((self.p - 1) * (self.q - 1)))
        print("Using EEA for e^(-1) mod (p-1)(q-1)...")
        print("GCD: ", gcd)
        print("x = ", x)
        print("y = ", y)
        if x < 0:  # make x p positive if not already
            x = get_positive_x(x, self.e, ((self.p - 1) * (self.q - 1)))
        self.d = x  # modular multiplicative inverse of e (mod (p-1)(q-1))
        self.private_key = str(self.d)
        write_to_file(text=self.private_key, filename="private_key.txt")
        print("Checking if modular inverse valid...")
        print("d * e (mod (p-1)(q-1) = ", x * self.e % ((self.p - 1) * (self.q - 1)))
        print("Private Key ", self.d)

    def encrypt(self):
        """
        Encrypts message found in message.txt
        Writes ciphertext to ciphertext.txt file
        """
        # read in from files
        public_key = read_file("public_key.txt").splitlines()
        message = read_file("message.txt")

        # compute ciphertext with modular exponentiation
        ciphertext = str(modular_exponentiation(int(message), int(public_key[1]), int(public_key[0])))

        write_to_file(text=ciphertext, filename="ciphertext.txt")

    def decrypt(self):
        """
        Decrypts ciphertext given private key and public key
        Writes decrypted message to decrypted_message.txt
        """
        public_key = read_file("public_key.txt").splitlines()
        private_key = read_file("private_key.txt")
        ciphertext = read_file("ciphertext.txt")

        decrypted_message = str(modular_exponentiation(int(ciphertext), int(private_key), int(public_key[0])))
        write_to_file(text=decrypted_message, filename="decrypted_message.txt")


if __name__ == '__main__':
    rsa = rsa_system()
    rsa.generate_keys()  # generate public & private keys and output to files
    # #
    rsa.encrypt()  # encrypt message (from message.txt)
    rsa.decrypt()  # decrypt the ciphertext generated from prev. steps
