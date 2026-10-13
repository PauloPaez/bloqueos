import sys
from pathlib import Path
from generadorCampos import definir_campos

def generar_formulario_campos(model_lower, tipoComponente):

    model_capitalized = model_lower.capitalize()
    # Archivo destino
    directorio_actual = Path(__file__).resolve().parent
    directorio_componente = ((directorio_actual.parent).parent) / "front" / "src" / "components" / model_capitalized
    Path(directorio_componente).mkdir(parents=True, exist_ok=True)
    componente = directorio_componente / f"Formulario{tipoComponente}.js"

    campos = definir_campos(model_lower)

    # Normalizar campos
    campos_limpios = [
        campo.strip().replace('\t', '').rstrip(',')
        for campo in campos
    ]

    with open(componente, 'w', encoding='utf-8') as f:
        f.write("export const formularioCampos = [\n")

        for campo in campos_limpios:
            f.write(f"  {campo},\n")

        f.write("];\n")
