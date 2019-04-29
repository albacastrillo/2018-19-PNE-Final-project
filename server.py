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

        # When we write the endpoint "/listSpecies" it opens the Response.html and add the list of
        # species to the contents
        elif action == "/listSpecies":
            if self.input_value():
                list_of_species = list_species(self.input_value())
            else:
                list_of_species = list_species()
            file = open("Response.html", "r")
            contents = file.read()
            contents += "<h1>List of species:</h1><ul>"
            for item in list_of_species:
                contents += "<li>" + item + "</li>"
            contents += "</ul></body></html>"

        # When we write the endpoint "/karyotype" it opens the Response.html and add the list of chromosomes
        elif action == "/karyotype":
            file = open("Response.html", "r")
            contents = file.read()
            if self.input_value():
                karyot = karyotype(self.input_value())
                contents += "Karyotype of " + self.input_value() + ":<ul>"
                if len(karyot) == 0:
                    contents += "<p><strong>None</strong></p>"
                else:
                    for item in karyot:
                        contents += "<li>" + item + "</li>"
            contents += "</body></html>"

        # When we write the endpoint /chromosomeLength it opens the Response.html and add the name of the specie,
        # the name of the chromosome and its length
        elif action == "/chromosomeLength":
            file = open("Response.html", "r")
            contents = file.read()
            if self.input_value():
                specie, chromo = self.input_value()
                contents += "The length of chromosome " + chromo + " of " + specie + " is: "
                contents += "<strong>" + str(chromosomeLength(specie, chromo)) + "</strong>"
            contents += "</body></html>"
        else:
            # It shows the ERROR page
            file = open("Error.html", "r")
            contents = file.read()

        self.send_response(200)  # Everything is OK!
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(str.encode(contents)))
        self.end_headers()
        self.wfile.write(str.encode(contents))


def list_species(limit=199):
    server = "https://rest.ensembl.org"
    ext = "/info/species?"
    request = requests.get(server + ext, headers={"Content-Type": "application/json"})
    if not request.ok:
        request.raise_for_status()
        sys.exit()
    decoded = request.json()
    results = decoded.get('species')
    species_list = []
    if not limit:
        n = len(results)
    else:
        n = int(limit)
    i = 1
    if results:
        for specie in results:
            name = specie['name']
            species_list.append(name)
            if i < n:
                i += 1
            else:
                break
    return species_list


def karyotype(specie):
    server = "http://rest.ensembl.org"
    ext = "/info/assembly/" + specie
    request = requests.get(server + ext, headers={"Content-Type": "application/json"})
    if not request.ok:
        request.raise_for_status()
        sys.exit()
    decoded = request.json()
    karyot_list = decoded['karyotype']
    return karyot_list


def chromosomeLength(specie, chromo):
    server = "http://rest.ensembl.org"
    ext = "/info/assembly/" + specie
    request = requests.get(server + ext, headers={"Content-Type": "application/json"})
    if not request.ok:
        request.raise_for_status()
        sys.exit()
    decoded = request.json()
    results = decoded.get('top_level_region')
    if results:
        for item in results:
            if item['name'] == chromo:
                return item['length']
        return "Not found!"


# Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at PORT", PORT)
    # Main loop: Attending the client. If there is a new client, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()

print("")
print("Server Stopped")
