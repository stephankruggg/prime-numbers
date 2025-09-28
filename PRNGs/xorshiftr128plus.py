import time

class Xorshiftr128Plus:
    def __init__(self, seed: int, seed2: int):
        # Ensure seeds are not zero
        if seed == 0 and seed2 == 0:
            raise ValueError("Seeds cannot be zero.")

        # Initialize state with two 64-bit integers
        self.state = [seed & 0xFFFFFFFFFFFFFFFF, seed2 & 0xFFFFFFFFFFFFFFFF]

    def next(self) -> int:
        """
        Generate the next 64-bit random number using xorshift128+.
        This follows Sebastiano Vigna's reference implementation.
        """

        # Retrieve each part of the state
        s0 = self.state[0]
        s1 = self.state[1]

        # Place the second part of the state into the first part for future use
        self.state[0] = s1

        # Perform a S0 XOR (S0 << 23)
        s0 ^= (s0 << 23) & 0xFFFFFFFFFFFFFFFF
        # Perform a S0 XOR (S0 >> 17)
        s0 ^= (s0 >> 17) & 0xFFFFFFFFFFFFFFFF
        # Perform a S0 XOR S1
        s0 ^= s1
        # Place the result into the second part of the state for future use
        self.state[1] = s0 + s1 & 0xFFFFFFFFFFFFFFFF

        # Return the result as the random number
        return s0

    def randbits(self, num_bits: int) -> int:
        """
        Generate a random integer with exactly num_bits bits.
        Correctly handles any number of bits by concatenating outputs.
        """

        # Initialize result and the number of bits collected
        result = 0
        bits_collected = 0

        # Continue until we have collected enough bits
        while bits_collected < num_bits:
            # Get the next 64-bit random number
            num = self.next()

            # Determine how many bits to take from this number
            take = min(64, num_bits - bits_collected)

            # Update the result with the taken bits from the random number
            result = (result << take) | (num & ((1 << take) - 1))

            # Update the number of bits collected
            bits_collected += take

        # Return the final result
        return result

if __name__ == "__main__":
    print('Testing Xorshift128+ PRNG generation times (in ms)\n')
    xorshiftr128plus = Xorshiftr128Plus(seed=12345, seed2=67890)

    # Test generation times for various bit sizes
    for nbits in [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]:
        # Generate 10 random nubmer for each bit size and average the time taken
        total_time = 0.0
        for _ in range(10):
            start = time.time()
            number = xorshiftr128plus.randbits(nbits)
            end = time.time()
            total_time += (end - start)

        avg_time = (total_time / 10) * 1000
        print(f"Generation time for {nbits} bits: {avg_time:.6f}\n")
