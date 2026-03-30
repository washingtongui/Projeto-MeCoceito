function FeaturedSection({ products, searchQuery = '', pageTitle }) {
  const normalizedQuery = searchQuery.trim().toLowerCase()
  const filteredProducts = normalizedQuery
    ? products.filter((product) =>
      [product.name, product.description]
        .join(' ')
        .toLowerCase()
        .includes(normalizedQuery),
    )
    : products

  const formatPrice = (value) => {
    const numberValue = Number(value)
    if (Number.isNaN(numberValue)) return ''
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(numberValue)
  }

  return (
    <section className="featured-section">
      <div className="featured-header">
        <span className="breadcrumb">{pageTitle.toUpperCase()} &gt; NEW</span>
        <h1>{pageTitle}</h1>
      </div>

      {filteredProducts.length === 0 ? (
        <div className="empty-search">Nenhum produto encontrado.</div>
      ) : (
        <div className="product-grid">
          {filteredProducts.map((product) => (
            <article
              key={product.id ?? `${product.name}-${product.price}`}
              className="product-card"
            >
              <div className={`product-image ${product.color ?? 'light'}`}>
                {product.image_url && (
                  <img
                    className="product-picture"
                    src={product.image_url}
                    alt={product.name}
                    loading="lazy"
                  />
                )}
                <span className="product-tag">{product.description}</span>
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
          ))}
        </div>
      )}
    </section>
  )
}

export default FeaturedSection
