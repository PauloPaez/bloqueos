import { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { Provider } from "react-redux";
import { store } from "./store/store";
import { BrowserRouter as Router } from "react-router-dom";
import Login from "./components/administracion/Login";
import ProtectedRoutes from "./components/administracion/Routes";
import { useSelector } from "react-redux";

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

function App() {
  return (
    <Provider store={store}>
      <AppWrapper />
    </Provider>
  );
}

export default App;
