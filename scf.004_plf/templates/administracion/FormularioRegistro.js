export const formularioRegistroCampos = [
  // Columna 1
  { name: "nombre", label: "Nombre", type: "text", required: true, col: 1 },
  { name: "apellido", label: "Apellido", type: "text", required: true, col: 1 },
  { name: "dni", label: "DNI", type: "text", required: true, col: 1 },
  { name: "celular", label: "Celular", type: "text", required: true, col: 1 },
  { name: "empresa", label: "Empresa", type: "text", required: true, col: 1 },

  // Columna 2
  { name: "login", label: "Login", type: "custom", col: 2 },
  { name: "clave", label: "Clave", type: "password", required: true, col: 2 },
  { name: "reclave", label: "Repetir clave", type: "password", required: true, col: 2 },
  { name: "tipo_comercio", label: "Tipo Comercio", type: "select", required: true, col: 2 },

  // Columna 3
  { name: "calle_nro", label: "Calle y Nº", type: "text", required: true, col: 3 },
  { name: "barrio", label: "Barrio", type: "text", required: true, col: 3 },
  { name: "departamento", label: "Departamento", type: "text", required: true, col: 3 },
  { name: "provincia", label: "Provincia", type: "text", required: true, col: 3 },
  { name: "correo", label: "Correo", type: "email", required: true, col: 3 },
];