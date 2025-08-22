import xmlrpc_redes as xmlrpc
import datetime

def construirFloat(a, b):
    aux = f'{a}.{b}'
    return float(aux)

def divisionReales(a, b):
    return a/b

def fechaHora(d, m, a, hh, mm, ss):
    return datetime.datetime(a, m, d, hh, mm, ss)

def xor(a, b):
    return not ((a and b) or (not a and not b))

def dias(f1, f2):
    return abs((f1-f2).days)


print('Por favor ingrese la IP para el servidor1: ')
my_ip = str(input())
print('Por favor ingrese el Puerto para el servidor1: ')
my_port = int(input())

server = xmlrpc.Server((my_ip, int(my_port)))

server.add_method(construirFloat)
server.add_method(divisionReales)
server.add_method(fechaHora)
server.add_method(xor)
server.add_method(dias)

server.serve()