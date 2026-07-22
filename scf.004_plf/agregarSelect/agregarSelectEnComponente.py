import sys
from pathlib import Path

componente_a_modificar =  sys.argv[1].lower()       # modelo donde se debe insertar el select
Modelo_del_select = sys.argv[2].capitalize()       # nombre del modelo de Select
labelKey = sys.argv[3].lower()      # el nombre que muestra el select "labelKey"
campo_del_formulario = sys.argv[4].lower()  # campo del formulario donde debe cargarse el selected
Label = sys.argv[5].capitalize()  # Etiqueta del campo en el formulario

# Directorio y archivo destino
Componente_a_modificar = componente_a_modificar.capitalize()    # modelo donde se debe insertar el select
directorio_actual = Path(__file__).resolve().parent
directorio_componente = ((directorio_actual.parent).parent) / "front" / "src" / "components" / Componente_a_modificar
Path(directorio_componente).mkdir(parents=True, exist_ok=True)
componente_modificar = directorio_componente / f"Editar{Componente_a_modificar}.jsx"

# Archivo del Modelo_del_select
directorio_componente = ((directorio_actual.parent).parent) / "front" / "src" / "components" / Modelo_del_select
Path(directorio_componente).mkdir(parents=True, exist_ok=True)
componente_select = directorio_componente / f"Select{Modelo_del_select}.jsx"

#--------------Iniciar Proceso----------------------
# Leer y procesar componente_a_modificar
with open(componente_modificar, 'r', encoding='utf-8') as f:
    lineasComponente = f.readlines()


# Procesar Componente donde se insertará el select
frase_a_buscar = "import"
p = next((i for i, dato in enumerate(lineasComponente) if frase_a_buscar in dato.strip()), len(lineasComponente))
linea = f'import Select{Modelo_del_select} from "../{Modelo_del_select}/Select{Modelo_del_select}";\n'
lineasComponente = lineasComponente[:p] + [linea] + lineasComponente[p:]    # Insertar import SelectModelo_del_select   

frase_a_buscar = "];"       
p = next((i for i, dato in enumerate(lineasComponente) if frase_a_buscar in dato.strip()), len(lineasComponente))
linea = f'const {Modelo_del_select}Value = watch("{componente_a_modificar}.0.{campo_del_formulario}"); \n'
lineasComponente = lineasComponente[:p+1] + [linea] + lineasComponente[p+1:] # Insertar 

# Diretorio Template
templateRt = directorio_actual / "templates" / "select_en_componente.txt"
with open(templateRt, 'r', encoding='utf-8') as f:
    mainLineas = f.readlines()

# print(f"templates: {templateRt}")

lineas = []
for linea in mainLineas:
    if "!Label!" in linea:
        linea = linea.replace("!Label!", Label)    
    if "!Modelo_del_select!" in linea:
        linea = linea.replace("!Modelo_del_select!", Modelo_del_select)
    if "!labelKey!" in linea:
        linea = linea.replace("!labelKey!", labelKey)         
    if "!campo_del_formulario!" in linea:
        linea = linea.replace("!campo_del_formulario!", campo_del_formulario)
    if "!componente_a_modificar!" in linea:    
        linea = linea.replace("!componente_a_modificar!", componente_a_modificar)
    lineas.append(linea)   
    
# Insertar Select en el formulario
frase_a_buscar = "))}"       
p = next((i for i, dato in enumerate(lineasComponente) if frase_a_buscar in dato.strip()), len(lineasComponente))
lineasComponente = lineasComponente[:p+1] + lineas + lineasComponente[p+1:] # Insertar 
                               
# Escribir archivo  
print(f"Archivo: {componente_modificar}")
# with open(componente_modificar, 'w', encoding='utf-8') as f:
#     f.writelines(lineasComponente)  
print("_________________________________________________________\n")
for linea in lineasComponente:
    print(linea, end="")
print("_________________________________________________________\n")






