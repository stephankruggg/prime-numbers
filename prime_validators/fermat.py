import random

class Fermat:
    def __init__(self, k=5):
        # Initialize the number of iterations (random bases) to test
        # Higher k increases the confidence that a number is prime
        self.k = k

    def is_prime(self, n):
        # Numbers less than or equal to 1 are not prime
        if n <= 1:
            return False

        # 2 and 3 are prime numbers
        if n <= 3:
            return True

        # Even numbers greater than 2 are not prime
        if n % 2 == 0:
            return False

        # Perform the Fermat primality test k times with random bases
        for _ in range(self.k):
            # Pick a random integer 'a' in the range [2, n-2]
            a = random.randint(2, n - 2)

            # Compute a^(n-1) mod n
            # If it is not 1, then n is definitely composite
            if pow(a, n - 1, n) != 1:
                return False

        # If n passes all k tests, it is probably prime
        return True
