import React from 'react';
import GenericFilter from '../../common/GenericFilter';

const FiltroMotivos = ({ filtroInicial, postFijo }) => {
  const configuracionFiltro = [
    {   'clave': 'motivo',
    'etiqueta': 'Motivo',
    'placeholder': 'Motivo',
    'tipo': 'str',
    'valor': ''},
    // {   'clave': 'activo',
    // 'etiqueta': 'Activo',
    // 'placeholder': 'Activo',
    // 'tipo': 'checkbox',
    // 'valor': ''},
];
  
  return (
    <GenericFilter
      configuracion={configuracionFiltro}
      filtroInicial={filtroInicial}
      postFijo={postFijo}
      claveFiltro="motivos"
    />
  );
};

export default FiltroMotivos;
