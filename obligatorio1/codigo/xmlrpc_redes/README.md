Documentación de la biblioteca XML-RPC sobre TCP/HTTP

-------------------------------------------------------------------------------------------------------------------------

1. Introducción

Esta biblioteca implementa un sistema de llamadas a procedimientos remotos (RPC) usando 
el protocolo XML-RPC transmitido sobre HTTP/TCP.
Permite que un cliente invoque métodos en un servidor remoto como si fueran funciones locales, 
utilizando XML para serializar los parámetros y resultados.

-------------------------------------------------------------------------------------------------------------------------

2. Estructura de módulos

client.py:
Maneja la conexión del cliente con el servidor. Se encarga de construir requests XML-RPC, enviarlos mediante TCP, recibir la respuesta HTTP y procesarla.

server.py
Implementa el servidor XML-RPC capaz de recibir y procesar llamadas remotas:

-Escucha conexiones TCP en un host y puerto.
-Procesa requests HTTP entrantes que contengan XML-RPC.
-Valida protocolo, método HTTP, encabezados y formato del body.
-Ejecuta el método invocado si está registrado.
-Devuelve una respuesta XML-RPC (con éxito o error).
-Maneja múltiples clientes concurrentemente usando threading.

xml.py
Módulo de utilidades XML-RPC: parsea requests y responses, construye elementos XML a partir de valores Python, y genera fallos (errores) en caso de excepción.

http.py
Este módulo se encarga de construir y parsear mensajes HTTP que transportan XML-RPC sobre TCP.
Permite al cliente y al servidor contruir y recibir requests/responses HTTP correctamente formateados, incluyendo cabeceras y body XML.

tcp.py
Este módulo implementa operaciones de envío y recepción de datos sobre sockets TCP de manera confiable, usadas por el cliente y el servidor para transportar requests/responses HTTP/XML-RPC.

-------------------------------------------------------------------------------------------------------------------------

3. Documentación detallada de clases y funciones

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

Clase Client

Client es una interfaz de alto nivel para conectarse a un servidor XML-RPC.
Permite crear una conexión con el método estático connect(host, port) y luego invocar métodos remotos como si fueran locales:

conn = Client.connect("127.0.0.1", 8080)
resultado = conn.sumar(5, 7)
print(resultado)  # 12

Objetivo: simplificar la creación de conexiones y la invocación de métodos remotos.

Nota: Internamente usa la clase Connection para manejar TCP, HTTP y XML-RPC.

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

Clase Server

Server implementa un servidor XML-RPC sobre TCP/HTTP.
Permite registrar funciones que pueden ser invocadas remotamente por clientes.

Constructor
    Server(address)
    -address → tupla (host, port) donde el servidor escuchará conexiones.
    -Inicializa un diccionario methods para almacenar las funciones registradas.

add_method(func)
    -Registra una función func para que pueda ser llamada remotamente.
    -La clave del diccionario methods es el nombre de la función.

_handle_connection(conn, addr)
    -Maneja una conexión individual en un hilo.
    -Valida el request HTTP y XML-RPC.
    -Ejecuta la función correspondiente si existe y devuelve la respuesta XML-RPC.
    -Envía errores como fault XML-RPC en caso de problemas de protocolo, headers, parseo o ejecución de la función.

serve()
    -Inicia el servidor escuchando en el host y puerto especificados.
    -Acepta conexiones entrantes y crea un hilo separado para cada cliente.
    -Permite atender múltiples clientes simultáneamente.

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

Clase tcp

Proporciona funciones para enviar y recibir datos sobre sockets TCP de forma confiable, usadas tanto por el cliente como por el servidor para transportar requests y responses HTTP/XML-RPC.

send(conn, data)
    -Envía todos los bytes de data a través del socket conn.
    -Codifica strings a bytes si es necesario.
    -Asegura que se envíen todos los bytes, incluso si conn.send envía parcialmente.
    -Relanza cualquier excepción para que el llamador la maneje.

