import React from 'react';
import { useNavigate } from 'react-router-dom';
import { API_BASE_URL } from 'config/apiConfig';
//Importaciones para la estetica:
import { useState } from 'react';
// material-ui
import { useTheme } from '@mui/material/styles';
import {
    Box,
    Button,
    Checkbox,
    FormControl,
    FormControlLabel,
    FormHelperText,
    Grid,
    IconButton,
    InputAdornment,
    InputLabel,
    OutlinedInput,
    Stack,
    Typography
} from '@mui/material';

// third party
import * as Yup from 'yup';
import { Formik } from 'formik';

// project imports
import useScriptRef from 'hooks/useScriptRef';
import AnimateButton from 'ui-component/extended/AnimateButton';

// assets
import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';



const AuthLogin = () => {
    const history = useNavigate();

    const theme = useTheme();
    const scriptedRef = useScriptRef();
    const [checked, setChecked] = useState(true);

    const handleLogin = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/login`);
            if (!response.ok) {
                throw new Error('No se pudo obtener la URL de autenticación');
            }
            const data = await response.json();
            window.location.href = data.authUrl;  // Redirige al usuario a Azure AD
        } catch (error) {
            console.error('Error al iniciar sesión:', error);
        }
    };


    return (
        <div>
            <Box sx={{ mt: 2 }}>
                <AnimateButton>
                    <Button onClick={handleLogin} fullWidth size="large" type="submit" variant="contained" color="secondary">
                    Iniciar Sesión con Azure AD
                    </Button>
                </AnimateButton>
            </Box>
        </div>
    );
};

export default AuthLogin;
