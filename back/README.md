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