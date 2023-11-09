// material-ui
// project imports
import MainCard from 'ui-component/cards/MainCard';
// material-ui
import { Grid } from '@mui/material';
import VideoCallIcon from '@mui/icons-material/VideoCall';
import Button from '@mui/material/Button';
import Webcam from "react-webcam";

import React, { useRef } from 'react';
import axios from 'axios';
// ==============================|| SAMPLE PAGE ||============================== //

const Camera = ({ apiURL }) => {
  const webcamRef = useRef(null);

  // Función para capturar la imagen de la cámara
  const capture = React.useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    // Aquí enviarías `imageSrc` al backend, por ejemplo, usando Axios y un endpoint de tu API
    axios.post(apiURL, { image: imageSrc })
      .then(response => {
        // Manejo de la respuesta
        console.log(response.data);
      })
      .catch(error => {
        // Manejo de errores
        console.error('Error al enviar la imagen', error);
      });
  }, [webcamRef, apiURL]);

  return (
    <MainCard title="Cámara">
      <Grid container spacing={2}>
        <Grid item lg={6} md={6} sm={6} xs={12}>
          <Webcam
            audio={false}
            ref={webcamRef}
            screenshotFormat="image/jpeg"
          />
        </Grid>
        <Grid item lg={6} md={6} sm={6} xs={6}>
        </Grid>
        <Button onClick={capture} variant="contained" endIcon={<VideoCallIcon />} color='secondary'>
          Iniciar Grabación
        </Button>
      </Grid>
    </MainCard>
  );
};

export default Camera;