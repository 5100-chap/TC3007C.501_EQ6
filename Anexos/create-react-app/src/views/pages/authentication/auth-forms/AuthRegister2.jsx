import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import jwt from "jwt-decode";
// material-ui
import { useTheme } from "@mui/material/styles";
import {
	Box,
	Button,
	FormControl,
	FormHelperText,
	Grid,
	IconButton,
	InputAdornment,
	InputLabel,
	OutlinedInput,
	TextField,
	Typography,
	useMediaQuery,
	Select,
	MenuItem,
} from "@mui/material";

// third party
import * as Yup from "yup";
import { Formik } from "formik";
import { toast, ToastContainer } from "react-toastify";

// project imports
import useScriptRef from "hooks/useScriptRef";
import AnimateButton from "ui-component/extended/AnimateButton";
import { strengthColor, strengthIndicator } from "utils/password-strength";

// assets
import Visibility from "@mui/icons-material/Visibility";
import VisibilityOff from "@mui/icons-material/VisibilityOff";

import { API_BASE_URL } from "config/apiConfig";
import axios from "axios";

var roles = ["Admin", "Mod", "Profesor", "Alumno"];
// ===========================|| FIREBASE - REGISTER ||=========================== //

const FirebaseRegister = ({ ...others }) => {
	const theme = useTheme();
	const scriptedRef = useScriptRef();
	const matchDownSM = useMediaQuery(theme.breakpoints.down("md"));
	const [showPassword, setShowPassword] = useState(false);

	const [strength, setStrength] = useState(0);
	const [level, setLevel] = useState("");

	const [fname, setFname] = useState("");
	const [lname, setLname] = useState("");
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const [role, setRole] = useState("");
	const [UserID, setUserID] = useState("");

	const history = useNavigate();

	const handleClickShowPassword = () => {
		setShowPassword(!showPassword);
	};

	const handleMouseDownPassword = (event) => {
		event.preventDefault();
	};

	const changePassword = (value) => {
		const temp = strengthIndicator(value);
		setStrength(temp);
		setLevel(strengthColor(temp));
	};

	const [isFormValid, setIsFormValid] = useState(false);

	useEffect(() => {
		const isFormNowValid =
			validateField("fname", fname) &&
			validateField("lname", lname) &&
			validateField("email", email) &&
			validateField("password", password) &&
			validateField("role", role) &&
			(role === "Profesor" || role === "Alumno"
				? validateField("userid", UserID)
				: true);
		setIsFormValid(isFormNowValid);
	}, [fname, lname, email, password, role, UserID]);

	const decodedJwt = jwt(localStorage.getItem("jwt"));
	const userRole = decodedJwt.user_role;
	const allowedRoles = {
		Dueño: ["Admin", "Mod", "Profesor", "Alumno"],
		Admin: ["Mod", "Profesor", "Alumno"],
		Mod: ["Profesor", "Alumno"],
		Profesor: ["Alumno"],
	};
	roles = allowedRoles[userRole];

	// Function to validate each field
	const validateField = (name, value) => {
		switch (name) {
			case "fname":
				return value.length > 0 && value.length <= 255;
			case "lname":
				return value.length > 0 && value.length <= 255;
			case "email":
				return /\S+@\S+\.\S+/.test(value) && value.length <= 255;
			case "password":
				return value.length > 0 && value.length <= 255;
			case "role":
				return value.length > 0 && value.length <= 255;
			case "userid":
				return value.length > 0 && value.length <= 255;
			default:
				return false;
		}
	};

	const handleRegistration = async (userRole, values, history) => {
		if (allowedRoles[userRole]?.includes(values.role)) {
			const user_data = {
				accountEnabled: true,
				displayName: `${values.fname} ${values.lname}`,
				givenName: values.fname,
				surname: values.lname,
				identities: [
					{
						signInType: "emailAddress",
						issuer: "your_tenant_name.onmicrosoft.com",
						issuerAssignedId: values.email,
					},
				],
				passwordProfile: {
					forceChangePasswordNextSignIn: false,
					password: values.password,
				},
				Rol: values.role,
				userID: UserID,
				Admin_id: decodedJwt.oid,
			};

			try {
				const response = await axios.post(
					API_BASE_URL + "/register",
					user_data
				);
				if (response.status === 201) {
					toast.success("Registro exitoso", {
						position: "top-center",
						autoClose: 9000,
						hideProgressBar: false,
						closeOnClick: true,
						pauseOnHover: true,
						draggable: true,
						progress: undefined,
						theme: "light",
					});
				} else {
					toast.error("Algo falló", {
						position: "top-center",
						autoClose: 9000,
						hideProgressBar: false,
						closeOnClick: true,
						pauseOnHover: true,
						draggable: true,
						progress: undefined,
						theme: "light",
					});
				}
			} catch (error) {
				toast.error("Algo falló", error, {
					position: "top-center",
					autoClose: 20000,
					hideProgressBar: false,
					closeOnClick: true,
					pauseOnHover: true,
					draggable: true,
					progress: undefined,
					theme: "light",
				});
			}
		} else {
			toast.error("Algo falló", {
				position: "top-center",
				autoClose: 9000,
				hideProgressBar: false,
				closeOnClick: true,
				pauseOnHover: true,
				draggable: true,
				progress: undefined,
				theme: "light",
			});
		}
	};

	const handleSubmit = async (
		values,
		{ setErrors, setStatus, setSubmitting }
	) => {
		try {
			if (scriptedRef.current) {
				setStatus({ success: true });
				setSubmitting(false);
				handleRegistration(userRole, values, history);
			}
		} catch (err) {
			console.error(err);
			if (scriptedRef.current) {
				setStatus({ success: false });
				setErrors({ submit: err.message });
				setSubmitting(false);
			}
		}
	};
	return (
		<>
			<ToastContainer
				position="top-center"
				autoClose={9000}
				hideProgressBar={false}
				newestOnTop={false}
				closeOnClick
				rtl={false}
				pauseOnFocusLoss
				draggable
				pauseOnHover
				theme="light"
			/>
			<Grid
				container
				direction="column"
				justifyContent="center"
				spacing={2}
			>
				<Grid
					item
					xs={12}
					container
					alignItems="center"
					justifyContent="center"
				>
					<Box sx={{ mb: 2 }}>
						<Typography variant="subtitle1">
							Registrar usuario
						</Typography>
					</Box>
				</Grid>
			</Grid>

			<Formik
				initialValues={{
					fname: "",
					lname: "",
					email: "",
					password: "",
					role: "",
					submit: null,
				}}
				validationSchema={Yup.object().shape({
					fname: Yup.string()
						.max(255)
						.required("Se requiere el nombre"),
					lname: Yup.string()
						.max(255)
						.required("Se requiere el apellido"),
					email: Yup.string()
						.email("Debe ser un correo electrónico válido")
						.max(255)
						.required("Se requiere el correo electrónico"),
					password: Yup.string()
						.max(255)
						.required("Se requiere la contraseña"),
					role: Yup.string().max(255).required("Se requiere el rol"),
				})}
				onSubmit={handleSubmit}
			>
				{({
					errors,
					handleBlur,
					handleChange,
					handleSubmit,
					isSubmitting,
					touched,
					values,
				}) => (
					<form noValidate onSubmit={handleSubmit} {...others}>
						<Grid container spacing={matchDownSM ? 0 : 2}>
							<Grid item xs={12} sm={6}>
								<TextField
									fullWidth
									label="Nombre"
									margin="normal"
									name="fname"
									type="text"
									value={values.fname}
									onBlur={handleBlur}
									onChange={(e) => {
										handleChange(e);
										setFname(e.target.value);
									}}
									sx={{ ...theme.typography.customInput }}
								/>
							</Grid>
							<Grid item xs={12} sm={6}>
								<TextField
									fullWidth
									label="Apellido"
									margin="normal"
									name="lname"
									type="text"
									value={values.lname}
									onBlur={handleBlur}
									onChange={(e) => {
										handleChange(e);
										setLname(e.target.value);
									}}
									sx={{ ...theme.typography.customInput }}
								/>
							</Grid>
							<Grid item xs={12}>
								<FormControl
									fullWidth
									error={Boolean(
										touched.email && errors.email
									)}
									sx={{ ...theme.typography.customInput }}
								>
									<InputLabel htmlFor="outlined-adornment-email-register">
										Dirección de correo electrónico / Nombre
										de usuario
									</InputLabel>
									<OutlinedInput
										id="outlined-adornment-email-register"
										type="email"
										value={values.email}
										name="email"
										onBlur={handleBlur}
										onChange={(e) => {
											handleChange(e);
											setEmail(e.target.value);
										}}
										inputProps={{}}
									/>
									{touched.email && errors.email && (
										<FormHelperText
											error
											id="standard-weight-helper-text--register"
										>
											{errors.email}
										</FormHelperText>
									)}
								</FormControl>
							</Grid>
							<Grid item xs={12}>
								<FormControl
									fullWidth
									error={Boolean(
										touched.password && errors.password
									)}
									sx={{ ...theme.typography.customInput }}
								>
									<InputLabel htmlFor="outlined-adornment-password-register">
										Contraseña
									</InputLabel>
									<OutlinedInput
										id="outlined-adornment-password-register"
										type={
											showPassword ? "text" : "password"
										}
										value={values.password}
										name="password"
										label="Contraseña"
										onBlur={handleBlur}
										onChange={(e) => {
											handleChange(e);
											changePassword(e.target.value);
											setPassword(e.target.value);
										}}
										endAdornment={
											<InputAdornment position="end">
												<IconButton
													aria-label="toggle password visibility"
													onClick={
														handleClickShowPassword
													}
													onMouseDown={
														handleMouseDownPassword
													}
													edge="end"
													size="large"
												>
													{showPassword ? (
														<Visibility />
													) : (
														<VisibilityOff />
													)}
												</IconButton>
											</InputAdornment>
										}
										inputProps={{}}
									/>
									{touched.password && errors.password && (
										<FormHelperText
											error
											id="standard-weight-helper-text-password-register"
										>
											{errors.password}
										</FormHelperText>
									)}
								</FormControl>
							</Grid>
							<Grid item xs={12}>
								<FormControl
									fullWidth
									error={Boolean(touched.role && errors.role)}
									sx={{ ...theme.typography.customInput }}
								>
									<InputLabel htmlFor="outlined-adornment-role-register"></InputLabel>
									<Select
										id="outlined-adornment-role-register"
										value={values.role}
										name="role"
										onBlur={handleBlur}
										onChange={(e) => {
											handleChange(e);
											setRole(e.target.value);
										}}
										input={<OutlinedInput label="Rol" />}
									>
										{roles.map((role) => (
											<MenuItem key={role} value={role}>
												{role}
											</MenuItem>
										))}
									</Select>
									{touched.role && errors.role && (
										<FormHelperText
											error
											id="standard-weight-helper-text--register"
										>
											{errors.role}
										</FormHelperText>
									)}
								</FormControl>
							</Grid>

							{values.role === "Profesor" && (
								<Grid item xs={12}>
									<TextField
										fullWidth
										label="Número de Nómina"
										margin="normal"
										name="teacherId"
										type="text"
										value={UserID}
										onBlur={handleBlur}
										onChange={(e) =>
											setUserID(e.target.value)
										}
										sx={{ ...theme.typography.customInput }}
									/>
								</Grid>
							)}

							{values.role === "Alumno" && (
								<Grid item xs={12}>
									<TextField
										fullWidth
										label="Matrícula"
										margin="normal"
										name="studentId"
										type="text"
										value={UserID}
										onBlur={handleBlur}
										onChange={(e) =>
											setUserID(e.target.value)
										}
										sx={{ ...theme.typography.customInput }}
									/>
								</Grid>
							)}
						</Grid>
						{strength !== 0 && (
							<FormControl fullWidth>
								<Box sx={{ mb: 2 }}>
									<Grid
										container
										spacing={2}
										alignItems="center"
									>
										<Grid item>
											<Box
												style={{
													backgroundColor:
														level?.color,
												}}
												sx={{
													width: 85,
													height: 8,
													borderRadius: "7px",
												}}
											/>
										</Grid>
										<Grid item>
											<Typography
												variant="subtitle1"
												fontSize="0.75rem"
											>
												{level?.label}
											</Typography>
										</Grid>
									</Grid>
								</Box>
							</FormControl>
						)}
						{errors.submit && (
							<Box sx={{ mt: 3 }}>
								<FormHelperText error>
									{errors.submit}
								</FormHelperText>
							</Box>
						)}

						<Box sx={{ mt: 2 }}>
							<AnimateButton>
								<Button
									disableElevation
									disabled={!isFormValid}
									fullWidth
									size="large"
									type="submit"
									variant="contained"
									color="secondary"
									onClick={handleSubmit}
								>
									Registrar
								</Button>
							</AnimateButton>
						</Box>
					</form>
				)}
			</Formik>
		</>
	);
};

export default FirebaseRegister;
