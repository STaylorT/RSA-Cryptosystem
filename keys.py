import random
import math


def is_coprime(a, b):
    return math.gcd(a, b) == 1


def compute_e(p, q):
    e = 2**16 + 1
    if is_coprime(e, (p-1)*(q-1)):
        return e
    else:
        print("E IS NOT PRIME.... ):")

def test_thing():
    # for i in range(400):
    #     if 2 ** i > 10**95:
    #         print(i)
    random.randint(4, 5)

def generate_large_int(p=-1):
    """
    returns: rand_int (random integer with k bits)
    optional argument: p, an int where |rand_int - p| > 10^95
    minimum k: 2^333 (>10^100)
    """
    min_bits = 333  # make sure number > 10^100
    max_bits = 2500

    # if we already have first prime, make sure difference btwn primes is large
    if p != -1:
        valid_bits_interval = [0, 0, 0, 0]  # min1, max1, min2, max2
        ks = [-1, -1]  # k's generated from 2 intervals (higher and lower than p)

        p_bits = p.bit_length()
        valid_bits_interval = [333, p_bits-316, p+316, 2500]
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
        print("Random integer: (Q) : ", rand_int)
        return rand_int

    # no optional 'p' argument provided
    k = random.randint(min_bits, max_bits)  # get random # of bits
    rand_int = random.getrandbits(k)  # calculate random int
    print("Random integer: (P) : ", rand_int)
    return rand_int


def primality_test(x):
    """
    takes in large integer
    returns: whether the int passes the primality test """
    return True


def generate_large_prime( p=-1):
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


def modular_expon(x, a, n):
    return (x ** a) % n


class keys:

    def __init__(self):
        self.generate_keys()
        self.p = -1
        self.q = -1
        self.n = -1
        self.e = -1

    def generate_keys(self):
        print("Keys being generated")
        self.p = generate_large_prime()
        self.q = generate_large_prime(self.p)

        # make sure valid p and q
        valid_q = abs(self.p-self.q) > 10**95
        while not valid_q:
            # print("L")
            self.q = generate_large_prime(self.p)
            valid_q = abs(self.p-self.q) > 10**95

        # calculate n and compute e
        self.n = self.p * self.q
        self.e = compute_e(self.p, self.q)
        print("Public Key: (", self.n, ", ", self.e, ")")

    def eea(self):
        print("eea")


key = keys()

