import React, { useState, useEffect, useRef } from 'react';

function MainRecPage({ filename }) {
  const [transcript, setTranscript] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const audioElementRef = useRef(null);
  const [title, setTitle] = useState('');
  const [author, setAuthor] = useState('');
  const [category, setCategory] = useState('');
  const [showTranscript, setShowTranscript] = useState(false);

  // Fetch image, transcript, and title data when filename changes
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`/images/${encodeURIComponent(filename)}`);
        if (response.ok) {
          const category = response.headers.get('Category');
          setCategory(category);
          const imageUrl = URL.createObjectURL(await response.blob());
          setImageUrl(imageUrl);
        } else {
          console.error('Error fetching image:', response.statusText);
        }

        const stmResponse = await fetch(`/get-stm?filename=${filename}`);
        if (stmResponse.ok) {
          const data = await stmResponse.text();
          setTranscript(data.replace(/"/g, ''));
        } else {
          console.error('Error fetching transcript:', stmResponse.statusText);
        }

        const titleResponse = await fetch(`/get-title?filename=${filename}`);
        if (titleResponse.ok) {
          const data = await titleResponse.text();
          const [extractedAuthor, extractedTitle] = data.split(':').map(str => str.trim());
          setAuthor(extractedAuthor);
          setTitle(extractedTitle.charAt(0).toUpperCase() + extractedTitle.slice(1));
        } else {
          console.error('Error fetching title:', titleResponse.statusText);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();

    return () => {
      if (imageUrl) {
        URL.revokeObjectURL(imageUrl);
      }
    };
  }, [filename]);

  // Handle audio playback and ensure it stops when navigating away
  useEffect(() => {
    if (audioElementRef.current) {
      audioElementRef.current.src = `/get-mp3?filename=${filename}`;
    }

    return () => {
      if (audioElementRef.current) {
        audioElementRef.current.pause(); 
        audioElementRef.current.currentTime = 0; 
        audioElementRef.current.src = ''; 
      }
    };
  }, [filename]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '75vh', marginTop: '8vh', alignItems: 'center' }}>
      <div style={{ textAlign: 'center', position: 'relative', maxWidth: '60%' }}>
        {/* Display title */}
        <h2 style={{ marginBottom: '10px' }}>{title}</h2>

        <div style={{ width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          {/* Display image if available */}
          {imageUrl && (
            <img
              src={imageUrl}
              alt="Recording"
              style={{ width: '100%', height: 'auto', maxHeight: '280px', objectFit: 'contain' }}
            />
          )}

          {/* Audio player */}
          <audio ref={audioElementRef} controls style={{ width: '50%', height: '60px', marginTop: '20px' }}>
            <source type="audio/mpeg" />
          </audio>
        </div>

        {/* Display author and category */}
        <div style={{ marginTop: '10px', fontWeight: 'bold' }}>
          {author && <span>Author: {author}</span>} {' | '}
          {category && <span>Topic: {category}</span>}
        </div>

        {/* Toggle transcript visibility */}
        <div
          onClick={() => setShowTranscript(!showTranscript)}
          style={{ cursor: 'pointer', marginTop: '10px', fontWeight: 'bold', color: '#C0392B' }}
        >
          {showTranscript ? 'Hide Transcript ▲' : 'Show Transcript ▼'}
        </div>

        {/* Transcript display with max height for scrolling */}
        <div style={{ marginTop: '10px', transition: 'max-height 0.3s ease', overflow: 'hidden', maxHeight: showTranscript ? '150px' : '0' }}>
          <div style={{ fontWeight: '600', maxHeight: '150px', overflowY: 'auto', textAlign: 'left' }}>
            <p>{transcript}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default MainRecPage;
