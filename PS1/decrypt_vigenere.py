def get_max_idx(lst):
    # assuming positive numbers
    max_idx = 0
    max_val = 0
    for i, v in enumerate(lst):
        if v > max_val:
            max_val = v
            max_idx = i
    return max_idx

def get_score(byte_freqs):
    total = sum(byte_freqs)
    return sum([(float(f) / total)**2 for f in byte_freqs])

def get_key_length(c, min_len, max_len):
    scores = []
    for l in range(min_len, max_len + 1):
        byte_freqs_lst = [[0] * 256 for i in range(l)]
        for i, byte in enumerate(c):
            byte_freqs_lst[i % l][byte] += 1
        individ_scores = [get_score(bf) for bf in byte_freqs_lst]
        avg_score = sum(individ_scores) / l
        scores.append(avg_score)
    return get_max_idx(scores) + min_len

f = open("ciphertext.txt")
data = f.read().strip()
f.close()

ctext = [(int(data[i:i+2],16)) for i in range(0, len(data), 2)]

key_len = get_key_length(ctext, 2, 13)