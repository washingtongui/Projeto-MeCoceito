import { useState } from 'react'
import { Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom'
import './App.css'
import Header from './components/Header.jsx'
import HomePage from './pages/HomePage.jsx'
import AboutPage from './pages/AboutPage.jsx'
import LoginPage from './pages/LoginPage.jsx'
import CategoryPage from './pages/CategoryPage.jsx'

const navigationItems = [
  { label: 'Loja', path: '/' },
  { label: 'Novidades', path: '/novidades' },
  { label: 'Feminino', path: '/feminino' },
  { label: 'Masculino', path: '/masculino' },
  { label: 'Sobre', path: '/sobre' },
]

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(
    Boolean(localStorage.getItem('authToken')),
  )
  const navigate = useNavigate()
  const location = useLocation()
  const isLoginPage = location.pathname === '/login'

  const handleLoginClick = () => {
    navigate('/login')
  }

  const handleLoginSuccess = () => {
    setIsLoggedIn(true)
    navigate('/')
  }

  return (
    <div className="site-shell">
      <Header
        navItems={navigationItems}
        onLoginClick={handleLoginClick}
      />

      <Routes>
        <Route
          path="/"
          element={
            <HomePage
              pageOrigin="LOJA"
              pageTitle="Loja"
            />
          }
        />
        <Route
          path="/loja"
          element={
            <HomePage
              pageOrigin="LOJA"
              pageTitle="Loja"
            />
          }
        />
        <Route
          path="/novidades"
          element={
            <CategoryPage
              pageSlug="novidades"
              pageTitle="Novidades"
            />
          }
        />
        <Route
          path="/novidades/:sectionSlug"
          element={
            <CategoryPage
              pageSlug="novidades"
              pageTitle="Novidades"
            />
          }
        />
        <Route
          path="/feminino"
          element={
            <CategoryPage
              pageSlug="feminino"
              pageTitle="Feminino"
            />
          }
        />
        <Route
          path="/feminino/:sectionSlug"
          element={
            <CategoryPage
              pageSlug="feminino"
              pageTitle="Feminino"
            />
          }
        />
        <Route
          path="/masculino"
          element={
            <CategoryPage
              pageSlug="masculino"
              pageTitle="Masculino"
            />
          }
        />
        <Route
          path="/masculino/:sectionSlug"
          element={
            <CategoryPage
              pageSlug="masculino"
              pageTitle="Masculino"
            />
          }
        />
        <Route path="/sobre" element={<AboutPage />} />
        <Route
          path="/login"
          element={
            <LoginPage
              onLoginSuccess={handleLoginSuccess}
              onBack={() => navigate('/')}
            />
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  )
}

export default App