receive(conn)
    -Recibe datos desde un socket conn hasta completar cabeceras y body HTTP.
    -Detecta el fin de cabecera con \r\n\r\n.
    -Extrae la start line, los headers en un diccionario y el body según Content-Length.
    Devuelve: start_line_first, start_line_second, start_line_third, headers, body

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

Clase http.py

Proporciona funciones para construir y parsear requests y responses HTTP que transportan mensajes XML-RPC sobre TCP.

get_http_request(conn)
    -Lee un request HTTP desde el socket conn.
    -Devuelve (method, path, proto, headers, body).

get_http_response(conn)
    -Lee una respuesta HTTP desde el socket conn.
    -Devuelve (proto, status_code, status_message, headers, body).

build_http_request(host, port, body_bytes)
    -Construye un request HTTP POST válido para XML-RPC.
    -Incluye cabeceras: Host, User-Agent, Content-Type y Content-Length.
    Devuelve los bytes listos para enviar por TCP.

build_http_response(body_bytes, status=200, status_text='OK')
    -Construye una respuesta HTTP para XML-RPC con un código de estado opcional.
    -Incluye cabeceras estándar y el cuerpo en bytes.


//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

Clase XML

Proporciona funciones auxiliares para construir y parsear mensajes XML-RPC, usadas tanto por el cliente como por el servidor.

parse_value(elem)
    -Convierte un nodo <value> de XML-RPC a su tipo Python correspondiente: int, float, bool, str, list, dict, datetime, bytes.

build_value_element(pyval)
    Convierte un valor Python en un nodo <value> XML-RPC adecuado.

parse_xmlrpc_request(body_bytes)
    Dado un request XML-RPC en bytes, devuelve (method_name, params).

build_xmlrpc_request(method_name, params)
    Construye un request XML-RPC válido a partir de un nombre de método y parámetros.

parse_xmlrpc_response(body_bytes)
    Procesa una respuesta XML-RPC.
    Si es fault → lanza Exception con código y mensaje.
    Si es éxito → devuelve el valor retornado por el método remoto.

build_xmlrpc_response(result)
    Construye un response XML-RPC exitoso con el resultado.

build_xmlrpc_fault(code, message)
    Construye un response XML-RPC con error (fault).

-------------------------------------------------------------------------------------------------------------------------

4. Ejemplo de uso

Servidor:

from biblioteca.server import Server

# Función remota que podrá ser llamada por el cliente
def sumar(x, y):
    return x + y

# Inicializo el servidor en localhost puerto 8080
srv = Server(("127.0.0.1", 8080))

# Registro la función para que sea invocable por XML-RPC
srv.add_method(sumar)

# Inicio el servidor de forma bloqueante y concurrente
srv.serve()

//////////////////////////////////////////////////////

Cliente:

from biblioteca.client import Client

# Conexión al servidor
conn = Client.connect("127.0.0.1", 8080)

# Llamada remota a la función "sumar"
resultado = conn.sumar(5, 7)

print(resultado)  # 12
----------------------------------------------------------------------------------------------------------------------------------
5. Manejo de errores

Errores de red: problemas en la conexión TCP (servidor caído, timeout) se detectan en tcp.py y 
connection.py y se propagan al cliente como excepciones.

Errores de servidor: llamadas a métodos inexistentes o fallas durante su ejecución 
son capturadas por server.py y devueltas como fault XML-RPC mediante xml.py. 
El cliente los recibe y lanza excepciones con el código y mensaje correspondiente.

Errores de parseo XML: XML mal formado se detecta en xml.py y se lanza una excepción inmediata en el cliente.

Errores HTTP/protocolo: requests con método incorrecto, headers faltantes o versión HTTP no soportada 
son detectados por server.py y convertidos en fault XML-RPC.
----------------------------------------------------------------------------------------------------------------------------------


