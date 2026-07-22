const ensureTrailingSlash = (url) => (url.endsWith("/") ? url : `${url}/`);

const rawApiBase = import.meta.env.VITE_API_BASE_URL;
const fallbackApiBase = typeof window !== "undefined" ? window.location.origin : "";

const rawWsBase = import.meta.env.VITE_WS_BASE_URL;

export const API_BASE_URL = ensureTrailingSlash(rawApiBase || fallbackApiBase);

const derivedWsBase = API_BASE_URL.replace(
  /^https?:/,
  API_BASE_URL.startsWith("https:") ? "wss:" : "ws:"
);

export const WS_BASE_URL = ensureTrailingSlash(rawWsBase ?? derivedWsBase);
