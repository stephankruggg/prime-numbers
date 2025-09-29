import secrets
import time
import numpy as np

from pyparsing import List


# Log2 of state size (8 => 256 elements)
RANDSIZL = 8
# State size - 2^8 = 256
RANDSIZ = 1 << RANDSIZL
# 64-bit mask
MASK64 = 0xFFFFFFFFFFFFFFFF

# Mix function which scrambles eight 64-bit integers using XORs, shifts, and additions
def _mix(a, b, c, d, e, f, g, h):
    a = (a - e) & MASK64; f ^= (h >> 9) & MASK64;  h = (h + a) & MASK64
    b = (b - f) & MASK64; g ^= (a << 9) & MASK64;  a = (a + b) & MASK64
    c = (c - g) & MASK64; h ^= (b >> 23) & MASK64; b = (b + c) & MASK64
    d = (d - h) & MASK64; a ^= (c << 15) & MASK64; c = (c + d) & MASK64
    e = (e - a) & MASK64; b ^= (d >> 14) & MASK64; d = (d + e) & MASK64
    f = (f - b) & MASK64; c ^= (e << 20) & MASK64; e = (e + f) & MASK64
    g = (g - c) & MASK64; d ^= (f >> 17) & MASK64; f = (f + g) & MASK64
    h = (h - d) & MASK64; e ^= (g << 14) & MASK64; g = (g + h) & MASK64

    return a, b, c, d, e, f, g, h

