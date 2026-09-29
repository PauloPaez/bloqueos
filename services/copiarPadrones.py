#!/usr/bin/env python3
"""
Se conecta al servidor remoto por SFTP, verifica cuáles de los archivos
<PREFIJO>.<PERIODO> existen en el directorio remoto y copia los que
encuentra al directorio local "fuentes".

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

PERIODO_DEFECTO = "SETIEMBRE26"
DIR_LOCAL = "fuentes"


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


def listar_y_descargar(host, username, password, dir_remoto, periodo):
    try:
        ssh = conectar(host, username, password)
    except paramiko.AuthenticationException:
        print("Error: autenticación fallida (usuario o contraseña incorrectos).")
        sys.exit(1)
    except Exception as e:
        print(f"Error de conexión: {e}")
        sys.exit(1)

    descargados, faltantes, con_error = [], [], []

    try:
        sftp = ssh.open_sftp()
        print("Conectado al servidor.\n")

        contenido_remoto = sftp.listdir(dir_remoto)
        os.makedirs(DIR_LOCAL, exist_ok=True)

        for archivo in nombres_archivos(periodo):
            ruta_remota = f"{dir_remoto.rstrip('/')}/{archivo}"
            ruta_local = os.path.join(DIR_LOCAL, archivo)

            if archivo not in contenido_remoto:
                print(f"[NO] {archivo}: no existe en {dir_remoto}")
                faltantes.append(archivo)
                continue

            try:
                info = sftp.stat(ruta_remota)
                sftp.get(ruta_remota, ruta_local)
                print(f"[OK] {archivo} ({info.st_size} bytes) -> {ruta_local}")
                descargados.append(archivo)
            except Exception as e:
                print(f"[ERROR] {archivo}: {e}")
                con_error.append(archivo)

        sftp.close()
    finally:
        ssh.close()

    print("\n--- Resumen ---")
    print(f"Descargados : {len(descargados)} {descargados if descargados else ''}")
    print(f"Faltantes   : {len(faltantes)} {faltantes if faltantes else ''}")
    print(f"Con error   : {len(con_error)} {con_error if con_error else ''}")

    return descargados, faltantes, con_error


def main():
    periodo = sys.argv[1].upper() if len(sys.argv) > 1 else PERIODO_DEFECTO
    host, username, password, dir_remoto = variables_ambiente()
    print(f"Período: {periodo}\n")
    listar_y_descargar(host, username, password, dir_remoto, periodo)


if __name__ == "__main__":
    main()
