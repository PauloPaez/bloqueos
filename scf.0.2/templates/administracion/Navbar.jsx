import { Link, useNavigate } from "react-router-dom";
import { useState, useRef, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { resetAcceso, resetFila } from '../../store/appSlice';

const SubMenu = ({ title, links, isOpen, onToggle, onClose }) => (
  <div style={{ display: "inline-block", position: "relative" }}>
    <button
      onClick={onToggle}
      style={{ color: "#fff", background: "none", border: "none", cursor: "pointer" }}
    >
      {title}
    </button>
    {isOpen && (
      <div
        style={{
          position: "absolute",
          top: "100%",
          left: 0,
          backgroundColor: "#555",
          color: "#fff",
          padding: "0.5rem",
          borderRadius: "5px",
          zIndex: 100,
          minWidth: "200px", // Aumenta el ancho del submenu
        }}
      >
        {links.map((link) => (
          <Link
            key={link.to}
            to={link.to}
            onClick={onClose}
            style={{ display: "block", color: "#fff", textDecoration: "none", padding: "0.5rem 0" }}
          >
            {link.label}
          </Link>
        ))}
      </div>
    )}
  </div>
);

const Navbar = () => {
  const dispatch = useDispatch();
  const [subMenus, setSubMenus] = useState({});
  const navRef = useRef(null);
  const navigate = useNavigate();
  const user = useSelector((state) => state.acceso.user); // Recuperar el usuario desde Redux

  const toggleSubMenu = (menuName) => {
    setSubMenus((prev) => ({ ...prev, [menuName]: !prev[menuName] }));
  };

  const closeAllSubMenus = () => setSubMenus({});

  const handleLogout = () => {
    dispatch(resetFila());
    dispatch(resetAcceso());
    navigate("/login");
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (navRef.current && !navRef.current.contains(event.target)) {
        closeAllSubMenus();
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Función para generar los menús dinámicamente basados en los permisos del usuario
  const generateDynamicMenus = () => {
    if (!user || !user.opciones || user.opciones.length === 0) return [];

    // Agrupar los permisos por categoría (primer segmento del path)
    const groupedMenus = user.opciones.reduce((acc, opcion) => {
      const category = opcion.path.split("/")[1]; // Ej: "Usuarios" o "Roles"
      if (!acc[category]) {
        acc[category] = [];
      }
      acc[category].push({
        label: opcion.componente.replace(/([A-Z])/g, " $1").trim(), // Formatea el nombre del componente
        to: opcion.path,
      });
      return acc;
    }, {});

    // Convertir el objeto agrupado en un array de menús
    return Object.entries(groupedMenus).map(([category, links]) => ({
      title: category,
      links,
    }));
  };

  const dynamicMenus = generateDynamicMenus();

  return (
    <nav
      ref={navRef}
      style={{
        display: "flex",
        justifyContent: "space-between",
        padding: "1rem",
        backgroundColor: "#333",
        color: "#fff",
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-evenly",
          flexGrow: 1,
        }}
      >
        {dynamicMenus.map((menu) => (
          <SubMenu
            key={menu.title}
            title={menu.title}
            links={menu.links}
            isOpen={subMenus[menu.title]}
            onToggle={() => toggleSubMenu(menu.title)}
            onClose={closeAllSubMenus}
          />
        ))}
      </div>
      <div style={{ display: "flex", alignItems: "center" }}>
        <span style={{ marginRight: "1rem", color: "yellow" }}>{user ? user.empresa : "Desconocido"}</span>
        <span onClick={handleLogout} style={{ cursor: "pointer", textDecoration: "underline" }}>
          {user ? user.login : "Desconocido"}
        </span>
      </div>
    </nav>
  );
};

export default Navbar;
