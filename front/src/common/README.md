# Filtros de listados

## Componentes y responsabilidades

- `GenericFilter.jsx` dibuja los controles a partir de una configuración y prepara el filtro que recibe el listado.
- `GenericFilter.css` define la grilla, los controles segmentados y el panel opcional **Más filtros**.
- `useFiltroListado.js` guarda el filtro aplicado y los valores de los controles en Redux, separados por `claveFiltro`.
- Cada módulo declara sus campos en un componente como `FiltroEscuelas.jsx` o `FiltroHabilitaciones.jsx` y pasa esa configuración a `GenericFilter`.

## Propiedades de `GenericFilter`

| Propiedad | Uso |
|---|---|
| `configuracion` | Lista de campos; determina qué controles aparecen y cómo se envían. |
| `filtroInicial` | Condiciones base que se agregan cuando se aplica sin completar campos. |
| `postFijo` | Condiciones que se agregan siempre y tienen prioridad si repiten una clave. |
| `claveFiltro` | Identificador único del listado para guardar y recuperar su estado. Conviene definirlo explícitamente. |
| `predictivo` | Si es `true`, aplica los cambios automáticamente tras 400 ms. Los botones **Limpiar** y **Aplicar** siguen disponibles. |

## Configurar un campo

Cada elemento de `configuracion` usa `clave`, `etiqueta` y `tipo`. Según el tipo, también puede usar:

- `placeholder`: texto de ayuda.
- `opciones`: opciones de un `select`, `list` o `tristate`. Para opciones con valor y texto visible se usa `{ value, label }`.
- `forzarSelect: true`: muestra un desplegable aunque las opciones todavía no hayan cargado.
- `masFiltros: true`: ubica el campo dentro del panel plegable **Más filtros**. Si se omite, queda en la zona principal.
- `columnSpan: 2`: hace que el campo ocupe dos columnas en pantallas de escritorio (992 px o más).
- `valor: 'all'`: valor inicial para un campo `tristate`; también es el valor al que vuelve al limpiar.

### Tipos de control

| `tipo` | Control y valor enviado |
|---|---|
| `str` | Texto. Se envía como cadena. La interpretación de búsqueda depende del listado/backend. |
| `number` | Número entero; se convierte con `parseInt`. |
| `list` / `select` | Desplegable. `opciones` puede ser una lista de cadenas u objetos `{ value, label }`. Si no hay opciones y no se fuerza el select, se muestra texto. |
| `checkbox` | Switch de dos estados. Marcado envía `true`; desmarcado omite el campo. No sirve para filtrar explícitamente por `false`. |
| `tristate` | Selector de tres opciones. `all` omite el campo; `true` y `false` se convierten a booleanos al aplicar. |
| Otro tipo | Usa el campo de texto genérico. Para controles especiales, hay que agregar un caso en `renderInput`. |

## Ejemplo: filtro Bloqueo

Este campo muestra **Todos · Sí · No**, dentro de **Más filtros**:

```js
{
  clave: 'bloqueo',
  etiqueta: 'Bloqueo',
  tipo: 'tristate',
  masFiltros: true,
  valor: 'all',
  opciones: [
    { value: 'all', label: 'Todos' },
    { value: 'true', label: 'Sí', indicador: 'positivo' },
    { value: 'false', label: 'No', indicador: 'neutro' },
  ],
}
```

- **Todos** no incluye `bloqueo` en el filtro enviado.
- **Sí** incluye `{ bloqueo: true }`.
- **No** incluye `{ bloqueo: false }`.
- Si **Sí** o **No** están seleccionados y el panel está cerrado, el botón muestra el valor activo como resumen.
- **Limpiar** vuelve al valor configurado en `valor` (`all` en este ejemplo).

Los indicadores disponibles para `tristate` son `positivo` (verde) y `neutro` (gris). Se pueden omitir para mostrar una opción sin punto.

## Agregar, quitar o mover filtros

1. Abrir la configuración del módulo, por ejemplo `components/Escuelas/FiltroEscuelas.jsx`.
2. Agregar o quitar un objeto de `configuracion` para incluir o eliminar un campo.
3. Para mover un campo a **Más filtros**, agregar `masFiltros: true`. Para devolverlo a la zona principal, quitar esa propiedad.
4. Agregar `columnSpan: 2` solo si necesita más ancho en escritorio; en pantallas menores el campo vuelve a ocupar una columna.

No hay que editar el JSX de `GenericFilter` para mover campos entre zonas. El filtro completo sigue participando en **Aplicar**, **Limpiar**, el guardado de estado y la aplicación predictiva, aunque esté plegado.

## Cómo se arma y guarda la búsqueda

1. Los campos empiezan vacíos; `checkbox` empieza desmarcado y `tristate` empieza en `valor` (o `all`). Si hay valores guardados para `claveFiltro`, se restauran. También se convierten los valores booleanos antiguos de `tristate` para conservar selecciones previas.
2. Al aplicar, los campos vacíos se omiten. `tristate` convierte los textos `true` y `false` a booleanos, y omite `all`.
3. Se agregan las condiciones de `postFijo`. Si no se completó ningún filtro y existe `filtroInicial`, se agrega también.
4. El filtro enviado y los valores de controles se guardan por `claveFiltro`, para que distintos listados no compartan selecciones.
5. **Limpiar** vacía los campos, restaura `checkbox` y `tristate` a sus valores iniciales, y aplica `filtroInicial` junto con `postFijo`.

### Particularidad de Acreditaciones

En `ListarEscuelas.jsx`, `activo: true` se agrega como condición fija. Por eso **Bloqueo: Todos** muestra acreditaciones activas bloqueadas y desbloqueadas; no incluye registros inactivos.
