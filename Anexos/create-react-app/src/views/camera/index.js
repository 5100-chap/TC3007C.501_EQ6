// material-ui
// project imports
import MainCard from "ui-component/cards/MainCard";
// material-ui
import { Grid, MenuItem, Select } from "@mui/material";
import VideoCallIcon from "@mui/icons-material/VideoCall";
import Button from "@mui/material/Button";
import Webcam from "react-webcam";
import { API_BASE_URL } from "config/apiConfig";
import React, { useRef, useState, useEffect, useCallback } from "react";
import axios from "axios";
import jwt from "jwt-decode";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

// ==============================|| SAMPLE PAGE ||============================== //

const Camera = ({ apiURL }) => {
	const webcamRef = useRef(null);
	const [processedImage, setProcessedImage] = useState(null);
	const [courses, setCourses] = useState([]);
	const [selectedCourse, setSelectedCourse] = useState("");
	const [transformedCourse, setTransformedCourse] = useState([]);
	const [isCourseSelected, setIsCourseSelected] = useState(false);
	const [isVideoStreaming, setIsVideoStreaming] = useState(false);
	const token = jwt(localStorage.getItem("jwt"));
	// Función para enviar la imagen capturada y el curso seleccionado a la API
	const sendImageToAPI = useCallback((imageSrc, typeRequest = false) => {
		axios
			.post(`${API_BASE_URL}/receive_fps_ml`, {
				image: imageSrc,
				course: selectedCourse,
				type_request: typeRequest,
				role: token.user_role,
			})
			.then((response) => {
				// Manejo de la respuesta
				setProcessedImage(
					`data:image/jpeg;base64,${response.data.image}`
				);
				if (response.data.results.is_finished === true) {
					const participants = 'y se han registrado '+ response.data.results.detected_participants + ' participaciones';
					toast.success(`Se ha registrado ${response.data.results.detected_faces} nuevas asistencias ${token.user_role === 'Alumno' ? '' : participants}`, {
						autoClose: 5000, // Cerrar el mensaje automáticamente después de 5 segundos
					}); // Mostrar notificación de éxito);
				}
			})
			.catch((error) => {
				// Manejo de errores
				console.error("Error al enviar la imagen", error);
			});
	}, [selectedCourse, token.user_role]);

	useEffect(() => {
		// Función para obtener los cursos de la API
		const fetchCourses = async () => {
			try {
				// Realizar la solicitud POST a la API para obtener los cursos
				const response = await axios.post(
					`${API_BASE_URL}/obtain_clases_info`,
					{
						oid: token.oid,
						user_role: token.user_role,
					}
				);
				// Almacenar los cursos en el estado
				setCourses(response.data);
				// Transformar los datos para que coincidan con la estructura esperada
				const transformedCourses = response.data.map((courseArray) => ({
					id: courseArray[0],
					name: `${courseArray[3]} - ${courseArray[9]}`, // Por ejemplo, "grupo 1 - Ensayo profesional..."
				}));
				console.log(response.data);
				console.log(transformedCourses);
				setTransformedCourse(transformedCourses);
			} catch (error) {
				console.error("Error al obtener los cursos", error);
			}
		};

		fetchCourses();
		console.log(courses);
	}, []);

	useEffect(() => {
		// Verificar si un curso está seleccionado
		if (selectedCourse !== "") {
			setIsCourseSelected(true);
			console.log(selectedCourse)
		} else {
			setIsCourseSelected(false);
		}
	}, [selectedCourse]);

	// Función para capturar el video de la cámara y enviarlo a la API
	const captureVideo = () => {
		setIsVideoStreaming(!isVideoStreaming);
	};

	useEffect(() => {
		let interval;
		if (isVideoStreaming) {
			interval = setInterval(() => {
				const imageSrc = webcamRef.current.getScreenshot();
				sendImageToAPI(imageSrc);
			}, 800); // Captura cada ms
		} else {
			const imageSrc = webcamRef.current.getScreenshot();
			sendImageToAPI(imageSrc, true);
		}

		return () => {
			if (interval) {
				clearInterval(interval);
			}
		};
	}, [isVideoStreaming, sendImageToAPI]);

	

	return (
		<MainCard title="Cámara">
			<Grid container spacing={2}>
				
				<Grid item lg={6} md={6} sm={6} xs={12}>
					<Webcam
						audio={false}
						ref={webcamRef}
						screenshotFormat="image/jpeg"
					/>
					{/* Mostrar la imagen procesada */}
					{processedImage && (
						<img src={processedImage} alt="Processed" />
					)}
				</Grid>
				<Grid item lg={6} md={6} sm={6} xs={6}></Grid>
				<Button
					onClick={captureVideo}
					variant="contained"
					endIcon={<VideoCallIcon />}
					color="secondary"
					disabled={!isCourseSelected}
				>
					{isVideoStreaming ? "Parar Video" : "Iniciar Video"}
				</Button>
				<Select
					value={selectedCourse}
					onChange={(event) => setSelectedCourse(event.target.value)}
				>
					{transformedCourse.map((transformedCourse) => (
						<MenuItem
							key={transformedCourse.id}
							value={transformedCourse.id}
						>
							{transformedCourse.name}
						</MenuItem>
					))}
				</Select>
				{!isCourseSelected && <p>Favor de seleccionar un curso</p>}
				<ToastContainer />{}
			</Grid>
		</MainCard>
	);
};

export default Camera;