import * as React from 'react';
import Box from '@mui/material/Box';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Checkbox from '@mui/material/Checkbox';
//import InputAdornment from '@mui/material/InputAdornment';
import OutlinedInput from '@mui/material/OutlinedInput';
import { FixedSizeList } from 'react-window';

function renderRow(props) {
  const { index, style } = props;

  return (
    <ListItem style={style} key={index} component="div" disablePadding>
      <ListItemButton>
        <Checkbox />
        <ListItemText primary={`A00${index + 1}`} />
      </ListItemButton>
    </ListItem>
  );
}

export default function VirtualizedList() {
  const [searchTerm, setSearchTerm] = React.useState('');
  const filteredItems = Array.from({ length: 200 }, (_, index) => `Item ${index + 1}`)
    .filter(item => item.toLowerCase().includes(searchTerm.toLowerCase()));

  return (
    <Box
      sx={{ width: '100%', height: 400, maxWidth: 360, bgcolor: 'background.paper' }}
    >
      <OutlinedInput
        fullWidth
        placeholder="Buscar..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        
        sx={{ marginBottom: 2 }}
      />
      <FixedSizeList
        height={400}
        width={360}
        itemSize={46}
        itemCount={filteredItems.length}
        overscanCount={5}
      >
        {({ index, style }) => {
          return renderRow({ index, style, data: filteredItems });
        }}
      </FixedSizeList>
    </Box>
  );
}
