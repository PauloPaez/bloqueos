import React from 'react';
import GenericFilter from '../../common/GenericFilter';

const FiltroMotivos = ({ filtroInicial }) => {
  const configuracionFiltro = [
    {   'clave': 'concepto',
    'etiqueta': 'Concepto',
    'placeholder': 'Concepto',
    'tipo': 'str',
    'valor': ''},
    {   'clave': 'activo',
    'etiqueta': 'Activo',
    'placeholder': 'Activo',
    'tipo': 'checkbox',
    'valor': ''},
];
  
  return (
    <GenericFilter
      configuracion={configuracionFiltro}
      filtroInicial={filtroInicial}
    />
  );
};

export default FiltroMotivos;
