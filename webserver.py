from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

                output = ""
                output+= "<html><body>HELLO</body></html>"
                self.wfile.write(output.encode())
                print(output)
                return
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

                output = ""
                output+= "<html><body>Hola! <a href = '/hello'> Back to Hello </a></body></html>"
                self.wfile.write(output.encode())
                print(output)
                return
        except IOError:
            self.send_error(404,"File not found: %s" % self.path)

    def do_POST(self):
        try:
        except:

def main ():
    try:
        port = 8080
        server = HTTPServer(('',port), WebServerHandler)
        print("WebServer is running on %s" % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print("Closing webserver...")
        server.socket.close()


if __name__ == '__main__':
    main()