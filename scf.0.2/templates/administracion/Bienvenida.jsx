import React from 'react';
import logo from '../../assets/TDS.png'; // Importamos el logo desde src/assets

const Bienvenida = () => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh', textAlign: 'center' }}>
      <img src={logo} alt="Logo TDS" style={{ width: '300px', height: 'auto', marginBottom: '20px' }} /> {/* Imagen centrada y más grande */}
      <h1 style={{ fontSize: '2rem', margin: 0 }}>TDS saluda</h1> {/* Texto debajo del logo */}
    </div>
  );
};

export default Bienvenida;

