import json

moduloDestino = "nro_notas"
moduloSecundario = "Tipo_notas"
ModuloDestino = "nro_notas".capitalize()
ModuloSecundario = "Tipo_notas".capitalize()
campoSecundario = "tipo"
campoPrimario = "categoria"


# Leer el archivo JSON
with open('codigos.json', 'r', encoding='utf-8') as file:
    arregloCodigo = json.load(file)

def reemplazarPalabras(codigoNuevo):
    replacements = {
    "!ModuloSecundario!": ModuloSecundario,
    "!moduloSecundario!": moduloSecundario,
    "!CampoSecundario!": campoSecundario.capitalize(),
    "!campoSecundario!": campoSecundario,
    "!CampoSecundario!": campoSecundario.capitalize(),
    "!campoPrimario!": campoPrimario,
    #"!NombreArreglo!": nombreArreglo.capitalize(),
    }
    for marcador, valor in replacements.items():
        codigoNuevo = codigoNuevo.replace(marcador, valor)
    return codigoNuevo

# Procesar como antes
for codigo in arregloCodigo:
    codigoNuevo = reemplazarPalabras(codigo['codigoNuevo'])
    print(codigo['criterio'], codigo['pre'], codigoNuevo)

    print("\n---\n")
    