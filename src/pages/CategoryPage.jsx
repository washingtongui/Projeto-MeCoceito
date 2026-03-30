import { useEffect, useState } from 'react'
import { NavLink, useParams } from 'react-router-dom'
import HeroSection from '../components/HeroSection.jsx'
import Footer from '../components/Footer.jsx'

function CategoryPage({ pageSlug, pageTitle }) {
  const { sectionSlug } = useParams()
  const [category, setCategory] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const formatPrice = (value) => {
    const numberValue = Number(value)
    if (Number.isNaN(numberValue)) return ''
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(numberValue)
  }

  useEffect(() => {
    setLoading(true)
    setError('')
    setCategory(null)

    fetch(`http://127.0.0.1:8000/api/categories/${pageSlug}/`)
      .then((response) => {
        if (!response.ok) throw new Error('Categoria não encontrada.')
        return response.json()
      })
      .then((data) => {
        setCategory(data)
      })
      .catch(() => {
        setError('Não foi possível carregar esta página.')
      })
      .finally(() => setLoading(false))
  }, [pageSlug])

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/visits/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ path: `/${pageSlug}${sectionSlug ? `/${sectionSlug}` : ''}` }),
    }).catch(() => {})
  }, [pageSlug, sectionSlug])

  if (loading) {
    return (
      <>
        <main className="page-content">
          <div className="empty-search">Carregando conteúdo...</div>
        </main>
        <Footer />
      </>
    )
  }

  if (error) {
    return (
      <>
        <main className="page-content">
          <div className="empty-search">{error}</div>
        </main>
        <Footer />
      </>
    )
  }

  if (!category) {
    return (
      <>
        <main className="page-content">
          <div className="empty-search">Categoria indisponível.</div>
        </main>
        <Footer />
      </>
    )
  }

  const uncategorizedSection = category.uncategorized_products?.length
    ? [
        {
          id: 'uncategorized',
          name: 'Outras peças',
          slug: 'sem-secao',
          description: 'Produtos sem seção definida',
          order: 999,
          products: category.uncategorized_products,
        },
      ]
    : []

  const allSections = [...category.sections, ...uncategorizedSection]
  const visibleSections = sectionSlug
    ? allSections.filter((section) => section.slug === sectionSlug)
    : allSections

  return (
    <>
      <main className="page-content">
        <section className="category-page">
          <div className="category-page-header">
            <h1>{pageTitle}</h1>
            {category.description && (
              <p className="category-description">{category.description}</p>
            )}
          </div>

          {(category.sections.length > 0 || category.uncategorized_products?.length > 0) && (
            <div className="subcategory-tabs">
              <NavLink
                to={`/${pageSlug}`}
                className={({ isActive }) =>
                  isActive ? 'subcategory-tab active' : 'subcategory-tab'
                }
              >
                Todos
              </NavLink>
              {category.sections.map((section) => (
                <NavLink
                  key={section.id}
                  to={`/${pageSlug}/${section.slug}`}
                  className={({ isActive }) =>
                    isActive ? 'subcategory-tab active' : 'subcategory-tab'
                  }
                >
                  {section.name}
                </NavLink>
              ))}
              {category.uncategorized_products?.length > 0 && (
                <NavLink
                  key="uncategorized"
                  to={`/${pageSlug}/sem-secao`}
                  className={({ isActive }) =>
                    isActive ? 'subcategory-tab active' : 'subcategory-tab'
                  }
                >
                  Outras peças
                </NavLink>
              )}
            </div>
          )}

          {visibleSections.length === 0 ? (
            <div className="empty-search">Nenhuma subcategoria encontrada.</div>
          ) : (
            visibleSections.map((section) => {
              return (
                <section key={section.id} className="category-group">
                  <div className="category-group-header">
                    <h2>{section.name}</h2>
                    {section.description && (
                      <p className="category-group-description">
                        {section.description}
                      </p>
                    )}
                  </div>

                  {section.products.length === 0 ? (
                    <div className="empty-search">
                      Nenhum produto cadastrado em {section.name}.
                    </div>
                  ) : (
                    <div className="product-grid">
                      {section.products.map((product) => {
                        return (
                          <article
                            key={product.id ?? `${product.name}-${product.price}`}
                            className="product-card"
                          >
                            <div className={`product-image ${product.color ?? 'light'}`}>
                              {product.image_url ? (
                                <img
                                  className="product-picture"
                                  src={product.image_url}
                                  alt={product.name}
                                  loading="lazy"
                                />
                              ) : (
                                <div className="product-image-placeholder">
                                  Sem imagem
                                </div>
                              )}
                            </div>
                            <div className="product-info">
                              <div className="product-title-block">
                                <strong className="product-name">{product.name}</strong>
                                <span className="product-price">
                                  {formatPrice(product.price)}
                                </span>
                              </div>
                              <button type="button" className="product-button">
                                Adicionar ao carrinho
                              </button>
                            </div>
                          </article>
                        )
                      })}
                    </div>
                  )}
                </section>
              )
            })
          )}
        </section>

        {pageSlug === 'novidades' && <HeroSection pageOrigin={pageSlug} />}
      </main>
      <Footer />
    </>
  )
}

export default CategoryPage
