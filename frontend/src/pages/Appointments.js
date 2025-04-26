import { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { getAppointments, createAppointment } from '../services/api';
import axios from 'axios';

const Appointments = () => {
  const { register, handleSubmit, formState: { errors }, reset } = useForm();
  const [appointments, setAppointments] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      setError('Veuillez vous connecter pour voir vos rendez-vous.');
      return;
    }

    const fetchAppointments = async () => {
      setLoading(true);
      try {
        const response = await getAppointments();
        setAppointments(response.data);
      } catch (err) {
        setError('Erreur lors du chargement des rendez-vous.');
        console.error('Erreur Appointments:', err);
      } finally {
        setLoading(false);
      }
    };

    const fetchDoctors = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/doctors/', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setDoctors(response.data);
      } catch (err) {
        console.error('Erreur chargement médecins:', err);
        setError('Erreur lors du chargement des médecins.');
      }
    };

    fetchAppointments();
    fetchDoctors();
  }, []);

  const onSubmit = async (data) => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      setError('Veuillez vous connecter pour prendre un rendez-vous.');
      return;
    }

    try {
      await createAppointment({
        médecin: parseInt(data.médecin), // Assurer que l'ID est un entier
        date: data.date,
        reason: data.reason,
      });
      setSuccess(true);
      reset();
      setTimeout(() => setSuccess(false), 3000);
      const response = await getAppointments();
      setAppointments(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Erreur lors de la création du rendez-vous.');
      console.error('Erreur création RDV:', err);
    }
  };

  if (loading) return <div className="text-center">Chargement...</div>;
  if (error) return <div className="text-center text-red-500">{error}</div>;

  return (
    <div className="max-w-7xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Mes Rendez-vous</h1>
      <div className="bg-white p-6 rounded-lg shadow mb-6">
        <h2 className="text-xl font-semibold mb-4">Prendre un rendez-vous</h2>
        <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4">
          <div>
            <label className="block text-sm font-medium">Médecin</label>
            <select
              {...register('médecin', { required: 'Veuillez sélectionner un médecin' })}
              className="mt-1 p-2 w-full border rounded"
            >
              <option value="">Sélectionner un médecin</option>
              {doctors.map((doctor) => (
                <option key={doctor.id} value={doctor.id}>
                  Dr {doctor.user.first_name} {doctor.user.last_name} - {doctor.specialty}
                </option>
              ))}
            </select>
            {errors.médecin && <p className="text-red-500 text-sm">{errors.médecin.message}</p>}
          </div>
          <div>
            <label className="block text-sm font-medium">Date et heure</label>
            <input
              type="datetime-local"
              {...register('date', { required: 'Veuillez sélectionner une date' })}
              className="mt-1 p-2 w-full border rounded"
            />
            {errors.date && <p className="text-red-500 text-sm">{errors.date.message}</p>}
          </div>
          <div>
            <label className="block text-sm font-medium">Raison</label>
            <textarea
              {...register('reason', { required: 'Veuillez indiquer la raison' })}
              className="mt-1 p-2 w-full border rounded"
            />
            {errors.reason && <p className="text-red-500 text-sm">{errors.reason.message}</p>}
          </div>
          <button
            type="submit"
            className="bg-blue-600 text-white p-2 rounded hover:bg-blue-700 w-48"
          >
            Confirmer
          </button>
        </form>
        {success && <p className="mt-2 text-green-500">Rendez-vous créé avec succès !</p>}
      </div>
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

export default Appointments;