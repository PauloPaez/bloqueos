import LayoutActualizar from "../../layout/LayoutActualizar";
import EditarAcreditaciones from "./EditarAcreditaciones";
import ListarAcreditaciones from "./ListarAcreditaciones";

const ActualizarAcreditaciones = () => {
  return (
    <>
      <LayoutActualizar
        ocultarEditar={true}
        listar={<ListarAcreditaciones claveFiltro="acreditaciones:actualizar" />}
      />

      <EditarAcreditaciones />
    </>
  );
};

export default ActualizarAcreditaciones;
