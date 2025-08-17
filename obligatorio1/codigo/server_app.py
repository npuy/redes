# server1.py
from xmlrpc_redes.server import Server

def suma(a, b): return a + b
def resta(a, b): return a - b
def concat(a, b): return str(a) + str(b)

server = Server(('127.0.0.1', 8000))
server.add_method(suma)
server.add_method(resta)
server.add_method(concat)
server.serve()
