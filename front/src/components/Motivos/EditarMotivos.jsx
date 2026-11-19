import React, { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { usePostMotivosMutation, usePatchMotivosMutation, useGetMotivosQuery } from '../../store/apiSlice';
import { useSelector, useDispatch } from 'react-redux';
import { resetModulo } from '../../store/appSlice';
import { formularioCampos } from './FormularioEditar';
import { obtenerCamposAValidar } from './camposValidacion';
import { Modal } from 'react-bootstrap';
import { Plus, Save } from 'lucide-react';
import { toast } from 'sonner';
import './EditarMotivos.css';

// Minúsculas y sin acentos, para que "liquidacion" coincida con "Liquidación".
const normalizar = (texto) =>
  (texto ?? '').trim().toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');

const EditarMotivos = () => {
  const dispatch = useDispatch();
  const user = useSelector((state) => state.acceso.user);
  const { datos: filaSeleccionada, mostrarModal } = useSelector(
    (state) => state.modulos.motivos
  );
  const esEdicion = Boolean(filaSeleccionada?.id);

// TODO: Arreglar problema al actualizar motivos, activo = false no aparece
  const [postMotivos] = usePostMotivosMutation();
  const [patchMotivos] = usePatchMotivosMutation();
  const { data: motivos = [] } = useGetMotivosQuery();
  const [faltanDatos, setFaltanDatos] = useState(false);

  // Valores de un motivo nuevo. Se pasan siempre a reset(): reset(valores) de la
  // edición reemplaza los valores por defecto, y un reset() vacío volvería a
  // cargar el último motivo editado.
  const formularioVacio = { motivos: [{ motivo: '', lleva_fecha: false }] };

  const { register, handleSubmit, reset, watch, formState: { isDirty } } = useForm({
    defaultValues: formularioVacio,
  });

  useEffect(() => {
    dispatch(resetModulo({ modulo: 'motivos' }));
  }, [dispatch]);

  const camposVisibles = formularioCampos.filter((field) => {
    if (field.placeholder === 'no_visible') return false;

    // El campo 'activo' solo se muestra si hay fila seleccionada
    if (field.name === 'activo' && !esEdicion) {
      return false;
    }
    return true;
  });
  const camposTexto = camposVisibles.filter((field) => field.type !== 'checkbox');
  const camposSwitch = camposVisibles.filter((field) => field.type === 'checkbox');

  // Cada vez que se abre el modal: carga la fila elegida o deja el formulario vacío.
  // Se usa reset con valores para que isDirty compare contra los datos originales.
  useEffect(() => {
    if (!mostrarModal) return;
    setFaltanDatos(false);

    if (esEdicion) {
      const valores = {};
      camposVisibles.forEach((field) => {
        valores[field.name] = filaSeleccionada[field.name] ?? null;
      });
      reset({ motivos: [valores] });
    } else {
      reset(formularioVacio);
    }
  }, [mostrarModal, filaSeleccionada]);

  // Avisa mientras se escribe si otro motivo de la empresa ya usa ese nombre.
  const motivoEscrito = watch('motivos.0.motivo') ?? '';
  const motivoDuplicado =
    normalizar(motivoEscrito) !== '' &&
    motivos.some(
      (item) =>
        item.id !== filaSeleccionada?.id &&
        item.empresa === user.empresa &&
        normalizar(item.motivo) === normalizar(motivoEscrito)
    );

  const errorMotivo = motivoDuplicado
    ? 'Ya existe un motivo con ese nombre.'
    : faltanDatos && !motivoEscrito
      ? 'Ingresá el nombre del motivo.'
      : null;

  const controlDatosFormulario = (motivos) => {
    const camposAValidar = obtenerCamposAValidar();

    return camposAValidar.some((fieldName) => {
      const value = motivos[fieldName];
      return value === undefined || value === null || value === '';
    });
  };

  const onSubmit = async (data) => {
    try {
      const motivos = data.motivos?.[0];

      if (!motivos || controlDatosFormulario(motivos)) {
        setFaltanDatos(true);
        return;
      }

      if (motivoDuplicado) return;

      const motivosData = {
        ...motivos,
        empresa: user.empresa,
        login: user.login,
        ...(esEdicion ? {} : { activo: true }),
      };

      if (esEdicion) {
        await patchMotivos({
          id: filaSeleccionada.id,
          ...motivosData,
        }).unwrap();

        const seDesactivo = filaSeleccionada.activo && !motivos.activo;
        toast.success('Motivo actualizado.', {
          description: seDesactivo
            ? `"${motivos.motivo}" quedó inactivo y ya no se ofrecerá al bloquear escuelas.`
            : undefined,
        });
      } else {
        await postMotivos(motivosData).unwrap();
        toast.success('Motivo creado.');
      }

      handleReset();
    } catch (error) {
      console.error('Error al enviar datos:', error);
      toast.error('No se pudo guardar el motivo.');
    }
  };

  const handleReset = () => {
    reset(formularioVacio);
    dispatch(resetModulo({ modulo: 'motivos' }));
  };

  const sinCambios = esEdicion && !isDirty;

  return (
    <Modal
      show={Boolean(mostrarModal)}
      onHide={handleReset}
      backdrop="static"
      centered
      dialogClassName="motivo-dialog"
    >
      <Modal.Header closeButton className="motivo-header">
        <div>
          <Modal.Title className="motivo-title">
            {esEdicion ? 'Editar motivo' : 'Nuevo motivo'}
          </Modal.Title>
          <p className="motivo-description">
            {esEdicion
              ? 'Los cambios se aplican a los próximos bloqueos.'
              : 'Quedará disponible al bloquear escuelas.'}
          </p>
        </div>
      </Modal.Header>

      <Modal.Body className="motivo-body">
        <form className="motivo-form" onSubmit={handleSubmit(onSubmit)} noValidate>
          <hr className="motivo-separator" />

          {camposTexto.map((field) => {
            const valor = watch(`motivos.0.${field.name}`) ?? '';
            const mostrarContador =
              field.maxLength && valor.length >= field.maxLength * 0.8;
            const error = field.name === 'motivo' ? errorMotivo : null;

            return (
              <div key={field.name} className="motivo-field">
                <div className="motivo-label-row">
                  <label className="motivo-label" htmlFor={`motivo-${field.name}`}>
                    {field.label}
                  </label>
                  {mostrarContador && (
                    <span className="motivo-counter">
                      {valor.length}/{field.maxLength}
                    </span>
                  )}
                </div>
                <input
                  id={`motivo-${field.name}`}
                  type={field.type}
                  className={`form-control motivo-control ${error ? 'is-invalid' : ''}`}
                  placeholder={field.placeholder}
                  maxLength={field.maxLength}
                  autoComplete="off"
                  autoFocus={!esEdicion}
                  {...register(`motivos.0.${field.name}`)}
                />
                {error && <p className="motivo-error">{error}</p>}
              </div>
            );
          })}

          {camposSwitch.length > 0 && (
            <div className="motivo-switches">
              {camposSwitch.map((field) => (
                <div key={field.name} className="motivo-switch-row">
                  <div>
                    <label className="motivo-label" htmlFor={`motivo-${field.name}`}>
                      {field.label}
                    </label>
                    {field.descripcion && (
                      <p className="motivo-switch-description">{field.descripcion}</p>
                    )}
                  </div>
                  <div className="form-check form-switch m-0 p-0">
                    <input
                      id={`motivo-${field.name}`}
                      type="checkbox"
                      role="switch"
                      className="form-check-input motivo-switch"
                      {...register(`motivos.0.${field.name}`)}
                    />
                  </div>
                </div>
              ))}
            </div>
          )}

          <hr className="motivo-separator" />

          <div className="motivo-footer">
            <button type="button" className="btn btn-outline-dark motivo-cancel" onClick={handleReset}>
              Cancelar
            </button>
            <button
              type="submit"
              className="btn btn-dark motivo-submit"
              disabled={sinCambios}
              title={sinCambios ? 'No hay cambios para guardar' : undefined}
            >
              {esEdicion ? <Save size={16} aria-hidden="true" /> : <Plus size={16} aria-hidden="true" />}
              {esEdicion ? 'Guardar cambios' : 'Crear motivo'}
            </button>
          </div>
        </form>
      </Modal.Body>
    </Modal>
  );
};

export default EditarMotivos;
