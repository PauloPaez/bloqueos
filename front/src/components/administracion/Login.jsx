import React, { useState, useEffect } from 'react';
import { usePostLoginByFieldMutation } from '../../store/apiSlice';
import { setAcceso } from '../../store/appSlice';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import Registro from './Registro';

const Login = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [mostrarRegistro, setMostrarRegistro] = useState(false);
  const [triggerLogin, { data: usuario, error, isLoading }] = usePostLoginByFieldMutation();

  const handleSubmit = (e) => {
    e.preventDefault();
    const login = e.target.elements.login.value.trim();
    // const empresas = e.target.elements.empresa.value.trim();
    const clave = e.target.elements.clave.value.trim();
    const activo = true;
    const app = false;
    if (login && clave) {
      triggerLogin({ login, 
        clave, 
        // empresas, 
        activo, 
        app });
    } else {
      alert("Por favor, ingrese usuario y contraseña.");
    }
  };

  useEffect(() => {
    if (usuario && usuario.login) {
      dispatch(setAcceso({ login: usuario.login, empresa: usuario.empresa, opciones: usuario.opciones }));
      navigate("/");
    } else if (error) {
      alert("Error de autenticación. Por favor, revise sus credenciales.");
    }
  }, [usuario, error, dispatch, navigate]);

  if (isLoading) return <p>Buscando...</p>;
  if (error) return <p>Error: {error.message}</p>;

  if (mostrarRegistro) {
    return <Registro volver={() => setMostrarRegistro(false)} />;
  }

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        padding: '1rem',
        boxSizing: 'border-box',
      }}
    >
      {/* Tarjeta flotante de login con mejor sombra */}
      <div
        className="card border-0"
        style={{
          width: '100%',
          maxWidth: '450px',
          background: 'rgba(255, 255, 255, 0.98)',
          borderRadius: '1.5rem',
          boxShadow: `
            0 10px 25px rgba(0, 0, 0, 0.15),
            0 5px 10px rgba(0, 0, 0, 0.1),
            0 2px 5px rgba(0, 0, 0, 0.08),
            0 0 0 1px rgba(255, 255, 255, 0.1)
          `,
          padding: '2.5rem 2rem',
          transition: 'all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.3)',
          position: 'relative',
          overflow: 'hidden',
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'translateY(-12px) scale(1.02)';
          e.currentTarget.style.boxShadow = `
            0 25px 50px rgba(0, 0, 0, 0.25),
            0 15px 25px rgba(0, 0, 0, 0.15),
            0 5px 15px rgba(0, 0, 0, 0.1),
            0 0 0 1px rgba(255, 255, 255, 0.2)
          `;
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'translateY(0) scale(1)';
          e.currentTarget.style.boxShadow = `
            0 10px 25px rgba(0, 0, 0, 0.15),
            0 5px 10px rgba(0, 0, 0, 0.1),
            0 2px 5px rgba(0, 0, 0, 0.08),
            0 0 0 1px rgba(255, 255, 255, 0.1)
          `;
        }}
      >
        {/* Efecto de brillo sutil */}
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            height: '1px',
            background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.8), transparent)',
          }}
        ></div>

        <div className="card-body" style={{ padding: 0 }}>
          {/* Encabezado */}
          <div className="text-center mb-4">
            <h3
              className="mb-3"
              style={{
                color: '#2c3e50',
                fontWeight: '600',
                fontSize: '1.75rem',
                textShadow: '0 1px 2px rgba(0,0,0,0.1)'
              }}
            >
              Iniciar Sesión-Bloqueos-Dev
            </h3>
            <div
              style={{
                height: '3px',
                background: 'linear-gradient(90deg, #667eea, #764ba2)',
                width: '60px',
                margin: '0 auto',
                borderRadius: '2px',
                boxShadow: '0 1px 3px rgba(102, 126, 234, 0.3)'
              }}
            ></div>
          </div>

          {/* Formulario */}
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label htmlFor="username" className="form-label" style={{ fontWeight: '500', color: '#34495e' }}>
                Usuario
              </label>
              <input
                type="text"
                className="form-control"
                name="login"
                placeholder="Ingrese su usuario"
                required
                style={{
                  borderRadius: '0.75rem',
                  padding: '0.75rem 1rem',
                  border: '1px solid #e1e8ed',
                  fontSize: '0.95rem',
                  transition: 'all 0.3s ease',
                  boxShadow: 'inset 0 1px 3px rgba(0,0,0,0.05)',
                  background: 'rgba(255,255,255,0.9)'
                }}
                onFocus={(e) => {
                  e.target.style.borderColor = '#667eea';
                  e.target.style.boxShadow = 'inset 0 1px 3px rgba(0,0,0,0.05), 0 0 0 3px rgba(102, 126, 234, 0.1)';
                  e.target.style.transform = 'translateY(-1px)';
                }}
                onBlur={(e) => {
                  e.target.style.borderColor = '#e1e8ed';
                  e.target.style.boxShadow = 'inset 0 1px 3px rgba(0,0,0,0.05)';
                  e.target.style.transform = 'translateY(0)';
                }}
              />
            </div>

            {/* <div className="mb-3">
              <label htmlFor="empresa" className="form-label" style={{ fontWeight: '500', color: '#34495e' }}>
                Empresa
              </label>
              <input
                type="text"
                className="form-control"
                name="empresa"
                placeholder="Ingrese empresa"
                required
                style={{
                  borderRadius: '0.75rem',
                  padding: '0.75rem 1rem',
                  border: '1px solid #e1e8ed',
                  fontSize: '0.95rem',
                  transition: 'all 0.3s ease',
                  boxShadow: 'inset 0 1px 3px rgba(0,0,0,0.05)',
                  background: 'rgba(255,255,255,0.9)'
                }}
                onFocus={(e) => {
                  e.target.style.borderColor = '#667eea';
                  e.target.style.boxShadow = 'inset 0 1px 3px rgba(0,0,0,0.05), 0 0 0 3px rgba(102, 126, 234, 0.1)';
                  e.target.style.transform = 'translateY(-1px)';
                }}
                onBlur={(e) => {
                  e.target.style.borderColor = '#e1e8ed';
                  e.target.style.boxShadow = 'inset 0 1px 3px rgba(0,0,0,0.05)';
                  e.target.style.transform = 'translateY(0)';
                }}
              />
            </div> */}

            <div className="mb-4">
              <label htmlFor="password" className="form-label" style={{ fontWeight: '500', color: '#34495e' }}>
                Contraseña
              </label>
              <input
                type="password"
                className="form-control"
                name="clave"
                placeholder="Ingrese su contraseña"
                required
                style={{
                  borderRadius: '0.75rem',
                  padding: '0.75rem 1rem',
                  border: '1px solid #e1e8ed',
                  fontSize: '0.95rem',
                  transition: 'all 0.3s ease',
                  boxShadow: 'inset 0 1px 3px rgba(0,0,0,0.05)',
                  background: 'rgba(255,255,255,0.9)'
                }}
                onFocus={(e) => {
                  e.target.style.borderColor = '#667eea';
                  e.target.style.boxShadow = 'inset 0 1px 3px rgba(0,0,0,0.05), 0 0 0 3px rgba(102, 126, 234, 0.1)';
                  e.target.style.transform = 'translateY(-1px)';
                }}
                onBlur={(e) => {
                  e.target.style.borderColor = '#e1e8ed';
                  e.target.style.boxShadow = 'inset 0 1px 3px rgba(0,0,0,0.05)';
                  e.target.style.transform = 'translateY(0)';
                }}
              />
            </div>

            <button
              type="submit"
              className="btn w-100"
              style={{
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                border: 'none',
                borderRadius: '0.75rem',
                padding: '0.75rem 1.5rem',
                fontWeight: '600',
                fontSize: '1rem',
                transition: 'all 0.3s ease',
                boxShadow: `
                  0 4px 15px rgba(102, 126, 234, 0.4),
                  0 2px 5px rgba(102, 126, 234, 0.3)
                `,
                position: 'relative',
                overflow: 'hidden'
              }}
              onMouseEnter={(e) => {
                e.target.style.transform = 'translateY(-3px)';
                e.target.style.boxShadow = `
                  0 8px 25px rgba(102, 126, 234, 0.6),
                  0 4px 10px rgba(102, 126, 234, 0.4)
                `;
              }}
              onMouseLeave={(e) => {
                e.target.style.transform = 'translateY(0)';
                e.target.style.boxShadow = `
                  0 4px 15px rgba(102, 126, 234, 0.4),
                  0 2px 5px rgba(102, 126, 234, 0.3)
                `;
              }}
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  Iniciando Sesión...
                </>
              ) : (
                'Iniciar Sesión'
              )}
            </button>
          </form>

          {/* Pie de tarjeta */}
        <div className="text-center mt-3">
          <small
            style={{ cursor: 'pointer', color: '#667eea', fontWeight: 500 }}
            onClick={() => setMostrarRegistro(true)}
          >
            ¿No tienes una cuenta? Regístrate aquí
          </small>
        </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
