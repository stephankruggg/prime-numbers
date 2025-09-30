from prime_validators.miller_rabin import MillerRabin
from prime_validators.fermat import Fermat

if __name__ == "__main__":
    known_pseudoprimes = [
        2047,       # 23 × 89
        3277,       # 29 × 113
        4033,       # 37 × 109
        4681,       # 31 × 151
        8321,       # 53 × 157
        15841,      # 31 × 511
        29341,      # 13 × 37 × 61
        42799,      # 127 × 337
        49141,      # 13 × 37 × 101
        3215031751  # 151 × 751 × 132151
    ]

    for n in known_pseudoprimes:
        fermat_validator = Fermat(k=1)
        miller_rabin_validator = MillerRabin(k=1)

        print(f"{n} -> Fermat says prime? {fermat_validator.is_prime(n)}")
        print(f"{n} -> Miller-Rabin says prime? {miller_rabin_validator.is_prime(n)}\n")
