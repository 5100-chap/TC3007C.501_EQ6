// assets
import { IconDashboard } from '@tabler/icons';
import PhotoCameraFrontIcon from '@mui/icons-material/PhotoCameraFront';
import HomeIcon from '@mui/icons-material/Home';

// constant
const icons = { IconDashboard,PhotoCameraFrontIcon, HomeIcon  };

// ==============================|| DASHBOARD MENU ITEMS ||============================== //

const dashboard = {
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

export default dashboard;
