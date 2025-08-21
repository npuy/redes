import socket
import threading
from . import xml
from . import http

class Server:
    def __init__(self, address):
        self.host, self.port = address
        self.methods = {} #diccionario para guardar métodos registrados

    def add_method(self, func):
        self.methods[func.__name__] = func

    def _handle_connection(self, conn, addr):
        try:
            method, path, proto, headers, body = http.get_http_request(conn)

            if method != 'POST':
                conn.sendall(http.build_http_response(b'Method Not Allowed', 405, 'Method Not Allowed'))
                return

            try:
                method_name, params = xml.parse_xmlrpc_request(body)
            except Exception as e:
                resp = xml.build_xmlrpc_fault(1, f'Error parseo de XML: {e}')
                conn.sendall(http.build_http_response(resp))
                return

            func = self.methods.get(method_name)
            if func is None:
                resp = xml.build_xmlrpc_fault(2, f'No existe el método invocado: Método {method_name}')
                conn.sendall(http.build_http_response(resp))
                return

            try:
                result = func(*params)
                resp = xml.build_xmlrpc_response(result)
            except TypeError as e:
                resp = xml.build_xmlrpc_fault(3, f'Error en parámetros del método invocado: {e}')
            except Exception as e:
                resp = xml.build_xmlrpc_fault(4, f'Error interno en la ejecución del método: {e}')
        except Exception as e:
            resp = xml.build_xmlrpc_fault(5, f'Error inesperado en el servidor: {e}')
        finally:
            try:
                conn.sendall(http.build_http_response(resp))
            finally:
                conn.close()

    def serve(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Crear un socket TCP
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #permite reutilizar la dir y puerto sin esperar a que se libere
        s.bind((self.host, self.port))  #asocia socket a (IP-PUERTO)
        s.listen(5)
        print(f"XMLRPC Server listening on {self.host}:{self.port}")
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=self._handle_connection, # función que atiende al cliente
                                 args=(conn, addr),              # socket y dirección del cliente   
                                 daemon=True)                    # el hilo se cierra automáticamente al terminar el programa
            # Arranca el hilo que procesa la conexión
            t.start() 
