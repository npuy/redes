# server1.py
import base64
from xmlrpc_redes.server import Server
import datetime as dt

def suma(a, b): return a + b
def resta(a, b): return a - b
def concat(a, b): return str(a) + str(b)
def append(l1, l2): return l1 + l2
def now(): return dt.datetime.now()
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
def name(data: dict): return data.get("name")
def person(name, ci): return {"name": name, "ci":ci, "list": [1,2,3]}

print(name({
    "name": "nico",
    "ci": 1234,
    "list": [
        1, 2 ,3
    ]
}))
print(person("nico", 1234))

server = Server(('127.0.0.1', 8000))
server.add_method(suma)
server.add_method(resta)
server.add_method(concat)
server.add_method(append)
server.add_method(now)
server.add_method(encode)
server.add_method(decode)
server.add_method(name)
server.add_method(person)
server.serve()
