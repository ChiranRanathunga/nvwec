from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import webbrowser
import json

url = "https://wallet-connector-cdla.vercel.app/"


class HTTPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        message = json.loads(data)['message']
        if message == '1':
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', 'http://localhost:3000')
            self.send_header('Access-Control-Allow-Methods', 'POST')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(bytes(json.dumps({'message': 'Validation Success'}), 'utf-8'))
            self.server.result = message
        else:
            self.send_error(400)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


def nvwec(iv):
    # open web to connect to metamask and validate the NFT
    webbrowser.open(url)

    # start a local web server to receive data
    server = HTTPServer(('localhost', 8000), HTTPHandler)
    server.result = None

    # start the server in a separate thread
    threading.Thread(target=server.serve_forever).start()

    # wait for incoming data
    while not server.result:
        pass

    # process the data
    data = server.result
    iv.result = data
    server.shutdown()
    return iv.result