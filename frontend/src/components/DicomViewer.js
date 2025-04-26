import { useEffect, useState } from 'react';
import { getDicomImages, uploadDicomFile } from '../services/api';

const DicomViewer = () => {
  const [images, setImages] = useState([]);
  const [selectedImage, setSelectedImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      setError('Veuillez vous connecter pour voir vos images DICOM.');
      return;
    }

    const fetchImages = async () => {
      setLoading(true);
      try {
        const response = await getDicomImages();
        setImages(response.data || []);
      } catch (err) {
        console.error('Erreur DicomViewer:', err);
        setError('Aucune image DICOM trouvée ou erreur de connexion au serveur.');
        setImages([]); // Assurer que l'interface reste accessible
      } finally {
        setLoading(false);
      }
    };
    fetchImages();
  }, []);

  const handleFileUpload = async (event) => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      setError('Veuillez vous connecter pour uploader une image.');
      return;
    }

    const file = event.target.files[0];
    if (!file) {
      setError('Veuillez sélectionner un fichier DICOM.');
      return;
    }

    setLoading(true);
    try {
      const response = await uploadDicomFile(file);
      const imageUrl = URL.createObjectURL(new Blob([response.data], { type: 'image/png' }));
      setImages([...images, { id: `uploaded-${Date.now()}`, url: imageUrl }]);
      setSelectedImage(imageUrl);
      setSuccess(true);
      setError(null);
      setTimeout(() => setSuccess(false), 3000);
    } catch (err) {
      console.error('Erreur upload:', err);
      setError(err.response?.data?.error || 'Erreur lors de l’upload de l’image DICOM.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Visualiseur DICOM</h1>
      <div className="mb-6">
        <label className="block text-sm font-medium mb-2">Uploader une image DICOM</label>
        <input
          type="file"
          accept=".dcm"
          onChange={handleFileUpload}
          className="p-2 border rounded"
          disabled={loading}
        />
        {success && <p className="mt-2 text-green-500">Image uploadée avec succès !</p>}
        {error && <p className="mt-2 text-red-500">{error}</p>}
      </div>
      {loading && <div className="text-center">Chargement...</div>}
      <div className="flex gap-6">
        <div className="w-1/4">
          <h2 className="text-xl font-semibold mb-4">Images disponibles</h2>
          {images.length > 0 ? (
            <div className="grid grid-cols-1 gap-2">
              {images.map((img) => (
                <div
                  key={img.id}
                  className={`p-2 border rounded cursor-pointer ${selectedImage === img.url ? 'bg-blue-100' : ''}`}
                  onClick={() => setSelectedImage(img.url)}
                >
                  Image {img.id}
                </div>
              ))}
            </div>
          ) : (
            <p>Aucune image disponible.</p>
          )}
        </div>
        <div className="w-3/4">
          {selectedImage ? (
            // eslint-disable-next-line jsx-a11y/img-redundant-alt
            <img src={selectedImage} alt="DICOM" className="max-w-full h-auto" />
          ) : (
            <p>Sélectionnez une image pour l’afficher.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default DicomViewer;