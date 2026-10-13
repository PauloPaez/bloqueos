import React from 'react';
import GenericFilter from '../../common/GenericFilter';

const FiltroHabilitaciones = ({
  filtroInicial,
  postFijo,
  claveFiltro = "habilitaciones:listar",
}) => {
  const configuracionFiltro = [
    {   'clave': 'rol',
    'etiqueta': 'Área',
    'placeholder': 'Área',
    'tipo': 'list',
    'valor': ''},
    {   'clave': 'periodo',
    'etiqueta': 'Periodo',
    'placeholder': 'Periodo',
    'tipo': 'str',
    'valor': ''},
    {   'clave': 'fecha_cierre',
    'etiqueta': 'Fecha Cierre',
    'placeholder': 'Fecha Cierre',
    'tipo': 'datetime',
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
      postFijo={postFijo}
      claveFiltro={claveFiltro}
    />
  );
};

export default FiltroHabilitaciones;
