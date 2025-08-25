import socket
import threading
from . import xml
from . import http
from . import tcp

class Server:
    def __init__(self, address):
        self.host, self.port = address
        self.methods = {}

    def add_method(self, func):
        self.methods[func.__name__] = func 
            
    def _handle_connection(self, conn, addr):

        conn.settimeout(10)  # 10 segundos máximo por operación de recv/send - LO DIMOS EN LA CARTILLA

        # Inicializo resp como bytes
        resp = xml.build_xmlrpc_fault(1, "Error interno")

        try:
            method, path, proto, headers, body = http.get_http_request(conn)

            if proto != 'HTTP/1.1':
                resp = xml.build_xmlrpc_fault(1, "Protocolo no soportado: use HTTP/1.1")
                tcp.send(conn, http.build_http_response(resp, 505, 'HTTP Version Not Supported'))
                return

            if method != 'POST':
                resp = xml.build_xmlrpc_fault(1, "Método no permitido: use POST")
                tcp.send(conn, http.build_http_response(resp, 405, 'Method Not Allowed'))
                return
            
            if headers.get('content-type') != 'text/xml':
                resp = xml.build_xmlrpc_fault(2, "Content-Type debe ser text/xml")
                tcp.send(conn, http.build_http_response(resp, 422, 'Unprocessable Entity'))
                return
            
            if 'user-agent' not in headers:
                resp = xml.build_xmlrpc_fault(3, "User-Agent requerido")
                tcp.send(conn, http.build_http_response(resp, 403, 'Forbidden'))
                return

            if headers.get('host') != f'{self.host}:{self.port}':
                resp = xml.build_xmlrpc_fault(4, "Host incorrecto")
                tcp.send(conn, http.build_http_response(resp, 400, 'Bad Request'))
                return
            
            if 'content-length' not in headers:
                resp = xml.build_xmlrpc_fault(5, "Content-Length requerido")
                tcp.send(conn, http.build_http_response(resp, 411, 'Length Required'))
                return
            
            try:
                method_name, params = xml.parse_xmlrpc_request(body)
            except Exception as e:
                resp = xml.build_xmlrpc_fault(6, f'Error parseo de XML: {e}')
                tcp.send(conn, http.build_http_response(resp))
                return

            func = self.methods.get(method_name)
            if func is None:
                resp = xml.build_xmlrpc_fault(7, f'No existe el método invocado: {method_name}')
                tcp.send(conn, http.build_http_response(resp))
                return

            try:
                result = func(*params)
                resp = xml.build_xmlrpc_response(result)
            except TypeError as e:
                resp = xml.build_xmlrpc_fault(8, f'Error en parámetros del método: {e}')
            except Exception as e:
                resp = xml.build_xmlrpc_fault(9, f'Error interno en la ejecución del método: {e}')

        except Exception as e:
            resp = xml.build_xmlrpc_fault(10, f'Error inesperado en el servidor: {e}')
        finally:
            tcp.send(conn, http.build_http_response(resp))
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
