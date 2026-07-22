from pathlib import Path
import sys

endpoint_lower = sys.argv[1].lower()
endpoint = endpoint_lower.capitalize()

# Directorio destino
directorio_actual = Path(__file__).resolve().parent
directorio_contiene_a_back = ((directorio_actual.parent).parent)
webSocket = directorio_contiene_a_back / "back" / "utils" / "websockets_manager.py"
with open(webSocket, 'r', encoding='utf-8') as f:
    mainLineas = f.readlines()
    
cadena_a_buscar = "entities = ["
p = next((i for i, dato in enumerate(mainLineas) if cadena_a_buscar in dato.strip()), len(mainLineas))

if p is not None and f'"{endpoint_lower}"' not in mainLineas[p]:
    mainLineas[p] = (
        mainLineas[p].rstrip().rstrip(']')
        + f'"{endpoint_lower}", ]\n'
    )

# Agregar nuevo endpoint a la lista de entidades
# mainLineas = mainLineas[:p] + [f'    "{endpoint_lower}",\n'] + mainLineas[p:]

# Modificar lista de filtros de endpoint 
cadena_a_buscar = "active_connections: Dict[str, List[WebSocket]] = {"
p = next((i for i, l in enumerate(mainLineas) if cadena_a_buscar in l), None)

if p is not None:
    # buscar el cierre }
    fin = next(
        (i for i in range(p + 1, len(mainLineas)) if mainLineas[i].strip() == "}"),
        None
    )

    if fin is not None and f'"{endpoint_lower}"' not in ''.join(mainLineas[p:fin]):
        mainLineas.insert(fin, f'    "{endpoint_lower}": [],\n')

# Grabar modificaciones en webSocket.py 
with open(webSocket, 'w', encoding='utf-8') as f:
 	f.writelines(mainLineas)



