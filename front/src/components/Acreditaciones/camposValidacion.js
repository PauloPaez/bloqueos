import { formularioCampos } from './FormularioEditar';
import { camposRequeridosFormulario } from './camposRequeridosFormulario';

export const obtenerCamposAValidar = () => {
  // Caso parcial explícito
  if (camposRequeridosFormulario.length > 0) {
    return camposRequeridosFormulario;
  }

  // Caso arreglo vacío → validar todo el formulario
  return formularioCampos
    .filter(
      (field) =>
        field.placeholder !== 'no_visible' &&
        field.type !== 'checkbox'
    )
    .map((field) => field.name);
};