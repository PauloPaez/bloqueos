export const formularioCampos = [
  {name: "motivo", label: "Motivo", placeholder: "Ej. Baja por jubilación", type: "text", maxLength: 100},
  {name: "lleva_fecha", label: "Lleva fecha", placeholder: "Lleva fecha", type: "checkbox", descripcion: "Al bloquear una escuela con este motivo se pedirá una fecha."},
  {name: "login", label: "login", placeholder: "no_visible", type: "text"},
  {name: "empresa", label: "Empresa", placeholder: "no_visible", type: "text"},
  {name: "activo", label: "Activo", placeholder: "Activo", type: "checkbox", descripcion: "Los motivos inactivos no se ofrecen al bloquear escuelas."},
];
