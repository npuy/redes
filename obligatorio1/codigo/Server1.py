import xmlrpc_redes as xmlrpc
import datetime

def construirListaEnteros(a, b):
    lista = []
    if a < b:
        for i in range(a, b, 1):
            lista.append(i)
        lista.append(b)
    else:
        for i in range(a, b, -1):
            lista.append(i)
        lista.append(b)
    return lista

def divisionReales(a, b):
    return a/b

def existe(l, x):
    for i in l:
        if i == x:
            return True
    return False

def agregarElemento(m, k, v):
    m[k] = v
    return m

def fechaHora(d, m, a, hh, mm, ss):
    return datetime.datetime(a, m, d, hh, mm, ss)

""""
print('Por favor ingrese la IP del servidor: ')
my_ip = str(input())
print('Por favor ingrese el Puerto del servidor: ')
my_port = int(input())
"""
server = xmlrpc.Server(("127.0.0.1", 8000))

server.add_method(construirListaEnteros)
server.add_method(divisionReales)
server.add_method(existe)
server.add_method(agregrarElemento)
server.add_method(fechaHora)

server.serve()