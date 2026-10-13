// src/hooks/useBuscarPersona.js
import { useState, useEffect } from 'react';
import { usePostPersonasByFieldMutation } from '../store/apiSlice';
import { useSelector } from 'react-redux';

export const useBuscarPersona = () => {
  const [buscarPersonasByField] = usePostPersonasByFieldMutation();
  const user = useSelector((state) => state.acceso.user);
  const [persona, setPersona] = useState(null);
  const [loading, setLoading] = useState(false);

  const buscarPersona = async (filtro = null) => {
    const filtroBusqueda = filtro || {
      "login_cnx": user?.login,
      "empresa_cnx": user?.empresa
    };

    if (!filtroBusqueda.login_cnx || !filtroBusqueda.empresa_cnx) {
      console.log('*Faltan parámetros para buscar persona');
      return null;
    }

    setLoading(true);
    try {
      const response = await buscarPersonasByField(filtroBusqueda).unwrap();
      if (response.length > 0) {
        const personaRecuperada = response[0];
        setPersona(personaRecuperada);
        return personaRecuperada;
      } else {
        setPersona(null);
        return null;
      }
    } catch (error) {
      console.error('Error al buscar persona:', error);
      setPersona(null);
      return null;
    } finally {
      setLoading(false);
    }
  };

  // Búsqueda automática al montar
  useEffect(() => {
    if (user?.login && user?.empresa) {
      buscarPersona();
    }
  }, [user?.login, user?.empresa]);

  return {
    persona,
    loading,
    buscarPersona
  };
};