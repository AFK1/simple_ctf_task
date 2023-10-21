import requests
import base64

ips = ["0.0.0.0:9000"]

for ip in ips:
  print("[",ip,"]:")
  x = requests.get("http://"+ip+"/passwords")
  lines = x.text.split("\n")
  lines.pop()
  for line in lines:
    name, b64password = line.split(" ")
    print(name, "- name")
    xor = base64.b64decode(b64password).decode('utf-8')
    for i in range(len(xor)):
      print(chr(ord(xor[i]) ^ ord(name[i%len(name)])), end="")
    print(" - password")
    print()
  print()