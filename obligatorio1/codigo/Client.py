import xmlrpc_redes as xmlrpc

print('Por favor ingrese la IP del servidor: ')
sv_ip = str(input())
print('Por favor ingrese el Puerto del servidor: ')
sv_port = int(input())

conn = xmlrpc.Client.connect(sv_ip, sv_port)
print(f'Conexión establecida con {sv_ip}:{sv_port}')
"""
resultado1 = conn.construirListaEnteros(1, 10)
resultado2 = conn.divisionReales(10, 3.14)
resultado3 = conn.existe([1, 2, 3, '4', 5, 'i'], 'j')
"""
resultado4 = conn.agregrarElemento({'a': 1, 'b': 2}, 'c', 3)
print(resultado4)