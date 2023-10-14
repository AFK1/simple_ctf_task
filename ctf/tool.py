import base64

word = "ctf{N33d_p4Ssw0rD_haSh1ng}"
key = "admin"
xor = []
for i in range(len(word)):
    xor.append(ord(word[i]) ^ ord(key[i%len(key)]))
print(base64.b64encode(bytes(xor)))