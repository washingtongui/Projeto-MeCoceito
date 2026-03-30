import { useEffect, useState } from 'react'

function HeroSection({ pageOrigin }) {
  const [showcase, setShowcase] = useState({
    hero_title: 'ME CONCEITO',
    hero_description: 'Moda premium feita para sua rotina.',
    hero_image_url: '',
    button_label: 'SAIBA MAIS',
  })

  useEffect(() => {
    const query = pageOrigin
      ? `?origem_pagina=${encodeURIComponent(pageOrigin)}`
      : ''

    fetch(`http://127.0.0.1:8000/api/store-showcase/${query}`)
      .then((response) => response.json())
      .then((data) => {
        setShowcase((previous) => ({
          hero_title: data.hero_title || previous.hero_title,
          hero_description: data.hero_description || previous.hero_description,
          hero_image_url: data.hero_image_url || previous.hero_image_url,
          button_label: data.button_label || previous.button_label,
        }))
      })
      .catch(() => { })
  }, [pageOrigin])

  const heroStyle = showcase.hero_image_url
    ? { backgroundImage: `url(${showcase.hero_image_url})` }
    : {}

  return (
    <section className="hero-section">
      <div className="hero-card" style={heroStyle}>
        <div className="hero-content">
          <span className="hero-label">SHOP NOW</span>
          <h2>{showcase.hero_title}</h2>
          <p>{showcase.hero_description}</p>
          <button type="button" className="hero-button">
            {showcase.button_label}
          </button>
        </div>
      </div>
    </section>
  )
}

export default HeroSection
