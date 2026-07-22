from decimal import Decimal
import json
from pathlib import Path

registros = []
directorio_actual = Path(__file__).resolve().parent
directorio_fuentes = directorio_actual.parent / 'fuentes' / 'BSJ - ESCU0626' / 'BSJ-ESCU'
print(f"Directorio actual: {directorio_fuentes}")

def formatear_importe(valor: str) -> str:
    importe = Decimal(valor) / Decimal('100')
    parte_entera, parte_decimal = f"{importe:.2f}".split('.')
    parte_entera_formateada = f"{int(parte_entera):,}".replace(',', '.')
    return f"{parte_entera_formateada},{parte_decimal}"


def formatear_cuil(cuil: str) -> str:
    return f"{cuil[:2]}-{cuil[2:10]}-{cuil[10]}"

with open(directorio_fuentes / 'SUAC1.JUNIO26', 'r', encoding='utf-8') as f:
    for linea in f:
        linea = linea.rstrip('\n\r')
        #campo: fecha_pago
        año= linea[6:8].strip()
        mes= linea[8:10].strip()
        dia= linea[10:12].strip()
        #campo: cuenta_acreditacion_digito
        numCuentaAcreditacion= linea[15:22]
        digitoVerificador=linea[22]
        #campo: tipoynumdoc
        tipo=linea[68]
        dni=linea[69:77]
        #campo: sucursal_cuenta_digitodebito
        sucursal=linea[77:79]
        cuenta=linea[80:87]
        digitoDebito=linea[79]
        #campo: centro_sector
        centro = linea[100:102]
        sector= linea[102:105]
        #campo: padron_digitoverificador
        padron=linea[105:111]
        digitoPadron=linea[111]

        registro = {
            'tipo_reg': linea[0].strip(),
            'codigo_liquidacion': linea[1:3].strip(),
            'centro_pago': linea[3:6].strip(),
            'fecha_pago': f"{año}/{mes}/{dia}",
            'sucursal_acreditacion': linea[12:14],
            'tipo_acreditacion': linea[14],
            'cuenta_acreditacion_digito': f"{numCuentaAcreditacion}/{digitoVerificador}", #consultar
            'importe_acreditar':formatear_importe(float(linea[23:38])), #verificar
            'ayn': (linea[38:68]).strip(),
            'tipoynumdoc': f"{tipo}/{dni}",
            'sucursal_cuenta_digitodebito': f"{sucursal}/{cuenta}/{digitoDebito}",
            'cuil': formatear_cuil(linea[88:99]),
            'zona': linea[99],
            'centro_sector': f"{centro}/{sector}",
            'padron_digitoverificador': f"{padron}/{digitoPadron}",
            'codigo_banco': linea[126:128]


        }
        registros.append(registro)

with open('titulares.json', 'w', encoding='utf-8') as f:
    json.dump(registros, f, ensure_ascii=False, indent=2)

print(f"✅ {len(registros)} registros guardados en titulares.json")
print("-----")
print(registros[0])