import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Checkbox, Drawer, List, ListItem, ListItemText, ListItemIcon, IconButton, TextField, Box, FormControlLabel, Switch } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';

const FilterPage= ({ selectedCategories = [], setSelectedCategories }) => {
  const [categories, setCategories] = useState([]);
  const [drawerOpen, setDrawerOpen] = useState(false);
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

    filteredCategories.sort((a, b) => a.localeCompare(b));

    const sorted = [...filteredCategories].sort((a, b) => {
      const isSelectedA = selectedCategories.includes(a);
      const isSelectedB = selectedCategories.includes(b);
      if (isSelectedA && isSelectedB) {
        return 0;
      }
      if (isSelectedA) {
        return -1;
      }
      return 1;
    });

    setSortedCategories(sorted);
  }, [categories, searchQuery, selectedCategories]);

  const toggleDrawer = (open) => (event) => {
    if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
      return;
    }
    setDrawerOpen(open);
  };

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
    <div>
      <IconButton onClick={toggleDrawer(true)} color="inherit" aria-label="open drawer" edge="start">
        <MenuIcon />
      </IconButton>
      <Drawer anchor="left" open={drawerOpen} onClose={toggleDrawer(false)}>
        <Box mt={2} ml={1}>
          <TextField
            label="Search topics"
            variant="outlined"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </Box>
        <Box ml={1} mt={2}>
          <FormControlLabel
            control={<Switch checked={showSelected} onChange={() => setShowSelected(!showSelected)} />}
            label="Show selected topics"
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
    </div>
  );
};

export default FilterPage;
