import React from 'react';
import './app.css';  // Import the CSS file for styles

function AboutPage() {
    return (
      <div className="about-page">
        <h1>About Mind Map</h1>
        <p>Mind Map is a Web application designed to improve the way users 
          interact with large collections of spoken content, such as lectures, 
          podcasts, and seminars. Using Natural Language Processing and Machine 
          Learning techniques, Mind Map categorizes spoken content into 
          searchable topics, allowing users to quickly find information 
          relevant to their interests and research needs.</p>
        
        <h2>Design Inspiration</h2>
        <p>Our user interface is inspired by the vastness of the universe, 
          reflecting the expansive nature of large collections of spoken content. 
          Topics are displayed as central nodes with related talks or recordings 
          branching out as smaller orbiting nodes. These nodes represent 
          individual talks or recordings, clickable and leading users directly 
          to their respective audio and transcripts pages, creating an experience 
          similar to navigating a galaxy of ideas.</p>

        <h2>How It Works</h2>
        <p>At the core of Mind Map is our topic modeling system that processes 
          audio transcripts to identify and categorize topics using tf-idf and 
          K-Means clustering. Users interact with a responsive interface where 
          they can navigate through topics and access audio and transcripts 
          directly. Leveraging AI, Mind Map enhances topic identification and 
          visual representation, making exploration engaging and insightful.</p>
  
        <h2>Who We Are</h2>
        <p>Mind Map was developed by a team of computer science students to 
          improve spoken content navigation. Our team of students explored 
          machine learning, software development, and user experience to create 
          a functional and practical solution.</p>
        
        <h2>Contact Us</h2>
        <p>For more information, support, or feedback, please contact us at 
          2024mindmap@gmail.com.</p>
        <p>Open Source Contribution: The Web application and associated topic 
          modeling, preprocessing and image-generation scripts are available as 
          open-source resources on GitHub <a href="https://github.com/SirinaHaaland/mind-map" target="_blank">here</a>. 
          This allows others to explore, modify and adapt our approach to new speech media collections.</p>
      </div>
    );
  }
  
  export default AboutPage;
  
