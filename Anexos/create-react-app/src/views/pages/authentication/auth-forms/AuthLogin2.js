import React from 'react';
import {LOGIN_BASE_URL } from 'config/apiConfig';
import {
    Box,
    Button,
} from '@mui/material';


// project imports
import AnimateButton from 'ui-component/extended/AnimateButton';



const AuthLogin = () => {

    const handleLogin = async () => {
        try {
            const response = await fetch(`${LOGIN_BASE_URL}/login`);
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
