import React, { useState, useEffect, useRef } from 'react';
import { v4 as uuidv4 } from 'uuid'; 
import './app.css';

function MindMap({ selectedCategories, navigateToPage }) {
  const [mindMapData, setMindMapData] = useState([]);
  const [centralImageUrl, setCentralImageUrl] = useState("");
  const [loading, setLoading] = useState(true);
  const svgRef = useRef(null);
  const defaultWidth = 800;
  const defaultHeight = 600;
  const clipPathIds = [];
  //Fetch central image from server based on category(topic)
  useEffect(() => {
    const fetchCentralImage = async () => {
      if (selectedCategories.length > 0) {
        const category = selectedCategories[0];
        try {
          const response = await fetch('/data/central-image', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ categories: [category] }),
          });
          if (response.ok) {
            const imageUrl = URL.createObjectURL(await response.blob());
            setCentralImageUrl(imageUrl);
          } else {
            console.error('Error fetching central image:', response.statusText);
          }
        } catch (error) {
          console.error('Error fetching central image:', error);
        }
      }
    };

    fetchCentralImage();
  }, [selectedCategories]);

  //Fetch image for subnodes, by fetching filename with help of selectied categories and then use it to fetch image.
  useEffect(() => {
    const fetchDataForCategory = async () => {
      const nodes = [];
      for (const category of selectedCategories) {
        try {
          const response = await fetch('/data/categories', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ categories: [category] }),
          });
          const imageFilenames = await response.json();
          const sanitizedFilenames = imageFilenames.map(filename => filename.replace('.stm', ''));
          const categoryNodes = sanitizedFilenames.map(filename => ({
            imageUrl: `/images/${encodeURIComponent(filename)}`,
            filename: filename,
            category: category,
          }));
          nodes.push(...categoryNodes);
        } catch (error) {
          console.error(`Error fetching images for category ${category}:`, error);
        }
      }
      setMindMapData(nodes);
      setLoading(false);
    };

    if (selectedCategories.length > 0) {
      fetchDataForCategory();
    } else {
      setMindMapData([]);
      setLoading(false);
    }
  }, [selectedCategories]);
  
  useEffect(() => {
    const handleResize = () => {
      if (svgRef.current) {
        const boundingRect = svgRef.current.getBoundingClientRect();
        setSvgWidth(boundingRect.width);
        setSvgHeight(boundingRect.height);
      }
    };

    window.addEventListener('resize', handleResize);
    handleResize();
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const handleCircleClick = (filename, isCentralNode) => {
    if (!isCentralNode) {
      navigateToPage('mainrec', filename);
    }
  };

  const centralNodeRadius = 75;
  const circleRadius = 50;
  const centralNodeX = defaultWidth / 2;
  const centralNodeY = defaultHeight / 2;
  const maxCirclesPerLevel = 8;

  const circles = selectedCategories.length > 0 ? [{ x: centralNodeX, y: centralNodeY, radius: centralNodeRadius, imageUrl: centralImageUrl, isCentralNode: true }] : [];

  let remainingNodes = mindMapData.length;
  let currentLevel = 1;
  let dataIndex = 0;

  while (remainingNodes > 0) {
    const nodesThisLevel = Math.min(remainingNodes, maxCirclesPerLevel + currentLevel * 4);
    const angleIncrement = (2 * Math.PI) / nodesThisLevel;
    const radius = (currentLevel * circleRadius * 2.5) + centralNodeRadius;

    for (let i = 0; i < nodesThisLevel; i++) {
      const angle = i * angleIncrement;
      const x = centralNodeX + radius * Math.cos(angle);
      const y = centralNodeY + radius * Math.sin(angle);
      if (dataIndex < mindMapData.length) {
        circles.push({ x, y, radius: circleRadius, imageUrl: mindMapData[dataIndex].imageUrl, isCentralNode: false });
        dataIndex++;
      }
    }

    remainingNodes -= nodesThisLevel;
    currentLevel++;
  }

  const [svgWidth, setSvgWidth] = useState(defaultWidth);
  const [svgHeight, setSvgHeight] = useState(defaultHeight);

  // Calculate the bounding box of all circles
  const minX = circles.reduce((min, circle) => Math.min(min, circle.x - circle.radius), centralNodeX - centralNodeRadius);
  const maxX = circles.reduce((max, circle) => Math.max(max, circle.x + circle.radius), centralNodeX + centralNodeRadius);
  const minY = circles.reduce((min, circle) => Math.min(min, circle.y - circle.radius), centralNodeY - centralNodeRadius);
  const maxY = circles.reduce((max, circle) => Math.max(max, circle.y + circle.radius), centralNodeY + centralNodeRadius);

  // Calculate the width and height based on the bounding box
  const newWidth = maxX - minX + centralNodeRadius * 2;
  const newHeight = maxY - minY + centralNodeRadius * 2;

  // Conditional rendering based on loading state
  if (loading) {
    return null;
  }

  return (
    <svg width={newWidth} height={newHeight} ref={svgRef}>
      {selectedCategories.length > 0 && (
        <text
          x={newWidth / 2}
          y={20}
          textAnchor="middle"
          fill="black"
          fontSize="20"
          fontWeight="bold"
        >
          {selectedCategories[0]}
        </text>
      )}

      {/* Generate clip path IDs and store them in the array */}
      {circles.map((circle, index) => {
        if (circle.imageUrl) {
          const clipPathId = `clip-${index}-${uuidv4()}`;
          clipPathIds.push(clipPathId);

          return (
            <g key={index} onClick={() => handleCircleClick(circle.isCentralNode ? '' : mindMapData[index - 1]?.filename, circle.isCentralNode)}>
              <defs>
                <clipPath id={clipPathId}>
                  <circle cx={circle.x - minX + centralNodeRadius} cy={circle.y - minY + centralNodeRadius} r={circle.radius} />
                </clipPath>
              </defs>
              <circle
                cx={circle.x - minX + centralNodeRadius}
                cy={circle.y - minY + centralNodeRadius}
                r={circle.radius}
                fill={circle.isCentralNode ? "lightblue" : "lightgreen"}
                stroke="black"
                strokeWidth="2"
              />
              <image
                href={circle.imageUrl}
                x={circle.x - circle.radius - minX + centralNodeRadius}
                y={circle.y - circle.radius - minY + centralNodeRadius}
                width={circle.radius * 2}
                height={circle.radius * 2}
                clipPath={`url(#${clipPathId})`}
              />
            </g>
          );
        } else {
          return null;
        }
      })}
    </svg>
  );
}

export default MindMap;
