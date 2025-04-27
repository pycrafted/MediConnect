import React, { useState, useEffect, useRef } from 'react';
import cornerstone from 'cornerstone-core';
import { getDicomImages, uploadDicomFile } from '../services/api';
import { initializeImageLoader } from '../imageLoader';
import './DicomViewer.css';

const DicomViewer = () => {
  const [images, setImages] = useState([]);
  const [file, setFile] = useState(null);
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const dicomViewerRef = useRef(null);

  // Initialiser Cornerstone et le chargeur d'images
  useEffect(() => {
    console.log('Initialisation de Cornerstone et du chargeur d’images');
    initializeImageLoader();

    const element = dicomViewerRef.current;
    if (element) {
      console.log('Activation du visualiseur Cornerstone');
      cornerstone.enable(element);
    } else {
      console.error('Élément visualiseur non trouvé');
    }

    const loadImages = async () => {
      console.log('Chargement des images DICOM...');
      try {
        const response = await getDicomImages();
        console.log('Images DICOM reçues:', response.data);
        setImages(response.data);
      } catch (err) {
        console.error('Erreur chargement images:', err);
        setError('Erreur lors du chargement des images DICOM.');
      }
    };
    loadImages();

    return () => {
      if (element) {
        console.log('Désactivation du visualiseur Cornerstone');
        cornerstone.disable(element);
      }
    };
  }, []);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError(null);
  };

  const handleDescriptionChange = (e) => {
    setDescription(e.target.value);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Veuillez sélectionner un fichier DICOM.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('description', description);

      const response = await uploadDicomFile(formData);
      console.log('Réponse upload:', response.data);
      const { instance_id } = response.data;

      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
      setFile(null);
      setDescription('');

      const imagesResponse = await getDicomImages();
      setImages(imagesResponse.data);

      const element = dicomViewerRef.current;
      if (element && instance_id) {
        const imageId = `http://127.0.0.1:8000/api/orthanc/images/${instance_id}/`;
        console.log('Tentative d’affichage image après upload:', imageId);
        cornerstone.loadAndCacheImage(imageId).then((image) => {
          console.log('Image affichée avec succès:', imageId);
          cornerstone.displayImage(element, image);
        }).catch((err) => {
          console.error('Erreur affichage Cornerstone après upload:', err);
          setError('Erreur lors de l’affichage de l’image.');
        });
      }
    } catch (err) {
      console.error('Erreur upload:', err);
      const errorMessage = err.response?.data?.error || 'Erreur lors de l’upload du fichier DICOM.';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const displayImage = (instance_id) => {
    console.log('Appel de displayImage avec instance_id:', instance_id);
    const element = dicomViewerRef.current;
    if (!element) {
      console.error('Élément visualiseur non trouvé');
      setError('Visualiseur non initialisé.');
      return;
    }
    if (!instance_id) {
      console.error('instance_id manquant');
      setError('ID de l’image manquant.');
      return;
    }

    const imageId = `http://127.0.0.1:8000/api/orthanc/images/${instance_id}/`;
    console.log('Chargement image avec imageId:', imageId);
    cornerstone.loadAndCacheImage(imageId)
      .then((image) => {
        console.log('Image chargée et affichée:', imageId);
        cornerstone.displayImage(element, image);
      })
      .catch((err) => {
        console.error('Erreur affichage Cornerstone:', err);
        setError('Erreur lors de l’affichage de l’image.');
      });
  };

  return (
    <div className="dicom-viewer-container">
      <h2>Visualiseur DICOM</h2>

      <form onSubmit={handleUpload} className="upload-form">
        <div className="form-group">
          <label htmlFor="file">Fichier DICOM :</label>
          <input
            type="file"
            id="file"
            accept=".dcm"
            onChange={handleFileChange}
          />
        </div>
        <div className="form-group">
          <label htmlFor="description">Description :</label>
          <textarea
            id="description"
            value={description}
            onChange={handleDescriptionChange}
            placeholder="Entrez une description (facultatif)"
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Chargement...' : 'Uploader'}
        </button>
      </form>

      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">Upload réussi !</div>}

      <div className="viewer-section">
        <h3>Image DICOM</h3>
        <div
          ref={dicomViewerRef}
          id="dicom-viewer"
          style={{ width: '512px', height: '512px', background: 'black' }}
        />
      </div>

      <div className="images-list">
        <h3>Mes Images DICOM</h3>
        {images.length === 0 ? (
          <p>Aucune image DICOM disponible.</p>
        ) : (
          <ul>
            {images.map((image) => (
              <li key={image.instance_id}>
                <p><strong>Date :</strong> {new Date(image.uploaded_at).toLocaleString()}</p>
                <p><strong>Patient :</strong> {image.patient_name}</p>
                <p><strong>Étude :</strong> {image.study_date}</p>
                <p><strong>Description :</strong> {image.description || 'Aucune'}</p>
                <button onClick={() => displayImage(image.instance_id)}>
                  Afficher
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default DicomViewer;