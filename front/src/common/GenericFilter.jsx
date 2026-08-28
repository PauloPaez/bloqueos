import React, { useState, useEffect, useRef } from 'react';
import { RotateCcw, Search } from 'lucide-react';
import useFiltroListado from '../hooks/useFiltroListado';
import './GenericFilter.css';

const INLINE_APPLY_THRESHOLD = 7;

const GenericFilter = ({
  configuracion = [],
  filtroInicial = {},
  postFijo = {},
  claveFiltro,
  modulo,
  predictivo = false,
}) => {
  const clave = claveFiltro || modulo || 'default';
  const { valores: valoresPersistidos, guardarFiltro } = useFiltroListado(clave);
  const [valoresTemporales, setValoresTemporales] = useState({});
  const filtroInicializado = useRef(false);
  const ultimoValorAutomatico = useRef(null);
  // La configuración suele crearse como un nuevo arreglo en cada render.
  // Usamos una firma estable para no borrar los valores que el usuario ya
  // escribió cada vez que el componente vuelve a renderizarse.
  const configuracionKey = configuracion
    .map(item => `${item.clave}:${item.tipo}`)
    .join('|');

  // Inicializar valores
  useEffect(() => {
    const valoresIniciales = {};
    configuracion.forEach(item => {
      const tieneValorPersistido = Object.prototype.hasOwnProperty.call(
        valoresPersistidos || {},
        item.clave
      );

      valoresIniciales[item.clave] = tieneValorPersistido
        ? valoresPersistidos[item.clave]
        : item.tipo === 'checkbox' ? false : '';
    });
    setValoresTemporales(valoresIniciales);
  }, [configuracionKey, clave, valoresPersistidos]);

  useEffect(() => {
    if (!predictivo || Object.keys(valoresTemporales).length === 0) return;

    const firmaValores = JSON.stringify(valoresTemporales);

    if (!filtroInicializado.current) {
      filtroInicializado.current = true;
      ultimoValorAutomatico.current = firmaValores;
      return;
    }

    if (firmaValores === ultimoValorAutomatico.current) {
      return;
    }

    const temporizador = setTimeout(() => {
      ultimoValorAutomatico.current = firmaValores;
      aplicarFiltros();
    }, 400);

    return () => clearTimeout(temporizador);
  }, [predictivo, valoresTemporales]);

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
    }
  
    // Si todos los campos están vacíos, usar el filtro inicial.
    const filtro = todosVacios && Object.keys(filtroInicial).length > 0
      ? { ...filtroInicial, ...nuevosFiltros }
      : nuevosFiltros;

    guardarFiltro(filtro, valoresTemporales);
  };

  // Limpia los campos visibles y aplica nuevamente solo las condiciones
  // iniciales/fijas del listado.
  const limpiarFiltros = () => {
    const valoresReset = {};
    configuracion.forEach(item => {
      valoresReset[item.clave] = item.tipo === 'checkbox' ? false : '';
    });

    const filtroReset = { ...filtroInicial, ...postFijo };
    setValoresTemporales(valoresReset);
    guardarFiltro(filtroReset, valoresReset);
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
            <button
              type="button"
              className="btn generic-filter-clear"
              onClick={limpiarFiltros}
            >
              <RotateCcw size={16} aria-hidden="true" />
              Limpiar
            </button>
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
