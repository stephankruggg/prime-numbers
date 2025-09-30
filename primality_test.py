import time
from wsgiref.validate import validator

from prime_validators.fermat import Fermat
from prime_validators.miller_rabin import MillerRabin
from PRNGs.isaac64 import Isaac64
from PRNGs.xorshiftr128plus import Xorshiftr128Plus

def generate_prime(bits, prng, validator):
    candidate = prng.randbits(bits) | 1
    tries = 0

    while True:
        tries += 1
        if validator.is_prime(candidate):
            return candidate, tries
        else:
            candidate += 2


if __name__ == "__main__":
    prngs = [
        Xorshiftr128Plus(seed=12345, seed2=67890),
        Isaac64()
    ]

    validators = [
        MillerRabin(),
        Fermat()
    ]

    bit_sizes = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]

    for prng in prngs:
        print(f'Testing {prng.__class__.__name__} PRNG generation\n')
        for validator in validators:
            print(f'Using {validator.__class__.__name__} for primality testing\n')
            for bits in bit_sizes:
                start = time.time()
                prime, tries = generate_prime(bits, prng, validator)
                elapsed = (time.time() - start) * 1000
                print(f"{bits}-bit prime found in {elapsed:.2f} ms after {tries} tries")
                print(f"Prime: {prime}\n")
