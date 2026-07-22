import React, { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { usePostEscuelasMutation, usePatchEscuelasMutation } from '../../store/apiSlice';
import { useSelector, useDispatch } from 'react-redux';
import { resetModulo } from '../../store/appSlice';
import { formularioCampos } from './FormularioEditar';
import { separadoresFormulario } from './formularioSeparadores';
import { obtenerCamposAValidar } from './camposValidacion';

const EditarEscuelas = () => {
  const dispatch = useDispatch();
  const user = useSelector((state) => state.acceso.user);
  const filaSeleccionada = useSelector(
    (state) => state.modulos.escuelas).datos


  const [postEscuelas] = usePostEscuelasMutation();
  const [patchEscuelas] = usePatchEscuelasMutation();

  const { register, handleSubmit, setValue, reset } = useForm({
    defaultValues: {
      escuelas: [{}],
    },
  });

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
        if (field.type === 'date' && filaSeleccionada[field.name]) {
          setValue(
            `escuelas.0.${field.name}`,
            filaSeleccionada[field.name].split('T')[0]
          );
        } else {
          setValue(
            `escuelas.0.${field.name}`,
            filaSeleccionada[field.name] ?? null
          );
        }
      });
    } else {
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

const datosSelect = {
  "motivos": [],
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
        activo: true,
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
          ...register(`escuelas.0.${field.name}`),
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

export default EditarEscuelas;

