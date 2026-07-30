from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import json
import requests

class MedicationHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        #serving the index.html
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open("index.html", "r") as file:
                self.wfile.write(file.read().encode())
        #serving the styles.css
        elif self.path == '/styles.css':
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            with open("styles.css", "r") as file:
                self.wfile.write(file.read().encode())
        #serving the script.js
        elif self.path == '/medication_js/script.js':
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.end_headers()
            with open("medication_js/script.js", "r") as file:
                self.wfile.write(file.read().encode())
        #search for the medicine
        elif self.path.startswith('/medicine'):
            query = urllib.parse.urlparse(self.path).query
            parameters = urllib.parse.parse_qs(query)
            medicine = parameters.get('medicine', [None])[0]
            if medicine:
                url = (
                    "https://api.fda.gov/drug/label.json"
                    f"?search=openfda.generic_name:{medicine}"
                    "&limit=1"
                )
                response = requests.get(url)
                data = response.json()
                #Error handling if the medicine is not found
                try:
                    drug = data['results'][0]
                    medicine_info = {
                        "name": drug.get("openfda", {}).get("generic_name", ["N/A"])[0],
                        "description": drug.get("description", ["N/A"])[0],
                        "warnings": drug.get("warnings", ["No warnings found"])[0],
                        "dosage": drug.get("dosage_and_administration", ["No dosage information found"])[0],
                        "instructions": drug.get("instructions_for_use", ["No instructions available"])[0]
                    }
                except (KeyError, IndexError):
                    medicine_info = {"error": "Medicine not found or check the correct spelling."}

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(medicine_info).encode())
            else:
                #If no medicinie name is provided
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                error_message = {"error": "No medicine name provided."}
                self.wfile.write(json.dumps(error_message).encode())
        else:
            #wrong url path
            self.send_response(404)
            self.end_headers()
server = HTTPServer(('localhost', 8000), MedicationHandler)
print("Server running on http://localhost:8000")
server.serve_forever()

