import { Link } from "react-router-dom";
import { useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { isJwtExpired } from "jwt-check-expiration"; // Usa una librería para verificar la caducidad del JWT

// material-ui
import { useTheme } from "@mui/material/styles";
import { Divider, Grid, Stack, Typography, useMediaQuery } from "@mui/material";

// project imports
import AuthWrapper1 from "../AuthWrapper1";
import AuthCardWrapper from "../AuthCardWrapper";
import AuthLogin from "../auth-forms/AuthLogin2";
import { OWN_BASE_URL } from "config/apiConfig";
// assets

// ================================|| AUTH3 - LOGIN ||================================ //

const redirectToExternalUrl = (url) => {
	window.location.href = url;
};

const Login = () => {
	const navigate = useNavigate();
	const location = useLocation();
	const theme = useTheme();
	const matchDownSM = useMediaQuery(theme.breakpoints.down("md"));

	useEffect(() => {
		const queryParams = new URLSearchParams(location.search);
		const jwt = queryParams.get("jwt");

		if (jwt) {
			localStorage.setItem("jwt", jwt);
			navigate("/inicio");
		} else {
			const storedJwt = localStorage.getItem("jwt");
			if (storedJwt && !isJwtExpired(storedJwt)) {
				redirectToExternalUrl(OWN_BASE_URL + "/inicio");
			}
		}
	}, [location, navigate]);

	return (
		<AuthWrapper1>
			<Grid
				container
				direction="column"
				justifyContent="flex-end"
				sx={{ minHeight: "100vh" }}
			>
				<Grid item xs={12}>
					<Grid
						container
						justifyContent="center"
						alignItems="center"
						sx={{ minHeight: "calc(100vh - 68px)" }}
					>
						<Grid item sx={{ m: { xs: 1, sm: 3 }, mb: 0 }}>
							<AuthCardWrapper>
								<Grid
									container
									spacing={2}
									alignItems="center"
									justifyContent="center"
								>
									<Grid item sx={{ mb: 3 }}></Grid>
									<Grid item xs={12}>
										<Grid
											container
											direction={
												matchDownSM
													? "column-reverse"
													: "row"
											}
											alignItems="center"
											justifyContent="center"
										>
											<Grid item>
												<Stack
													alignItems="center"
													justifyContent="center"
													spacing={1}
												>
													<Typography
														color={
															theme.palette
																.secondary.main
														}
														gutterBottom
														variant={
															matchDownSM
																? "h3"
																: "h2"
														}
													>
														Bienvenido a Face N
														Learn
													</Typography>
													<Typography
														variant="caption"
														fontSize="16px"
														textAlign={
															matchDownSM
																? "center"
																: "inherit"
														}
													>
														Introduce tus
														credenciales para
														acceder a tu cuenta
													</Typography>
												</Stack>
											</Grid>
										</Grid>
									</Grid>
									<Grid item xs={12}>
										<AuthLogin />
									</Grid>
									<Grid item xs={12}>
										<Divider />
									</Grid>
									<Grid item xs={12}>
										<Grid
											item
											container
											direction="column"
											alignItems="center"
											xs={12}
										></Grid>
									</Grid>
								</Grid>
							</AuthCardWrapper>
						</Grid>
					</Grid>
				</Grid>
			</Grid>
		</AuthWrapper1>
	);
};

export default Login;
