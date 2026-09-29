#!/usr/bin/env python3
"""
Paso 1: solo conectarse al servidor remoto por SFTP y listar los archivos
<PREFIJO>.<PERIODO> que se encuentren en el directorio remoto (no descarga
nada todavía).

Variables de entorno (archivo .env):
    HOST        -> IP o nombre del servidor
    LOGIN       -> usuario
    PASSWORD    -> contraseña
    DIR_REMOTO  -> directorio remoto donde están los archivos

Uso:
    python3 listar_fuentes.py              # usa el período por defecto
    python3 listar_fuentes.py SEPTIEMBRE26 # período por parámetro
"""

import os
import sys

import paramiko
from dotenv import load_dotenv

PREFIJOS = [
    "SUAC1",
    "SUAC1OTROS",
    "TIAC1",
    "TIAC1COMN",
    "TIAC1COMNOTROS",
    "TIAC1OTROS",
]

PERIODO_DEFECTO = "AGOSTO26"


def variables_ambiente():
    load_dotenv()
    HOST = os.getenv("HOST")
    USERNAME = os.getenv("LOGIN")
    PASSWORD = os.getenv("PASSWORD")
    DIR_REMOTO = os.getenv("DIR_REMOTO")

    # No se imprime la contraseña
    print(f"Conexión: {USERNAME}@{HOST}  |  directorio remoto: {DIR_REMOTO}")

    # Validar que todas las variables existan
    if None in [HOST, USERNAME, PASSWORD, DIR_REMOTO]:
        print("Error: Faltan variables de entorno en el archivo .env")
        sys.exit(1)

    return HOST, USERNAME, PASSWORD, DIR_REMOTO


def nombres_archivos(periodo):
    """Genera los nombres PREFIJO.PERIODO."""
    return [f"{prefijo}.{periodo}" for prefijo in PREFIJOS]


def conectar(host, username, password):
    ssh = paramiko.SSHClient()
    # Acepta la clave del host automáticamente (red interna).
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password, timeout=15)
    return ssh


def listar_archivos(host, username, password, dir_remoto, periodo):
    try:
        ssh = conectar(host, username, password)
    except paramiko.AuthenticationException:
        print("Error: autenticación fallida (usuario o contraseña incorrectos).")
        sys.exit(1)
    except Exception as e:
        print(f"Error de conexión: {e}")
        sys.exit(1)

    encontrados, faltantes = [], []

    try:
        sftp = ssh.open_sftp()
        print("Conectado al servidor.\n")

        contenido_remoto = sftp.listdir(dir_remoto)

        for archivo in nombres_archivos(periodo):
            if archivo in contenido_remoto:
                info = sftp.stat(f"{dir_remoto.rstrip('/')}/{archivo}")
                print(f"[OK] {archivo}  ({info.st_size} bytes)")
                encontrados.append(archivo)
            else:
                print(f"[NO] {archivo}: no existe en {dir_remoto}")
                faltantes.append(archivo)

        sftp.close()
    finally:
        ssh.close()

    print("\n--- Resumen ---")
    print(f"Encontrados : {len(encontrados)} {encontrados if encontrados else ''}")
    print(f"Faltantes   : {len(faltantes)} {faltantes if faltantes else ''}")

    return encontrados, faltantes


def main():
    periodo = sys.argv[1].upper() if len(sys.argv) > 1 else PERIODO_DEFECTO
    host, username, password, dir_remoto = variables_ambiente()
    print(f"Período: {periodo}\n")
    listar_archivos(host, username, password, dir_remoto, periodo)


if __name__ == "__main__":
    main()
