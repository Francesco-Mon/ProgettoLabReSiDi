from http.server import HTTPServer
from server import RequestHandler

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server in esecuzione su http://127.0.0.1:{port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
