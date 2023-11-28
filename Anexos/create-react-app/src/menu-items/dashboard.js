// assets
import { IconDashboard } from '@tabler/icons';
import PhotoCameraFrontIcon from '@mui/icons-material/PhotoCameraFront';
import HomeIcon from '@mui/icons-material/Home';
import jwt from 'jwt-decode';

// constant
const icons = { IconDashboard, PhotoCameraFrontIcon, HomeIcon };

// ==============================|| DASHBOARD MENU ITEMS ||============================== //

let dashboard = {};

try {
  const token = jwt(localStorage.getItem("jwt"));
  if (token && token.user_role === "Alumno") {
    dashboard = {
      id: 'dashboard',
      title: 'Menú',
      type: 'group',
      children: [
        {
          id: 'inicio',
          title: 'Inicio',
          type: 'item',
          url: '/inicio',
          icon: icons.HomeIcon,
          breadcrumbs: false
        },
        {
          id: 'default',
          title: 'Dashboard',
          type: 'item',
          url: '/dashboard/default',
          icon: icons.IconDashboard,
          breadcrumbs: false
        }
      ]
    };
  } else {
    dashboard = {
      id: 'dashboard',
      title: 'Menú',
      type: 'group',
      children: [
        {
          id: 'inicio',
          title: 'Inicio',
          type: 'item',
          url: '/inicio',
          icon: icons.HomeIcon,
          breadcrumbs: false
        },
        {
          id: 'default',
          title: 'Dashboard',
          type: 'item',
          url: '/dashboard/default',
          icon: icons.IconDashboard,
          breadcrumbs: false
        },
        {
          id: 'camera',
          title: 'Camera',
          type: 'item',
          url: '/camera',
          icon: icons.PhotoCameraFrontIcon,
          breadcrumbs: false
        }
      ]
    };
  }
} catch (error) {
  dashboard = {};
}

export default dashboard;
