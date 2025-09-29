import random

class Fermat:
    def __init__(self, k=5):
        self.k = k

    def is_prime(self, n):
        if n <= 1:
            return False

        if n <= 3:
            return True

        if n % 2 == 0:
            return False

        for _ in range(self.k):
            a = random.randint(2, n - 2)

            if pow(a, n - 1, n) != 1:
                return False

        return True
