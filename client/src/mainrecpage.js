import React, { useState, useEffect, useRef } from 'react';

function MainRecPage({ filename }) {
  const [transcript, setTranscript] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const audioElementRef = useRef(null);
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState('');
  // Fetch image, transcript, and title data from the server based on the filename when it changes.
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`/images/${encodeURIComponent(filename)}`);
        if (response.ok) {
          const category = response.headers.get('Category'); // Extract category from response headers
          setCategory(category);
          const imageUrl = URL.createObjectURL(await response.blob());
          setImageUrl(imageUrl);
        } else {
          console.error('Error fetching image:', response.statusText);
        }

        const stmResponse = await fetch(`/get-stm?filename=${filename}`);
        if (stmResponse.ok) {
          const data = await stmResponse.text();
          const cleanedTranscript = data.replace(/"/g, '');
          setTranscript(cleanedTranscript);
        } else {
          console.error('Error fetching transcript:', stmResponse.statusText);
        }

        const titleResponse = await fetch(`/get-title?filename=${filename}`);
        if (titleResponse.ok) {
          const data = await titleResponse.text();
          setTitle(data);
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
  
  // Update the audio element's source to fetch the corresponding audio file based on the filename.
  useEffect(() => {
    if (audioElementRef.current) {
      audioElementRef.current.src = `/get-mp3?filename=${filename}`;
    }
  }, [filename]);

  return (
    <div style={{ display: 'flex', height: '75vh', marginTop: '8vh' }}>
      <div style={{ flex: 1 }}>
        <div style={{ textAlign: 'center' }}>
          {imageUrl && <img src={imageUrl} alt="Recording" style={{ maxWidth: '60%', height: 'auto', display: 'inline-block' }} />}
        
          <audio ref={audioElementRef} controls style={{ width: '80%', height: '100px' }}>
            <source type="audio/mpeg" />
          </audio>
        </div>
      </div>

      <div style={{ flex: 1, overflowY: 'auto' }}>
        <h2>{category && `${category}:`} {title}</h2>
        <p>{transcript}</p>
      </div>
    </div>
  );
}

export default MainRecPage;
