from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import os
import base64


def registration(name, password):
  f = open("./site/passwords", "a")
  xor = []
  for i in range(len(password)):
    xor.append(ord(password[i]) ^ ord(name[i%len(name)]))
  f.write(name)
  f.write(" ")
  f.write(str(base64.b64encode(bytes(xor)))[2:-1])
  f.write("\n")

def delete_account(name, password):
  f = open("./site/passwords", "r")
  lines = f.readlines()
  f.close()
  xor = []
  for i in range(len(password)):
    xor.append(ord(password[i]) ^ ord(name[i%len(name)]))

  f = open("./site/passwords", "w")
  for line in lines:
    if line.strip("\n") != (name+" "+xor):
      f.write(line)
  f.close()

class HttpGetHandler(BaseHTTPRequestHandler):
  def _response(self, code=200):
    self.send_response(code)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

  def do_GET(self):
    if (self.path.split("?")[0] == "/reg_me_pls"):
      try:
        args = dict([(i.split("=")[0], i.split("=")[1]) for i in self.path.split("?")[1].split("&")])
        registration(args["nick"], args["password"])
        self.send_response(301)
        self.send_header('Location', './index.html')
        self.end_headers()
      except Exception as e:
        print(e)
        self._response(400)
        self.wfile.write("wrong data".encode('utf-8'))
    elif (self.path.split("?")[0] == "/del_me_pls"):
      try:
        args = dict([(i.split("=")[0], i.split("=")[1]) for i in self.path.split("?")[1].split("&")])
        delete_account(args["nick"], args["password"])
        self.send_response(301)
        self.send_header('Location', './index.html')
        self.end_headers()
      except Exception as e:
        print(e)
        self._response(400)
        self.wfile.write("wrong data".encode('utf-8'))
    elif (self.path[1:] in os.listdir("./site/")):
      f = open("./site"+self.path, "r")
      self._response(200)
      self.wfile.write(f.read().encode('utf-8'))
    elif (self.path == "/"):
      self.send_response(301)
      self.send_header('Location', './index.html')
      self.end_headers()
    else:
      self._response(404)
      self.wfile.write("not found".encode('utf-8'))

def run(server_class=HTTPServer, handler_class=HttpGetHandler):
  server_address = ('', 9000)
  httpd = server_class(server_address, handler_class)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    httpd.server_close()

if __name__ == "__main__":
  run()