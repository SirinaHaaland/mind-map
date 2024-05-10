import React, { useState, useEffect } from 'react';
import MainRecPage from './mainrecpage'; 
import MainPage from './mainpage';
import FilterPage from './filterpage';
import FrontPage from './frontpage';
import About from './about';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [selectedCategories, setSelectedCategories] = useState([]);
  const [filename, setFilename] = useState(null);

  useEffect(() => {
    window.onpopstate = (event) => {
      const page = event.state ? event.state.page : 'home';
      setCurrentPage(page);
    };
  }, []);

  useEffect(() => {
    handleCategorySelect();
    updateURL(currentPage);
  }, [selectedCategories, currentPage]);

  const navigateToPage = (page, filename) => {
    setCurrentPage(page);
    setFilename(filename);
  };

  const handleCategorySelect = () => {
    if(currentPage === 'mainrec')return;
    if (currentPage ==='about')return;
    if (selectedCategories.length > 0) {
      setCurrentPage('mainpage');
    } 
    else {
      setCurrentPage('home');
    }
  };

  const handleHomeClick = () => {
    setSelectedCategories([]);
    setCurrentPage('home');
  };

  const updateURL = (page) => {
    window.history.pushState({ page }, '', `/${page}`);
  };

  return (
    <div className='NavL'>
      <NavigationLinks currentPage={currentPage} handleHomeClick={handleHomeClick} navigateToPage={navigateToPage} selectedCategories={selectedCategories} />
      {currentPage === 'home' && (
        <div>
          <FilterPage selectedCategories={selectedCategories} setSelectedCategories={setSelectedCategories} />
          <FrontPage setSelectedCategories={setSelectedCategories} setCurrentPage={setCurrentPage} /> 
        </div>
      )}
      {currentPage === 'mainpage' && (
        <div>
          <FilterPage selectedCategories={selectedCategories} setSelectedCategories={setSelectedCategories} />
          <MainPage selectedCategories={selectedCategories} navigateToPage={navigateToPage} />
        </div>
      )}
      {currentPage === 'mainrec' && (
        <MainRecPage filename={filename} />
      )}
      {currentPage === 'about' && (
        <About />
      )}
    </div>
  );
}

function NavigationLinks({ handleHomeClick, currentPage, navigateToPage, selectedCategories }) {
  return (
    <div className='NavB'>
      {currentPage === 'mainrec' && (
        <button onClick={() => navigateToPage('mainpage', null)}>Back</button>
      )}
      {currentPage === 'mainpage' && selectedCategories.length > 0 && (
        <button onClick={handleHomeClick}>Home</button>
      )}
      {currentPage === 'about' &&(
        <button onClick={handleHomeClick}>Home</button>
      )
      }
    </div>
  );
}

export default App;
