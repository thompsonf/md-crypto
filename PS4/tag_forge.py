# let m be the original message, and m1-m4 the blocks composing it
# let + be xor
# let t(m, m') be a tag for the message with two blocks m and m'
#
# then t(m) = t( t(m1,m2)+m3, m4 )
#
# m1       m2          m3            m4
# |         |          |             |
# --- F ----+----F-----+-----F-------+-------F--------
#                   |aka                            |
#                t1 = t(m1,m2)                      t
#                                             aka t2 = t(t1+m3, m4)

from oracle import *
import sys

msg = "I, the server, hereby agree that I will pay $100 to this student"
assert( len(msg) == 64 )

m1m2 = msg[:32]
m3 = msg[32:48]
m4 = msg[48:]

m3_bytes = bytearray(m3)

Oracle_Connect()

t1 = Mac(m1m2, 32)
inp = bytearray(len(t1))

for i in range(len(inp)):
    inp[i] = t1[i] ^ m3_bytes[i]

t2 = Mac(inp + m4, 32)
for b in t2:
    print(hex(b))

Oracle_Disconnect()