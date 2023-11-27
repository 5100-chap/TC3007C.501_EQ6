import PropTypes from 'prop-types';
import { useState, useEffect } from 'react';
import axios from 'axios';
// material-ui
import { useTheme, styled } from '@mui/material/styles';
import { Avatar, Box, Button, Grid, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Dialog, DialogTitle, DialogContent } from '@mui/material';

// third-party
import Chart from 'react-apexcharts';

// project imports
import MainCard from 'ui-component/cards/MainCard';
import SkeletonTotalOrderCard from 'ui-component/cards/Skeleton/EarningCard';

import ChartDataMonth from './chart-data/total-order-month-line-chart';
import ChartDataYear from './chart-data/total-order-year-line-chart';

// assets
import LocalMallOutlinedIcon from '@mui/icons-material/LocalMallOutlined';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';

import { API_BASE_URL } from 'config/apiConfig';

const CardWrapper = styled(MainCard)(({ theme }) => ({
  backgroundColor: theme.palette.primary.dark,
  color: '#fff',
  overflow: 'hidden',
  position: 'relative',
  '&>div': {
    position: 'relative',
    zIndex: 5
  },
  '&:after': {
    content: '""',
    position: 'absolute',
    width: 210,
    height: 210,
    background: theme.palette.primary[800],
    borderRadius: '50%',
    zIndex: 1,
    top: -85,
    right: -95,
    [theme.breakpoints.down('sm')]: {
      top: -105,
      right: -140
    }
  },
  '&:before': {
    content: '""',
    position: 'absolute',
    zIndex: 1,
    width: 210,
    height: 210,
    background: theme.palette.primary[800],
    borderRadius: '50%',
    top: -125,
    right: -15,
    opacity: 0.5,
    [theme.breakpoints.down('sm')]: {
      top: -155,
      right: -70
    }
  }
}));

// ==============================|| DASHBOARD - TOTAL ORDER LINE CHART CARD ||============================== //

