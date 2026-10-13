# Autor Paulo Paez
# Funcion Correctamente 07/05/26
import sys
import re
import shutil
from pathlib import Path
from datetime import datetime

# args: Modelo Campo
# ej: Maquinarias tipo
moduloAmodificar = input("Ingrese el módulo a modificar: ")
moduloDueñoDeCampo = input("Ingrese el módulo dueño del campo: ")
campo = input("Ingrese el campo para ser opciones: ")

moduloAmodificar_cap = moduloAmodificar.capitalize()
modelo_cap = moduloDueñoDeCampo .capitalize()
modelo_low = moduloDueñoDeCampo.lower()

# Paths
base = Path(__file__).resolve().parents[1]
componente = base / "front/src/components" / moduloAmodificar_cap

formulario = componente / "FormularioEditar.js"
editar = componente / f"Editar{moduloAmodificar_cap}.jsx"

contenido_form = formulario.read_text(encoding="utf-8")
contenido_edit = editar.read_text(encoding="utf-8")

# -------------------------------------------------
# BACKUP automático
# -------------------------------------------------
backup_dir = componente / "backups"
backup_dir.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_file = backup_dir / f"{editar.name}.{timestamp}.bak"

shutil.copy2(editar, backup_file)

# -------------------------------------------------
# 1. Obtener optionsKey
# -------------------------------------------------
pattern = rf"name:\s*\"{campo}\".*?optionsKey:\s*\"(\w+)\""
match = re.search(pattern, contenido_form, re.DOTALL)

if not match:
    raise Exception(f"No se encontró optionsKey para el campo '{campo}'")

options_key = match.group(1)
opt_cap = options_key.capitalize()

# -------------------------------------------------
# 2. Generar líneas
# -------------------------------------------------
linea_import = (
    f"import {{ useGetDistinct{modelo_cap}Query }} "
    f"from '../../store/apiSlice';\n"
)

linea_const = (
    f"  const {{ data: distinct{modelo_cap}{opt_cap} = [] }} = "
    f"useGetDistinct{modelo_cap}Query('{campo}');\n"
)

# -------------------------------------------------
# 3. Insertar IMPORT
# -------------------------------------------------
if linea_import.strip() not in contenido_edit:
    contenido_edit = re.sub(
        r"(from\s+'\./camposValidacion';\n)",
        r"\1" + linea_import,
        contenido_edit
    )

# -------------------------------------------------
# 4. Insertar CONST antes de useForm
# -------------------------------------------------
if f"distinct{modelo_cap}{opt_cap}" not in contenido_edit:
    contenido_edit = re.sub(
        r"(const\s+\{\s*register,\s*handleSubmit.*?useForm\()",
        linea_const + r"\1",
        contenido_edit,
        flags=re.DOTALL
    )

# -------------------------------------------------
# 5. Reemplazar datosSelect
# -------------------------------------------------
contenido_edit = re.sub(
    rf'"{options_key}"\s*:\s*\[.*?\]',
    f'"{options_key}": distinct{modelo_cap}{opt_cap}',
    contenido_edit,
    flags=re.DOTALL
)

# -------------------------------------------------
# 6. Guardar archivo
# -------------------------------------------------
editar.write_text(contenido_edit, encoding="utf-8")

print("✔ Auto-inserción completada")
print(f"✔ Backup creado: {backup_file.name}")
