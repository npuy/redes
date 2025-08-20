import xmlrpc_redes as xmlrpc

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

def agregrarElemento(m, k, v):
    m[k] = v
    return m

print('Por favor ingrese la IP del servidor: ')
my_ip = str(input())
print('Por favor ingrese el Puerto del servidor: ')
my_port = int(input())

server = xmlrpc.Server((my_ip, my_port))

server.add_method(construirListaEnteros)
server.add_method(divisionReales)
server.add_method(existe)
server.add_method(agregrarElemento)

server.serve()