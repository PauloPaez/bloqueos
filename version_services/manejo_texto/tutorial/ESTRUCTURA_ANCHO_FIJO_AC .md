# Estructura de registro — Archivos de Acreditaciones Bancarias

Este documento describe el formato de los archivos de acreditaciones bancarias generados
mensualmente.

## 1. Descripción general

Los archivos comparten **el mismo formato de registro**: cada línea representa una
acreditación bancaria (un pago a un beneficiario), con los campos siempre en la misma posición y
con el mismo largo fijo.

| Característica     | Detalle                                                                |
|----------------------|---------------------------------------------------------------------|
| Largo de registro     | 128 caracteres                                                       |
| Tipo de dato           | Texto plano (todos los campos son legibles)                         |
| Fin de línea           | Retorno de carro + salto de línea (CRLF)                             |
| Campos numéricos       | Rellenos con ceros a la izquierda                                    |
| Campos alfabéticos     | Alineados a la izquierda, con espacios en blanco a la derecha        |


## 2. Estructura del registro (128 caracteres)

| Posición | Longitud | Campo                                   | Columna (BD)  |
|---------:|---------:|-----------------------------------------|---------------------------|
| 1        |        1 | Tipo de registro                        | `TIPO_REG`                 |
| 4-6      |        3 | Centro de pago                          | `CENTRO_PAGO`              |
| 2-3      |        2 | Código de liquidación                   | `COD_LIQUIDACION`          |
| 7-8      |        2 | Año de pago                             | `PAGO_ANIO`                |
| 9-10     |        2 | Mes de pago                             | `PAGO_MES`                 |
| 11-12    |        2 | Día de pago                             | `PAGO_DIA`                 |
| 13-14    |        2 | Sucursal de acreditación                | `SUC_ACREDITACION`         |
| 15       |        1 | Tipo de acreditación                    | `TIPO_ACREDITACION`        |
| 16-22    |        7 | Número de cuenta de acreditación        | `CUENTA_ACREDITACION`      |
| 23       |        1 | Dígito verificador de cuenta            | `CUENTA_ACREDITACION_DV`   |
| 24-38    |       15 | Importe a acreditar                     | `IMPORTE_ACREDITADO`       |
| 39-68    |       30 | Apellido y nombre                       | `BENEFICIARIO_NOMBRE`      |
| 69       |        1 | Dígito de tipo de documento             | `DOCUMENTO_TIPO`           |
| 70-77    |        8 | Número de documento                     | `DOCUMENTO_NRO`            |
| 78-79    |        2 | Sucursal de débito                      | `SUC_DEBITO`               |
| 80       |        1 | Tipo de débito                          | `TIPO_DEBITO`              |
| 81-87    |        7 | Cuenta de débito                        | `CUENTA_DEBITO`            |
| 88       |        1 | Dígito verificador de cuenta de débito  | `CUENTA_DEBITO_DV`         |
| 89-99    |       11 | CUIL                                    | `CUIL`                     |
| 100      |        1 | Zona                                    | `ZONA`                     |
| 101-102  |        2 | Centro                                  | `CENTRO`                   |
| 103-105  |        3 | Sector                                  | `SECTOR`                   |
| 106-111  |        6 | Padrón                                  | `PADRON`                   |
| 112      |        1 | Dígito verificador de padrón            | `PADRON_DV`                |
| 113-126  |       14 | Reservado                               | `RESERVADO`                |
| 127-128  |        2 | Código de banco                         | `COD_BANCO`                |

**Total: 128 caracteres.**

## 3. Ejemplo de registro

```
A0225001071701000005852000000147058751VELAZQUEZ IGNACIO             7291553012000221826020291553010R206346169353              01
```

| Campo                                | Valor                   |
|-----------------------------------------|---------------------------|
| Tipo de registro                         | `A`                        |
| Código de liquidación                    | `02`                       |
| Centro de pago                           | `250`                      |
| Fecha de pago                            | `17/07/01`                 |
| Sucursal de acreditación                 | `01`                       |
| Tipo de acreditación                     | `0` — Cta. de acreditación de haberes |
| Cuenta de acreditación / dígito          | `0000585` / `2`            |
| Importe a acreditar                      | `1.470.587,51`             |
| Apellido y nombre                        | `VELAZQUEZ IGNACIO`        |
| Tipo y número de documento               | `7` / `29155301`           |
| Sucursal / cuenta / dígito de débito     | `20` / `0221826` / `0`     |
| CUIL                                      | `20-29155301-0`            |
| Zona                                      | `R`                        |
| Centro / Sector                          | `20` / `634`               |
| Padrón / dígito verificador              | `616935` / `3`             |
| Código de banco                          | `01`                       |

## 4. Nota

- El campo **Zona** (posición 100) solo se completa para el personal docente; en el resto de los
  casos queda en blanco.
