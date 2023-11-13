// material-ui
// project imports
import MainCard from "ui-component/cards/MainCard";
// material-ui
import { Grid } from "@mui/material";
import VideoCallIcon from "@mui/icons-material/VideoCall";
import Button from "@mui/material/Button";
import Webcam from "react-webcam";

import React, { useRef, useState } from "react";
import axios from "axios";
// ==============================|| SAMPLE PAGE ||============================== //

const Camera = ({ apiURL }) => {
	const webcamRef = useRef(null);
	const [imageSrc, setImageSrc] = useState(null);

	// Función para capturar la imagen de la cámara
	const capture = React.useCallback(() => {
		const imageSrc = webcamRef.current.getScreenshot();
		setImageSrc(imageSrc);
	}, [webcamRef]);

	// Función para enviar la imagen capturada a la API
	const sendImageToAPI = () => {
		axios
			.post(apiURL, { image: imageSrc })
			.then((response) => {
				// Manejo de la respuesta
				console.log(response.data);
			})
			.catch((error) => {
				// Manejo de errores
				console.error("Error al enviar la imagen", error);
			});
	};

	const captureVideo = () => {
		const interval = setInterval(() => {
			const imageSrc = webcamRef.current.getScreenshot();
			sendImageToAPI(imageSrc);
		}, 100); // Captura cada 100 ms

		return () => clearInterval(interval);
	};

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
				<Grid item lg={6} md={6} sm={6} xs={6}></Grid>
				<Button
					onClick={capture}
					variant="contained"
					endIcon={<VideoCallIcon />}
					color="secondary"
				>
					Capturar Imagen
				</Button>
				<Button
					onClick={captureVideo}
					variant="contained"
					color="primary"
				>
					Iniciar Video
				</Button>
			</Grid>
		</MainCard>
	);
};

export default Camera;
