import React, { useState, useEffect } from 'react';
import axios from 'axios';


const FrontPage = ({ setSelectedCategories, setCurrentPage }) => { 
  const [categories, setCategories] = useState([]);
  const [selectedCategoriesLocal, setSelectedCategoriesLocal] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  
  // Fetch categories from the server when the component mounts
  // and update the state with the sorted categories.
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

  const handleCheckboxChange = (category) => {
    if (selectedCategoriesLocal.includes(category)) {
      setSelectedCategoriesLocal(selectedCategoriesLocal.filter(cat => cat !== category));
    } else {
      setSelectedCategoriesLocal([...selectedCategoriesLocal, category]);
    }
  };

  const handleShowSelected = () => {
    setSelectedCategories(selectedCategoriesLocal);
  };

  const handleLearnMoreClick = (event) => {
    event.preventDefault();
    setCurrentPage('about');
  };

  // Filter categories based on search query
  const filteredCategories = categories.filter(category =>
    category.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div>
      <header className="App-header">
        <div className="App-logo" /> 
        <h1>Welcome to the Mind Map</h1>
        <p className="App-link">
          <a href="#" onClick={handleLearnMoreClick}>About</a>
        </p>
      </header>
      <div className= 'App-select'>
        <input className="search"
          type="text"
          placeholder="Search categories..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          style={{ padding: '5px' }}
        />
        <button className="btn" onClick={handleShowSelected}>Show selected topics</button>
      </div>
      <div style={{ display: 'grid',flexDirection: 'column', gridTemplateColumns: 'repeat(auto-fill, minmax(100px, 1fr))', gap: '10px', maxHeight: '335px', overflowY: 'auto', marginTop: '15px'}}>
        {filteredCategories.map(category => (
          <div key={category} className="category-item">
            <input
              type="checkbox"
              id={category}
              checked={selectedCategoriesLocal.includes(category)}
              onChange={() => handleCheckboxChange(category)}
            />
            <label htmlFor={category}>{category}</label>
          </div>
        ))}
      </div>
      </div>
  );
};

export default FrontPage;
