import { useEffect, useState } from 'react';
import { getPatientProfile, getAppointments } from '../services/api';

const Dashboard = () => {
  const [profile, setProfile] = useState(null);
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      setError('Veuillez vous connecter pour accéder au tableau de bord.');
      return;
    }

    const fetchData = async () => {
      setLoading(true);
      try {
        const profileResponse = await getPatientProfile();
        setProfile(profileResponse.data);
        const appointmentsResponse = await getAppointments();
        setAppointments(appointmentsResponse.data);
      } catch (err) {
        setError('Erreur lors du chargement des données.');
        console.error('Erreur Dashboard:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div className="text-center">Chargement...</div>;
  if (error) return <div className="text-center text-red-500">{error}</div>;

  return (
    <div className="max-w-7xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Tableau de Bord</h1>
      {profile ? (
        <div className="bg-white p-6 rounded-lg shadow mb-6">
          <h2 className="text-xl font-semibold mb-4">Bienvenue, {profile.user.first_name} {profile.user.last_name}</h2>
          <p><strong>Date de naissance :</strong> {profile.date_of_birth}</p>
          <p><strong>Téléphone :</strong> {profile.phone}</p>
          <p><strong>Adresse :</strong> {profile.address}, {profile.city} {profile.postal_code}</p>
        </div>
      ) : (
        <p>Aucun profil disponible.</p>
      )}
      <div>
        <h2 className="text-xl font-semibold mb-4">Rendez-vous à venir</h2>
        {appointments.length > 0 ? (
          <div className="grid grid-cols-1 gap-4">
            {appointments.map((appt) => (
              <div key={appt.id} className="bg-white p-4 rounded-lg shadow">
                <p><strong>Date :</strong> {appt.date}</p>
                <p><strong>Médecin :</strong> {appt.médecin_display}</p>
                <p><strong>Raison :</strong> {appt.reason}</p>
              </div>
            ))}
          </div>
        ) : (
          <p>Aucun rendez-vous à venir.</p>
        )}
      </div>
    </div>
  );
};

export default Dashboard;