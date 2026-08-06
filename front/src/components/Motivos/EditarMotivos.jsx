import React, { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { usePostMotivosMutation, usePatchMotivosMutation } from '../../store/apiSlice';
import { useSelector, useDispatch } from 'react-redux';
import { resetModulo } from '../../store/appSlice';
import { formularioCampos } from './FormularioEditar';
import { separadoresFormulario } from './formularioSeparadores';
import { obtenerCamposAValidar } from './camposValidacion';

const EditarMotivos = () => {
  const dispatch = useDispatch();
  const user = useSelector((state) => state.acceso.user);
  const filaSeleccionada = useSelector(
    (state) => state.modulos.motivos).datos


  const [postMotivos] = usePostMotivosMutation();
  const [patchMotivos] = usePatchMotivosMutation();

  const { register, handleSubmit, setValue, reset } = useForm({
    defaultValues: {
      motivos: [{}],
    },
  });

  useEffect(() => {
    dispatch(resetModulo({ modulo: 'motivos' }));
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
        if (field.type === 'date' && filaSeleccionada[field.name]) {
          setValue(
            `motivos.0.${field.name}`,
            filaSeleccionada[field.name].split('T')[0]
          );
        } else {
          setValue(
            `motivos.0.${field.name}`,
            filaSeleccionada[field.name] ?? null
          );
        }
      });
    } else {
      reset();
    }
  }, [filaSeleccionada]);

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
        alert('⚠️ Faltan completar datos formulario');
        return;
      }

      const motivosData = {
        ...motivos,
        empresa: user.empresa,
        login: user.login,
        activo: true,
      };

      if (filaSeleccionada?.id) {
        await patchMotivos({
          id: filaSeleccionada.id,
          ...motivosData,
        }).unwrap();

        dispatch(resetModulo({ modulo: 'motivos' }));
      } else {
        await postMotivos(motivosData).unwrap();
      }

      reset();
    } catch (error) {
      console.error('Error al enviar datos:', error);
    }
  };

  const handleReset = () => {
    reset();
    dispatch(resetModulo({ modulo: 'motivos' }));
  };

  return (
    <form
      style={{
        padding: '20px',
        backgroundColor: filaSeleccionada?.id ? '#fcf4dd' : '#ffffff',
      }}
    >
      {camposVisibles.map((field) => {
        const separador = separadoresFormulario.find(
          (s) => s.before === field.name
        );

        const fieldProps = {
          ...register(`motivos.0.${field.name}`),
          disabled: field.disabled,
          placeholder:
            field.placeholder !== 'no_visible'
              ? field.placeholder
              : undefined,
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

              {field.type === 'select' ? (
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
          {filaSeleccionada?.id ? 'Actualizar' : 'Grabar'}
        </button>

        <button
          type="button"
          className="btn btn-outline-danger"
          onClick={handleReset}
        >
          Reset
        </button>
      </div>
    </form>
  );
};

export default EditarMotivos;

