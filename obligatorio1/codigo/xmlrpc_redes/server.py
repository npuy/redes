import socket
import threading
from . import protocol

class Server:
    def __init__(self, address):
        self.host, self.port = address
        self.methods = {}

    def add_method(self, func):
        self.methods[func.__name__] = func

    def _handle_connection(self, conn, addr):
        try:
            data = b''
            while b'\r\n\r\n' not in data:
                chunk = conn.recv(4096)
                if not chunk: return
                data += chunk
            method, path, proto, headers, body = protocol.parse_http_request(data)
            cl = int(headers.get('content-length', '0'))
            while len(body) < cl:
                body += conn.recv(cl - len(body))

            if method != 'POST':
                conn.sendall(protocol.build_http_response(b'Method Not Allowed', 405, 'Method Not Allowed'))
                return

            try:
                method_name, params = protocol.parse_xmlrpc_request(body)
            except Exception as e:
                resp = protocol.build_xmlrpc_fault(400, f'Invalid XML: {e}')
                conn.sendall(protocol.build_http_response(resp))
                return

            func = self.methods.get(method_name)
            if func is None:
                resp = protocol.build_xmlrpc_fault(1, f'Method {method_name} not found')
                conn.sendall(protocol.build_http_response(resp))
                return

            try:
                result = func(*params)
                resp = protocol.build_xmlrpc_response(result)
            except Exception as e:
                resp = protocol.build_xmlrpc_fault(2, f'Execution error: {e}')

            conn.sendall(protocol.build_http_response(resp))
        finally:
            conn.close()

    def serve(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(5)
        print(f"XMLRPC Server listening on {self.host}:{self.port}")
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=self._handle_connection, args=(conn, addr), daemon=True)
            t.start()
