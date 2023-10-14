import base64

word = "base64_password_"
key = "user123"
xor = []
for i in range(len(word)):
    xor.append(ord(word[i]) ^ ord(key[i%len(key)]))
print(base64.b64encode(bytes(xor)))