import LayoutActualizar from "../../../layout/LayoutActualizar";
import EditarUsuarios from "./EditarUsuarios";
import ListarUsuarios from "./ListarUsuarios";

const ActualizarUsuarios = () => {
  return (
    <LayoutActualizar
      editar={<EditarUsuarios />}
      listar={<ListarUsuarios />}
      ratioEditar={25}
      ratioListar={75}
      tituloEditar="Editar Usuarios"
      tituloListar="Listado de Usuarios"
    />
  );
};

export default ActualizarUsuarios;
