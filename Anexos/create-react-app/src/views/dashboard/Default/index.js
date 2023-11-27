import { useEffect, useState, useCallback, useMemo } from "react";
//import AddIcon from "@mui/icons-material/Add";
// material-ui
// project imports
import EarningCard from "./EarningCard";
//import PopularCard from './PopularCard';
import TotalOrderLineChartCard from "./TotalOrderLineChartCard";
//import TotalIncomeDarkCard from './TotalIncomeDarkCard';
//import TotalIncomeLightCard from './TotalIncomeLightCard';
import { gridSpacing } from "store/constant";
import {
  Grid,
  TextField,
  MenuItem,
  /*
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  */
} from "@mui/material";
import VirtualizedList from "./list";
/*
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
*/
import axios from "axios";
import jwt from "jwt-decode";
import { API_BASE_URL } from "config/apiConfig";
import React from "react";
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, LabelList, Legend } from "recharts";
// ==============================|| DEFAULT DASHBOARD ||============================== //
const Dashboard = () => {
  const [value, setValue] = useState(-1);
  const [isLoading, setLoading] = useState(true);
  const [courses, setCourses] = useState([]);
  const [transformedCourses, setTransformedCourses] = useState([]);
  const [user_role, setUser_role] = useState();
  const [totalAsistencia, setTotalAsistencia] = useState(["Sin datos"]);
  const [asistenciaPorClase, setAsistenciaPorClase] = useState("Sin datos");
  const [participacionPorClase, setParticipacionPorClase] =
    useState("Sin datos");
  const [numeroAlumnos, setNumeroAlumnos] = useState(0);
  const [alumnos, setAlumnos] = useState([]);
  const [numeroCurso, setNumeroCurso] = useState();
  const [asistenciaPorClaseCount, setAsistenciaPorClaseCount] =
    useState("Sin datos");
  const [selectedCourse, setSelectedCourse] = useState(null);
  const token = jwt(localStorage.getItem("jwt"));
  const [barChartData, setBarChartData] = useState([]);
  const [pieChartData, setPieChartData] = useState([]);
  const [mustUpdate, setMustUpdate] = useState(true);


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

  const fetchCourses = useCallback(async () => {
    try {
      // Decifrar el JWT almacenado en localStorage y obtener los valores necesarios
      // Realizar la solicitud POST a la API para obtener los cursos
      console.log(numeroAlumnos);
      console.log(asistenciaPorClaseCount);
      setUser_role(token.user_role);
      const response = await axios.post(`${API_BASE_URL}/obtain_clases_info`, {
        oid: token.oid,
        user_role: token.user_role,
      });
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
  }, [asistenciaPorClaseCount, courses, numeroAlumnos, setCourses, setNumeroCurso, setTransformedCourses, setLoading, token]);

  useEffect(() => {
    if (mustUpdate) {
      fetchCourses();
      setMustUpdate(false);
    }
  }, [fetchCourses, mustUpdate]);

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
        console.log(totalAsistencia);
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
        const asistenciaPorClaseCount1 = asistenciaPorClaseData.length;
        setAsistenciaPorClase(asistenciaPorClaseData);
        setAsistenciaPorClaseCount(asistenciaPorClaseCount1); // Guardar el conteo en una variable
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
  }, [numeroCurso, totalAsistencia]);

  useEffect(() => {
    const foundCourse = courses.find(course => course.id.toString() === numeroCurso);
    setSelectedCourse(foundCourse);
  }, [numeroCurso, courses]);
/*
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
*/
  const obtainStudentsInfo = useCallback(async () => {
    try {
      const token = jwt(localStorage.getItem("jwt"));
      var response;
      if (user_role === "Alumno") {
        response = await axios.post(
          `${API_BASE_URL}/obtain_students_info`,
          {
            type: "Courses",
            oid: token.oid,
            Clase: courses.find((course) => course.id === value)?.Nombre,
            Curso: courses.find((course) => course.id === value)?.NombreCurso,
          }
        );
      } else {
        response = await axios.post(
          `${API_BASE_URL}/obtain_students_info`,
          {
            type: "Courses",
            oid: false,
            Clase: courses.find((course) => course.id === value)?.Nombre,
            Curso: courses.find((course) => course.id === value)?.NombreCurso,
          }
        );
      }
      const students = response.data;
      setAlumnos(students);
      console.log(students);
    } catch (error) {
      console.error(
        "Error al obtener la información de los estudiantes",
        error
      );
    }
  }, [user_role, value, courses]);

  useEffect(() => {
    obtainStudentsInfo();
  }, [value, obtainStudentsInfo]);
  const status = transformedCourses.map((course) => ({
    value: course.id,
    label: course.name,
  }));
