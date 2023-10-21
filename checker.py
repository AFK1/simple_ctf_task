import requests
import base64
import string
import random

ips = ["0.0.0.0:9000"]

for ip in ips:
  work = False
  name = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))
  password = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))
  requests.get("http://"+ip+"/reg_me_pls?nick="+name+"&password="+password)
  x = requests.get("http://"+ip+"/passwords")
  lines = x.text.split("\n")
  lines.pop()
  new_pasword = ""
  for line in lines:
    new_name, b64password = line.split(" ")
    if (new_name != name): continue
    xor = base64.b64decode(b64password).decode('utf-8')
    for i in range(len(xor)):
      new_pasword += chr(ord(xor[i]) ^ ord(name[i%len(name)]))
    if (new_pasword == password):
      work = True
  if (work):
    print(ip, "work")
  else:
    print(ip, "not work")
  