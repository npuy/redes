# ---------- HTTP helpers ----------

def get_http(conn):
    data = b''
    while b'\r\n\r\n' not in data:
        chunk = conn.recv(4096)
        if not chunk: return # TODO: Es esto necesario en cliente y servidor?
        data += chunk

    sep = b'\r\n\r\n'
    head, body = data.split(sep, 1) if sep in data else (data, b'')
    lines = head.decode().split('\r\n')
    start_line = lines[0]
    start_line_first, start_line_second, start_line_third = start_line.split(' ', 2)

    headers = {}
    for line in lines[1:]:
        if not line: continue
        k, v = line.split(':', 1)
        headers[k.strip().lower()] = v.strip()

    cl = int(headers.get('content-length', '0'))
    while len(body) < cl:
        body += conn.recv(cl - len(body))

    return start_line_first, start_line_second, start_line_third, headers, body

def get_http_request(conn):
    method, path, proto, headers, body = get_http(conn)
    return method, path, proto, headers, body

def get_http_response(conn):
    proto, status_code, status_message, headers, body = get_http(conn)
    return proto, status_code, status_message, headers, body

def build_http_request(host, port, body_bytes):
    req = f"POST /RPC2 HTTP/1.1\r\nHost: {host}:{port}\r\nContent-Type: text/xml\r\nContent-Length: {len(body_bytes)}\r\n\r\n".encode()
    return req + body_bytes

def build_http_response(body_bytes, status=200, status_text='OK'):
    h = f'HTTP/1.1 {status} {status_text}\r\nContent-Length: {len(body_bytes)}\r\nContent-Type: text/xml\r\n\r\n'
    return h.encode() + body_bytes