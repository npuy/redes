import xmlrpc_redes as xmlrpc
import base64

def listsToMap(l1, l2):
    m = {}
    i = 0
    j = 0
    while i < len(l1) and j < len(l2):
        m[l1[i]] = l2[j]
        i += 1
        j += 1
    return m

def concatStrings(*args):
    res = f''
    for s in args:
        res = res + s
    return res

def existe(l, x):
    for i in l:
        if i == x:
            return True
    return False

def agregarElemento(m, k, v):
    m[k] = v
    return m

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

def decode(data: bytes) -> str:
    # Convertimos el string a bytes
    data_bytes = data
    # Decodificamos base64
    decoded_bytes = base64.b64decode(data_bytes)
    # Convertimos los bytes decodificados a string
    return decoded_bytes.decode("utf-8")

def encode(data: str) -> bytes:
    # Convertimos el string a bytes
    data_bytes = data.encode("utf-8")
    # Codificamos en base64
    encoded_bytes = base64.b64encode(data_bytes)
    # Convertimos los bytes codificados a string
    return encoded_bytes

print('Por favor ingrese la IP para el servidor2: ')
my_ip = str(input())
print('Por favor ingrese el Puerto para el servidor2: ')
my_port = int(input())

server = xmlrpc.Server((my_ip, int(my_port)))

server.add_method(listsToMap)
server.add_method(concatStrings)
server.add_method(existe)
server.add_method(agregarElemento)
server.add_method(construirListaEnteros)
server.add_method(encode)
server.add_method(decode)


server.serve()