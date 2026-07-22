from decimal import Decimal
import json
from pathlib import Path

# ============================================================
# 1. Configuración de ruta (igual que el primer script)
# ============================================================
directorio_actual = Path(__file__).resolve().parent
directorio_back = directorio_actual.parent.parent
directorio_fuente = directorio_back.parent / "fuente_de_verdad"

print("Directorio fuente:", directorio_fuente)

if not directorio_fuente.exists():
    print(f"El directorio {directorio_fuente} no existe.")
    exit(1)

# ============================================================
# 2. Funciones de formateo (del segundo script)
# ============================================================
def formatear_importe(valor_str: str) -> str:
    """Convierte un valor en centavos (string) a formato moneda ej. 12345 -> 123,45"""
    valor_str = valor_str.strip()
    if not valor_str:
        return "0,00"
    importe = Decimal(valor_str) / Decimal('100')
    parte_entera, parte_decimal = f"{importe:.2f}".split('.')
    parte_entera_formateada = f"{int(parte_entera):,}".replace(',', '.')
    return f"{parte_entera_formateada},{parte_decimal}"

def formatear_cuil(cuil: str) -> str:
    """Formatea CUIL de 11 dígitos a XX-XXXXXXXX-X"""
    cuil = cuil.strip()
    if len(cuil) == 11:
        return f"{cuil[:2]}-{cuil[2:10]}-{cuil[10]}"
    return cuil

# ============================================================
# 3. Parseo de una línea (adaptado del segundo script)
# ============================================================
def parsear_linea(linea: str) -> dict:
    """
    Parsea una línea según el layout de posiciones fijas.
    Asume que todos los archivos comparten el mismo layout.
    """
    linea = linea.rstrip('\n\r')
    # Asegurar longitud mínima para evitar errores de índice
    if len(linea) < 128:
        linea = linea.ljust(128)

    # Extraer campos intermedios (para claridad)
    año = linea[6:8].strip()
    mes = linea[8:10].strip()
    dia = linea[10:12].strip()
    num_cuenta = linea[15:22].strip()
    digito_cuenta = linea[22].strip()
    tipo_doc = linea[68].strip()
    num_doc = linea[69:77].strip()
    sucursal_deb = linea[77:79].strip()
    cuenta_deb = linea[80:87].strip()
    digito_deb = linea[79].strip()
    centro = linea[100:102].strip()
    sector = linea[102:105].strip()
    padron = linea[105:111].strip()
    digito_padron = linea[111].strip()

    registro = {
        'tipo_reg': linea[0].strip(),
        'codigo_liquidacion': linea[1:3].strip(),
        'centro_pago': linea[3:6].strip(),
        'fecha_pago': f"{año}/{mes}/{dia}",
        'sucursal_acreditacion': linea[12:14].strip(),
        'tipo_acreditacion': linea[14].strip(),
        'cuenta_acreditacion_digito': f"{num_cuenta}/{digito_cuenta}" if digito_cuenta else num_cuenta,
        'importe_acreditar': formatear_importe(linea[23:38]),
        'ayn': linea[38:68].strip(),
        'tipoynumdoc': f"{tipo_doc}/{num_doc}" if tipo_doc and num_doc else "",
        'sucursal_cuenta_digitodebito': f"{sucursal_deb}/{cuenta_deb}/{digito_deb}" if digito_deb else f"{sucursal_deb}/{cuenta_deb}",
        'cuil': formatear_cuil(linea[88:99]),
        'zona': linea[99].strip(),
        'centro_sector': f"{centro}/{sector}" if centro and sector else "",
        'padron_digitoverificador': f"{padron}/{digito_padron}" if digito_padron else padron,
        'codigo_banco': linea[126:128].strip()
    }
    return registro

# ============================================================
# 4. Procesamiento de un archivo
# ============================================================
def procesar_archivo(ruta: Path) -> list:
    """Lee un archivo, parsea cada línea y devuelve lista de registros con fuente."""
    nombre = ruta.name
    registros = []
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            for num_linea, linea in enumerate(f, start=1):
                # Saltar líneas vacías
                if not linea.strip():
                    continue
                try:
                    registro = parsear_linea(linea)
                    registro['fuente'] = nombre   # Añadimos el nombre del archivo
                    registros.append(registro)
                except Exception as e:
                    print(f"Error en {nombre} línea {num_linea}: {e}")
    except Exception as e:
        print(f"Error al leer {ruta}: {e}")
    return registros

# ============================================================
# 5. Función principal
# ============================================================
def main():
    # Recorrer todos los archivos (recursivamente)
    todos = []
    for elemento in directorio_fuente.rglob('*'):
        if elemento.is_file():
            print(f"Procesando {elemento} ...")
            registros = procesar_archivo(elemento)
            todos.extend(registros)
            print(f"  -> {len(registros)} registros")

    # Guardar JSON
    with open('titulares.json', 'w', encoding='utf-8') as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Total: {len(todos)} registros guardados en titulares.json")
    if todos:
        print("\nMuestra del primer registro:")
        print(json.dumps(todos[0], ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()