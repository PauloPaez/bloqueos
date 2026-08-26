import React, { useEffect, useRef, useState } from 'react';
import { useForm } from 'react-hook-form';
import {
  usePostEscuelasMutation,
  usePatchEscuelasMutation,
  useGetDistinctMotivosQuery,
} from '../../store/apiSlice';
import { useSelector, useDispatch } from 'react-redux';
import { resetModulo } from '../../store/appSlice';
import { formularioCampos } from './FormularioEditar';
import { separadoresFormulario } from './formularioSeparadores';
import { obtenerCamposAValidar } from './camposValidacion';
import { Modal } from "react-bootstrap";
import { Calendar, Save } from "lucide-react";
import './EditarEscuelas.css';

const formatearFecha = (fecha) => {
  if (!fecha) return '';

  const [anio, mes, dia] = fecha.split('T')[0].split('-');
  return anio && mes && dia ? `${dia}/${mes}/${anio}` : '';
};

const convertirFecha = (fecha) => {
  const coincidencia = fecha.match(/^(\d{2})\/(\d{2})\/(\d{4})$/);
  if (!coincidencia) return '';

  const [, dia, mes, anio] = coincidencia;
  const fechaValida = new Date(`${anio}-${mes}-${dia}T00:00:00`);
  if (
    fechaValida.getFullYear() !== Number(anio) ||
    fechaValida.getMonth() + 1 !== Number(mes) ||
    fechaValida.getDate() !== Number(dia)
  ) {
    return '';
  }

  return `${anio}-${mes}-${dia}`;
};

