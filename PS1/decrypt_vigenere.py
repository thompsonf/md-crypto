ctext_fname = "ciphertext.txt"
MIN_KEY_LEN = 2
MAX_KEY_LEN = 13

KNOWN_LETTER_FREQS = [
    .082,
    .015,
    .028,
    .043,
    .127,
    .022,
    .020,
    .061,
    .070,
    .002,
    .008,
    .040,
    .024,
    .067,
    .015,
    .019,
    .001,
    .060,
    .063,
    .091,
    .028,
    .010,
    .024,
    .002,
    .020,
    .001
]

def get_max_idx(lst):
    # assuming positive numbers
    max_idx = 0
    max_val = 0
    for i, v in enumerate(lst):
        if v > max_val:
            max_val = v
            max_idx = i
    return max_idx

# the distribution of byte frequencies should be highly nonuniform if the byte frequencies
# come from english text all shifted by a consistent amount
def get_key_len_score(byte_freqs):
    total = sum(byte_freqs)
    return sum([(float(f) / total)**2 for f in byte_freqs])

def get_key_length(c, min_len, max_len):
    scores = []
    for l in range(min_len, max_len + 1):
        byte_freqs_lst = [[0] * 256 for i in range(l)]
        for i, byte in enumerate(c):
            byte_freqs_lst[i % l][byte] += 1
        individ_scores = [get_key_len_score(bf) for bf in byte_freqs_lst]
        avg_score = sum(individ_scores) / l
        scores.append(avg_score)
    return get_max_idx(scores) + min_len

# the frequencies of the lowercase letters in our bytestreams should be closest to the
# known frequencies of lowercase letters when the key is correct
def get_key_guess_score(letter_freqs):
    return sum([f1 * f2 for f1, f2 in zip(letter_freqs, KNOWN_LETTER_FREQS)])

def get_key_guess(bytestream):
    scores = []
    for key_guess in range(0, 255):
        bs = [b ^ key_guess for b in bytestream]
        lowercase_letter_freqs = [0] * 26
        invalid_byte_found = False
        for b in bs:
            # 32 and 127 are min and max values
            # for valid English text
            if b < 32 or b > 127:
                invalid_byte_found = True
                break
            if chr(b) in 'abcdefghijklmnopqrstuvwxyz':
                lowercase_letter_freqs[b - ord('a')] += 1
        score = get_key_guess_score(lowercase_letter_freqs)
        scores.append((key_guess, score))
    return max(scores, key=lambda x: x[1])[0]

def get_bytestreams(ctext, key_len):
    bytestreams = [[] for i in range(key_len)]
    for i, b in enumerate(ctext):
        bytestreams[i % key_len].append(b)
    return bytestreams

def apply_key(ctext, key):
    msg = ""
    for i, b in enumerate(ctext):
        char = chr(key[i % len(key)] ^ b)
        msg += char
    return msg

f = open(ctext_fname)
data = f.read().strip()
f.close()

ctext = [(int(data[i:i+2],16)) for i in range(0, len(data), 2)]

key_len = get_key_length(ctext, MIN_KEY_LEN, MAX_KEY_LEN)
bytestreams = get_bytestreams(ctext, key_len)
key = []
for bs in bytestreams:
    key.append(get_key_guess(bs))

print("Key:", key)
print("Decryption:")
print(apply_key(ctext, key))