/*
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
*/
  const pieChartColors = useMemo(
    () => ["#8884d8", "#4997D0", "#ffc658", "#ff7f00", "#ff5500", "#006000", "#0090ff"],
    []
  );
  const processBarChartData = useCallback(() => {
    const today = new Date();
    const last7Days = new Set(); // Usar un Set para un acceso más eficiente

    // Crear un array con las fechas de los últimos 7 días
    for (let i = 0; i < 7; i++) {
      const date = new Date();
      date.setDate(today.getDate() - i);
      last7Days.add(date.toISOString().split('T')[0]);
    }

    const dailyParticipations = {}; // Para almacenar la cuenta de participaciones por día

    // Contar participaciones por día
    if (asistenciaPorClase !== 'Sin datos') {
      asistenciaPorClase.forEach(data => {
        const date = data[4].split('T')[0];
        if (last7Days.has(date)) {
          dailyParticipations[date] = (dailyParticipations[date] || 0) + 1;
        }
      });
    }

    // Crear el array de datos para el gráfico
    return Object.keys(dailyParticipations).map((date, index) => ({
      name: date, // Fecha de la participación
      participaciones: dailyParticipations[date], // Número total de participaciones ese día
      color: pieChartColors[index % pieChartColors.length] // Asignar un color del arreglo
    }));
  }, [asistenciaPorClase, pieChartColors]); 

  const processPieChartData = useCallback(() => {
    const participationTypesCount = {}; // Almacenar el conteo de participaciones por tipo

    // Contar participaciones por tipo
    if (participacionPorClase !== 'Sin datos') {
      participacionPorClase.forEach(data => {
        const tipo = data[3]; // Tipo de Participación
        participationTypesCount[tipo] = (participationTypesCount[tipo] || 0) + 1;
      });
    }

    // Convertir el objeto de conteo en un array para el gráfico
    return Object.keys(participationTypesCount).map((tipo, index) => ({
      name: tipo, // Tipo de participación
      value: participationTypesCount[tipo], // Número total de participaciones de ese tipo
      color: pieChartColors[index % pieChartColors.length] // Asignar un color del arreglo
    }));
  }, [participacionPorClase, pieChartColors]);


  useEffect(() => {
    setBarChartData(processBarChartData());
    setPieChartData(processPieChartData());
  }, [participacionPorClase, processBarChartData, processPieChartData]);

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
          {/*userRoleButtons()*/}
        </Grid>
      </Grid>
      <Grid item xs={12}>
        <Grid container spacing={gridSpacing}>
          <Grid item lg={6} md={6} sm={6} xs={12}>
            <EarningCard
              isLoading={isLoading}
              totalParticipacion={participacionPorClase}
            />
          </Grid>
          <Grid item lg={6} md={6} sm={6} xs={12}>
            <TotalOrderLineChartCard
              isLoading={isLoading}
              asistenciaPorClase={asistenciaPorClase}
              rol={user_role}
              courses={selectedCourse ? [selectedCourse] : []}
            />
          </Grid>
        </Grid>
      </Grid>
      {/* Nuevo Grid container para la lista y gráficos */}
      <Grid container item xs={12} spacing={gridSpacing}>

        {/* Grid item para la lista de estudiantes */}
        <Grid item xs={12} md={7}>
          <VirtualizedList data={alumnos} />
        </Grid>

        {/* Grid item para los gráficos */}
        <Grid item xs={12} md={5}>
          <Grid container spacing={gridSpacing}>

            {/* Gráfico de barras */}
            <Grid item xs={12}>
              <BarChart width={300} height={300} data={barChartData}>
                <Bar dataKey="participaciones" fill="#8884d8">
                  <LabelList dataKey="name" position="top" /> {/* Etiquetas de datos */}
                </Bar>
                <XAxis dataKey="name" />
                <YAxis />
                <Legend /> {/* Leyenda */}
              </BarChart>
            </Grid>

            {/* Gráfico de pastel */}
            <Grid item xs={12}>
              <PieChart width={300} height={350}>
                <Pie
                  dataKey="value"
                  data={pieChartData}
                  cx={200}
                  cy={200}
                  outerRadius={80}
                  label
                >
                  {pieChartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={pieChartColors[index % pieChartColors.length]} />
                  ))}
                </Pie>
                <Legend align="center" /> {/* Leyenda */}
              </PieChart>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Grid>


  );
};



export default Dashboard;

