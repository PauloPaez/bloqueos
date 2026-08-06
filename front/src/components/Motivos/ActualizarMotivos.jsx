import LayoutActualizar from "../../layout/LayoutActualizar";
import EditarMotivos from './EditarMotivos';
import ListarMotivos from './ListarMotivos';

const ActualizarMotivos = () => {
  return (
    <LayoutActualizar
      editar={<EditarMotivos />}
      listar={<ListarMotivos />}
      ratioEditar={25}
      ratioListar={75}
      tituloEditar="Editar Motivos"
      tituloListar="Listado de Motivos"
    />
  );
};

export default ActualizarMotivos;
