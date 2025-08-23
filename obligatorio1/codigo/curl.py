#!/usr/bin/env python3
import subprocess

# Comando curl como si lo ejecutarás en terminal
curl_command = [
        "curl",
        "-X", "POST",
        "-H", "Content-Type: text/xml",
        "-H", "User-Agent: MiCliente/1.0",        
        "-H", "Content-Length: 1",
        "-H", "Host: 127.0.0.1:5000",
        "-d", '{"mensaje":"Hola servidor"}',
        "127.0.0.1:5000"
]

try:
    # Ejecuta curl y captura la salida
    result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
    print("Salida del comando:")
    print(result.stdout)
    print("Errores (si los hay):")
    print(result.stderr)
except subprocess.CalledProcessError as e:
    print("El comando falló con código:", e.returncode)
    print("Salida:", e.output)
