import React, { useState, useEffect, useCallback } from 'react';
import MainRecPage from './mainrecpage';
import MainPage from './mainpage';
import FilterPage from './filterpage';
import FrontPage from './frontpage';
import About from './about';
import { AppBar, Toolbar, Button, Box } from '@mui/material';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [selectedCategories, setSelectedCategories] = useState([]);
  const [filename, setFilename] = useState(null);

  // Load selectedCategories from localStorage when the component mounts
  useEffect(() => {
    const savedCategories = localStorage.getItem('selectedCategories');
    if (savedCategories) {
      setSelectedCategories(JSON.parse(savedCategories));
    }
  }, []);

  // Define updateURL first and memoize it.
  const updateURL = useCallback((page, filename, categories) => {
    const path = filename ? `/${page}/${filename}` : `/${page}`;
    window.history.pushState({ page, filename, categories }, '', path);
  }, []);

  // Memoize navigation function; include updateURL in dependency array.
  const navigateToPage = useCallback((page, filename = null, categories = null) => {
    setCurrentPage((prevPage) => {
      // Preserve categories when navigating away from mainpage
      const preservedCategories = prevPage === 'mainpage' ? selectedCategories : categories;
      updateURL(page, filename, preservedCategories);
      return page;
    });

    if (categories !== null) {
      setSelectedCategories(categories);
    }
    setFilename(filename);
  }, [updateURL, selectedCategories]);

  // Stable handler for home click
  const handleHomeClick = useCallback(() => {
    navigateToPage('home');
  }, [navigateToPage]);

  // Memoized mind map click handler
  const handleMindMapClick = useCallback(() => {
    navigateToPage('mainpage', null, selectedCategories);
  }, [navigateToPage, selectedCategories]);

  // Update history state when categories change
  useEffect(() => {
    if (currentPage === 'mainpage') {
      // Update the current history entry with latest categories
      window.history.replaceState(
        { ...window.history.state, categories: selectedCategories },
        '',
        window.location.href
      );
    }
  }, [selectedCategories, currentPage]);

  // History state management
  useEffect(() => {
    const handlePopState = (event) => {
      const newState = {
        ...window.history.state,
        ...(event.state || {}),
      };

      setCurrentPage(newState.page || 'home');

      if (newState.page === 'mainrec' && newState.filename) {
        setFilename(newState.filename);
      }
      if (newState.page === 'mainpage') {
        setSelectedCategories(newState.categories || []);
      }
    };

    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  // Reset state on page refresh
  useEffect(() => {
    if (performance.navigation.type === 1) {
      // Type 1 indicates a page reload
      setCurrentPage('home');
      setFilename(null);
      setSelectedCategories([]);
      window.history.replaceState({}, '', '/');
    }
  }, []);

  // Save selectedCategories to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('selectedCategories', JSON.stringify(selectedCategories));
  }, [selectedCategories]);

  return (
    <div className="App">
      <AppBar position="fixed" className="NavL">
        <Toolbar>
          <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
            <MemoNavigationLinks
              currentPage={currentPage}
              handleHomeClick={handleHomeClick}
              handleMindMapClick={handleMindMapClick}
              navigateToPage={navigateToPage}
            />
          </Box>
        </Toolbar>
      </AppBar>

      <div style={{ marginTop: '40px' }}>
        {/* Home Page */}
        <div style={{ display: currentPage === 'home' ? 'block' : 'none' }}>
          <FrontPage
            selectedCategories={selectedCategories}
            setSelectedCategories={setSelectedCategories}
            navigateToPage={navigateToPage}
          />
        </div>

        {/* Main Page (MindMap) */}
        <div style={{ display: currentPage === 'mainpage' ? 'flex' : 'none' }}>
          <FilterPage
            selectedCategories={selectedCategories}
            setSelectedCategories={setSelectedCategories}
          />
          <MainPage
            selectedCategories={selectedCategories}
            navigateToPage={navigateToPage}
          />
        </div>

        {/* MainRec Page - Ensure it unmounts when navigating away */}
        {currentPage === 'mainrec' ? <MainRecPage filename={filename} /> : null}

        {/* About Page */}
        <div style={{ display: currentPage === 'about' ? 'block' : 'none' }}>
          <About />
        </div>
      </div>
    </div>
  );
}

// Memoized navigation links
const MemoNavigationLinks = React.memo(({ 
  handleHomeClick, 
  currentPage, 
  handleMindMapClick, 
  navigateToPage 
}) => (
  <>
    <Button
      color="inherit"
      onClick={handleHomeClick}
      style={{ fontWeight: currentPage === 'home' ? 'bold' : 'normal' }}
    >
      Home
    </Button>
    <Button
      color="inherit"
      onClick={handleMindMapClick}
      style={{ fontWeight: currentPage === 'mainpage' ? 'bold' : 'normal' }}
    >
      Mind Map
    </Button>
    <Button
      color="inherit"
      onClick={() => navigateToPage('about')}
      style={{ fontWeight: currentPage === 'about' ? 'bold' : 'normal' }}
    >
      About
    </Button>
  </>
));

export default App;