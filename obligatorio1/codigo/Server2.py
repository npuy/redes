import xmlrpc_redes as xmlrpc
import datetime

def listsToMap(l1, l2):
    m = {}
    i = 0
    j = 0
    while i < len(l1) and j < len(l2):
        m[l1[i]] = l2[j]
        i += 1
        j += 1
    return m

""""
print('Por favor ingrese la IP del servidor: ')
my_ip = str(input())
print('Por favor ingrese el Puerto del servidor: ')
my_port = int(input())
"""
server = xmlrpc.Server(("127.0.0.1", 8000))

server.add_method(listsToMap)

server.serve()