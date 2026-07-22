import React, { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import {
  usePostPersonasMutation,
  usePatchPersonasMutation
} from '../../store/apiSlice';
import { useSelector, useDispatch } from 'react-redux';
import { resetModulo } from '../../store/appSlice';
import { formularioCampos } from './FormularioEditar';
import { separadoresFormulario } from './formularioSeparadores';
import { obtenerCamposAValidar } from './camposValidacion';

const EditarPersonas = () => {
  const dispatch = useDispatch();
  const user = useSelector((state) => state.acceso.user);
  const filaSeleccionada = useSelector(
    (state) => state.modulos.personas
  )?.datos;

  const [postPersonas] = usePostPersonasMutation();
  const [patchPersonas] = usePatchPersonasMutation();

  const { register, handleSubmit, setValue, reset } = useForm({
    defaultValues: {
      personas: [{}],
    },
  });

  // Reset al montar
  useEffect(() => {
    dispatch(resetModulo({ modulo: 'personas' }));
  }, [dispatch]);

  // Campos visibles (igual lógica que catalogos)
  const camposVisibles = formularioCampos.filter((field) => {
    if (field.placeholder === 'no_visible') return false;

    if (field.name === 'activo' && !filaSeleccionada?.id) {
      return false;
    }

    return true;
  });

  // Cargar datos en edición
  useEffect(() => {
    if (filaSeleccionada?.id) {
      camposVisibles.forEach((field) => {
        if (field.type === 'date' && filaSeleccionada[field.name]) {
          setValue(
            `personas.0.${field.name}`,
            filaSeleccionada[field.name].split('T')[0]
          );
        } else {
          setValue(
            `personas.0.${field.name}`,
            filaSeleccionada[field.name] ?? null
          );
        }
      });
    } else {
      reset();
    }
  }, [filaSeleccionada]);

  // Validación dinámica
  const controlDatosFormulario = (personas) => {
    const camposAValidar = obtenerCamposAValidar();

    return camposAValidar.some((fieldName) => {
      const value = personas[fieldName];
      return value === undefined || value === null || value === '';
    });
  };

  // Submit unificado
  const onSubmit = async (data) => {
    try {
      const personas = data.personas?.[0];

      if (!personas || controlDatosFormulario(personas)) {
        alert('⚠️ Faltan completar datos formulario');
        return;
      }

      const personasData = {
        ...personas,
        empresa: user.empresa,
        login: user.login,
        ...(filaSeleccionada?.id ? {} : { activo: true }),
      };

      if (filaSeleccionada?.id) {
        await patchPersonas({
          id: filaSeleccionada.id,
          ...personasData,
        }).unwrap();

        dispatch(resetModulo({ modulo: 'personas' }));
      } else {
        await postPersonas(personasData).unwrap();
      }

      reset();
    } catch (error) {
      console.error('Error al enviar datos:', error);
    }
  };

  const handleReset = () => {
    reset();
    dispatch(resetModulo({ modulo: 'personas' }));
  };

  return (
    <form
      style={{
        padding: '20px',
        backgroundColor: filaSeleccionada?.id
          ? '#fcf4dd'
          : '#ffffff',
      }}
    >
      {camposVisibles.map((field) => {
        const separador = separadoresFormulario.find(
          (s) => s.before === field.name
        );

        const fieldProps = {
          ...register(`personas.0.${field.name}`),
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
                field.type === 'checkbox'
                  ? 'form-check'
                  : ''
              }`}
            >
              {field.type !== 'checkbox' && (
                <label className="form-label">
                  {field.label}
                </label>
              )}

              {field.type === 'checkbox' ? (
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
          {filaSeleccionada?.id
            ? 'Actualizar'
            : 'Grabar'}
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

export default EditarPersonas;