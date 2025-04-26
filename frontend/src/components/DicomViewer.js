import React, { useState, useEffect, useRef } from 'react';
import cornerstone from 'cornerstone-core';
import cornerstoneTools from 'cornerstone-tools';
import { getDicomImages, uploadDicomFile } from '../services/api';
import './DicomViewer.css';

// Importer cornerstoneWebImageLoader si tu utilises des images PNG
import cornerstoneWebImageLoader from 'cornerstone-web-image-loader';

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
    // Enregistrer le chargeur pour les images HTTP (PNG)
    cornerstoneWebImageLoader.external.cornerstone = cornerstone;
    cornerstone.registerImageLoader('http', (imageId) => {
      return new Promise((resolve, reject) => {
        const img = new Image();
        img.src = imageId;
        img.onload = () => {
          resolve(cornerstoneWebImageLoader.createImage(img, imageId));
        };
        img.onerror = (err) => {
          reject(err);
        };
      });
    });

    // Initialiser le visualiseur
    const element = dicomViewerRef.current;
    if (element) {
      cornerstone.enable(element);
    }

    // Charger les images DICOM
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

    // Nettoyage
    return () => {
      if (element) {
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

      // Recharger les images
      const imagesResponse = await getDicomImages();
      setImages(imagesResponse.data);

      // Afficher l’image uploadée avec Cornerstone
      const element = dicomViewerRef.current;
      if (element && instance_id) {
        const imageId = `http://127.0.0.1:8000/api/orthanc/dicom-to-png/?id=${instance_id}`;
        cornerstone.loadAndCacheImage(imageId).then((image) => {
          cornerstone.displayImage(element, image);
        }).catch((err) => {
          console.error('Erreur affichage Cornerstone:', err);
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
    const element = dicomViewerRef.current;
    if (element && instance_id) {
      const imageId = `http://127.0.0.1:8000/api/orthanc/dicom-to-png/?id=${instance_id}`;
      cornerstone.loadAndCacheImage(imageId).then((image) => {
        cornerstone.displayImage(element, image);
      }).catch((err) => {
        console.error('Erreur affichage Cornerstone:', err);
        setError('Erreur lors de l’affichage de l’image.');
      });
    }
  };

  return (
    <div className="dicom-viewer-container">
      <h2>Visualiseur DICOM</h2>

      {/* Formulaire d'upload */}
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

      {/* Visualiseur */}
      <div className="viewer-section">
        <h3>Image DICOM</h3>
        <div
          ref={dicomViewerRef}
          id="dicom-viewer"
          style={{ width: '512px', height: '512px', background: 'black' }}
        />
      </div>

      {/* Liste des images */}
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