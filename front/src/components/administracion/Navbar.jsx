import { useEffect, useRef, useState } from "react";
import { ChevronDown, LogOut, Menu, MoreHorizontal, User, X } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { resetAcceso, resetFila } from "../../store/appSlice";
import "./Navbar.css";

const MAX_VISIBLE_ITEMS = 4;

const SubMenu = ({ menu, open, onToggle, onClose }) => {
  const hasLinks = menu.links.length > 0;

  return (
    <div className="navbar-menu-item">
      <button
        type="button"
        className="navbar-menu-trigger"
        aria-expanded={open}
        onClick={onToggle}
      >
        {menu.title}
        {hasLinks && <ChevronDown size={15} aria-hidden="true" />}
      </button>
      {open && hasLinks && (
        <div className="navbar-dropdown">
          {menu.links.map((link) => (
            <Link key={link.to} to={link.to} className="navbar-dropdown-link" onClick={onClose}>
              {link.label}
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};

const MobileMenu = ({ menus, onClose }) => (
  <div className="navbar-mobile-menu">
    <div className="navbar-mobile-menu-title">Menú</div>
    {menus.map((menu) => (
      <div className="navbar-mobile-group" key={menu.title}>
        <div className="navbar-mobile-group-title">{menu.title}</div>
        {menu.links.map((link) => (
          <Link key={link.to} to={link.to} className="navbar-mobile-link" onClick={onClose}>
            {link.label}
          </Link>
        ))}
      </div>
    ))}
  </div>
);

const Navbar = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const navRef = useRef(null);
  const user = useSelector((state) => state.acceso.user);
  const [openMenu, setOpenMenu] = useState(null);
  const [mobileOpen, setMobileOpen] = useState(false);

  const dynamicMenus = (() => {
    if (!user?.opciones?.length) return [];

    const groupedMenus = user.opciones.reduce((acc, opcion) => {
      const category = opcion.path.split("/")[1];
      if (!acc[category]) acc[category] = [];
      acc[category].push({
        label: opcion.componente.replace(/([A-Z])/g, " $1").trim(),
        to: opcion.path,
      });
      return acc;
    }, {});

    return Object.entries(groupedMenus).map(([title, links]) => ({ title, links }));
  })();

  const visibleMenus = dynamicMenus.slice(0, MAX_VISIBLE_ITEMS);
  const overflowMenus = dynamicMenus.slice(MAX_VISIBLE_ITEMS);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (navRef.current && !navRef.current.contains(event.target)) {
        setOpenMenu(null);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const closeMenus = () => setOpenMenu(null);

  const handleLogout = () => {
    dispatch(resetFila());
    dispatch(resetAcceso());
    navigate("/login");
  };

  const toggleMenu = (menuName) => {
    setOpenMenu((current) => (current === menuName ? null : menuName));
  };

  return (
    <nav ref={navRef} className="app-navbar">
      <div className="navbar-inner">
        <button
          type="button"
          className="navbar-mobile-trigger"
          aria-label={mobileOpen ? "Cerrar menú" : "Abrir menú"}
          aria-expanded={mobileOpen}
          onClick={() => setMobileOpen((current) => !current)}
        >
          {mobileOpen ? <X size={20} /> : <Menu size={20} />}
        </button>

        <div className="navbar-desktop-menus">
          {visibleMenus.map((menu) => (
            <SubMenu
              key={menu.title}
              menu={menu}
              open={openMenu === menu.title}
              onToggle={() => toggleMenu(menu.title)}
              onClose={closeMenus}
            />
          ))}
          {overflowMenus.length > 0 && (
            <div className="navbar-menu-item">
              <button
                type="button"
                className="navbar-menu-trigger"
                aria-expanded={openMenu === "__more__"}
                onClick={() => toggleMenu("__more__")}
              >
                <MoreHorizontal size={16} aria-hidden="true" />
                Más
                <ChevronDown size={15} aria-hidden="true" />
              </button>
              {openMenu === "__more__" && (
                <div className="navbar-dropdown navbar-more-dropdown">
                  {overflowMenus.map((menu) => (
                    <div className="navbar-more-group" key={menu.title}>
                      <div className="navbar-more-title">{menu.title}</div>
                      {menu.links.map((link) => (
                        <Link key={link.to} to={link.to} className="navbar-dropdown-link" onClick={closeMenus}>
                          {link.label}
                        </Link>
                      ))}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>

        <div className="navbar-account">
          <div className="navbar-area">
            {/* <span>Área</span> */}
            <span className="navbar-area-value">{user?.empresa || "Desconocido"}</span>
          </div>
          <span className="navbar-separator" aria-hidden="true" />
          <button
            type="button"
            className="navbar-user-trigger"
            aria-expanded={openMenu === "__user__"}
            onClick={() => toggleMenu("__user__")}
          >
            <span className="navbar-user-avatar"><User size={14} aria-hidden="true" /></span>
            <span className="navbar-username">{user?.login || "Desconocido"}</span>
            <ChevronDown size={14} aria-hidden="true" />
          </button>
          {openMenu === "__user__" && (
            <div className="navbar-dropdown navbar-user-dropdown">
              <div className="navbar-user-details">
                <strong>{user?.login || "Desconocido"}</strong>
                <span>Área {user?.empresa || "Desconocido"}</span>
              </div>
              <button type="button" className="navbar-logout" onClick={handleLogout}>
                <LogOut size={16} aria-hidden="true" />
                Cerrar sesión
              </button>
            </div>
          )}
        </div>
      </div>

      {mobileOpen && <MobileMenu menus={dynamicMenus} onClose={() => setMobileOpen(false)} />}
    </nav>
  );
};

export default Navbar;
