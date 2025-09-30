import random

class MillerRabin:
    def __init__(self, k=5):
        # Initialize the number of iterations (random bases) to test
        # Higher k increases the confidence that a number is prime
        self.k = k

    def is_prime(self, n):
        # Numbers less than or equal to 1 are not prime
        if n <= 1:
            return False

        # Even numbers greater than 2 are not prime
        if n % 2 == 0:
            return False

        # Factor n-1 as 2^r * s with s odd
        r = 0
        s = n - 1
        while s % 2 == 0:
            r += 1
            s //= 2

        # Perform the test k times with random bases
        for _ in range(self.k):
            # Choose a random integer a in the range [2, n-2]
            a = random.randint(2, n - 2)

            # Compute x = a^s mod n
            x = pow(a, s, n)

            # If x is 1 or n-1, n passes this round of testing
            if x == 1 or x == n - 1:
                continue

            # Square x up to r-1 times
            for _ in range(r - 1):
                x = pow(x, 2, n)
                # If x becomes n-1, n passes this round
                if x == n - 1:
                    break
            else:
                # If x never becomes n-1, n is composite
                return False

        # If n passes all k rounds, it is probably prime
        return True
