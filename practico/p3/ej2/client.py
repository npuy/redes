# Ejercicio 2 Se desea implementar una aplicación con una arquitectura cliente-servidor de intercambio de
# mensajes que cumpla con las siguientes características:
# • El servidor espera conexiones TCP en todas sus interfaces en el puerto 8081.
# • Los clientes envían dos tipos de mensajes:
# 1. ECHO: texto\n
# 2. EXIT\n
# • Al recibir un mensaje de tipo ECHO el servidor debe contestar al cliente con texto.
# • Al recibir un mensaje de tipo EXIT el servidor deberá contestarle “CLOSE ip_cliente” donde
# ip_cliente es la dirección IP del cliente que envió el comando y cerrar la conexión con dicho
# cliente.
# Se pide:
# (a) Implemente en un lenguaje de alto nivel, utilizando las primitivas de la API de sockets del curso,
# el programa que ejecuta el servidor.
# (b) Implemente en un lenguaje de alto nivel, utilizando las primitivas de la API de sockets del curso,
# el programa que ejecuta un cliente que envía los mensajes 1 y 2.

import socket

def receive_msg(conn: socket.socket):
    data = b''
    while b'\n' not in data:
        print(data)
        data = data + conn.recv(2048)
    return data

def send_msg(conn: socket.socket, msg: bytes):
    while msg:
        bytes_sent = conn.send(msg)
        msg = msg[bytes_sent:]

HOST = 'localhost'
PORT = 8081
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((HOST, PORT))
send_msg(conn, b'ECHO: hola\n')
msg = receive_msg(conn)
print("Msg: ", msg)
send_msg(conn, b'EXIT\n')
msg = receive_msg(conn)
print("Msg: ", msg)
