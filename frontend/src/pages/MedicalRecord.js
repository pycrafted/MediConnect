import { useEffect, useState } from 'react';
import { getMedicalRecord } from '../services/api';

const MedicalRecord = () => {
  const [record, setRecord] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRecord = async () => {
      try {
        const response = await getMedicalRecord();
        setRecord(response.data);
      } catch (err) {
        setError('Erreur lors du chargement du dossier médical.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchRecord();
  }, []);

  if (loading) return <div className="text-center">Chargement...</div>;
  if (error) return <div className="text-center text-red-500">{error}</div>;

  return (
    <div className="max-w-7xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Mon Dossier Médical</h1>
      {record ? (
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Informations Médicales</h2>
          <p><strong>Allergies :</strong> {record.allergies || 'Aucune'}</p>
          <p><strong>Médicaments actuels :</strong> {record.current_medications || 'Aucun'}</p>
          <p><strong>Conditions médicales :</strong> {record.medical_conditions || 'Aucune'}</p>
        </div>
      ) : (
        <p>Aucune information médicale disponible.</p>
      )}
    </div>
  );
};

export default MedicalRecord;