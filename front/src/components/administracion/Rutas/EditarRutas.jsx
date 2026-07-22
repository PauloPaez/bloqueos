import React, { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { usePostRutasMutation, usePutRutasMutation } from "../../../store/apiSlice";
import { useSelector, useDispatch } from "react-redux";
import { resetFila } from "../../../store/appSlice";

const EditarRutas = () => {
  const [postRutas] = usePostRutasMutation();
  const [putRutas] = usePutRutasMutation(); // Importar la mutación PUT
  const dispatch = useDispatch();
  const filaSeleccionada = useSelector((state) => state.fila.elegida);

  const { register, handleSubmit, setValue, reset } = useForm({
    defaultValues: {
      rutas: [{}],
    },
  });

  const [isActualizarDisabled, setIsActualizarDisabled] = useState(true);
  const [isEnviarDisabled, setIsEnviarDisabled] = useState(false);

  const formFields = [
	{name: "rol", label: "Rol", placeholder: "Rol que acceder", type: "text"},
	{name: "componente", label: "Componente", placeholder: "Nombre del componente", type: "text"},
	{name: "path", label: "path", placeholder: "Ubicacion fisica del componente", type: "text"},
  ];

  useEffect(() => {
    if (filaSeleccionada.id) {
      setIsActualizarDisabled(false);
      setIsEnviarDisabled(true);
      formFields.forEach((field) => {
        setValue(`rutas.0.${field.name}`, filaSeleccionada[field.name] || "");
      });
    } else {
      setIsActualizarDisabled(true);
      setIsEnviarDisabled(false);
    }
  }, [filaSeleccionada, setValue, formFields]);

  const onSubmit = async (data) => {
    try {
      const response = await postRutas(data.rutas[0]).unwrap();
      console.log("Datos enviados (POST):", response);
      reset();
    } catch (error) {
      console.error("Error al enviar los datos (POST):", error);
    }
  };

  const onActualizar = async (data) => {
    try {
      const updatedData = { id: filaSeleccionada.id, ...data.rutas[0] };
      const response = await putRutas(updatedData).unwrap();
      console.log("Datos actualizados (PUT):", response);
      reset();
      dispatch(resetFila()); // Limpiar fila seleccionada tras actualizar
      setIsActualizarDisabled(true);
      setIsEnviarDisabled(false);
    } catch (error) {
      console.error("Error al actualizar los datos (PUT):", error);
    }
  };

  const handleReset = () => {
    reset();
    dispatch(resetFila());
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
            {...register(`rutas.0.${formField.name}`, {
              required: formField.type === "checkbox" ? false : `${formField.label} es obligatorio`,
            })}
            placeholder={formField.placeholder}
            type={formField.type}
            className={`form-input ${
              formField.type === "checkbox" ? "form-check-input" : "form-control"
            }`}
            id={formField.name}
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

export default EditarRutas;


