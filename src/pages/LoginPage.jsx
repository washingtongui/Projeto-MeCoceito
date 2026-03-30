import { useState } from 'react'

function LoginPage({ onLoginSuccess, onBack }) {
  const [mode, setMode] = useState('login')
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [errorMessage, setErrorMessage] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

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

  const handleSubmit = async (event) => {
    event.preventDefault()
    setErrorMessage('')

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

    setIsSubmitting(true)
    const url = mode === 'login'
      ? 'http://127.0.0.1:8000/api/auth/login/'
      : 'http://127.0.0.1:8000/api/auth/register/'
    const payload = {
      email: email.trim().toLowerCase(),
      password,
    }
    if (mode === 'register') {
      payload.name = name.trim()
    }

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      })

      const data = await response.json()
      if (!response.ok) {
        setErrorMessage(data.detail || data.email || data.password || 'Erro ao autenticar. Verifique suas credenciais.')
        return
      }

      localStorage.setItem('authToken', data.token)
      onLoginSuccess()
    } catch (error) {
      setErrorMessage('Erro de conexão. Tente novamente mais tarde.')
    } finally {
      setIsSubmitting(false)
    }
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

        <h2>{mode === 'login' ? 'Login' : 'Registrar'}</h2>
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
                autoComplete="name"
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
            autoComplete="email"
          />

          <label htmlFor="login-password">Senha</label>
          <input
            id="login-password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="********"
            autoComplete="current-password"
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
                autoComplete="new-password"
              />
            </>
          )}

          {errorMessage && (
            <p className="form-error" role="status" aria-live="polite">
              {errorMessage}
            </p>
          )}

          <button type="submit" className="login-submit" disabled={isSubmitting}>
            {isSubmitting
              ? mode === 'login'
                ? 'Entrando...'
                : 'Criando conta...'
              : mode === 'login'
              ? 'Entrar'
              : 'Criar conta'}
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
