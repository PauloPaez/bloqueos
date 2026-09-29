#!/usr/bin/env python3
"""
Descarga por SFTP (paramiko) los archivos <PREFIJO>.<PERIODO> desde un
servidor remoto hacia el directorio local "fuentes".

Variables de entorno (archivo .env):
    HOST        -> IP o nombre del servidor
    LOGIN       -> usuario
    PASSWORD    -> contraseña
    DIR_REMOTO  -> directorio remoto donde están los archivos

Uso:
    python3 descargar_fuentes.py              # usa el período por defecto
    python3 descargar_fuentes.py SEPTIEMBRE26 # período por parámetro
"""

import os
import sys
import stat

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


def descargar_archivos(host, username, password, dir_remoto, periodo):
    os.makedirs(DIR_LOCAL, exist_ok=True)

    ssh = paramiko.SSHClient()
    # Acepta la clave del host automáticamente (red interna).
    # Para mayor seguridad, cargar known_hosts y usar RejectPolicy.
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    descargados, faltantes, con_error = [], [], []

    try:
        ssh.connect(host, username=username, password=password, timeout=15)
        sftp = ssh.open_sftp()
        print("Conectado al servidor.\n")

        for archivo in nombres_archivos(periodo):
            ruta_remota = f"{dir_remoto.rstrip('/')}/{archivo}"
            ruta_local = os.path.join(DIR_LOCAL, archivo)

            try:
                info = sftp.stat(ruta_remota)
                if stat.S_ISDIR(info.st_mode):
                    print(f"[--] {archivo}: es un directorio, se omite")
                    con_error.append(archivo)
                    continue

                sftp.get(ruta_remota, ruta_local)
                print(f"[OK] {archivo} ({info.st_size} bytes) -> {ruta_local}")
                descargados.append(archivo)

            except FileNotFoundError:
                print(f"[NO] {archivo}: no existe en {dir_remoto}")
                faltantes.append(archivo)
            except Exception as e:
                print(f"[ERROR] {archivo}: {e}")
                con_error.append(archivo)

        sftp.close()

    except paramiko.AuthenticationException:
        print("Error: autenticación fallida (usuario o contraseña incorrectos).")
        sys.exit(1)
    except Exception as e:
        print(f"Error de conexión: {e}")
        sys.exit(1)
    finally:
        ssh.close()

    print("\n--- Resumen ---")
    print(f"Descargados : {len(descargados)}")
    print(f"No existen  : {len(faltantes)} {faltantes if faltantes else ''}")
    print(f"Con error   : {len(con_error)} {con_error if con_error else ''}")


def main():
    periodo = sys.argv[1].upper() if len(sys.argv) > 1 else PERIODO_DEFECTO
    host, username, password, dir_remoto = variables_ambiente()
    print(f"Período: {periodo}\n")
    descargar_archivos(host, username, password, dir_remoto, periodo)


if __name__ == "__main__":
    main()
