import socket
import threading

localHost = 'localhost'

def forward(connFrom: socket.socket, connTo: socket.socket):
    try:
        while True:
            data = connFrom.recv(2048)
            while data:
                bytesSent = connTo.send(data)
                data = data[bytesSent:]
    finally:
        connFrom.close()
        connTo.close()

def handle_connection(conn: socket.socket, destinationHost: str, destinationPort: int):
    connDest = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connDest.connect((destinationHost, destinationPort))
    t1 = threading.Thread(
        target=forward,
        args=(conn, connDest)
    )
    t2 = threading.Thread(
        target=forward,
        args=(connDest, conn)
    )
    t1.start()
    t2.start()

def redirect(localPort: int, destinationHost: str, destinationPort: int):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((localHost, localPort))
    s.listen()
    print(f"Server listening on {localHost}:{localPort}")
    while True:
        conn, addr = s.accept()
        t = threading.Thread(
            target=handle_connection, 
            args=(conn, destinationHost, destinationPort), 
            daemon=True
        )
        t.start()

redirect(8080, 'localhost', 8000)