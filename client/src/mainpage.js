import React from 'react';
import Mindmap from './mindmap';
import './app.css';

function MainPage({ selectedCategories, navigateToPage }) {
  return (
    <div className="main-page-container">
      <div className="mind-map-grid">
        {selectedCategories.map((category) => (
          <div key={category} className="mind-map-item">
            <Mindmap
              selectedCategories={[category]}
              navigateToPage={navigateToPage}
            />
          </div>
        ))}
      </div>
    </div>
  );
}

export default MainPage;
