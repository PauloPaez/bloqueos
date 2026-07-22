import sys
from pathlib import Path
from generadorCampos import definir_campos
from generdorFromulario import generar_formulario_campos

# Recibir nombre Modelo
model_lower =  sys.argv[1].lower()
model_capitalized = model_lower.capitalize()

# Directorio y archivo destino
directorio_actual = Path(__file__).resolve().parent
directorio_componente = ((directorio_actual.parent).parent) / "front" / "src" / "components" / model_capitalized
Path(directorio_componente).mkdir(parents=True, exist_ok=True)
componente = directorio_componente / f"Editar{model_capitalized}.jsx"

# Diretorio Template
templateEr = directorio_actual / "templates" / "editar.txt"

with open(templateEr, 'r', encoding='utf-8') as f:
    mainLineas = f.readlines()

# Poner nombre del modelo en el template
a_buscar_lower = "!model!"
a_buscar_capitalized = "!Model!"

for ix, linea in enumerate(mainLineas):
    linea = linea.replace(a_buscar_lower, model_lower).replace(a_buscar_capitalized, model_capitalized)
    mainLineas[ix] = linea

# Agregar los campos al formulario 
# campos = definir_campos(model_lower)
# cadena_a_buscar = "const formFields = ["
# p = next((i for i, dato in enumerate(mainLineas) if cadena_a_buscar in dato.strip()), len(mainLineas)) + 1
# mainLineas = mainLineas[:p] + campos + mainLineas[p:]

# ... (código anterior se mantiene igual hasta la definición de campos)

# Agregar los campos al formulario 
campos = definir_campos(model_lower)
# cadena_a_buscar = "const formFields = ["
# p = next((i for i, dato in enumerate(mainLineas) if cadena_a_buscar in dato.strip()), len(mainLineas)) + 1
# mainLineas = mainLineas[:p] + campos + mainLineas[p:]

# Procesar campos select
campos = definir_campos(model_lower)
selects = [campo for campo in campos if 'type: "select"' in campo]
if selects:
    print('Hay campos select')
    select_keys = []
    for campo in selects:
        if 'optionsKey' in campo:
            try:
                # Extraer el optionsKey de manera más segura
                key = campo.split('optionsKey: "')[1].split('"')[0]
                select_keys.append(f'"{key}"')
            except IndexError:
                continue
    
    if select_keys:
        # Crear el estado para los selects
        select_state = f'const datosSelect = {{\n'
        select_state += f'  {select_keys[0]}: [],\n'  # Inicializa cada select con array vacío
        
        # Si hay más de un select, agregar los demás
        if len(select_keys) > 1:
            for key in select_keys[1:]:
                select_state += f'  {key}: [],\n'
        
        select_state += '};\n\n'
        
        # Buscar la línea después de formFields para insertar el estado
        insert_pos = next(
            (i for i, line in enumerate(mainLineas)
            if 'const onSubmit = async (data) => {' in line),
            -1
        )

        if insert_pos != -1:
            mainLineas.insert(insert_pos, select_state)

# for ix, linea in enumerate(mainLineas):
#     print(linea, end='')  # Imprimir cada línea sin añadir un salto de línea extra
    
# Imprimir el resultado final

with open(componente, 'w', encoding='utf-8') as f:
	f.writelines(mainLineas)

generar_formulario_campos(model_lower, "Editar")