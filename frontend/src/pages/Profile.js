import { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { getPatientProfile, updatePatientProfile } from '../services/api';

const Profile = () => {
  const { register, handleSubmit, setValue, formState: { errors } } = useForm();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      setError('Veuillez vous connecter pour accéder à votre profil.');
      return;
    }

    const fetchProfile = async () => {
      setLoading(true);
      try {
        const response = await getPatientProfile();
        setProfile(response.data);
        // Pré-remplir le formulaire
        setValue('phone', response.data.phone);
        setValue('address', response.data.address);
        setValue('city', response.data.city);
        setValue('postal_code', response.data.postal_code);
        setValue('emergency_contact', response.data.emergency_contact);
        setValue('emergency_phone', response.data.emergency_phone);
      } catch (err) {
        setError('Erreur lors du chargement du profil.');
        console.error('Erreur Profile:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, [setValue]);

  const onSubmit = async (data) => {
    try {
      await updatePatientProfile(data);
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
      // Recharger le profil
      const response = await getPatientProfile();
      setProfile(response.data);
    } catch (err) {
      setError('Erreur lors de la mise à jour du profil.');
      console.error('Erreur mise à jour:', err);
    }
  };

  if (loading) return <div className="text-center">Chargement...</div>;
  if (error) return <div className="text-center text-red-500">{error}</div>;

  return (
    <div className="max-w-7xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Mon Profil</h1>
      {profile ? (
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Informations Personnelles</h2>
          <p><strong>Nom :</strong> {profile.user.first_name} {profile.user.last_name}</p>
          <p><strong>Date de naissance :</strong> {profile.date_of_birth}</p>
          <p><strong>Genre :</strong> {profile.gender === 'M' ? 'Masculin' : profile.gender === 'F' ? 'Féminin' : 'Autre'}</p>
          <h2 className="text-xl font-semibold mt-6 mb-4">Modifier les Informations</h2>
          <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4">
            <div>
              <label className="block text-sm font-medium">Téléphone</label>
              <input
                {...register('phone', { required: 'Ce champ est requis' })}
                className="mt-1 p-2 w-full border rounded"
              />
              {errors.phone && <p className="text-red-500 text-sm">{errors.phone.message}</p>}
            </div>
            <div>
              <label className="block text-sm font-medium">Adresse</label>
              <input
                {...register('address', { required: 'Ce champ est requis' })}
                className="mt-1 p-2 w-full border rounded"
              />
              {errors.address && <p className="text-red-500 text-sm">{errors.address.message}</p>}
            </div>
            <div>
              <label className="block text-sm font-medium">Ville</label>
              <input
                {...register('city', { required: 'Ce champ est requis' })}
                className="mt-1 p-2 w-full border rounded"
              />
              {errors.city && <p className="text-red-500 text-sm">{errors.city.message}</p>}
            </div>
            <div>
              <label className="block text-sm font-medium">Code postal</label>
              <input
                {...register('postal_code', { required: 'Ce champ est requis' })}
                className="mt-1 p-2 w-full border rounded"
              />
              {errors.postal_code && <p className="text-red-500 text-sm">{errors.postal_code.message}</p>}
            </div>
            <div>
              <label className="block text-sm font-medium">Contact d'urgence</label>
              <input
                {...register('emergency_contact')}
                className="mt-1 p-2 w-full border rounded"
              />
            </div>
            <div>
              <label className="block text-sm font-medium">Téléphone d'urgence</label>
              <input
                {...register('emergency_phone')}
                className="mt-1 p-2 w-full border rounded"
              />
            </div>
            <button
              type="submit"
              className="bg-blue-600 text-white p-2 rounded hover:bg-blue-700 w-48"
            >
              Mettre à jour
            </button>
          </form>
          {success && <p className="mt-2 text-green-500">Profil mis à jour avec succès !</p>}
        </div>
      ) : (
        <p>Aucun profil disponible.</p>
      )}
    </div>
  );
};

export default Profile;