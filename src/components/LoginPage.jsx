import { useState } from 'react'

function LoginPage({ onLoginSuccess, onBack }) {
  const [mode, setMode] = useState('login')
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [errorMessage, setErrorMessage] = useState('')

  const resetForm = () => {
    setName('')
    setEmail('')
    setPassword('')
    setConfirmPassword('')
    setErrorMessage('')
  }

  const handleModeChange = (nextMode) => {
    setMode(nextMode)
    resetForm()
  }

  const handleSubmit = (event) => {
    event.preventDefault()

    if (mode === 'login') {
      if (!email.trim() || !password.trim()) {
        setErrorMessage('Por favor preencha todos os campos.')
        return
      }
    } else {
      if (!name.trim() || !email.trim() || !password.trim() || !confirmPassword.trim()) {
        setErrorMessage('Por favor preencha todos os campos para registrar.')
        return
      }
      if (password !== confirmPassword) {
        setErrorMessage('As senhas não coincidem.')
        return
      }
    }

    setErrorMessage('')
    onLoginSuccess()
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="auth-tabs">
          <button
            type="button"
            className={`auth-tab ${mode === 'login' ? 'active' : ''}`}
            onClick={() => handleModeChange('login')}
          >
            Entrar
          </button>
          <button
            type="button"
            className={`auth-tab ${mode === 'register' ? 'active' : ''}`}
            onClick={() => handleModeChange('register')}
          >
            Registrar
          </button>
        </div>

        <h2>{mode === 'login' ? 'Login' : 'Registrar'} </h2>
        <p>
          {mode === 'login'
            ? 'Entre na sua conta para continuar e acessar a loja.'
            : 'Crie sua conta para começar a comprar com estilo.'}
        </p>

        <form className="login-form" onSubmit={handleSubmit}>
          {mode === 'register' && (
            <>
              <label htmlFor="register-name">Nome completo</label>
              <input
                id="register-name"
                type="text"
                value={name}
                onChange={(event) => setName(event.target.value)}
                placeholder="Seu nome"
              />
            </>
          )}

          <label htmlFor="login-email">Email</label>
          <input
            id="login-email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="seu@email.com"
          />

          <label htmlFor="login-password">Senha</label>
          <input
            id="login-password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="********"
          />

          {mode === 'register' && (
            <>
              <label htmlFor="confirm-password">Confirmar senha</label>
              <input
                id="confirm-password"
                type="password"
                value={confirmPassword}
                onChange={(event) => setConfirmPassword(event.target.value)}
                placeholder="********"
              />
            </>
          )}

          {errorMessage && <p className="form-error">{errorMessage}</p>}

          <button type="submit" className="login-submit">
            {mode === 'login' ? 'Entrar' : 'Criar conta'}
          </button>
        </form>

        <div className="auth-footer">
          {mode === 'login' ? (
            <p>
              Ainda não tem conta?{' '}
              <button
                type="button"
                className="auth-switch"
                onClick={() => handleModeChange('register')}
              >
                Registrar
              </button>
            </p>
          ) : (
            <p>
              Já tem conta?{' '}
              <button
                type="button"
                className="auth-switch"
                onClick={() => handleModeChange('login')}
              >
                Fazer login
              </button>
            </p>
          )}
        </div>

        <button type="button" className="login-back" onClick={onBack}>
          Voltar para loja
        </button>
      </div>
    </div>
  )
}

export default LoginPage
