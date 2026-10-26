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
            for nombre in archivos:
                if (destino / nombre).exists():
                    raise ValueError(f"Ya existe el archivo de cierre: {nombre}. No se sobrescribió.")
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
        for nombre in archivos:
            try:
                sftp.lstat(f"{destino}/{nombre}")
            except FileNotFoundError:
                continue
            raise ValueError(f"Ya existe el archivo de cierre: {nombre}. No se sobrescribió.")
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
