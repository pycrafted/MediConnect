import React, { useState } from 'react';
import axios from 'axios';

const DicomViewer = () => {
  const [file, setFile] = useState(null);
  const [imageUrl, setImageUrl] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setImageUrl(null); // Réinitialiser l'image
    setError(null); // Réinitialiser l'erreur
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      setError('Veuillez sélectionner un fichier DICOM');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const token = localStorage.getItem('access_token'); // Supposons que le token JWT est stocké ici
      const response = await axios.post('/api/orthanc/dicom-to-png/', formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
        responseType: 'blob', // Important pour recevoir une image binaire
      });

      // Créer une URL pour l'image
      const imageBlob = new Blob([response.data], { type: 'image/png' });
      const imageObjectUrl = URL.createObjectURL(imageBlob);
      setImageUrl(imageObjectUrl);
    } catch (err) {
      setError('tkt ca va finir par marché');
      console.error(err);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Visualiseur DICOM</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept=".dcm"
          onChange={handleFileChange}
        />
        <button type="submit">Convertir et afficher</button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {imageUrl && (
        <div>
          <h3>Image DICOM :</h3>
          <img src={imageUrl} alt="DICOM converted to PNG" style={{ maxWidth: '100%' }} />
        </div>
      )}
    </div>
  );
};

export default DicomViewer;