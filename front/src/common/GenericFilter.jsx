import React, { useState, useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { Search } from 'lucide-react';
import { setFiltroListado } from '../store/appSlice';
import './GenericFilter.css';

const INLINE_APPLY_THRESHOLD = 3;

const GenericFilter = ({ configuracion = [], filtroInicial = {} , postFijo = {}}) => {
  const dispatch = useDispatch();
  const [valoresTemporales, setValoresTemporales] = useState({});

  // Inicializar valores
  useEffect(() => {
    const valoresIniciales = {};
    configuracion.forEach(item => {
      valoresIniciales[item.clave] = item.tipo === 'checkbox' ? false : '';
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
        !(['list', 'select'].includes(item.tipo) && valor === '') &&
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
            className="form-control generic-filter-control"
            value={valoresTemporales[item.clave] || ''}
            onChange={(e) => handleChange(
              item.clave,
              item.tipo === 'number' ? parseInt(e.target.value) || '' : e.target.value
            )}
            onKeyDown={handleKeyPress}
            placeholder={item.placeholder || item.etiqueta}
          />
        );
      case 'list':
      case 'select': {
        const opciones = item.opciones || (Array.isArray(item.valor) ? item.valor : []);

        if (opciones.length === 0) {
          return (
            <input
              type="text"
              className="form-control generic-filter-control"
              value={valoresTemporales[item.clave] || ''}
              onChange={(e) => handleChange(item.clave, e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder={item.placeholder || item.etiqueta}
            />
          );
        }

        return (
          <select
            className="form-select generic-filter-control"
            value={valoresTemporales[item.clave] || ''}
            onChange={(e) => handleChange(item.clave, e.target.value)}
          >
            <option value="">{item.placeholder || `Elija ${item.etiqueta.toLowerCase()}`}</option>
            {opciones.map((opcion, index) => {
              const value = typeof opcion === 'object' ? opcion.value : opcion;
              const label = typeof opcion === 'object' ? opcion.label : opcion;
              return <option key={index} value={value}>{label}</option>;
            })}
          </select>
        );
      }
      case 'checkbox':
        return (
          <div className="generic-filter-switch">
            <input
              className="generic-filter-switch-input"
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
    <div className="generic-filter card mb-4">
      <div className="generic-filter-body"> 
        <div className={`generic-filter-grid ${configuracion.length <= INLINE_APPLY_THRESHOLD ? 'generic-filter-grid-compact' : ''}`}>
          {configuracion.filter((item) => item.tipo !== 'checkbox').map((item) => (
            <div key={item.clave} className="generic-filter-field">
              <label className="generic-filter-label" htmlFor={`filter-${item.clave}`}>
                {item.etiqueta}
              </label>
              {renderInput(item)}
            </div>
          ))}

          {configuracion.some((item) => item.tipo === 'checkbox') && (
            <div className="generic-filter-switches">
              {configuracion.filter((item) => item.tipo === 'checkbox').map((item) => (
                <div key={item.clave} className="generic-filter-field generic-filter-field-switch">
                  <label className="generic-filter-label" htmlFor={`filter-${item.clave}`}>
                    {item.etiqueta}
                  </label>
                  {renderInput(item)}
                </div>
              ))}
            </div>
          )}
          <div className="generic-filter-actions">
            <button type="button" className="btn btn-dark generic-filter-apply" onClick={aplicarFiltros}>
              <Search size={16} aria-hidden="true" />
              Aplicar
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default React.memo(GenericFilter);
