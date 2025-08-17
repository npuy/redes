# client_app.py
from xmlrpc_redes.client import Client

conn = Client.connect('127.0.0.1', 8000)
print("2+3 =", conn.suma(2,3))
print("5-1 =", conn.resta(5,1))
print("hola+chau =", conn.concat("hola", "chau"))
print("llamada a método inexistente ->")
try:
    print(conn.noexiste(1,2))
except Exception as e:
    print("Error:", e)
