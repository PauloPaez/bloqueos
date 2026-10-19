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
- `ControlCargas` reserva la operación completa con `_id: "padrones"`. Al terminar se elimina ese documento. No tiene vencimiento automático para evitar liberar una carga que todavía trabaja.
- La importación valida todo el JSON, vacía los documentos de `Escuelas` con `delete_many({})` e inserta por lotes de 10.000. Se conservan los índices y opciones; no se crea ni renombra una colección temporal.
- Durante la inserción `Escuelas` puede estar vacía o parcial. Una carga incompleta no debe utilizarse para trabajar con acreditaciones. `ControlCargas` impide otra carga, pero no bloquea por sí sola las consultas o ediciones de escuelas.
- Si una importación o un guardado queda incierto, la reserva conserva el documento de habilitación previsto, incluido su `_id`. Antes de liberar la reserva, comprobar que el proceso terminó y revisar `Escuelas` y ese `_id` en `Habilitaciones`. Si la inserción quedó parcial, después de esa revisión se puede liberar la reserva y reintentar: la importación vuelve a vaciar `Escuelas` antes de cargar, sin duplicar documentos. Si las acreditaciones se cargaron completas pero falta la habilitación, recuperar su registro sin repetir la importación.
- La solicitud permanece abierta hasta terminar. El servidor o proxy debe permitir la duración de descarga, generación e importación. No se configuró ningún proxy desde este cambio.
- El histórico de bloqueados sigue pendiente. Por ahora se exige el cierre manual, pero no se comprueba que exista un histórico: la carga elimina las acreditaciones anteriores sin respaldo completo.