const EditarEscuelas = () => {
  const dispatch = useDispatch();
  const user = useSelector((state) => state.acceso.user);
  const filaSeleccionada = useSelector(
    (state) => state.modulos.escuelas).datos


  const [postEscuelas] = usePostEscuelasMutation();
  const [patchEscuelas] = usePatchEscuelasMutation();
  const {
    data: motivos = [],
    isLoading: motivosLoading,
    isError: motivosError,
  } = useGetDistinctMotivosQuery('motivo');

  const { register, handleSubmit, setValue, reset, watch } = useForm({
    defaultValues: {
      escuelas: [{}],
    },
  });

  const bloqueoSeleccionado = watch('escuelas.0.bloqueo', false);
  const fechaBaja = watch('escuelas.0.fecha_baja', '');
  const [fechaBajaTexto, setFechaBajaTexto] = useState('');
  const fechaBajaPickerRef = useRef(null);

  useEffect(() => {
    dispatch(resetModulo({ modulo: 'escuelas' }));
  }, [dispatch]);

  const camposVisibles = formularioCampos.filter((field) => {
    if (field.placeholder === 'no_visible') return false;

    // El campo 'activo' solo se muestra si hay fila seleccionada
    if (field.name === 'activo' && !filaSeleccionada?.id) {
      return false;
    }
    return true;
  });


  useEffect(() => {
    if (filaSeleccionada?.id) {
      camposVisibles.forEach((field) => {
        if (field.type === 'date') {
          setFechaBajaTexto(formatearFecha(filaSeleccionada[field.name]));
          setValue(
            `escuelas.0.${field.name}`,
            filaSeleccionada[field.name]
              ? filaSeleccionada[field.name].split('T')[0]
              : null
          );
        } else {
          setValue(
            `escuelas.0.${field.name}`,
            filaSeleccionada[field.name] ?? null
          );
        }
      });
    } else {
      setFechaBajaTexto('');
      reset();
    }
  }, [filaSeleccionada]);

  const controlDatosFormulario = (escuelas) => {
    const camposAValidar = obtenerCamposAValidar();

    return camposAValidar.some((fieldName) => {
      const value = escuelas[fieldName];
      return value === undefined || value === null || value === '';
    });
  };

  const onSubmit = async (data) => {
    try {
      const escuelas = data.escuelas?.[0];

      if (!escuelas || controlDatosFormulario(escuelas)) {
        alert('⚠️ Faltan completar datos formulario');
        return;
      }

      const escuelasData = {
        ...escuelas,
        empresa: user.empresa,
        login: user.login,
        ...(filaSeleccionada?.id ? {} : { activo: true })
      };

      if (filaSeleccionada?.id) {
        await patchEscuelas({
          id: filaSeleccionada.id,
          ...escuelasData,
        }).unwrap();

        dispatch(resetModulo({ modulo: 'escuelas' }));
      } else {
        await postEscuelas(escuelasData).unwrap();
      }

      reset();
    } catch (error) {
      console.error('Error al enviar datos:', error);
    }
  };

  const handleReset = () => {
    reset();
    dispatch(resetModulo({ modulo: 'escuelas' }));
  };



  return (
  <Modal
    show={!!filaSeleccionada?.id}
    onHide={handleReset}
    backdrop="static"
    centered
    dialogClassName="edit-school-dialog"
  >
    <Modal.Header closeButton className="edit-school-header">
      <Modal.Title className="edit-school-title">Editar Escuela</Modal.Title>
    </Modal.Header>

    <Modal.Body className="edit-school-body">
      <form className="edit-school-form" onSubmit={handleSubmit(onSubmit)}>
        {camposVisibles.map((field) => {
          const separador = separadoresFormulario.find(
            (s) => s.before === field.name
          );

          const fieldProps = {
            ...register(`escuelas.0.${field.name}`),
            disabled:
              field.disabled ||
              (['motivo', 'fecha_baja'].includes(field.name) && !bloqueoSeleccionado),
            placeholder:
              field.placeholder !== "no_visible"
                ? field.placeholder
                : undefined,
          };

          return (
            <React.Fragment key={field.name}>
              {separador && (
                <div className="edit-school-section">
                  <hr />
                  {separador.label && <div className="edit-school-section-label">{separador.label}</div>}
                </div>
              )}

              <div
                className={field.type === "checkbox" ? "edit-school-field edit-school-switch-row" : "edit-school-field"}
              >
                {field.type !== "checkbox" && (
                  <label className="edit-school-label" htmlFor={`edit-${field.name}`}>{field.label}</label>
                )}

                {field.type === "date" ? (
                  <div className="edit-school-date-picker">
                    <input
                      id={`edit-${field.name}`}
                      type="text"
                      inputMode="numeric"
                      placeholder="dd/mm/yyyy"
                      className="form-control edit-school-control"
                      value={fechaBajaTexto}
                      disabled={fieldProps.disabled}
                      onChange={(event) => {
                        const texto = event.target.value;
                        setFechaBajaTexto(texto);
                        setValue(
                          `escuelas.0.${field.name}`,
                          convertirFecha(texto),
                          { shouldDirty: true }
                        );
                      }}
                    />
                    <input
                      type="date"
                      className="edit-school-native-date-picker"
                      {...fieldProps}
                      ref={(element) => {
                        fieldProps.ref(element);
                        fechaBajaPickerRef.current = element;
                      }}
                      value={fechaBaja || ''}
                      onChange={(event) => {
                        fieldProps.onChange(event);
                        setFechaBajaTexto(formatearFecha(event.target.value));
                      }}
                      aria-label="Seleccionar fecha"
                    />
                    <button
                      type="button"
                      className="edit-school-date-button"
                      onClick={() => {
                        const picker = fechaBajaPickerRef.current;
                        if (picker?.showPicker) picker.showPicker();
                        else picker?.click();
                      }}
                      disabled={fieldProps.disabled}
                      aria-label="Abrir calendario"
                    >
                      <Calendar size={18} aria-hidden="true" />
                    </button>
                  </div>
                ) : field.type === "select" ? (
                  <select id={`edit-${field.name}`} className="form-select edit-school-control" {...fieldProps}>
                    <option value="">
                      {motivosLoading
                        ? 'Cargando motivos...'
                        : motivosError
                          ? 'No se pudieron cargar los motivos'
                          : `Seleccione ${field.label.toLowerCase()}`}
                    </option>
                    {field.optionsKey === 'motivos' && motivos.map((motivo) => (
                      <option key={motivo} value={motivo}>
                        {motivo}
                      </option>
                    ))}
                  </select>
                ) : field.type === "checkbox" ? (
                  <>
                    <label className="edit-school-label" htmlFor={`edit-${field.name}`}>{field.label}</label>
                    <input id={`edit-${field.name}`} type="checkbox" className="form-check-input edit-school-switch" {...fieldProps} />
                  </>
                ) : (
                  <input
                    id={`edit-${field.name}`}
                    type={field.type === "float" ? "number" : field.type}
                    step={field.type === "float" ? "any" : undefined}
                    className="form-control edit-school-control"
                    {...fieldProps}
                  />
                )}
              </div>
            </React.Fragment>
          );
        })}

        <hr className="edit-school-footer-separator" />
        <div className="edit-school-footer">
          <button
            type="button"
            className="btn btn-outline-dark cerrar-btn"
            onClick={handleReset}
          >
            Cerrar
          </button>

          <button
            type="submit"
            className="btn btn-primary edit-school-submit"
          >
            <Save size={16} aria-hidden="true" />
            {filaSeleccionada?.id ? "Actualizar" : "Grabar"}
          </button>
        </div>
      </form>
    </Modal.Body>

  </Modal>
    );
};

export default EditarEscuelas;
