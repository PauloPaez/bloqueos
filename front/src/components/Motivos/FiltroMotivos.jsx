import React from 'react';
import GenericFilter from '../../common/GenericFilter';

const FiltroMotivos = ({
  filtroInicial,
  postFijo,
  claveFiltro = "motivos:listar",
}) => {
  const configuracionFiltro = [
    {   'clave': 'motivo',
    'etiqueta': 'Motivo',
    'placeholder': 'Motivo',
    'tipo': 'str',
    'valor': ''},
    {   'clave': 'lleva_fecha',
    'etiqueta': 'Lleva fecha',
    'tipo': 'tristate',
    'valor': 'all'},
    {   'clave': 'activo',
    'etiqueta': 'Activo',
    'tipo': 'tristate',
    'valor': 'all'},
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

export default FiltroMotivos;
