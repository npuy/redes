from . import tcp

def get_http_request(conn):
    # Lee un request HTTP desde el socket y devuelve start line, headers y body
    method, path, proto, headers, body = tcp.receive(conn)
    return method, path, proto, headers, body

def get_http_response(conn):
    # Lee una respuesta HTTP desde el socket y devuelve start line, headers y body
    proto, status_code, status_message, headers, body = tcp.receive(conn)
    return proto, status_code, status_message, headers, body

def build_http_request(host, port, body_bytes):
    # Construye un request HTTP POST para XML-RPC
    req = (
        f"POST /RPC2 HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        f"User-Agent: MiClienteXMLRPC/1.0\r\n"
        f"Content-Type: text/xml\r\n"
        f"Content-Length: {len(body_bytes)}\r\n\r\n"
    ).encode('utf-8')
    return req + body_bytes

def build_http_response(body_bytes, status=200, status_text='OK'):
    # Construye una respuesta HTTP para XML-RPC
    h = f'HTTP/1.1 {status} {status_text}\r\nContent-Length: {len(body_bytes)}\r\nContent-Type: text/xml\r\n\r\n'
    return h.encode() + body_bytes