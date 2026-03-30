import { useEffect, useState } from 'react'
import FeaturedSection from '../components/FeaturedSection.jsx'
import HeroSection from '../components/HeroSection.jsx'
import Footer from '../components/Footer.jsx'

function HomePage({ pageOrigin, pageTitle, searchQuery = '' }) {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    setLoading(true)
    setError('')

    fetch(`http://127.0.0.1:8000/api/cards/?origem_pagina=${encodeURIComponent(pageOrigin)}`)
      .then((response) => {
        if (!response.ok) throw new Error('Erro ao carregar produtos.')
        return response.json()
      })
      .then((data) => {
        setProducts(Array.isArray(data) ? data : [])
      })
      .catch(() => {
        setProducts([])
        setError('Não foi possível carregar produtos para esta página.')
      })
      .finally(() => {
        setLoading(false)
      })
  }, [pageOrigin])

  useEffect(() => {
    const path = pageOrigin === 'LOJA' ? '/loja' : `/${pageOrigin.toLowerCase()}`
    fetch('http://127.0.0.1:8000/api/visits/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ path }),
    }).catch(() => { })
  }, [pageOrigin])

  return (
    <>
      <main className="page-content">
        {loading && <div className="empty-search">Carregando conteúdo...</div>}
        {error && <div className="empty-search">{error}</div>}
        {!loading && !error && products.length === 0 && (
          <div className="empty-search">Nenhum item cadastrado para esta página.</div>
        )}

        <FeaturedSection
          products={products}
          searchQuery={searchQuery}
          pageTitle={pageTitle}
        />
        <HeroSection pageOrigin={pageOrigin} />
      </main>

      <Footer />
    </>
  )
}

export default HomePage
