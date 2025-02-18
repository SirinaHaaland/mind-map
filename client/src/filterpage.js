import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Checkbox, List, ListItem, ListItemText, ListItemIcon, TextField, Box, FormControlLabel, Switch, Drawer } from '@mui/material';

const FilterPage = ({ selectedCategories = [], setSelectedCategories }) => {
  const [categories, setCategories] = useState([]);
  const [checkedCategories, setCheckedCategories] = useState(() => selectedCategories);
  const [searchQuery, setSearchQuery] = useState('');
  const [sortedCategories, setSortedCategories] = useState([]);
  const [showSelected, setShowSelected] = useState(true);

  // Update the checked categories state when selected categories change.
  useEffect(() => {
    setCheckedCategories(selectedCategories);
  }, [selectedCategories]);

  // Fetch categories from the server when the component mounts.
  useEffect(() => {
    axios.get('/data')
      .then(response => {
        setCategories(response.data.categories);
      })
      .catch(error => {
        console.error('Error fetching categories:', error);
      });
  }, []);

  // Save the checked categories to local storage and remove them when the component unmounts.
  useEffect(() => {
    localStorage.setItem('checkedCategories', JSON.stringify(checkedCategories));
  
    const handleBeforeUnload = () => {
      localStorage.removeItem('checkedCategories');
    };
  
    window.addEventListener('beforeunload', handleBeforeUnload);
  
    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };
  }, [checkedCategories]);

  // Filter, sort, and update the sorted categories based on search query and selected categories.
  useEffect(() => {
    const filteredCategories = categories.filter(category =>
      category.toLowerCase().includes(searchQuery.toLowerCase())
    );
  
    const sorted = [...filteredCategories].sort((a, b) => {
      const isSelectedA = selectedCategories.includes(a);
      const isSelectedB = selectedCategories.includes(b);
  
      if (isSelectedA !== isSelectedB) {
        return isSelectedA ? -1 : 1; // Selected categories first
      }
  
      const nameA = a.toLowerCase();
      const nameB = b.toLowerCase();
  
      if (nameA < nameB) return -1; // Alphabetical order
      if (nameA > nameB) return 1;
      return 0;
    });
  
    setSortedCategories(sorted);
  }, [categories, searchQuery, selectedCategories]);

  const handleCategoryChange = (event) => {
    const { value, checked } = event.target;
    if (checked) {
      setSelectedCategories(prev => [...prev, value]);
      setCheckedCategories(prev => [...prev, value]);
    } else {
      setSelectedCategories(prev => prev.filter(cat => cat !== value));
      setCheckedCategories(prev => prev.filter(cat => cat !== value));
    }
  };

  return (
    <Drawer
      variant="persistent"
      anchor="left"
      open={true} // Drawer is always open
      sx={{
        width: 250,
        flexShrink: 0,
        mt: 8,  // This pushes the drawer below the AppBar (64px height)
        '& .MuiDrawer-paper': {
          width: 250,
          boxSizing: 'border-box',
          mt: '64px', // Match this with the AppBar height
        },
      }}
    >
      <Box mt={2} mx={2}>
        <TextField
          label="Search categories..."
          variant="outlined"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          fullWidth
          sx={{
            '& label': { 
              color: "black" // Change label text color
            },
            '& label.Mui-focused': { 
              color: "black" // Keep it black when focused
            },
            '& .MuiOutlinedInput-root': {
              '& fieldset': { 
                borderColor: "black" // Default border color
              },
              '&:hover fieldset': { 
                borderColor: "black" // Border color on hover
              },
              '&.Mui-focused fieldset': { 
                borderColor: "black" // Keep border black on focus
              }
            }
          }}
        />
      </Box>
      <Box mt={2} mx={2}>
        <FormControlLabel
          control={<Switch checked={showSelected} onChange={() => setShowSelected(!showSelected)} />}
          label="Show selected categories"
          labelPlacement="start"
        />
      </Box>
      <List>
        {showSelected && selectedCategories.map((category) => (
          <ListItem key={category}>
            <ListItemIcon>
              <Checkbox 
                onChange={handleCategoryChange} 
                value={category} 
                checked={checkedCategories.includes(category)}
                sx={{
                  color: "#2C3E50", // Unchecked color
                  '&.Mui-checked': {
                    color: "#2C3E50", // Checked color
                  },
                }}
              />
            </ListItemIcon>
            <ListItemText primary={category} />
          </ListItem>
        ))}
        {sortedCategories.map((category) => (
          !selectedCategories.includes(category) && (
            <ListItem key={category}>
              <ListItemIcon>
                <Checkbox 
                  onChange={handleCategoryChange} 
                  value={category} 
                  checked={checkedCategories.includes(category)}
                />
              </ListItemIcon>
              <ListItemText primary={category} />
            </ListItem>
          )
        ))}
      </List>
    </Drawer>
  );
};

export default FilterPage;
