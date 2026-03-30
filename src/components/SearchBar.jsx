function SearchBar({ isOpen, value, onChange }) {
  return (
    <div className={isOpen ? 'search-bar open' : 'search-bar'}>
      <input
        className="search-input"
        type="search"
        placeholder="Pesquisar produtos..."
        value={value}
        onChange={(event) => onChange(event.target.value)}
        aria-label="Pesquisar produtos"
      />
    </div>
  )
}

export default SearchBar
