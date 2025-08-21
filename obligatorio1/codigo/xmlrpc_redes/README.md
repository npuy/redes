
`xmlrpc_redes` es una biblioteca de Python que implementa un **sistema de llamadas remotas (RPC) usando XML-RPC sobre HTTP**, utilizando sockets TCP y threads para comunicación cliente-servidor.

- El **cliente** envía llamadas a métodos remotos en forma de XML-RPC a través de HTTP.  
- El **servidor** recibe solicitudes, ejecuta funciones Python registradas y responde con XML-RPC.

Esta biblioteca utiliza las primitivas de la **API de sockets del curso INCO** para TCP, threads y DNS.

---

## 1️⃣ Cliente (`xmlrpc_redes.client`)

### `Client.connect(host, port)`

- Crea un objeto `Connection` que actúa como proxy de métodos remotos.  
- **Primitivas de sockets usadas:**
  - `socket.tcp()` → crea socket TCP master.
  - `connect(host, port)` → establece conexión con servidor.
  - `gethost()` → obtiene IP y puerto locales.

### Llamadas a métodos remotos

`conn.suma(2,3)`

**Flujo interno:**

1. `build_xmlrpc_request()` → construye XML-RPC.
    
2. `build_http_request()` → arma request HTTP con el XML.
    
3. `client.send(request_bytes)` → envía al servidor.
    
4. `client.receive()` → recibe respuesta HTTP/XML.
    
5. `parse_xmlrpc_response()` → obtiene resultado Python o lanza error.

---
## 2️⃣ Servidor (`xmlrpc_redes.server`)

### `Server(address)`

- Crea un socket master TCP y lo vincula a `(host, port)`.
    
- Mantiene un diccionario `self.methods` con funciones registradas.

### `add_method(func)`

- Registra funciones Python como métodos remotos.

### `server()`

- Convierte el socket master en **socket server** y entra en un bucle de aceptación de conexiones.
    
- Cada conexión se maneja en un hilo independiente mediante `thread.new(_handle_connection, conn, addr)`.
    

### `_handle_connection(conn, addr)`

1. `client.receive()` → recibe request HTTP.
    
2. `parse_xmlrpc_request()` → obtiene `method_name` y `params`.
    
3. Ejecuta la función: `result = func(*params)`.
    
4. Construye la respuesta: `build_xmlrpc_response(result)` o `build_xmlrpc_fault(code, msg)` en caso de error.
    
5. Envía la respuesta al cliente: `client.send(response_bytes)`.
    
6. Cierra la conexión: `client.close()`.

## 3️⃣ HTTP y XML-RPC

- `build_http_request(host, port, body_bytes)` → request HTTP POST.
    
- `build_http_response(body_bytes, status, status_text)` → response HTTP.
    
- `parse_xmlrpc_request(body_bytes)` → extrae método y parámetros.
    
- `parse_xmlrpc_response(body_bytes)` → obtiene resultado Python o lanza excepción.
    
- `build_xmlrpc_request(method_name, params)` → genera XML-RPC request.
    
- `build_xmlrpc_response(result)` → genera XML-RPC response.
    
- `build_xmlrpc_fault(code, message)` → genera fault XML-RPC en caso de error.

## 4️⃣ Concurrencia

Cada conexión se maneja en un **hilo independiente** para permitir que el servidor atienda múltiples clientes concurrentemente.

## 5️⃣ Cierre de Recursos

- **Cliente:** `client.close()`
    
- **Servidor:** `server.close()`
    

Libera los puertos y la memoria asociados al socket.


## 6️⃣ Flujo de Comunicación Cliente ↔ Servidor

|Cliente Python|Flujo|Servidor Python|
|:--|:-:|:--|
|`conn.metodo(args)`|-------->|recibe request HTTP/XML|
|`build_xmlrpc_request()`||`parse_xmlrpc_request()`|
|`build_http_request()`||busca función en `self.methods`|
|`client.send()`||ejecuta función Python|
|`client.receive()`|<--------|`build_xmlrpc_response()` o `build_xmlrpc_fault()`|
|`parse_xmlrpc_response()`||`build_http_response()`|
|retorna resultado Python|<------|`client.send()`|
- El cliente ve solo llamadas a métodos Python.
    
- El servidor recibe bytes, ejecuta funciones y devuelve XML-RPC.

## 7️⃣ Ejemplo de Uso

# Servidor
```python
from xmlrpc_redes.server import Server

def suma(a, b):
    return a + b

server = Server(('127.0.0.1', 8000))
server.add_method(suma)
server.serve()

```

# Client

```python
from xmlrpc_redes.client import Client

conn = Client.connect('127.0.0.1', 8000)
print(conn.suma(2, 3))

```

## 8️⃣ Referencias

- **API de sockets utilizada:** INCO - Redes de Computadoras API de Sockets 2.0
    
- Basado en **XML-RPC** y **HTTP/1.1**