from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import os
import base64


def registration(name, password):
  f = open("./site/database.data", "a")
  xor = []
  for i in range(len(password)):
      xor.append(ord(password[i]) ^ ord(name[i%len(name)]))
  f.write(name)
  f.write(" ")
  f.write(base64.b64encode(bytes(xor)))
  f.write("\n")

def delete_account(name, password):
  pass

class HttpGetHandler(BaseHTTPRequestHandler):
  def _response(self, code=200):
    self.send_response(code)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

  def do_GET(self):
    if (self.path[1:] in os.listdir("./site/")):
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

  def do_POST(self):
    content_length = int(self.headers['Content-Length'])
    post_data = self.rfile.read(content_length)
    print(post_data)

    self._response()
    self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=HttpGetHandler):
  server_address = ('', 9000)
  httpd = server_class(server_address, handler_class)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    httpd.server_close()

if __name__ == "__main__":
  run()