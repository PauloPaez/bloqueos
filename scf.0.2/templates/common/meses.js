// src/components/common/meses.js
export const mesANumero = {
    enero: 1,
    febrero: 2,
    marzo: 3,
    abril: 4,
    mayo: 5,
    junio: 6,
    julio: 7,
    agosto: 8,
    septiembre: 9,
    octubre: 10,
    noviembre: 11,
    diciembre: 12
  };
  
  export const numeroAMes = {
    1: "enero",
    2: "febrero",
    3: "marzo",
    4: "abril",
    5: "mayo",
    6: "junio",
    7: "julio",
    8: "agosto",
    9: "septiembre",
    10: "octubre",
    11: "noviembre",
    12: "diciembre"
  };
  
  export const mesesArray = [
    { id: 1, nombre: "enero" },
    { id: 2, nombre: "febrero" },
    { id: 3, nombre: "marzo" },
    { id: 4, nombre: "abril" },
    { id: 5, nombre: "mayo" },
    { id: 6, nombre: "junio" },
    { id: 7, nombre: "julio" },
    { id: 8, nombre: "agosto" },
    { id: 9, nombre: "septiembre" },
    { id: 10, nombre: "octubre" },
    { id: 11, nombre: "noviembre" },
    { id: 12, nombre: "diciembre" }
  ];
  
  // Función utilitaria para convertir nombre de mes a número
  export const convertirMesANumero = (nombreMes) => {
    if (!nombreMes) return null;
    return mesANumero[nombreMes.toLowerCase()] || null;
  };
  
  // Función utilitaria para convertir número de mes a nombre
  export const convertirNumeroAMes = (numeroMes) => {
    if (!numeroMes) return null;
    return numeroAMes[numeroMes] || null;
  };