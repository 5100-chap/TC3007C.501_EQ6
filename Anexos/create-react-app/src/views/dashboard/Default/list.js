import * as React from 'react';
import Box from '@mui/material/Box';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Checkbox from '@mui/material/Checkbox';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogActions from '@mui/material/DialogActions';
import Button from '@mui/material/Button';
import OutlinedInput from '@mui/material/OutlinedInput';
import { FixedSizeList } from 'react-window';

function renderRow(props) {
  const { index, style, data, handleClickOpen } = props;
  const item = data[index];

  return (
    <ListItem style={style} key={index} component="div" disablePadding>
      <ListItemButton onClick={() => handleClickOpen(item)}>
        <Checkbox />
        <ListItemText primary={`${item[5]}`} secondary={`${item[1]} ${item[2]}`} />
      </ListItemButton>
    </ListItem>
  );
}

const defaultList = [
  [`Sin datos`, `Nombre`, `Apellido`, `Correo`, `Sin datos`, `sin datos`, `null`]
];

export default function VirtualizedList({ data }) {
  const [searchTerm, setSearchTerm] = React.useState();
  const [open, setOpen] = React.useState(false);
  const [selectedItem, setSelectedItem] = React.useState(null);
  const filteredItems = data ? (data.length === 0 ? defaultList : data) : defaultList;

  const handleClickOpen = (item) => {
    setSelectedItem(item);
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <Box sx={{ width: '100%', height: 400, maxWidth: 360, bgcolor: 'background.paper' }}>
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
          return renderRow({ index, style, data: filteredItems, handleClickOpen });
        }}
      </FixedSizeList>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Información del alumno</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Nombre: {selectedItem && selectedItem[1]}
            <br />
            Apellido: {selectedItem && selectedItem[2]}
            <br />
            Matrícula: {selectedItem && selectedItem[5]}
            <br />
            Correo Electrónico: {selectedItem && selectedItem[3]}
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cerrar</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
