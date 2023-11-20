import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { Button, Typography } from "@mui/material";
import MainCard from "ui-component/cards/MainCard";
import RegistroCara from "views/camera/registroCara"; // Importar el componente de la página /registro-cara
import Register from "views/pages/authentication/authentication3/Register3";

const Inicio = () => {
	const history = useNavigate();
	const [showRegistroCara, setShowRegistroCara] = useState(false); // Agregar estado para mostrar/ocultar el componente RegistroCara
	const [showRegistro, setShowRegistro] = useState(false);
	const handleAddProfile = () => {
		const jwt = localStorage.getItem("jwt");
		if (jwt) {
			const [, payload] = jwt.split(".");
			const decodedPayload = JSON.parse(atob(payload));
			const userRole = decodedPayload.user_role;
			if (
				userRole === "Admin" ||
				userRole === "Mod" ||
				userRole === "Dueño"
			) {
				setShowRegistro(!showRegistro);
			}
		}
	};

  const handlePhotoProfile = () => {
    const jwt = localStorage.getItem("jwt");
    if (jwt) {
      const [, payload] = jwt.split(".");
      const decodedPayload = JSON.parse(atob(payload));
      const userRole = decodedPayload.user_role;
    if (
        userRole === "Admin" ||
        userRole === "Mod" ||
        userRole === "Dueño" ||
        userRole === "Alumno" || 
        userRole === "Profesor"
      ) {
        setShowRegistroCara(!showRegistroCara);
      }
    }
  };


	const jwt = localStorage.getItem("jwt");
	if (jwt) {
		const [, payload] = jwt.split(".");
		const decodedPayload = JSON.parse(atob(payload));
		const userRole = decodedPayload.user_role;
		console.log(decodedPayload);
		if (userRole === "Alumno") {
			return (
				<MainCard title="Bienvenido Alumno">
					<Typography variant="body2"></Typography>
					{showRegistroCara && <RegistroCara />}{" "}
					<Button variant="contained" onClick={handlePhotoProfile}>
						Agregar cara
					</Button>
				</MainCard>
			);
		} else if (userRole === "Profesor") {
			return (
				<MainCard title="Bienvenido Profesor">
					<Typography variant="body2">
						Lorem ipsum dolor sit amen, consenter nipissing eli, sed
						do elusion tempos incident ut laborers et doolie magna
						alissa. Ut enif ad minim venice, quin nostrum
						exercitation illampu laborings nisi ut liquid ex ea
						commons construal. Duos aube grue dolor in reprehended
						in voltage veil esse colum doolie eu fujian bulla
						parian. Exceptive sin ocean cuspidate non president,
						sunk in culpa qui officiate descent molls anim id est
						labours.
					</Typography>
					{/* Aquí podrías mostrar los cursos del profesor */}
				</MainCard>
			);
		} else if (
			userRole === "Admin" ||
			userRole === "Mod" ||
			userRole === "Dueño"
		) {
			return (
				<MainCard
					title={
						userRole === "Admin"
							? "Bienvenido Administrador"
							: userRole === "Mod"
							? "Bienvenido Moderador"
							: userRole === "Dueño"
							? "Bienvenido Dueño"
							: "Bienvenido"
					}
				>
					<Typography variant="body2">
						Buen dia estimado {decodedPayload.user_name}, aqui se
						podra seleccionar la opcion de poder agregar un usuario
						al sistema, ya sea profesor o alumno
						{showRegistro && <Register />}{" "}
						{showRegistroCara && <RegistroCara />}{""}
					</Typography>
					<Button variant="contained" onClick={handleAddProfile}>
						{showRegistro
							? "Ocultar registro"
							: "Registrar usuario"}
					</Button>
          <>  </>
          <Button variant="contained" onClick={handlePhotoProfile}>
						{showRegistroCara
							? "Ocultar registro de cara"
							: "Registrar cara de usuario"}
					</Button>
				</MainCard>
			);
		}
	} else {
		return (
			<MainCard title="Bienvenido">
				<Typography variant="body2">
					Lorem ipsum dolor sit amen, consenter nipissing eli, sed do
					elusion tempos incident ut laborers et doolie magna alissa.
					Ut enif ad minim venice, quin nostrum exercitation illampu
					laborings nisi ut liquid ex ea commons construal. Duos aube
					grue dolor in reprehended in voltage veil esse colum doolie
					eu fujian bulla parian. Exceptive sin ocean cuspidate non
					president, sunk in culpa qui officiate descent molls anim id
					est labours.
				</Typography>
				<Button
					variant="contained"
					onClick={() => history.push("/login")}
				>
					Iniciar sesión
				</Button>
			</MainCard>
		);
	}
};

export default Inicio;
