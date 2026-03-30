function NewsletterSection() {
  return (
    <section className="newsletter-section">
      <div className="newsletter-label">Receba nossas ofertas</div>
      <form className="newsletter-form">
        <label htmlFor="email" className="visually-hidden">
          Endereço de email
        </label>
        <input
          id="email"
          type="email"
          placeholder="Seu email"
          aria-label="Endereço de email"
          autoComplete="email"
        />
        <button type="submit">Enviar</button>
      </form>
    </section>
  )
}

export default NewsletterSection
