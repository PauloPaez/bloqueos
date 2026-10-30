**Cambios implementados para motivos**
- El campo motivo del modal de escuelas solo se habilita cuando bloqueo está activo.
- Se agregó la edición de fecha_baja mediante calendario.
- La fecha se muestra en formato dd/mm/yyyy.
- La fecha es opcional según la configuración del motivo.
- Se agregó lleva_fecha al modelo de motivos.
- Los motivos existentes sin ese campo se consideran automáticamente como lleva_fecha=false.
- Si un motivo requiere fecha, el backend valida que fecha_baja esté completa.
- Si el motivo no requiere fecha, la fecha se limpia automáticamente.
**Bloqueo masivo por DNI**
**Para los motivos “Baja por jubilación” y “Baja por fallecimiento”:**
- Se muestra la opción para bloquear todos los padrones activos correspondientes al DNI.
- Se solicita confirmación antes de ejecutar la acción.
- Se actualizan todos los registros activos del mismo DNI.
- Se sobrescriben el motivo y la fecha elegidos.
- Los registros inactivos no se modifican.
- Se informa la cantidad de registros actualizados.
**Padrón**
- Se agregó el campo DV Padrón al modal.
- El padrón y su dígito verificador se muestran combinados, por ejemplo: 463359/4.
- Los campos Padrón y DV Padrón quedaron bloqueados para edición.
Exportación de documentos
- Excel y DOCX ahora agregan la fecha al motivo únicamente cuando el motivo tiene lleva_fecha=true.
- Se eliminó la lógica fija que dependía del texto "baja".
- La configuración de motivos se carga antes de generar los documentos y se reutiliza en el formateador común.
**Actualización automática de motivos**
- Se corrigió el websocket de motivos.
- El listado de motivos ahora se actualiza automáticamente después de crear o modificar un motivo, sin tener que volver a aplicar el filtro.
**Corrección de valores booleanos**
- Se corrigió el caso en que bloquear_todos_padrones_dni se enviaba como null.
- Ahora se envía como false cuando no está seleccionado, sin alterar otros campos como activo.
*Nota: los cambios relacionados con el botón para desbloquear todos los padrones por DNI quedaron guardados en un stash y no forman parte de la implementación activa actual.*

**Carga de acreditaciones desde Habilitaciones**

- Grabar (POST) valida el período y el cierre manual del último período activo, descarga por SFTP, genera el JSON, importa y registra la habilitación al final. Actualizar (PATCH/PUT) no ejecuta los scripts.
- Los períodos se comparan con las habilitaciones activas registradas; no se aceptan períodos iguales o anteriores. Los documentos de una carga parcial en `Escuelas` no definen un período completado. La fecha de cierre no cierra automáticamente un período.
- El cierre manual se realiza desde el listado de escuelas, para el único período mostrado en la tabla. El backend comprueba que tenga acreditaciones activas y una única habilitación activa, y permite cerrar hasta la fecha y hora de `fecha_cierre` y `hora_cierre`, según la hora de Argentina. Las habilitaciones antiguas sin `hora_cierre` siguen vigentes hasta el final del día de `fecha_cierre`. Si no tiene fecha o el plazo venció, informa el motivo y no cierra.
- Habilitaciones permite modificar sus datos, pero PATCH/PUT rechazan cambios de `cerrado`; ese estado solo lo cambia la acción de cierre de escuelas. El cierre copia las acreditaciones activas bloqueadas a `BloqueadosHistoricos` y verifica su cantidad antes de marcar la habilitación como cerrada. No modifica las acreditaciones de `Escuelas`.
- `ControlCargas` reserva la operación completa con `_id: "padrones"`. Al terminar se elimina ese documento. No tiene vencimiento automático para evitar liberar una carga que todavía trabaja.
- La importación valida todo el JSON, vacía los documentos de `Escuelas` con `delete_many({})` e inserta por lotes de 10.000. Se conservan los índices y opciones; no se crea ni renombra una colección temporal.
- Después de confirmar la importación y el registro de la habilitación, se eliminan únicamente las fuentes y el JSON locales de ese período, antes de liberar `ControlCargas`. Si la carga falla, los archivos se conservan. Si falla una eliminación, se registra el error y se continúa con los demás archivos, sin informar la carga como fallida. No se borran archivos remotos ni se limpian automáticamente períodos anteriores.
- Durante la inserción `Escuelas` puede estar vacía o parcial. Una carga incompleta no debe utilizarse para trabajar con acreditaciones. `ControlCargas` impide otra carga, pero no bloquea por sí sola las consultas o ediciones de escuelas.
- Si una importación o un guardado queda incierto, la reserva conserva el documento de habilitación previsto, incluido su `_id`. Antes de liberar la reserva, comprobar que el proceso terminó y revisar `Escuelas` y ese `_id` en `Habilitaciones`. Si la inserción quedó parcial, después de esa revisión se puede liberar la reserva y reintentar: la importación vuelve a vaciar `Escuelas` antes de cargar, sin duplicar documentos. Si las acreditaciones se cargaron completas pero falta la habilitación, recuperar su registro sin repetir la importación.
- La solicitud permanece abierta hasta terminar. El servidor o proxy debe permitir la duración de descarga, generación e importación. No se configuró ningún proxy desde este cambio.
- Los cierres nuevos guardan `historico_generado`, `cantidad_bloqueadas` y `fecha_cierre_real` en la habilitación. Si no hay bloqueados, se registra cantidad cero. Los períodos cerrados antes de esta implementación no generan un histórico automáticamente.

