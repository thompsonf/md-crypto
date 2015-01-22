# How to solve:
#
# if m 63-digit hex number,
# M = 0x00 m 0x00 m
# implies
# M = m*2^512 + m
# M = m(1 + 2^512)
#
# M^d = m^d * (1 + 2^512)^d mod N
#
# suppose a, b are any two factors of m
# then
# M^d = (ab)^d * (1 + 2^512)^d mod N
#
# let A = 0x00 a 0x00 a, B = 0x00 b 0x00 b s.t.
# A^d = a^d * (1 + 2^512)^d mod N
# B^d = b^d * (1 + 2^512)^d mod N
#
# then
# A^d * B^d = m^d * (1 + 2^512)^(2d) mod N
#           = M^d * (1 + 2^512)^d mod N
#
# therefore
# M^d = A^d * B^d * ((1 + 2^512)^d)^-1 mod N
#
# Now we just need to figure out what (1 + 2^512)^d is so that we can divide by it
#
# let h = 1
# then H = h(1 + 2^512) = 1 + 2^512
# so Sign(1) = Sign(h) = H^d = (1 + 2^512)^d mod N
# Sign(1) = (1 + 2^512)^d mod N

from oracle import *
from helper import *

N = 119077393994976313358209514872004186781083638474007212865571534799455802984783764695504518716476645854434703350542987348935664430222174597252144205891641172082602942313168180100366024600206994820541840725743590501646516068078269875871068596540116450747659687492528762004294694507524718065820838211568885027869
e = 65537

Oracle_Connect()

msg = "Crypto is hard --- even schemes that look complex can be broken"
m = ascii_to_int(msg)

# first, let's calculate the constant value (1 + 2^512)^d
# it's easy to do this by finding Sign(1)
# Sign(1) = (1*2^512 + 1)^d mod N
#         = (1 + 2^512)^d mod N
const = Sign(1)

# now let's try to factor m. All we need is numbers a and b s.t. m = ab mod N, a > 1, b > 1
# very inefficient, but we can just count up until we find one.
# One easy way to do this is to take a = 2, b = m*(2^-1)
# 2 will always have an inverse since N will never be even (because it's a product of big primes)
a = 2
b = m * modinv(2, N) % N
assert(a * b % N == m)

# now we get the signs of a and b, which we can combine with const to get Sign(m)
a_s = Sign(a)
b_s = Sign(b)

# calculate m_s as explained above
m_s = (a_s * b_s % N) * modinv(const, N) % N
print(hex(m_s))

Oracle_Disconnect()