from decimal import Decimal
import json
from pathlib import Path

# ============================================================
# 1. Configuración de ruta (igual que el primer script)
# ============================================================
directorio_actual = Path(__file__).resolve().parent
directorio_back = directorio_actual.parent.parent
directorio_fuente = directorio_back.parent / "bloqueos" / "fuente_de_verdad"

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

    return {
        "tipo_reg": linea[0:1].strip(),                     # 1
        "codigo_liquidacion": linea[1:3].strip(),           # 2-3
        "centro_pago": linea[3:6].strip(),                  # 4-6
        "pago_anio": año,                                  # 7-8
        "pago_mes": mes,                                    # 9-10
        "pago_dia": dia,                                    # 11-12
        "suc_acreditacion": linea[12:14].strip(),           # 13-14
        "tipo_acreditacion": linea[14:15].strip(),          # 15
        "cuenta_acreditacion": linea[15:22].strip(),        # 16-22
        "cuenta_acreditacion_dv": linea[22:23].strip(),     # 23
        "importe_acreditado": formatear_importe(linea[23:38]),         # 24-38
        "beneficiario_nombre": linea[38:68].strip(),        # 39-68
        "documento_tipo": linea[68:69].strip(),             # 69
        "documento_nro": linea[69:77].strip(),              # 70-77
        "suc_debito": linea[77:79].strip(),                 # 78-79
        "tipo_debito": linea[79:80].strip(),                # 80
        "cuenta_debito": linea[80:87].strip(),              # 81-87
        "cuenta_debito_dv": linea[87:88].strip(),           # 88
        "cuil": formatear_cuil(linea[88:99]),                       # 89-99
        "zona": linea[99:100].strip(),                      # 100
        "centro": linea[100:102].strip(),                   # 101-102
        "sector": linea[102:105].strip(),                   # 103-105
        "padron": linea[105:111].strip(),                   # 106-111
        "padron_dv": linea[111:112].strip(),                # 112
        "reservado": linea[112:126].strip(),                # 113-126
        "cod_banco": linea[126:128].strip(),                # 127-128
        "fecha_pago": f"{dia}/{mes}/{año}",
    }

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
    with open('titulares2.json', 'w', encoding='utf-8') as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Total: {len(todos)} registros guardados en titulares.json")
    if todos:
        print("\nMuestra del primer registro:")
        print(json.dumps(todos[0], ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()