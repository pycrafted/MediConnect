import { NavLink } from 'react-router-dom';
import { HomeIcon, UserIcon, CalendarIcon, DocumentTextIcon, PhotoIcon } from '@heroicons/react/24/outline';

const Sidebar = ({ onLogout }) => {
  return (
    <div className="w-64 bg-gray-800 text-white h-screen p-4">
      <h2 className="text-2xl font-bold mb-6">MediConnect</h2>
      <nav>
        <NavLink
          to="/"
          className={({ isActive }) =>
            `flex items-center p-2 mb-2 rounded ${isActive ? 'bg-blue-600' : 'hover:bg-gray-700'}`
          }
        >
          <HomeIcon className="w-6 h-6 mr-2" />
          Tableau de bord
        </NavLink>
        <NavLink
          to="/profile"
          className={({ isActive }) =>
            `flex items-center p-2 mb-2 rounded ${isActive ? 'bg-blue-600' : 'hover:bg-gray-700'}`
          }
        >
          <UserIcon className="w-6 h-6 mr-2" />
          Profil
        </NavLink>
        <NavLink
          to="/appointments"
          className={({ isActive }) =>
            `flex items-center p-2 mb-2 rounded ${isActive ? 'bg-blue-600' : 'hover:bg-gray-700'}`
          }
        >
          <CalendarIcon className="w-6 h-6 mr-2" />
          Rendez-vous
        </NavLink>
        <NavLink
          to="/medical-record"
          className={({ isActive }) =>
            `flex items-center p-2 mb-2 rounded ${isActive ? 'bg-blue-600' : 'hover:bg-gray-700'}`
          }
        >
          <DocumentTextIcon className="w-6 h-6 mr-2" />
          Dossier médical
        </NavLink>
        <NavLink
          to="/dicom-viewer"
          className={({ isActive }) =>
            `flex items-center p-2 mb-2 rounded ${isActive ? 'bg-blue-600' : 'hover:bg-gray-700'}`
          }
        >
          <PhotoIcon className="w-6 h-6 mr-2" />
          Images DICOM
        </NavLink>
        <button
          onClick={onLogout}
          className="flex items-center p-2 mb-2 rounded w-full text-left hover:bg-gray-700"
        >
          <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
            />
          </svg>
          Se déconnecter
        </button>
      </nav>
    </div>
  );
};

export default Sidebar;