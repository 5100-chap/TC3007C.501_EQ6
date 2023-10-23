// material-ui
// project imports
import MainCard from 'ui-component/cards/MainCard';
// material-ui
import { Grid } from '@mui/material';
import VideoCallIcon from '@mui/icons-material/VideoCall';
import Button from '@mui/material/Button';
import Webcam from "react-webcam";

// ==============================|| SAMPLE PAGE ||============================== //

const Camera = () => (
  <MainCard title="Camara">
    <Grid item lg={6} md={6} sm={6} xs={12}>
      <Webcam></Webcam>
    </Grid>
    <Grid item lg={6} md={6} sm={6} xs={6}>
            <Button   variant="contained" endIcon={<VideoCallIcon />} color='inherit'>
            Iniciar Grabación
            </Button>
          </Grid>
  </MainCard>
);

export default Camera;