import stat
from contextlib import contextmanager
from pathlib import Path

import paramiko

from utils.padrones.descargarPadrones import validar_periodo, variables_ambiente


class RecuperacionPendiente(RuntimeError):
    """Alguna escritura del intento no pudo deshacerse; requiere revisión manual."""


def borrar_creados(creados, borrar):
    errores = []
    for ruta in reversed(creados):
        try:
            borrar(ruta)
        except Exception as error:
            errores.append(f"{ruta}: {error}")
    if errores:
        raise RecuperacionPendiente("No se pudieron borrar archivos del intento: " + "; ".join(errores))


def mensaje_existentes(destino, periodo):
    """Al cerrar, cualquier TXT previo del período es inválido: se pide borrarlos todos."""
    return (f"Ya existen archivos de cierre en {destino}. Pida al encargado de los archivos que borre "
            f"los BLOQUEO-*.{periodo}.txt para poder cerrar el período y generar los TXT.")


# INICIO PRUEBA LOCAL TEMPORAL: replica /datos dentro del repositorio.
# No consulta el .env ni abre una conexión SFTP. Eliminar este destino al activar SFTP.
RAIZ_PRUEBA = Path(__file__).resolve().parents[3] / "datos"


@contextmanager
def guardar_txt_local_prueba(periodo, archivos):
    destino = RAIZ_PRUEBA / validar_periodo(periodo) / "Bloqueos" / "ESCU"
    creados = []
    try:
        if archivos:
            destino.mkdir(parents=True, exist_ok=True)
            if any(destino.glob(f"BLOQUEO-*.{periodo}.txt")):
                raise ValueError(mensaje_existentes(destino, periodo))
            for nombre, contenido in archivos.items():
                ruta = destino / nombre
                # xb garantiza que tampoco sobrescribimos si el archivo aparece después del control.
                with ruta.open("xb") as salida:
                    creados.append(ruta)
                    salida.write(contenido)
        yield [str(ruta) for ruta in creados]
    except BaseException:
        borrar_creados(creados, lambda ruta: ruta.unlink(missing_ok=True))
        raise


def descartar_txt_local_prueba(periodo):
    """Borra los TXT del cierre; si ya no están, no hace nada."""
    periodo = validar_periodo(periodo)
    carpeta = RAIZ_PRUEBA / periodo / "Bloqueos" / "ESCU"
    for archivo in carpeta.glob(f"BLOQUEO-*.{periodo}.txt"):
        archivo.unlink(missing_ok=True)
# FIN PRUEBA LOCAL TEMPORAL.


@contextmanager
def guardar_txt_sftp(periodo, archivos):
    """Destino real preparado, pero NO conectado al cierre mientras dure la prueba local."""
    if not archivos:
        yield []
        return
    periodo = validar_periodo(periodo)
    host, usuario, clave, _ = variables_ambiente()
    destino = f"/datos/{periodo}/Bloqueos/ESCU"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sftp = None
    creados = []
    try:
        ssh.connect(host, username=usuario, password=clave, timeout=15)
        sftp = ssh.open_sftp()
        sftp.get_channel().settimeout(30)
        # /datos/PERIODO debe existir: solo creamos sus carpetas de salida faltantes.
        if not stat.S_ISDIR(sftp.stat(f"/datos/{periodo}").st_mode):
            raise ValueError("El directorio remoto del período no es una carpeta.")
        for carpeta in (f"/datos/{periodo}/Bloqueos", destino):
            try:
                info = sftp.stat(carpeta)
            except FileNotFoundError:
                sftp.mkdir(carpeta)
            else:
                if not stat.S_ISDIR(info.st_mode):
                    raise ValueError(f"No es un directorio: {carpeta}")
        if any(nombre.startswith("BLOQUEO-") and nombre.endswith(f".{periodo}.txt")
               for nombre in sftp.listdir(destino)):
            raise ValueError(mensaje_existentes(destino, periodo))
        try:
            for nombre, contenido in archivos.items():
                ruta = f"{destino}/{nombre}"
                with sftp.open(ruta, "wx") as salida:
                    creados.append(ruta)
                    salida.write(contenido)
                if sftp.stat(ruta).st_size != len(contenido):
                    raise RuntimeError(f"Tamaño remoto inesperado: {nombre}")
            yield creados
        except BaseException:
            borrar_creados(creados, sftp.remove)
            raise
    finally:
        # El envío ya fue verificado o revertido. Cerrar el canal no cambia su resultado.
        for conexion in (sftp, ssh):
            if conexion is not None:
                try:
                    conexion.close()
                except Exception as error:
                    print(f"ERROR al cerrar la conexión SFTP del cierre: {error}")


# PRUEBA LOCAL TEMPORAL — ÚNICO DESTINO ACTIVO DEL CIERRE.
# Al pasar a producción, reemplazar la asignación por guardar_txt_sftp.
# No cambiar esto hasta confirmar que finalizaron las pruebas locales.
guardar_txt_cierre = guardar_txt_local_prueba
