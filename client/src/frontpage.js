import React, { useState, useEffect } from 'react';
import axios from 'axios';

const FrontPage = ({ selectedCategories, setSelectedCategories, navigateToPage }) => {
  const [categories, setCategories] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');

  // Fetch categories from the server
  useEffect(() => {
    axios.get('/data')
      .then(response => {
        const sortedCategories = response.data.categories.sort((a, b) => a.localeCompare(b));
        setCategories(sortedCategories);
      })
      .catch(error => {
        console.error('Error fetching categories:', error);
      });
  }, []);

  // Handle checkbox changes
  const handleCheckboxChange = (category) => {
    const newCategories = selectedCategories.includes(category)
      ? selectedCategories.filter(cat => cat !== category)
      : [...selectedCategories, category];
    setSelectedCategories(newCategories);
  };

  // Handle showing selected categories
  const handleShowSelected = () => {
    if (selectedCategories.length > 0) {
      navigateToPage('mainpage', null, selectedCategories);
    }
  };

  // Filter categories based on search query
  const filteredCategories = categories.filter(category =>
    category.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="front-page-container">
      <header className="App-header">
        <div className="App-logo" />
        <h1>Mind Map</h1>
      </header>
      <div className="App-select">
        <input
          className="search"
          type="text"
          placeholder="Search categories..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          style={{ padding: '5px' }}
        />
        <button
          className="btn"
          onClick={handleShowSelected}
          disabled={selectedCategories.length === 0}
        >
          Show selected categories
        </button>
      </div>
      <div className="categories-container">
        {Object.entries(
          filteredCategories.reduce((acc, category) => {
            const letter = category[0].toUpperCase();
            if (!acc[letter]) acc[letter] = [];
            acc[letter].push(category);
            return acc;
          }, {})
        ).map(([letter, categories]) => (
          <div key={letter} className="category-section">
            <h2 className="category-letter">{letter}</h2>
            <hr className="category-divider" />
            <div className="category-items">
              {categories.map(category => (
                <div key={category} className="category-item">
                  <input
                    type="checkbox"
                    id={category}
                    checked={selectedCategories.includes(category)}
                    onChange={() => handleCheckboxChange(category)}
                  />
                  <label htmlFor={category}>{category}</label>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default FrontPage;