import React from 'react';
import GenericFilter from '../../common/GenericFilter';

const FiltroPersonas = ({
  filtroInicial,
  postFijo,
  claveFiltro = "personas:listar",
}) => {
  const configuracionFiltro = [
    // {   'clave': 'cuit',
    // 'etiqueta': 'CUIT',
    // 'placeholder': 'CUIT',
    // 'tipo': 'str',
    // 'valor': ''},
    {   'clave': 'nombre',
    'etiqueta': 'Nombre',
    'placeholder': 'Nombre',
    'tipo': 'str',
    'valor': ''},
    {   'clave': 'apellido',
    'etiqueta': 'Apellido',
    'placeholder': 'Apellido',
    'tipo': 'str',
    'valor': ''},
    {   'clave': 'empresa_cnx',
    'etiqueta': 'Empresa',
    'placeholder': 'Empresa',
    'tipo': 'str',
    'valor': ''},
    // {   'clave': 'login_cnx',
    // 'etiqueta': 'login',
    // 'placeholder': 'login',
    // 'tipo': 'str',
    // 'valor': ''},
    {   'clave': 'calle_nro',
    'etiqueta': 'Calle y Nro',
    'placeholder': 'Calle y Nro',
    'tipo': 'str',
    'valor': ''},
    {   'clave': 'barrio',
    'etiqueta': 'Barrio',
    'placeholder': 'Barrio',
    'tipo': 'str',
    'valor': ''},
    {   'clave': 'departamento',
    'etiqueta': 'Departamento',
    'placeholder': 'Departamento',
    'tipo': 'str',
    'valor': ''},
    // {   'clave': 'provincia',
    // 'etiqueta': 'Provincia',
    // 'placeholder': 'Provincia',
    // 'tipo': 'str',
    // 'valor': ''},
    // {   'clave': 'cargo',
    // 'etiqueta': 'Cargo',
    // 'placeholder': 'Cargo',
    // 'tipo': 'select',
    // 'valor': ''},
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
      claveFiltro={claveFiltro}
    />
  );
};

export default FiltroPersonas;
