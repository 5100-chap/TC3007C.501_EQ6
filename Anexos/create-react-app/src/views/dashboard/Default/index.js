import { useEffect, useState } from 'react';
import AddIcon from '@mui/icons-material/Add';
// material-ui
import { Grid } from '@mui/material';

// project imports
import EarningCard from './EarningCard';
//import PopularCard from './PopularCard';
import TotalOrderLineChartCard from './TotalOrderLineChartCard';
//import TotalIncomeDarkCard from './TotalIncomeDarkCard';
//import TotalIncomeLightCard from './TotalIncomeLightCard';
import TotalGrowthBarChart from './TotalGrowthBarChart';
import { gridSpacing } from 'store/constant';
import { DataGrid } from '@mui/x-data-grid';
import Button from '@mui/material/Button';

import { MenuItem, TextField } from '@mui/material';
// ==============================|| DEFAULT DASHBOARD ||============================== //



const Dashboard = () => {
  const [value, setValue] = useState('grupo1');
  const [isLoading, setLoading] = useState(true);
  useEffect(() => {
    setLoading(false);
  }, []);
  
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
          <Grid item lg={6} md={6} sm={6} xs={12}>
                  <TextField fullWidth={true} id="standard-select-currency" select value={value} onChange={(e) => setValue(e.target.value)} >
                    {status.map((option) => (
                      <MenuItem key={option.value} value={option.value}>
                        {option.label}
                      </MenuItem>
                    ))}
                  </TextField>
          </Grid>
          <Grid item lg={6} md={6} sm={6} xs={12}>
          <Button fullWidth={true} size="large" variant="contained" endIcon={<AddIcon />}>
            Nuevo Curso</Button>
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
