import { useEffect, useState } from "react";
import AddIcon from "@mui/icons-material/Add";
import { DataGrid } from "@mui/x-data-grid";
import {
    Grid,
    TextField,
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
} from "@mui/material";
import { API_BASE_URL } from "config/apiConfig";
import axios from "axios";
import jwt from "jwt-decode";
import { useCallback, useMemo } from "react";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const gridSpacing = 8;
const RegistroCara = () => {
    const initialState = useMemo(() => [
        { id: -1, nombre: "", apellido: "", email: "", oid: "", matricula: "", fotoRostro: '' }
    ], []); // Empty dependency array means this runs once on component mount
    
    const [userRole, setUserRole] = useState("");
    const [alumnos, setAlumnos] = useState(initialState);
    const [selectedAlumno, setSelectedAlumno] = useState(null);
    const [openDialog, setOpenDialog] = useState(false);
    const [fotoRostro, setFotoRostro] = useState(null);

    const fetchAlumnos = useCallback(async () => {
        setAlumnos(initialState);
        const decodedJwt = jwt(localStorage.getItem("jwt"));
        setUserRole(decodedJwt.user_role);
        const userRole = decodedJwt.user_role;
    
        try {
            const response = await axios.post(
                `${API_BASE_URL}/obtain_students_info`,
                {
                    type: userRole === "Alumno" ? "Other" : "AllStudentRequest",
                    oid: userRole === "Alumno" ? decodedJwt.oid : undefined,
                    Clase: userRole === "Alumno" ? 'None' : undefined,
                    Curso: userRole === "Alumno" ? 'None' : undefined
                }
            );
            const data = response.data;
            const alumnosTransformados = data.map((alumno) => ({
                id: alumno[0],
                nombre: alumno[1],
                apellido: alumno[2],
                email: alumno[3],
                oid: alumno[4],
                matricula: alumno[5],
                fotoRostro: alumno[6],
            }));
            setAlumnos(alumnosTransformados);
        } catch (error) {
            console.error(error);
        }
    }, [initialState]); // Include other dependencies if they exist
    
    useEffect(() => {
        // Obtener el rol del usuario almacenado en el JWT en el localStorage
        const role = localStorage.getItem("userRole");
        setUserRole(role);
    }, []);

    useEffect(() => {
        // Obtener la lista de alumnos
        fetchAlumnos();
    }, [fetchAlumnos]);

    const handleAlumnoSelection = (alumno) => {
        setSelectedAlumno(alumno);
        setOpenDialog(true);
    };

    const handleFotoUpload = async () => {
        try {
            const formData = new FormData();
            const decodedJwt = jwt(localStorage.getItem("jwt"));
            formData.append("oid", selectedAlumno.oid);
            formData.append("user_oid", decodedJwt.oid);
            formData.append("Rol", userRole);
            formData.append("file", fotoRostro);

            const response = await fetch(`${API_BASE_URL}/alumnos/foto`, {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("jwt")}`,
                },
                body: formData,
            });

            const data = await response.json();
            // Actualizar la lista de alumnos con la nueva información
            setAlumnos((prevAlumnos) =>
                prevAlumnos.map((alumno) =>
                    alumno.oid === selectedAlumno.oid ? data : alumno
                )
            );
            setOpenDialog(false);
            toast.success("La foto se ha subido exitosamente.", {
                autoClose: 5000, // Cerrar el mensaje automáticamente después de 5 segundos
            }); // Mostrar notificación de éxito
            fetchAlumnos();
        } catch (error) {
            console.error(error);
            toast.error("Error al subir la foto. Por favor, inténtalo de nuevo.", {
                autoClose: 5000, // Cerrar el mensaje automáticamente después de 5 segundos
            }); // Mostrar notificación de error
            fetchAlumnos();
        }
    };

    return (
        <div>
            <ToastContainer /> {/* Contenedor para mostrar los mensajes de toast */}
            {userRole === "Admin" ||
            userRole === "Mod" ||
            userRole === "Dueño" ||
            userRole === "Profesor" ||
            userRole === "Alumno" ? (
                <Grid container spacing={gridSpacing}>
                    <Grid item xs={12}>
                        <DataGrid
                            rows={alumnos}
                            columns={[
                                { field: "id", headerName: "ID", width: 100 },
                                {
                                    field: "nombre",
                                    headerName: "Nombre",
                                    width: 200,
                                },
                                {
                                    field: "apellido",
                                    headerName: "Apellido",
                                    width: 200,
                                },
                                {
                                    field: "email",
                                    headerName: "Email",
                                    width: 200,
                                },
                            ]}
                            onRowClick={(params) =>
                                handleAlumnoSelection(params.row)
                            }
                        />
                    </Grid>
                </Grid>
            ) : (
                <Grid container spacing={gridSpacing}>
                    <Grid item xs={12}>
                        <TextField
                            label="Nombre"
                            value={selectedAlumno?.nombre || ""}
                            disabled
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField
                            label="Apellido"
                            value={selectedAlumno?.apellido || ""}
                            disabled
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField
                            label="Foto Rostro"
                            value={
                                selectedAlumno?.fotoRostro
                                    ? "Ya tiene foto"
                                    : "Debe subir una foto"
                            }
                            disabled
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <Button
                            variant="contained"
                            component="label"
                            startIcon={<AddIcon />}
                        >
                            Subir Foto
                            <input
                                type="file"
                                accept="image/*"
                                style={{ display: "none" }}
                                onChange={(e) =>
                                    setFotoRostro(e.target.files[0])
                                }
                            />
                        </Button>
                    </Grid>
                </Grid>
            )}

            <Dialog open={openDialog} onClose={() => setOpenDialog(false)}>
                <DialogTitle>Subir Foto</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        {selectedAlumno?.fotoRostro
                            ? "Ya tiene una foto. ¿Desea actualizarla?"
                            : "Debe subir una foto."}
                    </DialogContentText>
                    <input
                        type="file"
                        accept="image/*"
                        onChange={(e) => setFotoRostro(e.target.files[0])}
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setOpenDialog(false)}>
                        Cancelar
                    </Button>
                    <Button onClick={handleFotoUpload} color="primary">
                        Subir
                    </Button>
                </DialogActions>
            </Dialog>
        </div>
    );
};

export default RegistroCara;
