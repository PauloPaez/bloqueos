from __future__ import annotations

import io
from collections.abc import Iterable
from zipfile import ZIP_DEFLATED, ZipFile


def crear_zip(archivos: Iterable[tuple[str, io.BytesIO]]) -> io.BytesIO:
    buffer = io.BytesIO()

    with ZipFile(buffer, "w", ZIP_DEFLATED) as archivo_zip:
        for nombre, contenido in archivos:
            contenido.seek(0)
            archivo_zip.writestr(nombre, contenido.read())

    buffer.seek(0)
    return buffer
