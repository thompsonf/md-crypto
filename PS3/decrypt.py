from oracle import *
import sys

def get_blocks(lst, block_size):
    blocks = []
    for i in xrange(0, len(lst), block_size):
        blocks.append(lst[i:i + block_size])
    return blocks

def remove_padding(block):
    pad_val = block[-1]
    m_without_padding = block[:-pad_val]
    padding = block[-pad_val:]
    for v in padding:
        assert(v == pad_val)
    return m_without_padding

def bytes_to_string(bytes):
    return "".join([chr(b) for b in bytes])

def decrypt(iv, c):
    block_size = len(c)
    # m is the decryption of c
    # -1 will indicate that that byte of m is unknown for now
    m = [-1] * block_size
    # decrypt c from end to beginning
    for decrypt_idx in range(block_size-1, -1, -1):
        print "decrypt_idx", decrypt_idx
        new_iv = iv[:]
        num_padding_bytes = block_size - decrypt_idx
        # modify the IV so that the bytes after the one we're processing
        # will decrypt to the correct padding scheme
        # i.e. if we're trying to decrypt the byte at index 13 when
        # block_size is 16, we want it to look like the final two bytes
        # of the plaintext were 0x03 0x03, so we do
        # new_IV[idx] = old_IV[idx] xor message[idx] xor 3
        for iv_modify_idx in range(decrypt_idx + 1, block_size):
            assert( m[iv_modify_idx] >= 0 )
            new_iv[iv_modify_idx] = iv[iv_modify_idx] ^ m[iv_modify_idx] ^ num_padding_bytes
        
        # try all possible values for IV at the current idx until one works
        working_IV_val = -1
        for i in range(0, 255):
            new_iv[decrypt_idx] = i
            if Oracle_Send(new_iv + c, 2) == 1:
                if decrypt_idx == block_size - 1:
                    # if we're looking at the final byte, we need to make sure
                    # that we're actually changing the final byte of the message
                    # to 1, not coincidentally matching existing padding.
                    # To test this, also change the next-to-last IV byte.
                    # Oracle should still decrypt successfully
                    old_val = new_iv[block_size - 2]
                    new_iv[block_size - 2] = (old_val + 1) % 256
                    if Oracle_Send(new_iv + c, 2) == 1:
                        assert(working_IV_val == -1)
                        working_IV_val = i
                        new_iv[block_size - 2] = old_val
                        break
                    new_iv[block_size - 2] = old_val
                else:
                    working_IV_val = i
                    break
        assert(working_IV_val >= 0)

        # we know that working_IV_val xor m[decrypt_idx] == num_padding_bytes xor original iv val
        # therefore, m[decrypt_idx] = num_padding_bytes xor working_IV_val
        m[decrypt_idx] = num_padding_bytes ^ working_IV_val ^ iv[decrypt_idx]
        assert(m[decrypt_idx] >= 0)
        print m
    return m

if len(sys.argv) < 2:
    print "Usage: python decrypt.py <filename>"
    sys.exit(-1)

f = open(sys.argv[1])
data = f.read()
f.close()

block_size = 16
ctext = [(int(data[i:i+2],16)) for i in range(0, len(data), 2)]
c_lst = get_blocks(ctext, block_size)

Oracle_Connect()

m_lst = []
# iterate over consecutive pairs of ciphertext blocks
for iv, c in zip(c_lst[:-1], c_lst[1:]):
    m_lst.append(decrypt(iv, c))

m_lst[-1] = remove_padding(m_lst[-1])
flattenend_m = [byte for block in m_lst for byte in block]
message = bytes_to_string(flattened_m)
print message