**TXT por archivo de origen al cerrar — prueba local temporal**

- Se quitó el botón Descargar TXT y el endpoint que reunía todos los bloqueados en un solo archivo. DOCX y Excel siguen disponibles.
- Cerrar período selecciona todos los registros de `Escuelas` con el período solicitado, `activo: true` y `bloqueo: true`, sin paginación ni filtros de pantalla. Esa misma lista se usa para los TXT y el histórico.
- Se genera un TXT por `tipo_archivo` que tenga bloqueados. Ejemplo: `BLOQUEO-TIAC188517.OCTUBRE26.txt`. Mantiene el formato anterior: un padrón con su dígito verificador, sin `/`, por línea, en UTF-8 y sin cabecera. No se generan archivos vacíos ni se eliminan duplicados.
- **El destino activo es local:** `<raíz del repositorio>/datos/OCTUBRE26/Bloqueos/ESCU/`. El período cambia según el cierre. La acción no abre SFTP ni lee sus credenciales. Los archivos de `datos/` están excluidos de Git.
- Para probar desde la pantalla, usar un período abierto, dentro del plazo y con bloqueados. Confirmar Cerrar período y revisar esa carpeta, el histórico y la habilitación cerrada. Esto sí modifica la base configurada del backend. Las pruebas automatizadas usan carpetas temporales y conexiones simuladas.
- El código temporal está marcado con `PRUEBA LOCAL TEMPORAL` en `utils/padrones/archivosCierre.py`, en la llamada del cierre y en el aviso de `front/src/components/Escuelas/CierrePeriodo.jsx`. La asignación `guardar_txt_cierre = guardar_txt_local_prueba` es la que activa la prueba. Para activar SFTP más adelante, reemplazarla por `guardar_txt_cierre = guardar_txt_sftp`, actualizar el aviso y retirar el destino local temporal.
- El destino SFTP está implementado pero **no está activo**: usa el mismo servidor y credenciales de descarga, con la ruta absoluta `/datos/PERIODO/Bloqueos/ESCU/`, independientemente de `DIR_REMOTO`. Exige que `/datos/PERIODO/` exista y crea únicamente las subcarpetas faltantes de salida.
- Ambos destinos rechazan nombres existentes y crean los archivos en modo exclusivo, sin sobrescribirlos. El período se marca cerrado después de completar los TXT y el histórico. Sin bloqueados, cierra con cantidad cero y sin TXT.
- Ante un fallo se intentan borrar únicamente los TXT creados por ese intento, eliminar sus copias históricas y restaurar los campos de cierre si la actualización pudo haberse aplicado. Las carpetas vacías creadas pueden permanecer. MongoDB y el destino de archivos no comparten una transacción: un corte del proceso o de la conexión puede requerir revisión manual.
- El cierre usa la reserva `ControlCargas` con `_id: "padrones"`, `operacion: "cierre"`, `habilitacion_id` e `intento`. Esto impide otra carga o cierre simultáneo. Si falla la recuperación, conserva la reserva e informa que quedó pendiente de revisión. Revisar la habilitación, sus copias históricas y los TXT del intento antes de liberar esa reserva; no borrar archivos ajenos o preexistentes. Si solo falla la liberación final, revisar si el cierre ya fue confirmado antes de reintentar.

**Consulta de bloqueados históricos**

- `GET /bloqueados-historicos/?page=1&page_size=10` lista los cierres con histórico confirmado, incluidos los de cantidad cero y los de habilitaciones luego desactivadas.
- `GET /bloqueados-historicos/{habilitacion_id}/?page=1&page_size=10` muestra las copias de ese cierre. Se usa el ID de la habilitación devuelto en el listado, no el nombre del período. Ambas consultas admiten hasta 100 registros por página. Este router no expone operaciones de escritura.
- Cada copia conserva los campos originales y agrega `escuela_id`, `habilitacion_id` y `fecha_cierre_real`. Su `_id` combina habilitación y acreditación para distinguir cierres. Se crea un índice en `habilitacion_id` para las consultas.
- Si falla la copia, se intenta eliminar el histórico parcial y los TXT del intento; la habilitación no se confirma como cerrada. Si falla esa recuperación, se conserva la reserva para revisión. Si ya está cerrado, no se vuelve a generar la copia ni se reenvían los TXT.
- Esta versión no agrega una transacción o un bloqueo compartido entre cierre y edición. La coordinación de operaciones simultáneas sigue pendiente; las validaciones previas de edición no cubren una escritura que ya estuviera en curso al comenzar el cierre. La pantalla del módulo también queda pendiente.
