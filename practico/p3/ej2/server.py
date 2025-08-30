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
        data = data + conn.recv(2048)
    return data

def send_msg(conn: socket.socket, msg: bytes):
    while msg:
        bytes_sent = conn.send(msg)
        msg = msg[bytes_sent:]


HOST = ''
PORT = 8081
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen()
while True:
    conn, addr = s.accept()
    print("Addr: ", addr)
    end = False
    while not end:
        msg = receive_msg(conn)
        print("Msg: ", msg)
        if b'ECHO: ' in msg:
            txt = msg.removeprefix(b'ECHO: ')
            print("Txt: ", txt)
            send_msg(conn, txt)
        elif msg == b'EXIT\n':
            msg_to_send = b'CLOSE '
            client_ip = conn.getpeername()[0]
            msg_to_send += client_ip.encode()
            msg_to_send += b'\n'
            print('Msg to send: ', msg_to_send)
            send_msg(conn, msg_to_send)
            conn.close()
            end = True

    conn.close()
