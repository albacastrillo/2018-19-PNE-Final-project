from http.server import BaseHTTPRequestHandler
import socketserver
import requests
import termcolor
import sys

HOST_NAME = 'localhost'
PORT = 8000


class Handler(BaseHTTPRequestHandler):

    def input_value(self):
        if self.path.find('?') > 0:
            enter = self.path.split("?")[1]
            if self.path.find('='):
                if self.path.find('&') > 0:
                    enter_1 = enter.split("&")[0]
                    enter_2 = enter.split("&")[1]
                    value_1 = enter_1.split("=")[1]
                    value_2 = enter_2.split("=")[1]
                    if enter_1.split("=")[0] == "specie":
                        return value_1, value_2
                    elif enter_1.split("=")[0] == "chromo":
                        return value_2, value_1
                    else:
                        return False
                else:  # Karyotype
                    value_3 = enter.split("=")[1]
                    return value_3
            else:
                return False
        else:
            return False

    def do_GET(self):
        termcolor.cprint(self.requestline + "\n", 'green')
        action = self.path.split("?")[0]

        # When we write the endpoint "/" it opens the index.html
        if action == "/":
            file = open("index.html", "r")
            contents = file.read()

        else:
            # It shows the ERROR page
            file = open("Error.html", "r")
            contents = file.read()

        self.send_response(200)  # -- Status line: OK!
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(str.encode(contents)))
        self.end_headers()
        self.wfile.write(str.encode(contents))


# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at PORT", PORT)
    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()

print("")
print("Server Stopped")
