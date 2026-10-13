import React, { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { usePostUsuariosMutation, usePutUsuariosMutation } from "../../../store/apiSlice";
import { useSelector, useDispatch } from "react-redux";
import { resetFila } from "../../../store/appSlice";
import SelectRoles from "../Roles/SelectRoles"; // Importar el componente SelectRoles

const EditarUsuarios = () => {
  const [postUsuarios] = usePostUsuariosMutation();
  const [putUsuarios] = usePutUsuariosMutation();
  const dispatch = useDispatch();
  const filaSeleccionada = useSelector((state) => state.fila.elegida);

  const { register, handleSubmit, setValue, reset, watch } = useForm({
    defaultValues: {
      usuarios: [{}],
    },
  });

  const [isActualizarDisabled, setIsActualizarDisabled] = useState(true);
  const [isEnviarDisabled, setIsEnviarDisabled] = useState(false);

  const formFields = [
    { name: "nombre", label: "Nombre", placeholder: "Nombre del usuario", type: "text" },
    { name: "apellido", label: "Apellido", placeholder: "Apellido del usuario", type: "text" },
    {name: "empresas", label: "Empresa", placeholder: "Empresa donde trabaja", type: "text"}, 
    { name: "login", label: "Login", placeholder: "Ingrese Login", type: "text" },
    { name: "clave", label: "Clave", placeholder: "****", type: "text" },
    { name: "activo", label: "Activo", placeholder: "Activo", type: "checkbox" },
  ];

  // Obtener el valor actual de "roles" del formulario
  const rolesValue = watch("usuarios.0.roles");

  // Sincronizar el formulario con filaSeleccionada
  useEffect(() => {
    if (filaSeleccionada?.id) {
      setIsActualizarDisabled(false);
      setIsEnviarDisabled(true);

      // Cargar los valores de la fila seleccionada en el formulario
      formFields.forEach((field) => {
        setValue(`usuarios.0.${field.name}`, filaSeleccionada[field.name] || "");
      });

      // Cargar los roles de la fila seleccionada
      setValue("usuarios.0.roles", filaSeleccionada.roles || []);
    } else {
      setIsActualizarDisabled(true);
      setIsEnviarDisabled(false);
    }
  }, [filaSeleccionada]); // Solo depende de filaSeleccionada

  const onSubmit = async (data) => {
    try {
      const newData = { ...data.usuarios[0] };
      newData.empresas = [newData.empresas] || [];
      const response = await postUsuarios(newData).unwrap();
      reset();
    } catch (error) {
      console.error("Error al enviar los datos (POST):", error);
    }
  };

  const onActualizar = async (data) => {
    try {
      const updatedData = { id: filaSeleccionada.id, ...data.usuarios[0] };
      const response = await putUsuarios(updatedData).unwrap();
      reset();
      dispatch(resetFila()); // Limpiar fila seleccionada tras actualizar
      setIsActualizarDisabled(true);
      setIsEnviarDisabled(false);
    } catch (error) {
      console.error("Error al actualizar los datos (PATCH):", error);
    }
  };

  const handleReset = () => {
    reset();
    dispatch(resetFila());
    setIsActualizarDisabled(true);
    setIsEnviarDisabled(false);
  };

  return (
    <form
      style={{
        padding: "20px",
        backgroundColor: !isActualizarDisabled ? "#fcf4dd" : "#ffffff",
      }}
    >
      {formFields
        .filter((formField) => formField.placeholder !== "no_visible")
        .map((formField) => (
          <div
            key={formField.name}
            className={`mb-3 ${formField.type === "checkbox" ? "form-check" : ""}`}
          >
            {formField.type !== "checkbox" && (
              <label className="form-label" htmlFor={formField.name}>
                {formField.label}
              </label>
            )}
            <input
              {...register(`usuarios.0.${formField.name}`, {
                required:
                  formField.type === "checkbox" ? false : `${formField.label} es obligatorio`,
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

      {/* Reemplazar el campo "roles" con el componente SelectRoles */}
      <div className="mb-3">
        <SelectRoles
          value={rolesValue || []} // Valor actual del campo "roles"
          onSelect={(value) => setValue("usuarios.0.roles", value)} // Actualizar el valor en el formulario
        />
      </div>

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginTop: "20px",
        }}
      >
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

export default EditarUsuarios;
