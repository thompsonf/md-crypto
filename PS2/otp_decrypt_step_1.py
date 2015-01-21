from collections import Counter

def get_most_common_val(lst):
    data = Counter(lst)
    return data.most_common(1)[0][0]

def get_probable_key_val(idx, ctexts):
    space_letter_pair_freq = [0] * len(ctexts)
    for i in range(len(ctexts)):
        for j in range(i+1, len(ctexts)):
            xor = ctexts[i][idx] ^ ctexts[j][idx]
            # check whether second bit is a 1
            if xor & 64:
                space_letter_pair_freq[i] += 1
                space_letter_pair_freq[j] += 1

    possible_spaces = []
    for i, f in enumerate(space_letter_pair_freq):
        if f > len(ctexts) / 2:
            possible_spaces.append(i)

    probable_space_ctext_vals = []
    for i in possible_spaces:
        probable_space_ctext_vals.append(ctexts[i][idx])

    if len(probable_space_ctext_vals) > 0:
        return get_most_common_val(probable_space_ctext_vals) ^ ord(' ')
    else:
        return 0

ctexts = []
f = open("otp_ciphertexts.txt")
for line in f:
    data = line.strip()
    ctext = [(int(data[i:i+2],16)) for i in range(0, len(data), 2)]
    ctexts.append(ctext)
f.close()

key = [None] * len(ctexts[0])

for i in range(len(key)):
    key[i] = get_probable_key_val(i, ctexts)

messages = []
for c in ctexts:
    decryption = [cb ^ kb for (cb, kb) in zip(c, key)]
    msg = ""
    for b in decryption:
        if (b >= 65 and b <= 90) or (b >= 97 and b <= 122):
            msg += chr(b)
        else:
            msg += ' '
    messages.append(msg)

for msg in messages:
    print msg