import React, { useState, useEffect, useRef } from 'react';
import { ChevronDown, RotateCcw, Search } from 'lucide-react';
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
  const [mostrarMasFiltros, setMostrarMasFiltros] = useState(false);
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
      const valorPersistido = valoresPersistidos?.[item.clave];

      if (item.tipo === 'tristate') {
        if (!tieneValorPersistido || valorPersistido === false || valorPersistido === 'all') {
          valoresIniciales[item.clave] = item.valor || 'all';
        } else if (valorPersistido === true || valorPersistido === 'true') {
          valoresIniciales[item.clave] = 'true';
        } else {
          valoresIniciales[item.clave] = valorPersistido === 'false' ? 'false' : item.valor || 'all';
        }
      } else {
        valoresIniciales[item.clave] = tieneValorPersistido
          ? valorPersistido
          : item.tipo === 'checkbox' ? false : '';
      }
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
      const shouldInclude = item.tipo === 'tristate'
        ? valor === 'true' || valor === 'false'
        : (
          valor !== undefined &&
          valor !== null &&
          !(['list', 'select'].includes(item.tipo) && valor === '') &&
          !(item.tipo === 'checkbox' && valor === false) &&
          valor !== ''
        );
  
      if (shouldInclude) {
        nuevosFiltros[item.clave] = item.tipo === 'tristate' ? valor === 'true' : valor;
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
      if (item.tipo === 'checkbox') valoresReset[item.clave] = false;
      else if (item.tipo === 'tristate') valoresReset[item.clave] = item.valor || 'all';
      else valoresReset[item.clave] = '';
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

  const clasesGrid = [
    'generic-filter-grid',
    configuracion.length <= INLINE_APPLY_THRESHOLD && 'generic-filter-grid-compact',
    configuracion.some((item) => item.tipo === 'tristate') && 'generic-filter-grid-has-tristate',
    configuracion.some((item) => item.masFiltros) && 'generic-filter-grid-has-more',
  ].filter(Boolean).join(' ');
  const filtrosAdicionales = configuracion.filter((item) => item.masFiltros);
  const resumenFiltrosAdicionales = filtrosAdicionales.map((item) => {
    const valor = valoresTemporales[item.clave];
    if (item.tipo === 'tristate') {
      if (!valor || valor === (item.valor || 'all')) return null;
      const opciones = item.opciones || [
        { value: 'all', label: 'Todos' },
        { value: 'true', label: 'Sí' },
        { value: 'false', label: 'No' },
      ];
      const opcion = opciones.find((actual) => actual.value === valor);
      return `${item.etiqueta}: ${opcion?.label || valor}`;
    }
    if (item.tipo === 'checkbox') return valor ? `${item.etiqueta}: Sí` : null;
    if (valor === undefined || valor === null || valor === '') return null;
    const opcion = item.opciones?.find((actual) => actual.value === valor);
    return `${item.etiqueta}: ${opcion?.label || valor}`;
  }).filter(Boolean).join(' · ');
  const idFiltrosAdicionales = `generic-filter-more-${clave}`;

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

        if (opciones.length === 0 && !item.forzarSelect) {
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
            className={`form-select generic-filter-control ${
              valoresTemporales[item.clave] ? '' : 'generic-filter-placeholder'
            }`}
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
      case 'tristate': {
        const opciones = item.opciones || [
          { value: 'all', label: 'Todos' },
          { value: 'true', label: 'Sí', indicador: 'positivo' },
          { value: 'false', label: 'No', indicador: 'neutro' },
        ];

        return (
          <div className="generic-filter-tristate" role="radiogroup" aria-labelledby={`filter-label-${item.clave}`}>
            {opciones.map((opcion) => (
              <label className="generic-filter-tristate-option" key={opcion.value}>
                <input
                  className="generic-filter-tristate-radio"
                  type="radio"
                  name={`filter-${item.clave}`}
                  value={opcion.value}
                  checked={valoresTemporales[item.clave] === opcion.value}
                  onChange={() => handleChange(item.clave, opcion.value)}
                />
                <span className="generic-filter-tristate-segment">
                  {opcion.indicador && <span className={`generic-filter-tristate-dot generic-filter-tristate-dot-${opcion.indicador}`} aria-hidden="true" />}
                  {opcion.label}
                </span>
              </label>
            ))}
          </div>
        );
      }

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

  const renderField = (item) => (
    <div
      key={item.clave}
      className={`generic-filter-field ${item.tipo === 'checkbox' ? 'generic-filter-field-switch' : ''} ${item.columnSpan > 1 ? 'generic-filter-field-wide' : ''}`}
      style={item.columnSpan > 1 ? { '--generic-filter-column-span': item.columnSpan } : undefined}
    >
      <label
        className="generic-filter-label"
        id={item.tipo === 'tristate' ? `filter-label-${item.clave}` : undefined}
        htmlFor={item.tipo === 'tristate' ? undefined : `filter-${item.clave}`}
      >
        {item.etiqueta}
      </label>
      {renderInput(item)}
    </div>
  );

  return (
    <div className="generic-filter card mb-4">
      <div className="generic-filter-body"> 
        <div className={clasesGrid}>
          {configuracion.filter((item) => item.tipo !== 'checkbox' && !item.masFiltros).map(renderField)}

          {configuracion.some((item) => item.tipo === 'checkbox' && !item.masFiltros) && (
            <div className="generic-filter-switches">
              {configuracion.filter((item) => item.tipo === 'checkbox' && !item.masFiltros).map((item) => (
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
            {filtrosAdicionales.length > 0 && (
              <button
                type="button"
                className={`generic-filter-more-toggle ${mostrarMasFiltros ? 'generic-filter-more-toggle-open' : ''}`}
                aria-expanded={mostrarMasFiltros}
                aria-controls={idFiltrosAdicionales}
                onClick={() => setMostrarMasFiltros((mostrar) => !mostrar)}
              >
                <ChevronDown size={16} aria-hidden="true" />
                Más filtros
                {resumenFiltrosAdicionales && (
                  <span className="generic-filter-more-summary">{resumenFiltrosAdicionales}</span>
                )}
              </button>
            )}
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
        {filtrosAdicionales.length > 0 && (
          <div
            id={idFiltrosAdicionales}
            className="generic-filter-more-grid"
            hidden={!mostrarMasFiltros}
          >
            {filtrosAdicionales.map(renderField)}
          </div>
        )}
      </div>
    </div>
  );
};

export default React.memo(GenericFilter);
