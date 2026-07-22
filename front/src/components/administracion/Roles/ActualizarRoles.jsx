import React from 'react';
import EditarRoles from './EditarRoles';
import ListarRoles from './ListarRoles';
import LayoutActualizar from '../../../layout/LayoutActualizar';
const ActualizarRoles = () => {
  return (
    <LayoutActualizar
      editar={<EditarRoles />}
      listar={<ListarRoles />}
      ratioEditar={25}
      ratioListar={75}
      tituloEditar="Editar Roles"
      tituloListar="Listado de Roles"
    />
  );
};

export default ActualizarRoles;
