import NewsletterSection from '../components/NewsletterSection.jsx'
import Footer from '../components/Footer.jsx'

function AboutPage() {
  return (
    <>
      <section className="about-page">
        <div className="about-page-card">
          <h1>Sobre a loja</h1>
          <p>
            A Me Conceito é a sua referência em moda urbana premium. Nosso objetivo é
            oferecer peças com estilo contemporâneo, qualidade superior e design
            sofisticado para clientes exigentes.
          </p>
          <p>
            Nossa loja se inspira em tendências globais e oferece um mix exclusivo de
            produtos para um guarda-roupa elegante e contemporâneo.
          </p>
          <div className="contact-details">
            <h2>Entre em contato</h2>
            <ul>
              <li>
                <strong>Telefone:</strong> +55 (11) 99999-9999
              </li>
              <li>
                <strong>Email:</strong> contato@meconceito.com
              </li>
              <li>
                <strong>Instagram:</strong> @meconceito.oficial
              </li>
              <li>
                <strong>Endereço:</strong> Av. Paulista, 1234, Bela Vista, São Paulo - SP
              </li>
            </ul>
          </div>
        </div>
      </section>
      <NewsletterSection />
      <Footer />
    </>
  )
}

export default AboutPage
