import random
import math
import os

# Author: Sean Taylor Thomas
# 4/22
# Implementation of an RSA Cryptosystem


def is_coprime(a, b):
    """ check if integers a and b are co-prime"""
    return math.gcd(a, b) == 1


def compute_e(p, q):
    """ compute e and make sure e and (p-1)(q-1) are co-prime"""
    e = 2 ** 16 + 1
    if is_coprime(e, (p - 1) * (q - 1)):
        return e
    else:
        print("E IS NOT CO-PRIME.... ):")


def test_thing():
    # for i in range(400):
    #     if 2 ** i > 10**95:
    #         print(i)
    # random.randint(4, 5)
    return 0

def generate_large_int(p=-1):
    """
    returns: rand_int (random integer with k bits)
    optional argument: p, an int where |rand_int - p| > 10^95
    minimum k: 333 (2^333>10^100)
    """
    min_bits = 333  # make sure number > 10^100
    max_bits = 2500

    # if we already have first prime, make sure difference btwn primes is large
    if p != -1:
        valid_bits_interval = [0, 0, 0, 0]  # min1, max1, min2, max2
        ks = [-1, -1]  # k's generated from 2 intervals (higher and lower than p)

        p_bits = p.bit_length()
        valid_bits_interval = [min_bits, p_bits - 316, p_bits + 316, max_bits]
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


def primality_test(x):
    """
    takes in large integer
    returns: whether the int passes the primality test
    """
    n = 2**2500
    return modular_exponentiation(x, n-1, n) == 1


def generate_large_prime(p=-1):
    """
    gets large integer and checks if it passes the primality test
    returns: (probably) prime int
    """
    x = generate_large_int(p)
    passes_test = primality_test(x)
    while not passes_test:
        x = generate_large_int(p)
        passes_test = primality_test(x)
    return x


def modular_exponentiation(x, y, n):
    """
    recursive modular exponentiation
    arguments: x, y, n such that 0 <= x, y, <= n-1
    returns result of x^y (mod n)
    """
    z = 1
    for i in reversed(range(y.bit_length())):
        z = z**2 % n
        if y % 2 == 0:
            z = x*z % n
    return z


def eea(e, n):
    """
    recursive implementation of extended euclid algorithm
    for equation e (mod n) , solve e*x + n*y = gcd(e, n)
    returns: (gcd, x, y)
    """
    if e == 0:
        return n, 0, 1
    else:
        gcd, x, y = eea(n % e, e)
        return gcd, y - (n // e) * x, x


def write_to_file(text="nothing to write", filename="default.txt"):
    """ arguments:
        - text: text to write to file
        - filename: name of file to write to
        """
    if os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write(text)
    else:  # if file doesn't  exist, make a new file w/ this name
        with open(filename, 'x') as f:
            f.write(text)


class rsa_system:

    def __init__(self):
        self.generate_keys()
        self.public_key = ""
        self.private_key = ""
        self.p = -1
        self.q = -1
        self.n = -1
        self.e = -1
        self.d = -1

    def generate_keys(self):
        print("Keys being generated")
        print("_" * 100)

        # generate public_key and write to file
        self.generate_public_key()
        print("_" * 100)

        # generate private_key an write to file
        self.generate_private_key()
        print("_" * 100)

    def generate_public_key(self):
        print("Generating Public Key..")
        self.p = generate_large_prime()
        print("p generated: ", self.p)
        self.q = generate_large_prime(self.p)

        # make sure difference btwn p and q is large
        valid_q = abs(self.p - self.q) > 10 ** 95
        while not valid_q:
            print("L")
            self.q = generate_large_prime(self.p)
            valid_q = abs(self.p - self.q) > 10 ** 95
        print("q generated: ", self.q)

        # calculate n and compute e
        self.n = self.p * self.q
        self.e = compute_e(self.p, self.q)
        print("e computed: ", self.e)
        self.public_key = str(self.n) + "\n" + str(self.e)
        print("Public Key: (", self.n, ", ", self.e, ")")
        write_to_file(text=self.public_key, filename="public_key.txt")

    def generate_private_key(self):
        print("Generating Private Key..")
        gcd, x, y = eea(self.e, ((self.p - 1) * (self.q - 1)))
        print("Using EEA for e^(-1) mod (p-1)(q-1)...")
        print("GCD: ", gcd)
        print("x = ", x)
        print("y = ", y)
        self.d = x  # modular multiplicative inverse of e (mod (p-1)(q-1))
        self.private_key = str(self.d)
        write_to_file(text=self.private_key, filename="private_key.txt")
        print("Checking if modular inverse valid...")
        print("d * e (mod (p-1)(q-1) = ", x * self.e % ((self.p - 1) * (self.q - 1)))
        print("Private Key ", self.d)






key = rsa_system()
