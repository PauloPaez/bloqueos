import React, { useState, useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { setFiltroListado, resetFiltroListado } from '../store/appSlice';

const GenericFilter = ({ configuracion = [], filtroInicial = {} , postFijo = {}}) => {
  const dispatch = useDispatch();
  const [valoresTemporales, setValoresTemporales] = useState({});

  // Inicializar valores
  useEffect(() => {
    const valoresIniciales = {};
    configuracion.forEach(item => {
      valoresIniciales[item.clave] = item.tipo === 'checkbox' ? false : 
                                    item.tipo === 'list' ? '' : 
                                    item.valor || '';
    });
    setValoresTemporales(valoresIniciales);
  }, [configuracion]);

  // Manejar cambios en los inputs
  const handleChange = (clave, valor) => {
    setValoresTemporales(prev => ({
      ...prev,
      [clave]: valor
    }));
  };

  // Aplicar filtros
  const aplicarFiltros = () => {
    const nuevosFiltros = {};
    let todosVacios = true;
    
    configuracion.forEach(item => {
      const valor = valoresTemporales[item.clave];
      
      const shouldInclude = (
        valor !== undefined &&
        valor !== null &&
        !(item.tipo === 'list' && valor === '') &&
        !(item.tipo === 'checkbox' && valor === false) &&
        valor !== ''
      );
  
      if (shouldInclude) {
        nuevosFiltros[item.clave] = valor;
        todosVacios = false;
      }
    });
    
        // Incluir postFijo si tiene valores
     if (Object.keys(postFijo).length > 0) {
      Object.assign(nuevosFiltros, postFijo);
      todosVacios = false; 
    }
  
    // Si todos los campos están vacíos, usar el filtro inicial
    if (todosVacios && Object.keys(filtroInicial).length > 0) {
      dispatch(setFiltroListado(filtroInicial));
    } else {
      dispatch(setFiltroListado(nuevosFiltros));
    }
  };

  // Resetear filtros
  const resetearFiltros = () => {
    const valoresReset = {};
    configuracion.forEach(item => {
      valoresReset[item.clave] = item.tipo === 'checkbox' ? false : '';
    });
    setValoresTemporales(valoresReset);
    dispatch(resetFiltroListado());
  };

  // Manejar tecla Enter
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      aplicarFiltros();
    }
  };

  // Renderizar input según el tipo
  const renderInput = (item) => {
    switch (item.tipo) {
      case 'str':
      case 'number':
        return (
          <input
            type={item.tipo === 'number' ? 'number' : 'text'}
            className="form-control"
            value={valoresTemporales[item.clave] || ''}
            onChange={(e) => handleChange(
              item.clave,
              item.tipo === 'number' ? parseInt(e.target.value) || 0 : e.target.value
            )}
            onKeyPress={handleKeyPress}
            placeholder={item.placeholder || item.etiqueta}
          />
        );
        case 'list':
          return (
            <select
              className="form-select"
              value={valoresTemporales[item.clave] || ''}
              onChange={(e) => handleChange(item.clave, e.target.value)}
            >
              <option value="">{item.placeholder || `Elija ${item.etiqueta.toLowerCase()}`}</option>
              {item.valor.map((opcion, index) => (
                <option key={index} value={opcion}>
                  {opcion}
                </option>
              ))}
            </select>
          );
      case 'checkbox':
        return (
          <div className="form-check form-switch d-flex align-items-center">
            <input
              className="form-check-input"
              type="checkbox"
              checked={valoresTemporales[item.clave] || false}
              onChange={(e) => handleChange(item.clave, e.target.checked)}
              id={`filter-${item.clave}`}
            />
          </div>
        );

      default:
        return (
          <input
            type="text"
            className="form-control"
            value={valoresTemporales[item.clave] || ''}
            onChange={(e) => handleChange(item.clave, e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={item.placeholder || item.etiqueta}
          />
        );
    }
  };

  return (
    <div className="card mb-4 shadow-sm">
      <div className="card-body p-2">
        <div className="input-group">
          {configuracion.map((item, index) => (
            <React.Fragment key={index}>
              <span className="input-group-text">{item.etiqueta}</span>
              {item.tipo === 'checkbox' ? (
                <div className="card d-flex align-items-center justify-content-center p-2" 
                     style={{ width: "38px", height: "39px" }}>
                  {renderInput(item)}
                </div>
              ) : (
                renderInput(item)
              )}
            </React.Fragment>
          ))}
          
          {/* <span className="input-group-text" style={{ cursor: 'pointer' }}
                onClick={resetearFiltros}>
            Reset
          </span> */}
          <button className="btn btn-primary" 
                  onClick={aplicarFiltros}
                  style={{ borderTopLeftRadius: 0, borderBottomLeftRadius: 0 }}>
            Aplicar
          </button>
        </div>
      </div>
    </div>
  );
};

export default React.memo(GenericFilter);