class Isaac64:
    def __init__(self, seed: List[int] = []):
        """Initialize ISAAC64. Seed is a list of 256 64-bit integers."""
        # State size
        self.RANDSIZ = RANDSIZ
        # Internal states
        self.mm = [0]*self.RANDSIZ
        # Accumulator
        self.aa = 0
        # Last random value
        self.bb = 0
        # Counter
        self.cc = 0
        # Remaining numbers in the pool
        self.randcnt = 0

        # Use the seed if provided, otherwise use secure random values
        if seed:
            self.randrsl = [s & MASK64 for s in seed]
        else:
            self.randrsl = [secrets.randbits(64) for _ in range(self.RANDSIZ)]

        # Initialize the state with the seed
        self._randinit(flag = True)

    def next(self):
        """Return next 64-bit integer."""
        if self.randcnt == 0:
            self._isaac64()
            self.randcnt = self.RANDSIZ

        self.randcnt -= 1

        return self.randrsl[self.randcnt]

    def randbits(self, num_bits: int):
        """Return arbitrary-length random number."""
        result = 0
        bits_collected = 0
        while bits_collected < num_bits:
            r = self.next()
            take = min(64, num_bits - bits_collected)
            result = (result << take) | (r >> (64 - take))
            bits_collected += take

        return result

    def _randinit(self, flag: bool):
        """Initialize or reinitialize the state array (mm)."""

        # Initializes 8 variables to the golden ratio
        a = b = c = d = e = f = g = h = 0x9e3779b97f4a7c13

        # Mix the variables four times
        for _ in range(4):
            a, b, c, d, e, f, g, h = _mix(a, b, c, d, e, f, g, h)

        # Fill in the state array
        for i in range(0, self.RANDSIZ, 8):
            # Mix the seed into the variables if flag is True
            if flag:
                a = (a + self.randrsl[i  ]) & MASK64
                b = (b + self.randrsl[i+1]) & MASK64
                c = (c + self.randrsl[i+2]) & MASK64
                d = (d + self.randrsl[i+3]) & MASK64
                e = (e + self.randrsl[i+4]) & MASK64
                f = (f + self.randrsl[i+5]) & MASK64
                g = (g + self.randrsl[i+6]) & MASK64
                h = (h + self.randrsl[i+7]) & MASK64

            # Apply mixing function
            a,b,c,d,e,f,g,h = _mix(a,b,c,d,e,f,g,h)

            # Store mixed values into the state array
            self.mm[i  ] = a; self.mm[i+1] = b; self.mm[i+2] = c; self.mm[i+3] = d
            self.mm[i+4] = e; self.mm[i+5] = f; self.mm[i+6] = g; self.mm[i+7] = h

        # Second pass to further mix the state array
        if flag:
            for i in range(0, self.RANDSIZ, 8):
                a = (a + self.mm[i  ]) & MASK64
                b = (b + self.mm[i+1]) & MASK64
                c = (c + self.mm[i+2]) & MASK64
                d = (d + self.mm[i+3]) & MASK64
                e = (e + self.mm[i+4]) & MASK64
                f = (f + self.mm[i+5]) & MASK64
                g = (g + self.mm[i+6]) & MASK64
                h = (h + self.mm[i+7]) & MASK64

                a,b,c,d,e,f,g,h = _mix(a,b,c,d,e,f,g,h)

                self.mm[i  ] = a; self.mm[i+1] = b; self.mm[i+2] = c; self.mm[i+3] = d
                self.mm[i+4] = e; self.mm[i+5] = f; self.mm[i+6] = g; self.mm[i+7] = h

        # Generate the first set of random numbers
        self._isaac64()
        self.randcnt = self.RANDSIZ

    def _isaac64(self):
        """ISAAC64 algorithm: updates state and fills the state array with new values."""
        a = self.aa
        # Update the last random value and counter
        b = (self.bb + (self.cc + 1)) & MASK64
        self.cc = (self.cc + 1) & MASK64

        half = self.RANDSIZ // 2

        # Two passes over the state array
        for m in range(0, half):
            self._rngstep(~(a ^ (a << 21)) & MASK64, m,   half, a, b)
            self._rngstep( (a ^ (a >> 5))  & MASK64, m+1, half, a, b)
            self._rngstep( (a ^ (a << 12)) & MASK64, m+2, half, a, b)
            self._rngstep( (a ^ (a >> 33)) & MASK64, m+3, half, a, b)

        for m in range(0, half):
            self._rngstep(~(a ^ (a << 21)) & MASK64, m,   half, a, b)
            self._rngstep( (a ^ (a >> 5))  & MASK64, m+1, half, a, b)
            self._rngstep( (a ^ (a << 12)) & MASK64, m+2, half, a, b)
            self._rngstep( (a ^ (a >> 33)) & MASK64, m+3, half, a, b)

        # Update the accumulators
        self.aa = a
        self.bb = b

    def _rngstep(self, mix, m, m2_offset, a, b):
        """
        Perform one step of ISAAC64 generation.
        mix:   nonlinear transformation applied to 'a'
        m:     index into state array
        m2:    paired index (m + half)
        a, b:  accumulators
        """
        # Get the current state value and a far apart pair
        x = self.mm[m]
        m2 = self.mm[(m + m2_offset) % self.RANDSIZ]

        # Combine the mixing function with the state pair
        a = (mix + m2) & MASK64

        # Compute the new state position based on a word in position X plus the accumulator a plus b
        y = (self._ind(x) + a + b) & MASK64

        # Update state
        self.mm[m] = y

        # Compute the new random value based on a word in position Y plus X
        b = (self._ind(y >> RANDSIZL) + x) & MASK64
        self.randrsl[m] = b

    def _ind(self, x):
        """Indexing function: returns mm[x mod 256]."""
        return self.mm[x & (RANDSIZ - 1)]

if __name__ == "__main__":
    print('Testing Isaac PRNG generation times (in ms)\n')
    isaac = Isaac64()

    # Test generation times for various bit sizes
    for nbits in [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]:
        # Generate 10 random numbers for each bit size and average the time taken
        total_time = 0.0
        for _ in range(10):
            start = time.time()
            number = isaac.randbits(nbits)
            end = time.time()

            gen_time = (end - start) * 1000
            print(f"Generated {nbits}-bit number: {number} in {gen_time:.6f} ms")

            total_time += gen_time

        avg_time = total_time / 10
        print(f"Generation time for {nbits} bits: {avg_time:.6f} ms\n")

    # Verify the uniformity of the generated bits using a simple frequency test
    bits = []
    for _ in range(100000):
        num = isaac.randbits(64)
        bits.extend([int(b) for b in bin(num)[2:].zfill(64)])

    zeros = bits.count(0)
    ones = bits.count(1)

    total = zeros + ones
    expected = total / 2
    chi2 = ((zeros - expected)**2 + (ones - expected)**2) / expected
    p_value = np.exp(-chi2/2)

    print("Frequency Test:")
    print(f"0s: {zeros}, 1s: {ones}, Chi2: {chi2:.2f}, p-value ~ {p_value:.4f}\n")
