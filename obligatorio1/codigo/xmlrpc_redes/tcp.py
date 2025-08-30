def send(conn, data):
    try:
        if not isinstance(data, bytes):
            data = data.encode('utf-8')

        bytes_sent = conn.send(data)
        data = data[bytes_sent:]
        while data != b'':
            bytes_sent = conn.send(data)
            data = data[bytes_sent:]
    except Exception as e:
        print(f'Error al enviar paquete -> {e}')
        raise  # relanzo la excepción para que el cliente la maneje

def receive(conn):
    conn.settimeout(10)  # 10 segundos máximo por operación de recv/send - LO DIMOS EN LA CARTILLA
    data = b''
    while b'\r\n\r\n' not in data:
        chunk = conn.recv(2048)
        if not chunk: 
            return
        data = data + chunk

    sep = b'\r\n\r\n'
    #EN EL ULTIMO CHUNK TE PUEDE VENIR BYTES DEL BODY
    #head, body = data.split(sep, 1) if sep in data else (data, b'')
    head, body = data.split(sep, 1)
    lines = head.decode().split('\r\n')
    #TOMAMOS EL PRIMER HEADER Y NOS QUEDAMOS CON LOS 3 VALORES TIPICOS (POST /RPC2 HTTP/1.0)
    start_line = lines[0]
    start_line_first, start_line_second, start_line_third = start_line.split(' ', 2)

    headers = {}
    for line in lines[1:]:
        if not line: continue # ver si sacar
        k, v = line.split(':', 1)
        headers[k.strip().lower()] = v.strip() #elimina espacios vacios y pone todo en minusculas

    #print(headers)

    size = int(headers.get('content-length', '0')) #devuelve 0 si no encuentra la clave content-length
    while len(body) < size:
        chunk = conn.recv(2048)
        if not chunk: 
            return
        body = body + chunk

    return start_line_first, start_line_second, start_line_third, headers, body