const TotalOrderLineChartCard = ({ isLoading, asistenciaPorClase, rol, courses }) => {
  const isAsistenciaPorClaseArray = Array.isArray(asistenciaPorClase);
  const theme = useTheme();
  const [idClase] = useState(isAsistenciaPorClaseArray ? courses[0].ClaseID : -1); // courses[0].ClaseID
  const [timeValue, setTimeValue] = useState(false);
  const [totalAsistencias, setTotalAsistencias] = useState(0);
  const [totalAsistenciasBase, setTotalAsistenciaBase] = useState(0);
  const [promedio, setPromedio] = useState(null);
  const [update, setUpdate] = useState(false);
  const [showTable, setShowTable] = useState(false);

  const handleChangeTime = (event, newValue) => {
    setTimeValue(newValue);
    setUpdate(true);
  };

  const handleExportCSV = () => {
    const csvData = [];
    const headers = ["AsistenciaID", "EstudianteID", "Clase", "Curso", "HoraEntrada", "HoraSalida", "NombreEstudiante", "ApellidoEstudiante"];

    // Add headers to csvData
    csvData.push(headers);

    // Add data rows to csvData
    asistenciaPorClase.forEach((asistencia) => {
      // Asegúrate de que cada elemento de asistencia tiene los datos en el orden correcto
      const row = [
        asistencia[0], // AsistenciaID
        asistencia[1], // EstudianteID
        courses[0].Nombre, // Clase (asumiendo que es constante para todas las filas)
        courses[0].NombreCurso, // Curso (asumiendo que es constante para todas las filas)
        asistencia[3], // HoraEntrada
        asistencia[4], // HoraSalida
        asistencia[5], // NombreEstudiante
        asistencia[6], // ApellidoEstudiante
      ];
      csvData.push(row);
    });

    // Convert csvData to CSV string
    const csvString = csvData.map((row) => row.join(",")).join("\n");

    // Create a temporary anchor element
    const anchor = document.createElement("a");
    anchor.href = "data:text/csv;charset=utf-8," + encodeURIComponent(csvString);
    anchor.download = "asistencia.csv";
    anchor.click();
  };


  const toggleTable = () => {
    setShowTable(!showTable);
  };

  useEffect(() => {
    const calculateAsistencias = async () => {
      if ((asistenciaPorClase === 'Sin datos') || !update) {
        return;
      }
  
      let totalAsistenciasDelDia = 0;
      if (isAsistenciaPorClaseArray) {
        const today = new Date().toISOString().split('T')[0];
        const asistenciasHoy = asistenciaPorClase.filter(asistencia => asistencia[4].startsWith(today));
        totalAsistenciasDelDia = asistenciasHoy.length;
      }
  
      try {
        const response = await axios.post(`${API_BASE_URL}/calcular_dias_habiles`, { clase_id: courses[0].id });
        const diasHabiles = response.data.dias_habiles;
  
        setTotalAsistenciaBase(diasHabiles);
  
        if (!timeValue) {
          // Modo "Hoy"
          setTotalAsistencias(totalAsistenciasDelDia);
        } else {
          // Modo "Promedio"
          if (rol !== 'Alumno') {
            setTotalAsistencias(asistenciaPorClase.length);
          } else {
            setPromedio((asistenciaPorClase.length / diasHabiles).toFixed(2));
            setTotalAsistencias(asistenciaPorClase.length);
          }
        }
      } catch (error) {
        console.error('Error al calcular días hábiles:', error);
      }
  
      setUpdate(false);
    };
  
    if (update || (asistenciaPorClase !== 'Sin datos' && isAsistenciaPorClaseArray)) {
      calculateAsistencias();
    }
  
  }, [update, asistenciaPorClase, courses, isAsistenciaPorClaseArray, timeValue, idClase, rol]);
  
  useEffect(() => {
    if (typeof asistenciaPorClase === 'string') {
      setTotalAsistencias(0);
      setTotalAsistenciaBase(0);
      setPromedio(null);
      setUpdate(true);
    }
  }, [asistenciaPorClase]);

  return (
    <>
      {isLoading ? (
        <SkeletonTotalOrderCard />
      ) : (
        <CardWrapper border={false} content={false}>
          <Box sx={{ p: 2.25 }}>
            <Grid container direction="column">
              <Grid item>
                <Grid container justifyContent="space-between">
                  <Grid item>
                    {showTable ? (
                      <Dialog
                        open={showTable}
                        onClose={toggleTable}
                        aria-labelledby="table-dialog-title"
                        maxWidth="lg"
                      >
                        <DialogTitle id="table-dialog-title">
                        </DialogTitle>
                        <DialogContent>
                          <TableContainer component={Paper}>
                            <Table>
                              <TableHead>
                                <TableRow>
                                  <TableCell>AsistenciaID</TableCell>
                                  <TableCell>EstudianteID</TableCell>
                                  <TableCell>Clase</TableCell>
                                  <TableCell>Curso</TableCell>
                                  <TableCell>HoraEntrada</TableCell>
                                  <TableCell>HoraSalida</TableCell>
                                  <TableCell>NombreEstudiante</TableCell>
                                  <TableCell>ApellidoEstudiante</TableCell>
                                </TableRow>
                              </TableHead>
                              <TableBody>
                                {isAsistenciaPorClaseArray && asistenciaPorClase.map((asistencia, index) => (
                                  <TableRow key={index}>
                                    <TableCell>{asistencia[0]}</TableCell>
                                    <TableCell>{asistencia[1]}</TableCell>
                                    <TableCell>{courses[0].Nombre}</TableCell>
                                    <TableCell>{courses[0].NombreCurso}</TableCell>
                                    <TableCell>{asistencia[3]}</TableCell>
                                    <TableCell>{asistencia[4]}</TableCell>
                                    <TableCell>{asistencia[5]}</TableCell>
                                    <TableCell>{asistencia[6]}</TableCell>
                                  </TableRow>
                                ))}
                              </TableBody>
                            </Table>
                          </TableContainer>
                        </DialogContent>
                      </Dialog>
                    ) : (
                      <Avatar
                        variant="rounded"
                        sx={{
                          ...theme.typography.commonAvatar,
                          ...theme.typography.largeAvatar,
                          backgroundColor: theme.palette.primary[800],
                          color: '#fff',
                          mt: 1
                        }}
                      >
                        <LocalMallOutlinedIcon fontSize="inherit" />
                      </Avatar>
                    )}
                  </Grid>
                  <Grid item>
                    <Button
                      disableElevation
                      variant={timeValue ? 'contained' : 'text'}
                      size="small"
                      sx={{ color: 'inherit' }}
                      onClick={(e) => handleChangeTime(e, true)}
                    >
                      {rol === 'Alumno' ? 'Promedio' : 'Total'}
                    </Button>
                    <Button
                      disableElevation
                      variant={!timeValue ? 'contained' : 'text'}
                      size="small"
                      sx={{ color: 'inherit' }}
                      onClick={(e) => handleChangeTime(e, false)}
                    >
                      Hoy
                    </Button>
                    <Button
                      disableElevation
                      variant="contained"
                      size="small"
                      sx={{ color: 'inherit' }}
                      onClick={toggleTable}
                      disabled={typeof asistenciaPorClase === 'string'}
                    >
                      Mostrar Tabla
                    </Button>
                    <Button
                      disableElevation
                      variant="contained"
                      size="small"
                      sx={{ color: 'inherit' }}
                      onClick={handleExportCSV}
                      disabled={typeof asistenciaPorClase === 'string'}
                    >
                      Exportar a CSV
                    </Button>
                  </Grid>
                </Grid>
              </Grid>
              <Grid item sx={{ mb: 0.75 }}>
                <Grid container alignItems="center">
                  <Grid item xs={6}>
                    <Grid container alignItems="center">
                      <Grid item>
                        <Typography>
                          {timeValue ? (rol === 'Aluimno' ? `${totalAsistencias}/${totalAsistenciasBase} (${promedio}%)` : totalAsistencias) : totalAsistencias.toString()} asistencias
                        </Typography>
                      </Grid>
                      <Grid item>
                        <Avatar
                          sx={{
                            ...theme.typography.smallAvatar,
                            cursor: 'pointer',
                            backgroundColor: theme.palette.primary[200],
                            color: theme.palette.primary.dark
                          }}
                        >
                          <ArrowDownwardIcon fontSize="inherit" sx={{ transform: 'rotate3d(1, 1, 1, 45deg)' }} />
                        </Avatar>
                      </Grid>
                      <Grid item xs={12}>
                        <Typography
                          sx={{
                            fontSize: '1rem',
                            fontWeight: 500,
                            color: theme.palette.primary[200]
                          }}
                        >
                          Asistencias
                        </Typography>
                      </Grid>
                    </Grid>
                  </Grid>
                  <Grid item xs={6}>
                    {timeValue ? <Chart {...ChartDataMonth} /> : <Chart {...ChartDataYear} />}
                  </Grid>
                </Grid>
              </Grid>
            </Grid>
          </Box>
        </CardWrapper>
      )}
    </>
  );
};

TotalOrderLineChartCard.propTypes = {
  isLoading: PropTypes.bool
};

export default TotalOrderLineChartCard;


