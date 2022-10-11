from http.server import HTTPServer, BaseHTTPRequestHandler
from io import StringIO
from json import dump


class MetricServerHandler(BaseHTTPRequestHandler):
    metrics = [{1: 2}]

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        if self.metrics:
            metric = self.metrics.pop()
            response = StringIO()
            dump(metric, response)
            self.wfile.write(response.getvalue().encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        
        if body:
            sample = StringIO()
            dump(body.decode('utf-8'), sample)
            self.metrics.append(sample.getvalue())

        self.send_response(200)
        self.end_headers()

def run(address='', port=8080):
    server_socket = (address, port)
    server = HTTPServer(server_socket, MetricServerHandler)
    
    print('starting server on address {} and port {}'.format(address, port))
    server.serve_forever()
    
if __name__ == "__main__":  
    from sys import argv
  
    if len(argv) == 3:
        run(address=int(argv[1]), port=int(argv[2]))
    elif len(argv) == 2:
        run(address=int(argv[1]))
    else:
        run()
