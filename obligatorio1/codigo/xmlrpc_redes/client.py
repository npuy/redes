import socket
from . import xml
from . import http
import time

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
            try:
                data = req
                bytes_enviados = conn.send(data)
                data = data[bytes_enviados:]
                while data != b'':
                    bytes_enviados = conn.send(data)
                    data = data[bytes_enviados:]
            except Exception as e:
                print(f'Error al enviar paquete -> {e}')
                conn.close()
            else:
                proto, status_code, status_message, headers, body = http.get_http_response(conn)
                conn.close()
                return xml.parse_xmlrpc_response(body)
        return remote_call

def connect(host, port):
    return Connection(host, port)

class Client:
    connect = staticmethod(connect)
