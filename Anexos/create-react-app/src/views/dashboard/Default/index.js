import { useEffect, useState } from "react";
import AddIcon from "@mui/icons-material/Add";
// material-ui
// project imports
import EarningCard from "./EarningCard";
//import PopularCard from './PopularCard';
import TotalOrderLineChartCard from "./TotalOrderLineChartCard";
//import TotalIncomeDarkCard from './TotalIncomeDarkCard';
//import TotalIncomeLightCard from './TotalIncomeLightCard';
import TotalGrowthBarChart from "./TotalGrowthBarChart";
import { gridSpacing } from "store/constant";
import { DataGrid } from "@mui/x-data-grid";
import {
  Grid,
  TextField,
  MenuItem,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
} from "@mui/material";

import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";

import Lista from "./list";
import axios from "axios";
import jwt from "jwt-decode";
import { API_BASE_URL } from "config/apiConfig";
// ==============================|| DEFAULT DASHBOARD ||============================== //

const Dashboard = () => {
  const [value, setValue] = useState(-1);
  const [isLoading, setLoading] = useState(true);
  const [courses, setCourses] = useState([]);
  const [transformedCourses, setTransformedCourses] = useState([]);
  const [user_role, setUser_role] = useState();
  const [totalAsistencia, setTotalAsistencia] = useState("Sin datos");
  const [asistenciaPorClase, setAsistenciaPorClase] = useState("Sin datos");
  const [participacionPorClase, setParticipacionPorClase] = useState("Sin datos");
  const [numeroAlumnos, setNumeroAlumnos] = useState(0);
  const [numeroCurso, setNumeroCurso] = useState();
  const [asistenciaPorClaseCount, setAsistenciaPorClaseCount] = useState('Sin datos');

  // Cambio en la función de actualización de valor
  const handleChange = (event) => {
    const selectedCourseId = event.target.value;
    setValue(selectedCourseId);
    setNumeroCurso(selectedCourseId.toString()); // Actualizar el curso seleccionado
    // Restablecer los datos a "Sin datos" hasta que se carguen los nuevos
    setTotalAsistencia("Sin datos");
    setAsistenciaPorClase("Sin datos");
    setParticipacionPorClase("Sin datos");
  };
  useEffect(() => {
    const fetchCourses = async () => {
      try {
        // Decifrar el JWT almacenado en localStorage y obtener los valores necesarios
        const token = jwt(localStorage.getItem("jwt"));
        // Realizar la solicitud POST a la API para obtener los cursos
        setUser_role(token.user_role);
        const response = await axios.post(
          `${API_BASE_URL}/obtain_clases_info`,
          {
            oid: token.oid,
            user_role: token.user_role,
          }
        );
        // Almacenar los cursos en el estado

        const transformedCourses2 = response.data.map((courseArray) => ({
          id: courseArray[0],
          ClaseID: courseArray[0],
          CursoID: courseArray[1],
          Ubicacion: courseArray[2],
          Nombre: courseArray[3],
          FechaInicio: courseArray[4],
          FechaFin: courseArray[5],
          HoraInicio: courseArray[6],
          HoraFin: courseArray[7],
          ProfesorID: courseArray[8],
          NombreCurso: courseArray[9],
          NombreProfesor: courseArray[10],
          ApellidoProfesor: courseArray[11],
        }));
        setCourses(transformedCourses2);
        console.log(courses);
        // Transformar los datos para que coincidan con la estructura esperada
        const transformedCourses = response.data.map((courseArray) => ({
          id: courseArray[0],
          name: `${courseArray[3]} - ${courseArray[9]}`, // Por ejemplo, "grupo 1 - Ensayo profesional..."
        }));
        setNumeroCurso(courses[0]);
        setTransformedCourses(transformedCourses);
        console.log(transformedCourses);
        setLoading(false);
      } catch (error) {
        console.error("Error al obtener los cursos", error);
      }
    };


    fetchCourses();
  }, []);

  useEffect(() => {
    if (!numeroCurso) {
      return;
    }
    const fetchTotalAsistencia = async () => {
      try {
        const response = await axios.post(
          `${API_BASE_URL}/calcular_asistencia_total`,
          {
            clase_id: numeroCurso,
          }
        );
        setTotalAsistencia(response.data.total_asistencia);
      } catch (error) {
        console.error("Error al obtener la asistencia total", error);
      }
    };

    const fetchAsistenciaPorClase = async () => {
      try {
        const response = await axios.post(
          `${API_BASE_URL}/get_asistencia_por_clase`,
          {
            clase_id: numeroCurso,
          }
        );
        const asistenciaPorClaseData = response.data;
        const asistenciaPorClaseCount = asistenciaPorClaseData.length;
        setAsistenciaPorClase(asistenciaPorClaseData);
        setAsistenciaPorClaseCount(asistenciaPorClaseCount); // Guardar el conteo en una variable
      } catch (error) {
        console.error(
          "Error al obtener la asistencia por clase",
          error
        );
      }
    };

    const fetchParticipacionPorClase = async () => {
      try {
        const response = await axios.post(
          `${API_BASE_URL}/get_participacion_por_clase`,
          {
            clase_id: numeroCurso,
          }
        );
        setParticipacionPorClase(response.data);
      } catch (error) {
        console.error(
          "Error al obtener la participación por clase",
          error
        );
      }
    };

    const fetchNumeroAlumnos = async () => {
      try {
        const response = await axios.post(
          `${API_BASE_URL}/get_numero_alumnos`,
          {
            clase_id: numeroCurso,
          }
        );
        setNumeroAlumnos(response.data.numero_alumnos);
      } catch (error) {
        console.error("Error al obtener el número de alumnos", error);
      }
    };

    fetchNumeroAlumnos();

    fetchParticipacionPorClase();

    fetchAsistenciaPorClase();

    fetchTotalAsistencia();
  }, [numeroCurso]);

  const [openDialog, setOpenDialog] = useState(false);
  const [openEdit, setopenEdit] = useState(false);
  const [openDelete, setopenDelete] = useState(false);

  const handleDialogOpen = () => {
    setOpenDialog(true);
  };

  const handleDialogClose = () => {
    setOpenDialog(false);
  };

  const handleEditOpen = () => {
    setopenEdit(true);
  };

  const handleEditClose = () => {
    setopenEdit(false);
  };

  const handleDeleteOpen = () => {
    setopenDelete(true);
  };

  const handleDeleteClose = () => {
    setopenDelete(false);
  };

  const [columns, setColumns] = useState([]);
  const [rows, setRows] = useState([]);

  const obtainStudentsInfo = async () => {
    try {
      const token = jwt(localStorage.getItem("jwt"));
      var response
      if (user_role === 'Alumno') {
        response = await axios.post(`${API_BASE_URL}/obtain_students_info`, {
          type: "Courses",
          oid: token.oid,
          Clase: courses.find(course => course.id === value)?.Nombre,
          Curso: courses.find(course => course.id === value)?.NombreCurso,
        });
      }
      else {
        response = await axios.post(`${API_BASE_URL}/obtain_students_info`, {
          type: "Courses",
          oid: false,
          Clase: courses.find(course => course.id === value)?.Nombre,
          Curso: courses.find(course => course.id === value)?.NombreCurso,
        });
      }
      console.log(courses.find(course => course.id === value)?.ClaseID);
      console.log(courses.find(course => course.id === value)?.CursoID);
      const students = response.data;
      console.log(response.data);
      const columns = [
        { field: "id", headerName: "Matricula", width: 130 },
        { field: "firstName", headerName: "Nombre", width: 150 },
        { field: "lastName", headerName: "Apellidos", width: 150 },
      ];
      const rows = students.map(student => ({
        id: student.id,
        lastName: student.lastName,
        firstName: student.firstName,
        participacion: student.participacion,
      }));
      setColumns(columns);
      setRows(rows);
    } catch (error) {
      console.error("Error al obtener la información de los estudiantes", error);
    }
  };

  useEffect(() => {
    obtainStudentsInfo();
  }, [value]);
  const status = transformedCourses.map((course) => ({
    value: course.id,
    label: course.name,
  }));

  const userRoleButtons = () => {
    if (
      user_role === "Dueño" ||
      user_role === "Admin" ||
      user_role === "Mod"
    ) {
      return (
        <>
          <Grid item md={1.5} xs={12}>
            <Button
              fullWidth={true}
              size="large"
              variant="contained"
              endIcon={<EditIcon />}
              color="secondary"
              onClick={handleEditOpen}
            >
              Editar
            </Button>
          </Grid>
          <Grid item md={1.5} xs={12}>
            <Button
              fullWidth={true}
              size="large"
              variant="contained"
              endIcon={<DeleteIcon />}
              color="error"
              onClick={handleDeleteOpen}
            >
              Eliminar
            </Button>
          </Grid>
          <Grid item lg={6} md={6} sm={6} xs={12}>
            <Button
              fullWidth={true}
              size="large"
              variant="contained"
              endIcon={<AddIcon />}
              onClick={handleDialogOpen}
            >
              Nuevo Curso
            </Button>
          </Grid>
        </>
      );
    } else if (user_role === "Profesor") {
      return (
        <Grid item md={1.5} xs={12}>
          <Button
            fullWidth={true}
            size="large"
            variant="contained"
            endIcon={<EditIcon />}
            color="secondary"
            onClick={handleEditOpen}
          >
            Editar
          </Button>
        </Grid>
      );
    } else {
      return null;
    }
  };

  return (
    <Grid container spacing={gridSpacing}>
      <Grid item xs={12}>
        <Grid container spacing={gridSpacing}>
          <Grid item md={3} xs={12}>
            <TextField
              fullWidth={true}
              id="standard-select-currency"
              select
              value={value}
              onChange={handleChange}
            >
              {status.map((option) => (
                <MenuItem
                  key={option.value}
                  value={option.value}
                >
                  {option.label}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          {userRoleButtons()}
        </Grid>
      </Grid>
      <Grid item xs={12}>
        <Grid container spacing={gridSpacing}>
          <Grid item lg={6} md={6} sm={6} xs={12}>
            <EarningCard
              isLoading={isLoading}
              totalAsistencia={totalAsistencia}
            />
          </Grid>
          <Grid item lg={6} md={6} sm={6} xs={12}>
            <TotalOrderLineChartCard
              isLoading={isLoading}
              asistenciaPorClase={asistenciaPorClaseCount}
            />
          </Grid>
        </Grid>
      </Grid>
      <Grid item xs={12}>
        <Grid container spacing={gridSpacing}>
          <Grid item xs={12} md={7}>
          </Grid>
          <Grid item xs={12} md={5}>


            {/* <PopularCard isLoading={isLoading} /> */}
          </Grid>
        </Grid>
      </Grid>
    </Grid>
  );
};

export default Dashboard;
