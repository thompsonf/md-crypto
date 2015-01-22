from oracle import *
import sys

#data = "01234567890123456789012345678901"
data = "abcdefghijklmnopqrstuvwxyzabcdef"
b = bytearray(data)

Oracle_Connect()

tag1 = Mac(data, len(data))
#tag2 = Mac(b, len(data))

ret1 = Vrfy(data, 32, tag1)

Oracle_Disconnect()

print tag1
print tag2

if (ret1):
    print "string verified successfully!"
else:
    print "string verification failed."

# if (ret2):
#     print "bytearray verified successfully!"
# else:
#     print "bytearray verification failed."
