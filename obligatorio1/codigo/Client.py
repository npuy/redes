import xmlrpc_redes as xmlrpc
import datetime

print('Por favor ingrese la IP del servidor1: ')
sv1_ip = str(input())
print('Por favor ingrese el Puerto del servidor1: ')
sv1_port = int(input())

conn1 = xmlrpc.Client.connect(sv1_ip, int(sv1_port))
print(f'Conexión establecida con {sv1_ip}:{sv1_port}')

print('Por favor ingrese la IP del servidor2: ')
sv2_ip = str(input())
print('Por favor ingrese el Puerto del servidor2: ')
sv2_port = int(input())

conn2 = xmlrpc.Client.connect(sv2_ip, int(sv2_port))
print(f'Conexión establecida con {sv2_ip}:{sv2_port}')
print()

resultado1 = conn1.construirFloat(3, 14)
resultado2 = conn1.divisionReales(10, 3.14)
resultado3 = conn1.fechaHora(24, 9, 2025, 8, 30, 0)
resultado4 = conn1.xor(True, True)
resultado5 = conn1.dias(datetime.datetime(2024, 1, 1), datetime.datetime(2025, 1, 1))

print('Resultados funciones Servidor1: ')
print(f'construirFloat(3, 14) = {resultado1}')
print(f'divisionReales(10, 3.14) = {resultado2}')
print(f'fechaHora(24, 9, 2025, 8, 30, 0) = {resultado3}')
print(f'xor(True, True) = {resultado4}')
print(f'dias(datetime.datetime(2024, 1, 1), datetime.datetime(2025, 1, 1)) = {resultado5}')
print()

resultado6 = conn2.listsToMap(['a','b','c'],[1, 2]) # LAS CLAVES EN UN DICCIONARIO DE XLRPC DEBEN SER STRINGS
resultado7 = conn2.concatStrings('hello', 'world', '!', '!', '!')
resultado8 = conn2.existe([1, 2, 3, '4', 5, 'i'], 'j')
resultado9 = conn2.agregarElemento({'a': 1, 'b': 2}, 'c', 3)
resultado10 = conn2.construirListaEnteros(1, 10)
resultado11 = conn2.encode('Hello world!')
resultado12 = conn2.decode(b'SG9sYSBtdW5kbyE=')

print('Resultados funciones Servidor2: ')
print(f'listsToMap(["a","b","c"],[1, 2]) = {resultado6}')
print(f'concatStrings("hello", "world", "!", "!", "!") = {resultado7}')
print(f'existe([1, 2, 3, "4", 5, "i"], "j") = {resultado8}')
print(f'agregarElemento({{"a": 1, "b": 2}}, "c", 3) = {resultado9}')
print(f'construirListaEnteros(1, 10) = {resultado10}')
print(f'encode("Hello world!") = {resultado11}')
print(f'decode(b"SG9sYSBtdW5kbyE=") = {resultado12}')