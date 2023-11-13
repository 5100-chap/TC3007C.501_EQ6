import { lazy } from 'react';
import { Navigate } from 'react-router-dom';
import { isJwtExpired } from "jwt-check-expiration"; // import the library
import { API_BASE_URL} from 'config/apiConfig';

// project imports
import MainLayout from 'layout/MainLayout';
import Loadable from 'ui-component/Loadable';

// dashboard routing
const DashboardDefault = Loadable(lazy(() => import('views/dashboard/Default')));
const CameraDefault = Loadable(lazy(() => import('views/camera')));
const InicioDefault = Loadable(lazy(() => import('views/inicio')));
// utilities routing
const UtilsTypography = Loadable(lazy(() => import('views/utilities/Typography')));
const UtilsColor = Loadable(lazy(() => import('views/utilities/Color')));
const UtilsShadow = Loadable(lazy(() => import('views/utilities/Shadow')));
const UtilsMaterialIcons = Loadable(lazy(() => import('views/utilities/MaterialIcons')));
const UtilsTablerIcons = Loadable(lazy(() => import('views/utilities/TablerIcons')));



const checkTokenValidity = (token) => {
  try {
    return isJwtExpired(token) ? false : true;
  } catch (error) {
    console.error("Invalid token provided");
    return false;
  }
};

// ==============================|| MAIN ROUTING ||============================== //

const MainRoutes = {

  path: '/',
  element: <MainLayout />,
  children: [
    {
      path: '/',
      element: <DashboardDefault />
    },
    {
      path: 'dashboard',
      children: [
        {
          path: 'default',
          element: checkTokenValidity(localStorage.getItem("jwt")) ? <DashboardDefault /> : <Navigate to="/login" />
        }
      ]
    },
    {
      path: 'camera',
      element: checkTokenValidity(localStorage.getItem("jwt")) ? <CameraDefault apiURL={API_BASE_URL + "/process_video"} /> : <Navigate to="/login" />
    },
    {
      path: 'inicio',
      element: checkTokenValidity(localStorage.getItem("jwt")) ? <InicioDefault /> : <Navigate to="/login" />
    },
    {
      path: 'utils',
      children: [
        {
          path: 'util-typography',
          element: checkTokenValidity(localStorage.getItem("jwt")) ? <UtilsTypography /> : <Navigate to="/login" />
        }
      ]
    },
    {
      path: 'utils',
      children: [
        {
          path: 'util-color',
          element: checkTokenValidity(localStorage.getItem("jwt")) ? <UtilsColor /> : <Navigate to="/login" />
        }
      ]
    },
    {
      path: 'utils',
      children: [
        {
          path: 'util-shadow',
          element: checkTokenValidity(localStorage.getItem("jwt")) ? <UtilsShadow /> : <Navigate to="/login" />
        }
      ]
    },
    {
      path: 'icons',
      children: [
        {
          path: 'tabler-icons',
          element: checkTokenValidity(localStorage.getItem("jwt")) ? <UtilsTablerIcons /> : <Navigate to="/login" />
        }
      ]
    },
    {
      path: 'icons',
      children: [
        {
          path: 'material-icons',
          element: checkTokenValidity(localStorage.getItem("jwt")) ? <UtilsMaterialIcons /> : <Navigate to="/login" />
        }
      ]
    }
  ]
};

export default MainRoutes;


