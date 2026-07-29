// components/layout/LayoutActualizar.jsx
import React from "react";

const LayoutActualizar = ({
  editar,
  listar,
  ratioEditar = 0,
  ratioListar = 100,
  ocultarEditar = false,
  tituloEditar,
  tituloListar,
}) => {
  return (
    <div
      className={`pantalla-container ${
        ocultarEditar ? "solo-listar" : ""
      }`}
    >
      {!ocultarEditar && (
        <div
          className="editar-modelo"
          style={{ flexBasis: `${ratioEditar}%` }}
        >
          {tituloEditar && (
            <div className="listado-header">
              <h5 className="listado-titulo">{tituloEditar}</h5>
            </div>
          )}
          {editar}
        </div>
      )}

      <div
        className="listar-modelo"
        style={{ flexBasis: `${ratioListar}%` }}
      >
        {tituloListar && (
          <div className="listado-header">
            <h5 className="listado-titulo">{tituloListar}</h5>
          </div>
        )}
        {listar}
      </div>
    </div>
  );
};

export default LayoutActualizar;

