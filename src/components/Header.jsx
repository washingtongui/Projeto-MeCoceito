import { NavLink } from 'react-router-dom'
import userIcon from '../assets/icons/user.png'
import logoImg from '../assets/logo/logo.png'

function Header({
  navItems,
  onLoginClick,
}) {
  return (
    <header className="site-header">
      <div className="brand-block">
        <img src={logoImg} alt="Me Conceito logo" className="brand-logo" />
        <span className="brand-name">ME CONCEITO</span>
      </div>

      <nav className="site-nav" aria-label="Main navigation">
        <ul>
          {navItems.map((item) => (
            <li key={item.path}>
              <NavLink
                to={item.path}
                className={({ isActive }) =>
                  isActive ? 'nav-button active' : 'nav-button'
                }
              >
                {item.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      <div className="header-icons">
        <button
          type="button"
          className="icon-button"
          aria-label="Login"
          onClick={onLoginClick}
        >
          <img src={userIcon} alt="User icon" />
        </button>
      </div>
    </header>
  )
}

export default Header
