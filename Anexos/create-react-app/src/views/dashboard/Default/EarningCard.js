import PropTypes from 'prop-types';
import { useState } from 'react';
import { format, isToday } from 'date-fns';

// material-ui
import { styled, useTheme } from '@mui/material/styles';
import { Avatar, Box, Grid, Menu, MenuItem, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

// project imports
import MainCard from 'ui-component/cards/MainCard';
import SkeletonEarningCard from 'ui-component/cards/Skeleton/EarningCard';

// assets
import EarningIcon from 'assets/images/icons/earning.svg';
import MoreHorizIcon from '@mui/icons-material/MoreHoriz';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import GetAppTwoToneIcon from '@mui/icons-material/GetAppOutlined';
import FileCopyTwoToneIcon from '@mui/icons-material/FileCopyOutlined';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';


// Función auxiliar para exportar a CSV
const exportToCSV = (data, filename = 'export.csv') => {
  let csvContent = "data:text/csv;charset=utf-8,";

  // Agregar los headers al csv
  const headers = [
    "ParticipacionID",
    "EstudianteID",
    "ClaseID",
    "TipoParticipacion",
    "Detalles",
    "Timestamp",
    "NombreEstudiante",
    "ApellidoEstudiante"
  ];
  csvContent += headers.join(",") + "\n";

  csvContent += data.map(e => e.join(",")).join("\n");

  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", filename);
  document.body.appendChild(link); // Necesario para FF

  link.click(); // Iniciar descarga
  document.body.removeChild(link); // Limpiar después de descargar
};


const CardWrapper = styled(MainCard)(({ theme }) => ({
  backgroundColor: theme.palette.secondary.dark,
  color: '#fff',
  overflow: 'hidden',
  position: 'relative',
  '&:after': {
    content: '""',
    position: 'absolute',
    width: 210,
    height: 210,
    background: theme.palette.secondary[800],
    borderRadius: '50%',
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
    width: 210,
    height: 210,
    background: theme.palette.secondary[800],
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

// ===========================|| DASHBOARD DEFAULT - EARNING CARD ||=========================== //

const EarningCard = ({ isLoading, totalParticipacion }) => {



  const theme = useTheme();
  const [anchorEl, setAnchorEl] = useState(null);
  const [showTable, setShowTable] = useState(false);
  const [isTodayView, setIsTodayView] = useState(true);
  const isTotalParticipacionArray = Array.isArray(totalParticipacion);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const toggleTable = () => {
    setShowTable(!showTable);
  };

  const participacionesHoy = totalParticipacion === 'Sin datos' ? [] : totalParticipacion.filter((participacion) => {
    const timestamp = new Date(participacion[5]);
    return isToday(timestamp);
  });

  // Función para alternar entre vistas totales y de hoy
  const toggleView = () => {
    setIsTodayView(!isTodayView);
    handleClose();
  };

  // Función para manejar la exportación a CSV
  const handleExportCSV = () => {
    const dataToExport = isTodayView ? participacionesHoy : totalParticipacion;
    exportToCSV(dataToExport, 'participaciones.csv');
    handleClose();
  };

  const dataToShow = isTodayView ? participacionesHoy : (isTotalParticipacionArray ? totalParticipacion : []);
  return (
    <>
      {isLoading ? (
        <SkeletonEarningCard />
      ) : (
        <CardWrapper border={false} content={false}>
          <Box sx={{ p: 2.25 }}>
            <Grid container direction="column">
              <Grid item>
                <Grid container justifyContent="space-between">
                  <Grid item>
                    <Avatar
                      onClick={toggleTable}
                      variant="rounded"
                      sx={{
                        ...theme.typography.commonAvatar,
                        ...theme.typography.largeAvatar,
                        backgroundColor: theme.palette.secondary[800],
                        mt: 1
                      }}
                    >
                      <img src={EarningIcon} alt="Notification" />
                    </Avatar>
                  </Grid>
                  <Grid item>
                    <Avatar
                      variant="rounded"
                      sx={{
                        ...theme.typography.commonAvatar,
                        ...theme.typography.mediumAvatar,
                        backgroundColor: theme.palette.secondary.dark,
                        color: theme.palette.secondary[200],
                        zIndex: 1
                      }}
                      aria-controls="menu-earning-card"
                      aria-haspopup="true"
                      onClick={handleClick}
                    >
                      <MoreHorizIcon fontSize="inherit" />
                    </Avatar>
                    <Dialog
                      open={showTable}
                      onClose={toggleTable}
                      aria-labelledby="table-dialog-title"
                      maxWidth="lg"
                    >
                      <DialogTitle id="table-dialog-title">
                        {isTodayView ? "Participaciones de Hoy" : "Todas las Participaciones"}
                      </DialogTitle>
                      <DialogContent>
                        <TableContainer component={Paper}>
                          <Table sx={{ minWidth: 650 }} aria-label="simple table">
                            <TableHead>
                              <TableRow>
                                <TableCell>ParticipacionID</TableCell>
                                <TableCell>EstudianteID</TableCell>
                                <TableCell>ClaseID</TableCell>
                                <TableCell>TipoParticipacion</TableCell>
                                <TableCell>Detalles</TableCell>
                                <TableCell>Timestamp</TableCell>
                                <TableCell>NombreEstudiante</TableCell>
                                <TableCell>ApellidoEstudiante</TableCell>
                              </TableRow>
                            </TableHead>
                            <TableBody>
                              {dataToShow.map((row) => (
                                <TableRow
                                  key={row[0]}
                                  sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                >
                                  <TableCell component="th" scope="row">
                                    {row[0]}
                                  </TableCell>
                                  <TableCell>{row[1]}</TableCell>
                                  <TableCell>{row[2]}</TableCell>
                                  <TableCell>{row[3]}</TableCell>
                                  <TableCell>{row[4]}</TableCell>
                                  <TableCell>{format(new Date(row[5]), 'yyyy-MM-dd HH:mm:ss')}</TableCell>
                                  <TableCell>{row[6]}</TableCell>
                                  <TableCell>{row[7]}</TableCell>
                                </TableRow>
                              ))}
                            </TableBody>
                          </Table>
                        </TableContainer>
                      </DialogContent>
                    </Dialog>
                    {totalParticipacion !== 'string' && (
                      <Menu
                        id="menu-earning-card"
                        anchorEl={anchorEl}
                        keepMounted
                        open={Boolean(anchorEl)}
                        onClose={handleClose}
                        variant="selectedMenu"
                        anchorOrigin={{
                          vertical: 'bottom',
                          horizontal: 'right'
                        }}
                        transformOrigin={{
                          vertical: 'top',
                          horizontal: 'right'
                        }}
                      >
                        <MenuItem onClick={toggleView}>
                          <FileCopyTwoToneIcon sx={{ mr: 1.75 }} />
                          {isTodayView ? "Ver Participaciones Totales" : "Ver Participaciones de Hoy"}
                        </MenuItem>
                        <MenuItem onClick={handleExportCSV}>
                          <GetAppTwoToneIcon sx={{ mr: 1.75 }} /> Exportar a CSV
                        </MenuItem>
                      </Menu>
                    )}
                  </Grid>
                </Grid>
              </Grid>
              <Grid item>
                <Grid container alignItems="center">
                  <Grid item><Typography sx={{ fontSize: '2.125rem', fontWeight: 500, mr: 1, mt: 1.75, mb: 0.75 }}>
                    {dataToShow.length}
                  </Typography>
                  </Grid>
                  <Grid item>
                    <Avatar
                      sx={{
                        cursor: 'pointer',
                        ...theme.typography.smallAvatar,
                        backgroundColor: theme.palette.secondary[200],
                        color: theme.palette.secondary.dark
                      }}
                    >
                      <ArrowUpwardIcon fontSize="inherit" sx={{ transform: 'rotate3d(1, 1, 1, 45deg)' }} />
                    </Avatar>
                  </Grid>
                </Grid>
              </Grid>
              <Grid item sx={{ mb: 1.25 }}>
                <Typography
                  sx={{
                    fontSize: '1rem',
                    fontWeight: 500,
                    color: theme.palette.secondary[200]
                  }}
                >
                  Participaciones
                </Typography>
              </Grid>
            </Grid>
          </Box>
        </CardWrapper>
      )}
    </>
  );
};

EarningCard.propTypes = {
  isLoading: PropTypes.bool,
  totalParticipacion: PropTypes.arrayOf(PropTypes.array)
};

export default EarningCard;
