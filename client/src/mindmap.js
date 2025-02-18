import React, { useState, useEffect, useRef, useMemo, useCallback } from 'react';
import { v4 as uuidv4 } from 'uuid';
import './app.css';
import Tippy from '@tippyjs/react';
import 'tippy.js/dist/tippy.css';

function MindMap({ selectedCategories, navigateToPage }) {
  const [mindMapData, setMindMapData] = useState([]);
  const [centralImageUrl, setCentralImageUrl] = useState("");
  const [loading, setLoading] = useState(true);
  const svgRef = useRef(null);
  const defaultWidth = 800;
  const defaultHeight = 600;

  // Constants
  const centralNodeRadius = 75;
  const circleRadius = 50;
  const centralNodeX = defaultWidth / 2;
  const centralNodeY = defaultHeight / 2;
  const maxCirclesPerLevel = 8;

  // Fetch central image
  useEffect(() => {
    const fetchCentralImage = async () => {
      if (selectedCategories.length > 0) {
        const category = selectedCategories[0];
        try {
          const response = await fetch('/data/central-image', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
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

  // Fetch subnode data
  useEffect(() => {
    const fetchDataForCategory = async () => {
      const nodes = [];
      for (const category of selectedCategories) {
        try {
          const response = await fetch('/data/categories', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ categories: [category] }),
          });
          const imageFilenames = await response.json();
          const sanitizedFilenames = imageFilenames.map(filename => filename.replace('.stm', ''));

          for (const filename of sanitizedFilenames) {
            try {
              const titleResponse = await fetch(`/get-title?filename=${filename}`);
              let title = filename;
              if (titleResponse.ok) {
                title = await titleResponse.text();
              }

              const imageUrl = `/images/${encodeURIComponent(filename)}`;
              const imageResponse = await fetch(imageUrl);
              let actualCategory = 'Unknown Category';
              if (imageResponse.ok) {
                actualCategory = imageResponse.headers.get('Category') || actualCategory;
              }

              nodes.push({ imageUrl, filename, category: actualCategory, title });
            } catch (error) {
              console.error(`Error fetching data for filename ${filename}:`, error);
            }
          }
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

  // Memoized circle generation
  const { circles, minX, maxX, minY, maxY } = useMemo(() => {
    const baseCircles = selectedCategories.length > 0
      ? [{ x: centralNodeX, y: centralNodeY, radius: centralNodeRadius, imageUrl: centralImageUrl, isCentralNode: true }]
      : [];

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
          baseCircles.push({
            x,
            y,
            radius: circleRadius,
            imageUrl: mindMapData[dataIndex].imageUrl,
            isCentralNode: false,
            title: mindMapData[dataIndex].title,
            category: mindMapData[dataIndex].category,
          });
          dataIndex++;
        }
      }

      remainingNodes -= nodesThisLevel;
      currentLevel++;
    }

    const minX = baseCircles.reduce((min, circle) => Math.min(min, circle.x - circle.radius), centralNodeX - centralNodeRadius);
    const maxX = baseCircles.reduce((max, circle) => Math.max(max, circle.x + circle.radius), centralNodeX + centralNodeRadius);
    const minY = baseCircles.reduce((min, circle) => Math.min(min, circle.y - circle.radius), centralNodeY - centralNodeRadius);
    const maxY = baseCircles.reduce((max, circle) => Math.max(max, circle.y + circle.radius), centralNodeY + centralNodeRadius);

    return { circles: baseCircles, minX, maxX, minY, maxY };
  }, [selectedCategories, centralImageUrl, mindMapData, centralNodeX, centralNodeY]);

  const svgDimensions = useMemo(() => ({
    width: maxX - minX + centralNodeRadius * 2,
    height: maxY - minY + centralNodeRadius * 2,
  }), [maxX, minX, maxY, minY]);

  // Handle circle click
  const handleCircleClick = useCallback((filename, isCentralNode) => {
    if (!isCentralNode) {
      navigateToPage('mainrec', filename);
    }
  }, [navigateToPage]);

  // Conditional rendering
  if (loading) {
    return null;
  }

  return (
    <svg width={svgDimensions.width} height={svgDimensions.height} ref={svgRef}>
      {selectedCategories.length > 0 && (
        <text x={svgDimensions.width / 2} y={20} textAnchor="middle" fill="black" fontSize="20" fontWeight="bold">
          {selectedCategories[0]}
        </text>
      )}
      {circles.map((circle, index) => {
        if (circle.imageUrl) {
          const clipPathId = `clip-${index}-${uuidv4()}`;
          return (
            <g key={index} onClick={() => handleCircleClick(circle.isCentralNode ? '' : mindMapData[index - 1]?.filename, circle.isCentralNode)}>
              <defs>
                <clipPath id={clipPathId}>
                  <circle cx={circle.x - minX + centralNodeRadius} cy={circle.y - minY + centralNodeRadius} r={circle.radius} />
                </clipPath>
              </defs>
              <circle cx={circle.x - minX + centralNodeRadius} cy={circle.y - minY + centralNodeRadius} r={circle.radius} fill={circle.isCentralNode ? "lightblue" : "lightgreen"} stroke="black" strokeWidth="2" />
              <image href={circle.imageUrl} x={circle.x - circle.radius - minX + centralNodeRadius} y={circle.y - circle.radius - minY + centralNodeRadius} width={circle.radius * 2} height={circle.radius * 2} clipPath={`url(#${clipPathId})`} />
              {!circle.isCentralNode && (
                <Tippy content={`${circle.title} (${circle.category || 'Unknown Category'})`} placement="top" arrow={false} theme="dark">
                  <circle cx={circle.x - minX + centralNodeRadius} cy={circle.y - minY + centralNodeRadius} r={circle.radius} fill="transparent" stroke="none" />
                </Tippy>
              )}
            </g>
          );
        }
        return null;
      })}
    </svg>
  );
}

export default MindMap;