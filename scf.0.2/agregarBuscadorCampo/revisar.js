import React, { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { usePostReportesMutation, usePatchReportesMutation } from "../../store/apiSlice";
import { usePostEmpleadosByFieldMutation } from "../../store/apiSlice";
import { useSelector, useDispatch } from "react-redux";
import { resetModulo } from "../../store/appSlice";

const EditarReportes = () => {
  const [postReportes] = usePostReportesMutation();
  const [patchReportes] = usePatchReportesMutation(); // Importar la mutación PATCH
  const [postEmpleadosByField] = usePostEmpleadosByFieldMutation();
  const dispatch = useDispatch();
  const user = useSelector((state) => state.acceso.user);
  
  // Resetear la fila seleccionada al montar el componente
  useEffect(() => {
    dispatch(resetModulo({ modulo: '!model' }));
    
  }, [dispatch]);

  const filaSeleccionada = useSelector((state) => state.modulos.reportes).datos;

  const { register, handleSubmit, setValue, reset, watch } = useForm({
    defaultValues: {
      reportes: [{}],
    },
  });

  const [isActualizarDisabled, setIsActualizarDisabled] = useState(true);
  const [isEnviarDisabled, setIsEnviarDisabled] = useState(false);

  const formFields = [
	{name: "dni", label: "DNI", placeholder: "DNI", type: "text"},
	{name: "nombre", label: "Nmbre", placeholder: "Nombre", type: "text"},
	{name: "apellido", label: "Apellido", placeholder: "Apellido", type: "text"},
	{name: "fecha_Ingreso", label: "Fecha Ingreso", placeholder: "Fecha Ingreso", type: "date"},
	{name: "empresa", label: "Empresa", placeholder: "Empresa", type: "text"},
	{name: "reporte", label: "Reporte", placeholder: "Reporte", type: "text"},
	{name: "activo", label: "Activo", placeholder: "Activo", type: "checkbox"},
  ];

  useEffect(() => {
    if (filaSeleccionada?.id) {
      setIsActualizarDisabled(false);
      setIsEnviarDisabled(true);
      formFields.forEach((field) => {
        if (field.type === "date" && filaSeleccionada[field.name]) {
          // Convertir el valor datetime a date
          const fechaFormateada = filaSeleccionada[field.name].split('T')[0];
          setValue(`reportes.0.${field.name}`, fechaFormateada);
        } else {
          setValue(`reportes.0.${field.name}`, filaSeleccionada[field.name] || "");
        }
      });
    } else {
      setIsActualizarDisabled(true);
      setIsEnviarDisabled(false);
      reset({ reportes: [{}] });
    }
  }, [filaSeleccionada]);


  const actualizarFormulario = (datos) => {
    if (!datos) return;
    const camposComunes = ['nombre', 'dni', 'empresa', 'apellido', 'activo']
    camposComunes.forEach(campo => {
      if (datos[campo] !== undefined) {
        setValue(`reportes.0.${campo}`, datos[campo] ?? "");
      }
    })
  };
  const buscarDni = async (dni) => {
    if (dni) {
      const filtro = { dni: dni, activo: true };
      try {
        const result = await postEmpleadosByField(filtro).unwrap();
        // Si hay resultados, actualizar los campos del formulario
        if (result && result.length > 0) {
          const empleados = result[0];
          actualizarFormulario(empleados, 'empleados');
        }
      } catch (error) {
        console.error("Error al buscar empleados:", error);
      }
    } else {
      console.error("Dni no proporcionado");
    }
  };

  const onSubmit = async (data) => {
    try {
          const reportesData = {
        	...data.reportes[0],
        	empresa: user.empresa
      		};
      const response = await postReportes(reportesData).unwrap();
      reset();
    } catch (error) {
      console.error("Error al enviar los datos (POST):", error);
    }
  };

  const onActualizar = async (data) => {
    try {
      const updatedData = { id: filaSeleccionada.id, ...data.reportes[0] };
      const response = await patchReportes(updatedData).unwrap();
      reset();
      dispatch(resetModulo({ modulo: 'reportes' })); 
      setIsActualizarDisabled(true);
      setIsEnviarDisabled(false);
    } catch (error) {
      console.error("Error al actualizar los datos (PATCH):", error);
    }
  };

  const handleReset = () => {
    reset();
    dispatch(resetModulo({ modulo: 'empleado' }));
    setIsActualizarDisabled(true);
    setIsEnviarDisabled(false);
  };

  return (
    <form style={{ padding: "20px",
      backgroundColor: !isActualizarDisabled ? "#fcf4dd" : "#ffffff", }}>
      {formFields.filter((formField) => formField.placeholder !== "no_visible").map((formField) => (
        <div
          key={formField.name}
          className={`mb-3 ${
            formField.type === "checkbox" ? "form-check" : ""
          }`}
        >
          {formField.type !== "checkbox" && (
            <label className="form-label" htmlFor={formField.name}>
              {formField.label}
            </label>
          )}
          <input
            {...register(`reportes.0.${formField.name}`, {
              required: formField.type === "checkbox" ? false : `${formField.label} es obligatorio`, })}
            placeholder={formField.placeholder}
            type={formField.type}
            className={`form-input ${
              formField.type === "checkbox" ? "form-check-input" : "form-control"}`}
            {...(formField.name === "dni" && {
              onKeyDown: (e) => {
                if (e.key === "Enter") {
                  e.preventDefault();
                  const dniValue = e.target.value;
                  buscarDni(dniValue);
                }
              }
            })}
          // fin input form
          />
          {formField.type === "checkbox" && (
            <label className="form-check-label" htmlFor={formField.name}>
              {formField.label}
            </label>
          )}
        </div>
      ))}
      <div style={{ display: "flex", justifyContent: "space-between", marginTop: "20px" }}>
        <button
          type="button"
          className="btn btn-outline-primary"
          disabled={isEnviarDisabled}
          onClick={handleSubmit(onSubmit)}
        >
          Enviar
        </button>
        <button
          type="button"
          className="btn btn-outline-warning"
          disabled={isActualizarDisabled}
          onClick={handleSubmit(onActualizar)}
        >
          Actualizar
        </button>
        <button type="button" className="btn btn-outline-danger" onClick={handleReset}>
          Reset
        </button>
      </div>
    </form>
  );
};

export default EditarReportes;


