import { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { Provider } from "react-redux";
import { store } from "./store/store";
import { BrowserRouter as Router } from "react-router-dom";
import Login from "./components/administracion/Login";
import ProtectedRoutes from "./components/administracion/Routes";
import { useSelector } from "react-redux";
import { Toaster } from "sonner";

function AppWrapper() {
  const accesos = useSelector((state) => state.acceso.user);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Verifica si `accesos` tiene datos válidos
    if (accesos && accesos.login && accesos.opciones) {
      setIsAuthenticated(true);
    } else {
      setIsAuthenticated(false);
    }
  }, [accesos]);

  return (
    <Router>
      {isAuthenticated ? <ProtectedRoutes /> : <Login />}
    </Router>
  );
}

// La duracion del toaster es en ms, richColors es para que tenga colores dependiendo del estado de la noti, success: verde, etc
function App() {
  return (
    <Provider store={store}>
      <Toaster position="top-right" duration={5000} richColors/>
      <AppWrapper />
    </Provider>
  );
}

export default App;
