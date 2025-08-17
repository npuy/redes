# client_app.py
from xmlrpc_redes.client import Client

conn = Client.connect('127.0.0.1', 8000)
print("2+3 =", conn.suma(2,3))
print("(-2)+(-3) =", conn.suma(-2,-3))
print("5-1 =", conn.resta(5,1))
print("hola+chau =", conn.concat("hola", "chau"))
print("llamada a método inexistente ->")
print(conn.append([1,"a"],[2,3,4]))
print(conn.append([1,"a"],[]))
print(conn.append([],[]))
print(conn.now())
print(conn.encode("Hola mundo!"))
print(conn.decode(b'SG9sYSBtdW5kbyE='))
print(conn.name({
    "name": "nico",
    "ci": 1234,
    "list": [
        1, 2 ,3
    ]
}))
print(conn.person("nico", 1234))


try:
    print(conn.noexiste(1,2))
except Exception as e:
    print("Error:", e)
