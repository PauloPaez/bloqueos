import json
from pathlib import Path

# Pedir datos al usuario
# ModeloDestino = input("Ingrese el nombre del MODELO de destino (ej. rubricas): ").strip().capitalize()
# modelSecundario = input("Ingrese el nombre del MODELO desde donde se obtiene las opciones: ").strip().capitalize()
# campoSecundario = input("Ingrese el nombre del CAMPO que será la opción: ").strip().lower()
# campoPrimario = input("Ingrese el nombre del CAMPO de cual depende las opciones anteriores: ").strip().lower()

moduloDestino = "domicilios"
moduloSecundario = "provincias"
ModuloDestino = "domicilios".capitalize()
ModuloSecundario = "provincias".capitalize()
campoSecundario = "departamentos"
campoPrimario = "provincias"

# Rutas
directorio_actual = Path(__file__).resolve().parent
plantilla_path = directorio_actual / "templates" / "recuperarDatos0.txt"
diccModeloDestino = (
    directorio_actual.parent
    / "agregarModeloFuentes"
    / "diccModelo"
    / f"{ModuloDestino.lower()}.json"
)
componente_path = (
    directorio_actual.parent.parent
    / "front"
    / "src"
    / "components"
    / ModuloDestino
    / f"Editar{ModuloDestino}.jsx"
)


def funcionesParaCargarArregloSecundario(nombreArreglo):
    # Capitalizar solo la primera letra para mantener camelCase
    CampoSecundario = (
        campoSecundario[0].upper() + campoSecundario[1:] if campoSecundario else ""
    )

    # Leer y procesar plantilla
    with plantilla_path.open("r", encoding="utf-8") as archivo:
        contenido = archivo.read()

    # Realizar reemplazos
    replacements = {
        "!ModuloSecundario!": ModuloSecundario,
        "!moduloSecundario!": moduloSecundario,
        "!CampoSecundario!": CampoSecundario,
        "!campoSecundario!": campoSecundario,
        "!CampoSecundario!": campoSecundario.capitalize(),
        "!campoPrimario!": campoPrimario,
        "!NombreArreglo!": nombreArreglo.capitalize(),
    }

    for marcador, valor in replacements.items():
        contenido = contenido.replace(marcador, valor)

    # Guardar archivo resultante
    # with output_path.open("w", encoding="utf-8") as archivo:
    #     archivo.write(contenido)

    # print(f"Archivo generado exitosamente en: {output_path}")
    return contenido


def componenteDestino():
    with componente_path.open("r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()
    return lineas


def insertar_codigo(contenido, patron, codigo, insertar_antes=False):
    p = next((i for i, linea in enumerate(contenido) if patron in linea), None)
    if p is not None:
        if insertar_antes:
            contenido = contenido[:p] + [codigo] + contenido[p:]
        else:
            contenido = contenido[: p + 1] + [codigo] + contenido[p + 1 :]
    return contenido


def asignarArregloRecuperado(contenido):
    # Obtener nombre del arreglo desde JSON
    with diccModeloDestino.open("r", encoding="utf-8") as archivo:
        arreglo_campos = json.load(archivo)

    nombreArreglo = next(
        (
            campo["optionsKey"]
            for campo in arreglo_campos
            if campo["type"] == "select" and campo["name"] == campoSecundario
        ),
        None,
    )
    if not nombreArreglo:
        print(f"No se encontró campo select con nombre '{campoSecundario}'")
        return []
    else:
        # Buscar y reemplazar
        for i, linea in enumerate(contenido):
            if f'"{nombreArreglo}": []' in linea:
                contenido[i] = f'\t"{nombreArreglo}": {nombreArreglo.capitalize()},\n'
                break
        else:
            print(f"No se encontró el arreglo ")
            return []
        return contenido, nombreArreglo


componente = componenteDestino()

#
criterio = 'import { resetModulo } from "../../store/appSlice";'
codigo_nuevo = 'import { usePost!ModuloSecundario!ByFieldMutation } from "../../store/apiSlice";\n'
codigo_nuevo = codigo_nuevo.replace("!ModuloSecundario!", ModuloSecundario)
contenido = insertar_codigo(componente, criterio, codigo_nuevo, insertar_antes=True)
#
#
criterio = "const user = useSelector((state) => state.acceso.user);"
codigo_nuevo = "const [buscar!CampoSecundario!] = usePost!ModuloSecundario!ByFieldMutation();"
codigo_nuevo = codigo_nuevo.replace("!CampoSecundario!", campoSecundario.capitalize()).replace('!ModuloSecundario!', ModuloSecundario)
contenido = insertar_codigo(contenido, criterio, codigo_nuevo)
#
contenido, nombreArreglo = asignarArregloRecuperado(contenido)
#
criterio = 'const filaSeleccionada = useSelector((state) => state.modulos.nro_notas).datos;'
codigo_nuevo = funcionesParaCargarArregloSecundario(nombreArreglo)
contenido = insertar_codigo(contenido, criterio, codigo_nuevo)
#
for x in contenido:
    print(x)

componente_tpath = directorio_actual / 'edt.jsx'
# Guardar el archivo modificado    
# with componente_tpath.open("w", encoding="utf-8") as archivo:
#     archivo.writelines(contenido)


