import os
import stat
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import paramiko
from dotenv import load_dotenv

if __package__:
    from .prefijos import es_archivo_padron
else:
    from prefijos import es_archivo_padron

# Raíz del proyecto: .../back/utils/padrones/descargarPadrones.py -> 3 niveles arriba
RAIZ = Path(__file__).resolve().parents[2]
RAIZ_DATOS = Path(__file__).resolve().parents[3]
ARCHIVO_ENV = RAIZ / ".env"
DIR_LOCAL = RAIZ_DATOS / "datos" / "fuentes"


def variables_ambiente():
    if not ARCHIVO_ENV.exists():
        raise ValueError(f"No se encontró el archivo .env en {ARCHIVO_ENV}")

    load_dotenv(ARCHIVO_ENV)
    HOST = os.getenv("HOST")
    USERNAME = os.getenv("LOGIN")
    PASSWORD = os.getenv("PASSWORD")
    DIR_REMOTO = os.getenv("DIR_REMOTO")

    # Validar antes de imprimir
    if any(not valor or not valor.strip() for valor in [HOST, USERNAME, PASSWORD, DIR_REMOTO]):
        raise ValueError("Faltan variables de entorno en el archivo .env")

    # No se imprime la contraseña
    print(f"Conexión: {USERNAME}@{HOST}  |  directorio remoto: {DIR_REMOTO}")
    return HOST, USERNAME, PASSWORD, DIR_REMOTO


def validar_periodo(periodo):
    if not periodo or not periodo.isascii() or not periodo.isalnum():
        raise ValueError("El período debe contener solamente letras y números ASCII.")
    return periodo.upper()

def descargar_archivos(host, username, password, dir_remoto, periodo, dir_local=DIR_LOCAL):
    periodo = validar_periodo(periodo)
    if any(not valor or not valor.strip() for valor in [host, username, password, dir_remoto]):
        raise ValueError("Faltan datos para la conexión SFTP.")

    ssh = paramiko.SSHClient()
    # Acepta la clave del host automáticamente (red interna).
    # Para mayor seguridad, cargar known_hosts y usar RejectPolicy.
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    sftp = None

    try:
        ssh.connect(host, username=username, password=password, timeout=15)
        sftp = ssh.open_sftp()
        sftp.get_channel().settimeout(30)
        print("Conectado al servidor.\n")

        # En el servidor solo listamos atributos y leemos archivos (get).
        archivos_remotos = []
        directorio = f"{dir_remoto.rstrip('/')}/{periodo}/B"
        for info in sorted(sftp.listdir_attr(directorio), key=lambda item: item.filename):
            archivo = info.filename
            if not es_archivo_padron(archivo, periodo):
                continue
            if not stat.S_ISREG(info.st_mode) or info.st_size == 0:
                continue
            ruta_remota = f"{directorio}/{archivo}"
            archivos_remotos.append((archivo, ruta_remota, info.st_size))

        if not archivos_remotos:
            print("No hay archivos SUAC/TIAC con datos para descargar.")
            return []

        # La carpeta temporal es LOCAL. Una descarga fallida no borra las fuentes anteriores.
        dir_local.parent.mkdir(parents=True, exist_ok=True)
        with TemporaryDirectory(dir=dir_local.parent) as temporal:
            nuevas = Path(temporal) / "nuevas"
            nuevas.mkdir()
            for archivo, ruta_remota, tamano in archivos_remotos:
                ruta_local = nuevas / archivo
                try:
                    sftp.get(ruta_remota, str(ruta_local))
                except (OSError, paramiko.SSHException) as e:
                    raise RuntimeError(f"No se pudo descargar {archivo}: {e}") from e
                if ruta_local.stat().st_size != tamano:
                    raise ValueError(f"Tamaño descargado inesperado: {archivo}")
                print(f"[OK] {archivo} ({tamano} bytes)")

            # Solo sustituimos las fuentes LOCALES cuando todas las descargas se completaron.
            anteriores = Path(temporal) / "anteriores"
            if dir_local.exists():
                dir_local.rename(anteriores)
            try:
                nuevas.rename(dir_local)
            except OSError:
                # Si falla la sustitución local, recuperamos la carpeta anterior.
                if anteriores.exists():
                    anteriores.rename(dir_local)
                raise
    finally:
        try:
            if sftp is not None:
                sftp.close()
        finally:
            ssh.close()

    descargados = [dir_local / archivo for archivo, _, _ in archivos_remotos]
    print(f"Descargados: {len(descargados)} archivos en {dir_local}")
    return descargados


def main():
    if len(sys.argv) != 2:
        print("Uso: python descargarPadrones.py PERIODO", file=sys.stderr)
        return 1
    try:
        periodo = validar_periodo(sys.argv[1])
        host, username, password, dir_remoto = variables_ambiente()
        print(f"Período: {periodo}\n")
        descargar_archivos(host, username, password, dir_remoto, periodo)
    except (ValueError, RuntimeError, OSError, paramiko.SSHException) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
