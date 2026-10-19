import React, { useEffect, useRef, useState } from 'react';
import { useForm } from 'react-hook-form';
import { usePostHabilitacionesMutation, usePatchHabilitacionesMutation } from '../../store/apiSlice';
import { useSelector, useDispatch } from 'react-redux';
import { resetModulo } from '../../store/appSlice';
import { formularioCampos } from './FormularioEditar';
import { separadoresFormulario } from './formularioSeparadores';
import { obtenerCamposAValidar } from './camposValidacion';

const mesesPeriodo = [
  'ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO',
  'JULIO', 'AGOSTO', 'SETIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE',
];

const hoyEnArgentina = () => new Intl.DateTimeFormat('sv-SE', {
  timeZone: 'America/Argentina/Buenos_Aires',
  year: 'numeric', month: '2-digit', day: '2-digit',
}).format(new Date());

const EditarHabilitaciones = () => {
  const dispatch = useDispatch();
  const user = useSelector((state) => state.acceso.user);
  const filaSeleccionada = useSelector(
    (state) => state.modulos.habilitaciones).datos


  const [postHabilitaciones, { isLoading: cargando }] = usePostHabilitacionesMutation();
  const [patchHabilitaciones] = usePatchHabilitacionesMutation();
  const cargaEnCurso = useRef(false);
  const [errorCarga, setErrorCarga] = useState('');

  const { register, handleSubmit, setValue, reset } = useForm({
    defaultValues: {
      habilitaciones: [{}],
      mesPeriodo: '',
      anioPeriodo: '',
    },
  });

  useEffect(() => {
    dispatch(resetModulo({ modulo: 'habilitaciones' }));
  }, [dispatch]);

  const camposVisibles = formularioCampos.filter((field) => {
    if (field.placeholder === 'no_visible') return false;

    // Los estados solo se muestran al editar una habilitación existente.
    if (['activo', 'cerrado'].includes(field.name) && !filaSeleccionada?.id) {
      return false;
    }
    return true;
  });


  useEffect(() => {
    if (filaSeleccionada?.id) {
      camposVisibles.forEach((field) => {
        if (field.name === 'periodo') {
          const periodo = filaSeleccionada.periodo?.toUpperCase().replace('SEPTIEMBRE', 'SETIEMBRE');
          const partes = periodo?.match(/^([A-Z]+)(\d{2})$/);
          setValue('mesPeriodo', partes && mesesPeriodo.includes(partes[1]) ? partes[1] : '');
          setValue('anioPeriodo', partes ? `20${partes[2]}` : '');
        } else if (field.type === 'date' && filaSeleccionada[field.name]) {
          setValue(
            `habilitaciones.0.${field.name}`,
            filaSeleccionada[field.name].split('T')[0]
          );
        } else {
          setValue(
            `habilitaciones.0.${field.name}`,
            filaSeleccionada[field.name] ?? (field.type === 'checkbox' ? false : null)
          );
        }
      });
    } else {
      reset();
    }
  }, [filaSeleccionada]);

  const controlDatosFormulario = (habilitaciones) => {
    const camposAValidar = obtenerCamposAValidar();

    return camposAValidar.some((fieldName) => {
      const value = habilitaciones[fieldName];
      return value === undefined || value === null || value === '';
    });
  };

  const onSubmit = async (data) => {
    if (cargaEnCurso.current) return;
    setErrorCarga('');
    try {
      const { mesPeriodo, anioPeriodo } = data;
      // MESAA representa los años 2000 a 2099 usando sus últimos dos dígitos.
      if (!mesesPeriodo.includes(mesPeriodo) || !/^20\d{2}$/.test(String(anioPeriodo))) {
        alert('Seleccione el mes e ingrese un año entre 2000 y 2099.');
        return;
      }
      const habilitaciones = data.habilitaciones?.[0] && {
        ...data.habilitaciones[0],
        periodo: `${mesPeriodo}${String(anioPeriodo).slice(-2)}`,
      };

      if (!habilitaciones || controlDatosFormulario(habilitaciones)) {
        alert('⚠️ Faltan completar datos formulario');
        return;
      }

      const habilitacionesData = {
        ...habilitaciones,
        empresa: user.empresa,
        login: user.login,
      };

      const fechaAnterior = filaSeleccionada?.fecha_cierre?.split('T')[0] ?? '';
      const fechaCambiada = !filaSeleccionada?.id || habilitaciones.fecha_cierre !== fechaAnterior;
      if (fechaCambiada && habilitaciones.fecha_cierre && habilitaciones.fecha_cierre < hoyEnArgentina()) {
        alert('La fecha de cierre no puede ser anterior a hoy.');
        return;
      }

      if (filaSeleccionada?.id) {
        // No reenviar una fecha histórica sin cambios al editar otro campo.
        if (!fechaCambiada) delete habilitacionesData.fecha_cierre;
        await patchHabilitaciones({
          id: filaSeleccionada.id,
          ...habilitacionesData,
        }).unwrap();

        dispatch(resetModulo({ modulo: 'habilitaciones' }));
      } else {
        cargaEnCurso.current = true;
        await postHabilitaciones({ ...habilitacionesData, activo: true }).unwrap();
        alert('Acreditaciones cargadas y habilitación registrada correctamente.');
      }

      reset();
    } catch (error) {
      console.error('Error al enviar datos:', error);
      const detalle = error?.data?.detail;
      setErrorCarga(typeof detalle === 'string' ? detalle : Array.isArray(detalle)
        ? detalle.map((item) => item.msg).join(' ')
        : 'No se pudo confirmar el guardado. Revise el listado antes de reintentar.');
    } finally {
      cargaEnCurso.current = false;
    }
  };

  const handleReset = () => {
    if (cargaEnCurso.current) return;
    setErrorCarga('');
    reset();
    dispatch(resetModulo({ modulo: 'habilitaciones' }));
  };

  return (
    <form
      style={{
        padding: '20px',
        backgroundColor: filaSeleccionada?.id ? '#fcf4dd' : '#ffffff',
      }}
    >
      {cargando && (
        <div className="alert alert-info" role="status">
          Descargando y cargando acreditaciones. La operación puede tardar varios minutos.
          Espere el resultado antes de cerrar esta pantalla.
        </div>
      )}
      {errorCarga && <div className="alert alert-danger" role="alert">{errorCarga}</div>}
      <fieldset disabled={cargando}>
      {camposVisibles.map((field) => {
        const separador = separadoresFormulario.find(
          (s) => s.before === field.name
        );

        const fieldProps = {
          ...(field.name === 'periodo' ? {} : register(`habilitaciones.0.${field.name}`)),
          disabled: field.disabled || cargando,
          placeholder:
            field.placeholder !== 'no_visible'
              ? field.placeholder
              : undefined,
          min: field.name === 'fecha_cierre' ? hoyEnArgentina() : undefined,
        };

        return (
          <React.Fragment key={field.name}>
            {separador && (
              <div className="my-4">
                <hr className="border border-warning opacity-100" />
                {separador.label && (
                  <div
                    style={{
                      fontWeight: 'bold',
                      color: '#0d6efd',
                      textAlign: 'center',
                      marginTop: '0.5rem',
                    }}
                  >
                    {separador.label}
                  </div>
                )}
              </div>
            )}

            <div
              className={`mb-3 ${
                field.type === 'checkbox' ? 'form-check' : ''
              }`}
            >
              {field.type !== 'checkbox' && (
                <label className="form-label">{field.label}</label>
              )}

              {field.name === 'periodo' ? (
                <div className="row g-2">
                  <div className="col-7">
                    <label className="form-label" htmlFor="habilitaciones-mes">Mes</label>
                    <select
                      id="habilitaciones-mes"
                      className="form-select"
                      {...register('mesPeriodo')}
                    >
                      <option value="">Seleccione mes</option>
                      {mesesPeriodo.map((mes) => (
                        <option key={mes} value={mes}>
                          {mes.charAt(0) + mes.slice(1).toLowerCase()}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="col-5">
                    <label className="form-label" htmlFor="habilitaciones-anio">Año</label>
                    <input
                      id="habilitaciones-anio"
                      type="number"
                      className="form-control"
                      placeholder="2026"
                      min="2000"
                      max="2099"
                      step="1"
                      {...register('anioPeriodo')}
                    />
                  </div>
                </div>
              ) : field.type === 'select' ? (
                <select className="form-control" {...fieldProps}>
                  <option value="">
                    Seleccione {field.label.toLowerCase()}
                  </option>
                  {(datosSelect[field.optionsKey] || []).map((op, i) => (
                    <option key={i} value={op}>
                      {op}
                    </option>
                  ))}
                </select>
              ) : field.type === 'checkbox' ? (
                <>
                  <input
                    type="checkbox"
                    className="form-check-input"
                    {...fieldProps}
                  />
                  <label className="form-check-label">
                    {field.label}
                  </label>
                </>
              ) : (
                <input
                  type={field.type}
                  className="form-control"
                  {...fieldProps}
                />
              )}
            </div>
          </React.Fragment>
        );
      })}

      <div className="d-flex justify-content-between mt-3">
        <button
          type="button"
          className={`btn ${
            filaSeleccionada?.id
              ? 'btn-outline-warning'
              : 'btn-outline-primary'
          }`}
          onClick={handleSubmit(onSubmit)}
        >
          {cargando ? 'Cargando acreditaciones…' : filaSeleccionada?.id ? 'Actualizar' : 'Grabar'}
        </button>

        <button
          type="button"
          className="btn btn-outline-danger"
          onClick={handleReset}
        >
          Reset
        </button>
      </div>
      </fieldset>
    </form>
  );
};

export default EditarHabilitaciones;

