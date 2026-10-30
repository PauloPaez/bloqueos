import { useState } from 'react';
import { Modal } from 'react-bootstrap';
import { CalendarClock, CheckCircle2, Lock, TriangleAlert } from 'lucide-react';
import './CierrePeriodo.css';

function nombrePeriodo(periodo) {
  const partes = periodo?.match(/^([A-Z]+)(\d{2})$/);
  if (!partes) return periodo;
  const mes = partes[1].toLowerCase().replace('setiembre', 'septiembre');
  return `${mes[0].toUpperCase()}${mes.slice(1)} 20${partes[2]}`;
}

function fechaLimite(fecha, hora) {
  // La API entrega una fecha sin hora: no convertirla a UTC ni desplazar el día.
  const fechaFormateada = fecha ? fecha.split('-').reverse().join('/') : 'Sin fecha definida';
  return hora ? `${fechaFormateada} a las ${hora}` : fechaFormateada;
}

function textoRestante(segundos) {
  if (!Number.isFinite(segundos)) return 'No se pudo consultar el tiempo restante';
  if (segundos < 3600) return 'Queda menos de una hora para cerrar el período';
  const horasTotales = Math.floor(segundos / 3600);
  const dias = Math.floor(horasTotales / 24);
  const horas = horasTotales % 24;
  if (dias === 0) return `Quedan ${horasTotales} ${horasTotales === 1 ? 'hora' : 'horas'} para cerrar el período`;
  const textoDias = `${dias} ${dias === 1 ? 'día' : 'días'}`;
  const textoHoras = horas > 0 ? ` y ${horas} ${horas === 1 ? 'hora' : 'horas'}` : '';
  return `Quedan ${textoDias}${textoHoras} para cerrar el período`;
}

export function AvisoCierrePeriodo({ estado }) {
  if (!estado) return null;
  const dias = estado.dias_restantes;
  const tipo = estado.cerrado ? 'cerrado' : estado.vencido ? 'vencido' : dias === null ? 'aviso' : dias > 7 ? 'normal' : 'aviso';
  const Icono = estado.cerrado ? CheckCircle2
    : tipo === 'normal' ? CalendarClock
    : tipo === 'vencido' ? Lock : TriangleAlert;
  const mensaje = estado.cerrado ? 'Período cerrado'
    : dias === null ? 'El período no tiene fecha de cierre'
    : estado.vencido ? 'El plazo de cierre venció'
    : textoRestante(estado.segundos_restantes);
  const detalle = tipo === 'normal'
    ? mensaje
    : estado.cerrado
      ? `${estado.cantidad_bloqueadas} acreditaciones bloqueadas`
      : `Fecha límite: ${fechaLimite(estado.fecha_limite, estado.hora_limite)}`;
  const textoPrincipal = tipo === 'normal'
    ? `Fecha límite de cierre: ${fechaLimite(estado.fecha_limite, estado.hora_limite)}`
    : mensaje;
  return (
    <div className={`periodo-aviso periodo-aviso-${tipo}`} role={tipo === 'normal' || tipo === 'cerrado' ? 'status' : 'alert'}
      title={`${nombrePeriodo(estado.periodo)} · ${mensaje} · Fecha límite: ${fechaLimite(estado.fecha_limite, estado.hora_limite)}`}>
      <Icono size={16} aria-hidden="true" />
      <p>
        <span className="periodo-detalle">{nombrePeriodo(estado.periodo)} · </span>
        <strong>{textoPrincipal}</strong>
        <span className="periodo-detalle periodo-detalle-amplio">
          {' · '}{detalle}
        </span>
      </p>
    </div>
  );
}

export function BotonCierrePeriodo({ estado, disabled, consultando, cerrando, error, onAbrir, onConfirmar }) {
  const [mostrar, setMostrar] = useState(false);
  const abrir = () => {
    setMostrar(true);
    onAbrir();
  };
  const confirmar = async () => {
    if (await onConfirmar()) setMostrar(false);
  };
  return (
    <>
      <button type="button" className="btn btn-dark periodo-boton" onClick={abrir}
        disabled={disabled} title={estado?.mensaje}>
        {estado?.cerrado ? <CheckCircle2 size={16} aria-hidden="true" /> : <Lock size={16} aria-hidden="true" />}
        {estado?.cerrado ? 'Período cerrado' : 'Cerrar período'}
      </button>
      <Modal show={mostrar} onHide={() => !cerrando && setMostrar(false)} centered
        backdrop={cerrando ? 'static' : true} keyboard={!cerrando}
        contentClassName="periodo-dialogo" aria-labelledby="cierre-periodo-titulo"
        aria-describedby="cierre-periodo-descripcion">
        <Modal.Header>
          <Modal.Title id="cierre-periodo-titulo">¿Cerrar el período {nombrePeriodo(estado?.periodo)}?</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p id="cierre-periodo-descripcion">Se cerrará la habilitación de este período. Revise las acreditaciones bloqueadas antes de confirmar.</p>
          {/* PRUEBA LOCAL TEMPORAL: actualizar este aviso al activar el envío SFTP. */}
          <p>Se guardará un TXT por archivo de origen que tenga bloqueados, dentro del repositorio en
            {' '}<code>datos/{estado?.periodo}/Bloqueos/ESCU/</code>. Durante esta prueba no se enviarán archivos al servidor SFTP.</p>
          <div className="periodo-conteo" aria-live="polite">
            <strong>{consultando ? '…' : estado?.cantidad_bloqueadas?.toLocaleString('es-AR')}</strong>
            <span>acreditaciones bloqueadas en el período</span>
          </div>
          <p className="periodo-fecha"><CalendarClock size={14} aria-hidden="true" />
            Fecha límite de cierre: {fechaLimite(estado?.fecha_limite, estado?.hora_limite)}.
          </p>
          {error && <div className="alert alert-danger mb-0" role="alert">{error}</div>}
          {!error && estado && !estado.puede_cerrar && <p role="alert">{estado.mensaje}</p>}
        </Modal.Body>
        <Modal.Footer>
          <button type="button" className="btn btn-outline-secondary" disabled={cerrando} onClick={() => setMostrar(false)}>Cancelar</button>
          <button type="button" className="btn btn-dark" disabled={disabled || consultando || cerrando}
            onClick={confirmar}>{cerrando ? 'Cerrando…' : consultando ? 'Consultando…' : 'Cerrar período'}</button>
        </Modal.Footer>
      </Modal>
    </>
  );
}
