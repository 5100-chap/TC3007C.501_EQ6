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
				userRole === "Dueño" ||
				userRole === "Profesor"
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
						Buen dia estimado {decodedPayload.given_name + ' ' + decodedPayload.family_name}, aqui se
						podra seleccionar varias opciones acorde a lo que necesite:
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
					Esta es la pagina de face 'n learn, actualmente no cuenta con credenciales validas para acceder a la pagina, favor de ponerse en contacto con un administrador para que se pueda solucionar el problema.
					De igual forma puede intentar volver a iniciar sesión de la pagina con las mismas credenciales o con otras que se le hayan proporcionado.
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
