from http.server import BaseHTTPRequestHandler
import socketserver
import requests
import termcolor

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

                    # When there are two input values, in the function chromosomeLength
                    if enter_1.split("=")[0] == "specie":
                        return value_1, value_2
                    elif enter_1.split("=")[0] == "chromo":
                        return value_2, value_1
                    else:
                        return False
                # When there is only one input value
                else:
                    value_4 = enter.split("=")[1]
                    return value_4
            else:
                return False
        else:
            return False

    # When there are 3 input values (in the function geneList) we use this function instead of the input_value one
    # because now the "chromo" is in the first position instead of being in the second, like it was before
    def list_input(self):
        if self.path.find('?') > 0:
            enter = self.path.split("?")[1]
            if self.path.find('='):
                if self.path.find('&') > 0:
                    enter_1 = enter.split("&")[0]
                    enter_2 = enter.split("&")[1]
                    enter_3 = enter.split("&")[2]
                    value_1 = enter_1.split("=")[1]
                    value_2 = enter_2.split("=")[1]
                    value_3 = enter_3.split("=")[1]
                    return value_1, value_2, value_3
                else:
                    return False
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
                list_of_species = self.list_species(self.input_value())
            else:
                list_of_species = self.list_species(199)
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
                try:
                    karyot = self.karyotype(self.input_value())
                    contents += "The karyotype of " + self.input_value() + "is:<ul>"
                    if len(karyot) == 0:
                        contents += "<p><strong>There is no karyotype.<strong></p>"
                    else:
                        for item in karyot:
                            contents += "<li>" + item + "</li>"
                    contents += "</body></html>"
                except KeyError:
                    contents += "</body> This is an incorrect specie. Please, introduce a new one.</html>"
            else:
                contents += "</body>Please, introduce a specie.</html>"

        # When we write the endpoint "/chromosomeLength" it opens the Response.html and add the name of the specie,
        # the name of the chromosome and its length
        elif action == "/chromosomeLength":
            file = open("Response.html", "r")
            contents = file.read()
            if self.input_value():
                specie, chromo = self.input_value()
                if not specie or not chromo:
                    contents += "</body>Please, introduce both, a specie and a chromosome.</html>"
                elif specie and chromo:
                    if self.chromosomeLength(specie, chromo) == "wrong chromo":
                        contents += "</body>The specie introduced does not contain that chromosome.</html>"
                    elif self.chromosomeLength(specie, chromo) == "wrong specie":
                        contents += "</body>The specie is wrong. Please, introduce a new one.</html>"
                    else:
                        contents += "The length of chromosome " + chromo + " of " + specie + " is: "
                        contents += "<strong>" + str(self.chromosomeLength(specie, chromo)) + "</strong>"
                        contents += "</body></html>"
                else:
                    contents += "</body>Please, introduce both, a specie and a chromosome.</html>"
            else:
                contents += "</body>Please, introduce a specie and a chromosome.</html>"

        # When we write the endpoint "/genSeq" it opens the Response.html and add the sequence of a given human gene
        elif action == "/geneSeq":
            file = open("Response.html", "r")
            contents = file.read()
            if self.input_value():
                try:
                    gene = self.input_value()
                    seq = self.geneSeq(gene)
                    contents += "Sequence of human gene " + gene + ": "
                    contents += "<br><div style=\"overflow-wrap: break-word;\">"
                    contents += "<strong>" + str(seq) + "</strong></div>"
                    contents += "</body></html>"
                except IndexError:
                    contents += "</body>This gene is incorrect. Please, introduce a new one.</html>"
            else:
                contents += "</body>Please, introduce a gene.</html>"

        # When we write the endpoint "/genInfo" it opens the Response.html and add information about a human gene:
        # start, end, Length, id and Chromosome
        elif action == "/geneInfo":
            file = open("Response.html", "r")
            contents = file.read()
            try:
                if self.input_value():
                    gene = self.input_value()
                    gene_info = self.geneInfo(gene)
                    contents += "<h2>Information about human gene " + gene + ":</h2>"
                    contents += "<p> ID: " + gene_info['id'] + "</p>"
                    contents += "<p> Start: " + gene_info['start'] + "</p>"
                    contents += "<p> End: " + gene_info['end'] + "</p>"
                    contents += "<p> Length: " + gene_info['length'] + "</p>"
                    contents += "<p> Chromosome: " + gene_info['chromo'] + "</p>"
                    contents += "</body></html>"
                else:
                    contents += "</body>Please, introduce a gene.</html>"
            except IndexError:
                contents += "</body>This gene is incorrect. Please, introduce a new one.</html>"

        # When we write the endpoint "/genCalc" it opens the Response.html and add total length and the
        # percentage of all its bases
        elif action == "/geneCalc":
            file = open("Response.html", "r")
            contents = file.read()
            try:
                if self.input_value():
                    gene = self.input_value()
                    bases = self.geneCalc(gene)
                    contents += "<h2>Information about human gene bases " + gene + " bases:</h2>"
                    contents += "<h4>Number of bases:</h4><ul>"
                    contents += "<li> A: " + bases['base_a'] + "</li>"
                    contents += "<li> C: " + bases['base_c'] + "</li>"
                    contents += "<li> G: " + bases['base_g'] + "</li>"
                    contents += "<li> T: " + bases['base_t'] + "</li></ul>"
                    contents += "<h4>Percentage of bases:</h4><ul>"
                    contents += "<li> A: " + bases['perc_a'] + "</li>"
                    contents += "<li> C: " + bases['perc_c'] + "</li>"
                    contents += "<li> G: " + bases['perc_g'] + "</li>"
                    contents += "<li> T: " + bases['perc_t'] + "</li></ul>"
                    contents += "</body></html>"
                else:
                    contents += "</body>Please, introduce a gene.</html>"
            except IndexError:
                contents += "</body>This gene is incorrect. Please, introduce a new one.</html>"

        # When we write the endpoint "/genList" it opens the Response.html and add the names of the genes located
        # in the chromosome "chromo" from the start to end positions
        elif action == "/geneList":
            file = open("Response.html", "r")
            contents = file.read()
            try:
                if self.input_value():
                    chromo, start, end = self.list_input()
                    if self.geneList(chromo, start, end) == "wrong position":
                        contents += "</body> There are no genes in this position in the introduced chromosome.</html>"
                    else:
                        list_gene = self.geneList(chromo, start, end)
                        contents += "<h2>Genes located in the chromosome " + chromo + " </h2>"
                        contents += "<ul>"
                        for item in list_gene:
                            contents += "<li>" + item + "</li>"
                        contents += "</ul>"
                        contents += "</body></html>"
                else:
                    contents += "</body> Please, introduce a chromosome, a start and an end.</html>"
            except requests.exceptions.HTTPError:
                contents += "</body>Please, introduce a new chromosome, a start and an end.</html>"

        # It shows the ERROR page if the endpoint is incorrect
        else:
            file = open("Error.html", "r")
            contents = file.read()

        self.send_response(200)  # Status line: OK!
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(str.encode(contents)))
        self.end_headers()
        self.wfile.write(str.encode(contents))

    def list_species(self, limit):
        server = "https://rest.ensembl.org"
        ext = "/info/species?"
        r = requests.get(server + ext, headers={"Content-Type": "application/json"})
        if not r.ok:
            r.raise_for_status()
        decoded = r.json()
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

    def karyotype(self, specie):
        server = "http://rest.ensembl.org"
        ext = "/info/assembly/" + specie
        r = requests.get(server + ext, headers={"Content-Type": "application/json"})
        decoded = r.json()
        karyot_list = decoded['karyotype']
        return karyot_list

    def chromosomeLength(self, specie, chromo):
        server = "http://rest.ensembl.org"
        ext = "/info/assembly/"+specie
        r = requests.get(server + ext, headers={"Content-Type": "application/json"})
        decoded = r.json()
        results = decoded.get('top_level_region')
        if results:
            for item in results:
                if item['name'] == chromo:
                    return item['length']
            return "wrong chromo"
        return "wrong specie"

    def geneSeq(self, gene):
        server = "http://rest.ensembl.org"
        ext = "/xrefs/symbol/human/" + gene
        r = requests.get(server + ext, headers={"Content-Type": "application/json"})
        if not r.ok:
            r.raise_for_status()
        decoded = r.json()
        id = decoded[0].get('id')
        server = "http://rest.ensembl.org"
        ext = "/sequence/id/" + id
        r = requests.get(server + ext, headers={"Content-Type": "text/plain"})
        if not r.ok:
            r.raise_for_status()
        print("Seq: " + str(type(r.text)))
        return r.text

    def geneInfo(self, gene):
        server = "http://rest.ensembl.org"
        ext = "/xrefs/symbol/human/" + gene
        r = requests.get(server + ext, headers={"Content-Type": "application/json"})
        if not r.ok:
            r.raise_for_status()
        decoded = r.json()
        gene_id = decoded[0].get('id')
        server = "https://rest.ensembl.org"
        ext = "/sequence/id/" + gene_id + "?"
        r = requests.get(server + ext, headers={"Content-Type": "application/json"})
        if not r.ok:
            r.raise_for_status()
        decoded = r.json()
        cad = decoded['desc']
        info = {
            "id": decoded['query'],
            "start": str(cad.split(":")[3]),
            "end": str(cad.split(":")[4]),
            "length": str(len(decoded['seq'])),
            "chromo": str(cad.split(":")[2])
        }
        return info

    def geneCalc(self, gene):
        server = "http://rest.ensembl.org"
        ext = "/xrefs/symbol/human/" + gene
        r = requests.get(server + ext, headers={"Content-Type": "application/json"})
        if not r.ok:
            r.raise_for_status()
        decoded = r.json()
        gene_id = decoded[0].get('id')
        server = "https://rest.ensembl.org"
        ext = "/sequence/id/" + gene_id + "?"
        r = requests.get(server + ext, headers={"Content-Type": "application/json"})
        if not r.ok:
            r.raise_for_status()
        data = {
            "base_a": str(r.text.count('A')),
            "base_c": str(r.text.count('C')),
            "base_g": str(r.text.count('G')),
            "base_t": str(r.text.count('T')),
            "perc_a": str('{:0.2f}'.format(100 * int(r.text.count('A')) / len(r.text))) + "%",
            "perc_c": str('{:0.2f}'.format(100 * int(r.text.count('C')) / len(r.text))) + "%",
            "perc_g": str('{:0.2f}'.format(100 * int(r.text.count('G')) / len(r.text))) + "%",
            "perc_t": str('{:0.2f}'.format(100 * int(r.text.count('T')) / len(r.text))) + "%"
        }
        return data

    def geneList(self, chromo, start, end):
        server = "http://rest.ensembl.org"
        ext = "/overlap/region/human/" + str(chromo) + ":" + str(start) + "-" + str(end) + "?content-type=application" \
                                                                                           "/json;feature=gene"
        r = requests.get(server + ext, headers={"Content-Type": "application/json"})
        if not r.ok:
            r.raise_for_status()
        results = r.json()
        list_gene = []
        if results:
            for gene in results:
                name = gene['external_name']
                list_gene.append(name)
            return list_gene
        return "wrong position"


socketserver.TCPServer.allow_reuse_address = True

# MAIN PROGRAM
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at PORT", PORT)
    try:
        httpd.serve_forever()

    except KeyboardInterrupt:
        print("Server stopped by the user")
        httpd.server_close()

print("The server is stopped")
