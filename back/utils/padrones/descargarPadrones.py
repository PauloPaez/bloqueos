import os
import sys
import stat
from pathlib import Path

import paramiko
from dotenv import load_dotenv
import shutil

# Raíz del proyecto: .../back/utils/padrones/descargarPadrones.py -> 3 niveles arriba
RAIZ = Path(__file__).resolve().parents[2]
RAIZ_DATOS = Path(__file__).resolve().parents[3]
ARCHIVO_ENV = RAIZ / ".env"
DIR_LOCAL = RAIZ_DATOS / "datos" / "fuentes"

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
    if not ARCHIVO_ENV.exists():
        print(f"Error: no se encontró el archivo .env en {ARCHIVO_ENV}")
        sys.exit(1)

    load_dotenv(ARCHIVO_ENV)
    HOST = os.getenv("HOST")
    USERNAME = os.getenv("LOGIN")
    PASSWORD = os.getenv("PASSWORD")
    DIR_REMOTO = os.getenv("DIR_REMOTO")

    # Validar antes de imprimir
    if None in [HOST, USERNAME, PASSWORD, DIR_REMOTO]:
        print("Error: Faltan variables de entorno en el archivo .env")
        sys.exit(1)

    # No se imprime la contraseña
    print(f"Conexión: {USERNAME}@{HOST}  |  directorio remoto: {DIR_REMOTO}")
    return HOST, USERNAME, PASSWORD, DIR_REMOTO


def nombres_archivos(periodo):
    """Genera los nombres PREFIJO.PERIODO."""
    return [f"{prefijo}.{periodo}" for prefijo in PREFIJOS]
    

def limpiar_directorio(directorio: Path):
    """Borra el contenido de la carpeta (archivos y subcarpetas), pero no la carpeta."""
    directorio.mkdir(parents=True, exist_ok=True)
    for item in directorio.iterdir():
        if item.is_dir() and not item.is_symlink():
            shutil.rmtree(item)
        else:
            item.unlink()
    print(f"Directorio limpiado: {directorio}")


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
        limpiar_directorio(DIR_LOCAL)

        for archivo in nombres_archivos(periodo):
            ruta_remota = f"{dir_remoto.rstrip('/')}/{periodo}/B/{archivo}"
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
