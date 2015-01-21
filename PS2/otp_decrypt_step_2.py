#guessed this plaintext from result of otp_decrypt_step_1
known_plaintext_idx = 2
known_plaintext = "the current plan is top secret."
known_bytes = [ord(c) for c in known_plaintext]

ctexts = []
f = open("otp_ciphertexts.txt")
for line in f:
    data = line.strip()
    ctext = [(int(data[i:i+2],16)) for i in range(0, len(data), 2)]
    ctexts.append(ctext)
f.close()

probable_key = [mb ^ cb for (mb, cb) in zip(known_bytes, ctexts[known_plaintext_idx])]

messages = []
for c in ctexts:
    decryption = [chr(cb ^ kb) for (cb, kb) in zip(c, probable_key)]
    messages.append("".join(decryption))

for msg in messages:
    print msg