import React from 'react';
import './app.css';  // Import the CSS file for styles

function AboutPage() {
    return (
      <div className="about-page">
        <h1>About Mind Map</h1>
        <p>Mind Map is a web application designed to transform the way users interact with large collections of spoken content, such as lectures, podcasts, and seminars. Using advanced Natural Language Processing and Machine Learning techniques, Mind Map categorizes spoken content into intuitive, searchable topics, allowing users to quickly find information relevant to their interests and research needs.</p>
        
        <h2>Design Inspiration</h2>
        <p>Our user interface is inspired by the vastness of the universe, reflecting the expansive nature of large collections of spoken content. The UI shows topics as clustered nodes of images, with smaller nodes in orbit around the main topic node, reminiscent of celestial bodies in space. These nodes represent individual talks or recordings, clickable and leading users directly to their respective audio and transcripts pages, enhancing the exploratory experience of navigating through a galaxy of ideas.</p>
  
        <h2>Features</h2>
        <ul>
          <li><strong>AI-Enhanced Visuals:</strong> Experience our AI-generated visuals that give a pictorial summary of the talk's content, enriching the browsing experience.</li>
          <li><strong>Search and Filtering Capabilities:</strong> Utilize keywords to search through topics quickly, or scroll through the topics to check the filter boxes.</li>
          <li><strong>Interactive Transcripts:</strong> Scroll through transcripts corresponding with the audio files. This feature allows users to read along while listening, and quickly ascertain if the content is relevant.</li>
        </ul>
  
        <h2>How It Works</h2>
        <p>At the core of Mind Map is our sophisticated topic modeling system that processes audio transcripts to identify and categorize topics using TF-IDF and K-means clustering. Users interact with a responsive and intuitive interface where they can navigate through topics and access audio and transcripts directly. Leveraging cutting-edge AI, Mind Map enhances topic identification and visual representation, making exploration both engaging and insightful.</p>
  
        <h2>Who We Are</h2>
        <p>Mind Map was developed by a dedicated team of computer science students, passionate about making digital education more accessible and navigable. Our team combines expertise in machine learning, software development, and user experience to create innovative solutions to complex problems.</p>
  
        <h2>Contact Us</h2>
        <p>For more information, support, or feedback, please contact us at 2024mindmap@gmail.com.</p>
        <p>Open Source Contribution: The web application and associated custom preprocessing and image-generation scripts are available as open-source resources on GitHub <a href="https://github.com/SirinaHaaland/STG0006948">here</a>. This supports transparent collaboration and adaptation of our methodologies to new speech media collections by the community.</p>
  
        <p>Explore, learn, and discover with Mind Map today!</p>
      </div>
    );
  }
  
  export default AboutPage;
  
