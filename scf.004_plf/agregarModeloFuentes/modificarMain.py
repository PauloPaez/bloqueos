from pathlib import Path
import sys

endpoint_lower = sys.argv[1].lower()
endpoint = endpoint_lower.capitalize()

# Directorio destino
directorio_actual = Path(__file__).resolve().parent
directorio_contiene_a_back = ((directorio_actual.parent).parent)
main = directorio_contiene_a_back / "back" / "main.py"

with open(main, 'r', encoding='utf-8') as f:
    mainLineas = f.readlines()
    


def entidadesValidas(mainLineas):

    # -------------------------------
    # Modificar lista valid_entities
    # -------------------------------

    inicio = next(
        (i for i, l in enumerate(mainLineas) if 'valid_entities = [' in l),
        None
    )

    if inicio is not None:
        fin = None

        for i in range(inicio + 1, len(mainLineas)):
            if ']' in mainLineas[i]:
                fin = i
                break

        if fin is not None:
            # Verificar si ya existe
            ya_existe = any(
                f'"{endpoint_lower}"' in mainLineas[i]
                for i in range(inicio, fin)
            )

            if not ya_existe:
                nueva_linea = f'        "{endpoint_lower}",\n'
                mainLineas.insert(fin, nueva_linea)

    return mainLineas

    
#+------------------------+
#|      PRINCIPAL         |
#+------------------------+

# **Eliminar líneas vacías** #

mainLineas = [linea for linea in mainLineas if linea.strip()]  # Filtrar líneas no vacías

# Agregar las importaciones necesarias

cadena_a_buscar = "from utils.websockets_manager import ("

#cadena_a_buscar = "from utils.websockets_manager import add_connection, remove_connection, notify_clients"

p = next((i for i, dato in enumerate(mainLineas) if cadena_a_buscar in dato.strip()), len(mainLineas))

importacion =[f"from scripts.routers.{endpoint_lower} import {endpoint_lower}\n"]

mainLineas = mainLineas[:p] + importacion + mainLineas[p:]

# Modificar lista de Entidades Validas 

entidadesValidas(mainLineas)


# Agregar al final de archivo endpoint

cadena_a_buscar = 'logger.info("✅ Router mercado_pago incluido en la aplicación")'

p = next((i for i, dato in enumerate(mainLineas) if cadena_a_buscar in dato.strip()), len(mainLineas))

endPoint = [f"app.include_router({endpoint_lower}, tags=[\"{endpoint}\"])\n"]

mainLineas = mainLineas[:p] + endPoint + mainLineas[p:]

# Grabar modificaciones en main.py 

with open(main, 'w', encoding='utf-8') as f:
	f.writelines(mainLineas)

#for ml in mainLineas:
#    print('> ', ml)


