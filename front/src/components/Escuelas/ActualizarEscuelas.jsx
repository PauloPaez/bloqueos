import LayoutActualizar from "../../layout/LayoutActualizar";
import EditarEscuelas from './EditarEscuelas';
import ListarEscuelas from './ListarEscuelas';

const ActualizarEscuelas = () => {
  return (
    <LayoutActualizar
      editar={<EditarEscuelas />}
      listar={<ListarEscuelas />}
      // ratioEditar={25}
      ratioListar={100}
      // tituloEditar="Editar Escuelas"
      tituloListar="Listado de Escuelas"
    />
  );
};

export default ActualizarEscuelas;
