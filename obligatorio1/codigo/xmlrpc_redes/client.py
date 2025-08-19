import socket
from . import xml
from . import http

class Connection:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __getattr__(self, method_name):
        def remote_call(*args):
            body = xml.build_xmlrpc_request(method_name, args)
            req = http.build_http_request(self.host, self.port, body)

            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((self.host, self.port))
            conn.sendall(req)

            proto, status_code, status_message, headers, body = http.get_http_response(conn)
            conn.close()
            return xml.parse_xmlrpc_response(body)
        return remote_call

def connect(host, port):
    return Connection(host, port)

class Client:
    connect = staticmethod(connect)
