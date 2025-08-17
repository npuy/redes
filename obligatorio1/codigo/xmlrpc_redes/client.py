import socket
from . import protocol

class Connection:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __getattr__(self, method_name):
        def remote_call(*args):
            body = protocol.build_xmlrpc_request(method_name, args)
            req = protocol.build_http_request(self.host, self.port, body)

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host, self.port))
            s.sendall(req)

            data = b''
            while b'\r\n\r\n' not in data:
                data += s.recv(4096)
            head, rest = data.split(b'\r\n\r\n', 1)
            headers = head.decode().split('\r\n')
            hdrs = {}
            for line in headers[1:]:
                if not line: continue
                k, v = line.split(':', 1)
                hdrs[k.strip().lower()] = v.strip()
            cl = int(hdrs.get('content-length', '0'))
            body = rest
            while len(body) < cl:
                body += s.recv(cl - len(body))
            s.close()
            return protocol.parse_xmlrpc_response(body)
        return remote_call

def connect(host, port):
    return Connection(host, port)

class Client:
    connect = staticmethod(connect)

