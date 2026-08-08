const obtenerNombreArchivo = (contentDisposition, nombrePorDefecto) => {
  const match = contentDisposition.match(/filename="?([^";]+)"?/i);
  return match?.[1] || nombrePorDefecto;
};

export const descargarArchivo = async ({
  url,
  accept,
  nombrePorDefecto,
  mensajeError,
}) => {
  const response = await fetch(url, {
    method: "POST",
    headers: { Accept: accept },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || mensajeError);
  }

  const blob = await response.blob();
  const filename = obtenerNombreArchivo(
    response.headers.get("Content-Disposition") || "",
    nombrePorDefecto,
  );
  const urlArchivo = window.URL.createObjectURL(blob);
  const link = document.createElement("a");

  link.href = urlArchivo;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(urlArchivo);
};
