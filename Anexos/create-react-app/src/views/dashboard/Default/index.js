import { useEffect, useState } from 'react';
import AddIcon from '@mui/icons-material/Add';
// material-ui
// project imports
import EarningCard from './EarningCard';
//import PopularCard from './PopularCard';
import TotalOrderLineChartCard from './TotalOrderLineChartCard';
//import TotalIncomeDarkCard from './TotalIncomeDarkCard';
//import TotalIncomeLightCard from './TotalIncomeLightCard';
import TotalGrowthBarChart from './TotalGrowthBarChart';
import { gridSpacing } from 'store/constant';
import { DataGrid } from '@mui/x-data-grid';
import {
  Grid,
  TextField,
  MenuItem,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle
} from '@mui/material';

import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';

import Lista from './list';
// ==============================|| DEFAULT DASHBOARD ||============================== //



const Dashboard = () => {
  const [value, setValue] = useState('grupo1');
  const [isLoading, setLoading] = useState(true);
  useEffect(() => {
    setLoading(false);
  }, []);

  const [openDialog, setOpenDialog] = useState(false);

  const [openEdit, setopenEdit] = useState(false);

  const [openDelete, setopenDelete] = useState(false);

  const handleDialogOpen = () => {
    setOpenDialog(true);
  };

  const handleDialogClose = () => {
    setOpenDialog(false);
  };
  

  const handleEditOpen = () => {
    setopenEdit(true);
  };

  const handleEditClose = () => {
    setopenEdit(false);
  };

  const handleDeleteOpen = () => {
    setopenDelete(true);
  };

  const handleDeleteClose = () => {
    setopenDelete(false);
  };
  
const columns = [
  {field: 'id', headerName: 'Matricula', width: 130 }, 
  { field: 'firstName', headerName: 'Nombre', width: 150 },
  { field: 'lastName', headerName: 'Apellidos', width: 150 }, 
  {field: 'participacion', headerName: 'Participaciones', width: 130}
];

const rows = [
    { id: 1, lastName: 'Baños', firstName: 'Diego', participacion: 35 },
    { id: 2, lastName: 'Lozano', firstName: 'Carlos', participacion: 42 },
    { id: 3, lastName: 'Arrieta', firstName: 'Carol', participacion: 25 },
    { id: 4, lastName: 'Stark', firstName: 'Melissa', participacion: 16 },
    { id: 5, lastName: 'Targaryen', firstName: 'Fernanda', participacion: 70 },
    { id: 6, lastName: 'Melisandre', firstName: 'Dulce', participacion: 24 },
    { id: 7, lastName: 'Clifford', firstName: 'Sonia', participacion: 44 },
    { id: 8, lastName: 'Frances', firstName: 'Diego', participacion: 36 },
    { id: 9, lastName: 'Roxie', firstName: 'Harvey', participacion: 65 },
];

const status = [
  {
    value: 'grupo1',
    label: 'Grupo 1'
  },
  {
    value: 'grupo2',
    label: 'Grupo 2'
  },
  {
    value: 'grupo3',
    label: 'Grupo 3'
  }
];

  return (
    <Grid container spacing={gridSpacing}>
      <Grid item xs={12}>
        <Grid container spacing={gridSpacing}> 
          <Grid item md={3} xs={12}>
                  <TextField fullWidth={true} id="standard-select-currency" select value={value} onChange={(e) => setValue(e.target.value)} >
                    {status.map((option) => (
                      <MenuItem key={option.value} value={option.value}>
                        {option.label}
                      </MenuItem>
                    ))}
                  </TextField>
          </Grid>
          <Grid item md={1.5} xs={12}>
                  <Button fullWidth={true} size="large" variant="contained" endIcon={<EditIcon />} color='secondary' onClick={handleEditOpen}>Editar</Button>
                  <Dialog open={openEdit} onClose={handleEditClose} >
                  <DialogTitle>Editar curso</DialogTitle>
                  <DialogContent>
                    <DialogContentText>
                      <div>
                      <text>Grupo 1</text>
                      </div>
                      <div>
                      <text>Alumnos</text>
                      <Lista></Lista>
                      </div>
                    </DialogContentText>
                    {/* Agrega los campos del nuevo curso aquí */}
                  </DialogContent>
                  <DialogActions>
                    <Button onClick={handleEditClose} color="error" variant="contained">
                      Cancelar
                    </Button>
                    <Button onClick={handleEditClose} color="success" variant="contained">
                      Guardar
                    </Button>
                  </DialogActions>
                </Dialog>
          </Grid>
          <Grid item md={1.5} xs={12}>
                  <Button fullWidth={true} size="large" variant="contained" endIcon={<DeleteIcon />} color='error' onClick={handleDeleteOpen}>Eliminar</Button>
                  <Dialog open={openDelete} onClose={handleDeleteClose} >
                  <DialogTitle>Eliminar</DialogTitle>
                  <DialogContent>
                    <DialogContentText>
                      <text>Borrar permanentemente Grupo 1</text>
                    </DialogContentText>
                    {/* Agrega los campos del nuevo curso aquí */}
                  </DialogContent>
                  <DialogActions>
                    <Button onClick={handleDeleteClose} color="error" variant="contained">
                      Cancelar
                    </Button>
                    <Button onClick={handleDeleteClose} color="success" variant="contained">
                      Aceptar
                    </Button>
                  </DialogActions>
                </Dialog>
          </Grid>
          <Grid item lg={6} md={6} sm={6} xs={12}>
            {/* <Button fullWidth={true} size="large" variant="contained" endIcon={<AddIcon />} >
            Nuevo Curso
            </Button> */}
            <Button fullWidth={true} size="large" variant="contained" endIcon={<AddIcon />} onClick={handleDialogOpen}>
              Nuevo Curso
            </Button>
            {/* ... */}

            {/* Cuadro de Diálogo */}
            <Dialog open={openDialog} onClose={handleDialogClose} >
              <DialogTitle>Nuevo curso</DialogTitle>
              <DialogContent>
                <DialogContentText>
                  <div>
                  <TextField id="grupo" label="Numero de grupo"></TextField>
                  </div>
                  <div>
                  <text>Añadir alumnos</text>
                  <Lista></Lista>
                  </div>
                </DialogContentText>
                {/* Agrega los campos del nuevo curso aquí */}
              </DialogContent>
              <DialogActions>
                <Button onClick={handleDialogClose} color="error" variant="contained">
                  Cancelar
                </Button>
                <Button onClick={handleDialogClose} color="success" variant="contained">
                  Guardar
                </Button>
              </DialogActions>
            </Dialog>
          </Grid>

        </Grid>
      </Grid>
      <Grid item xs={12}>
        <Grid container spacing={gridSpacing}>
          <Grid item lg={6} md={6} sm={6} xs={12}>
            <EarningCard isLoading={isLoading} />
          </Grid>
          <Grid item lg={6} md={6} sm={6} xs={12}>
            <TotalOrderLineChartCard isLoading={isLoading} />
          </Grid>
          
        </Grid>
      </Grid>
      <Grid item xs={12}>
        <Grid container spacing={gridSpacing}>
          <Grid item xs={12} md={7}>
            <TotalGrowthBarChart isLoading={isLoading} />
          </Grid>
          <Grid item xs={12} md={5}>
          <DataGrid
            rows={rows}
            columns={columns}
            initialState={{
              pagination: {
                paginationModel: { page: 0, pageSize: 10 }
              },
            }}
            pageSizeOptions={[5, 10]}
            checkboxSelection
          />

            {/* <PopularCard isLoading={isLoading} /> */}
          </Grid>
        </Grid>
      </Grid>
      
    </Grid>
  );
};

export default Dashboard;
