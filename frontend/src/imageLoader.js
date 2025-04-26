import axios from 'axios';
import cornerstone from 'cornerstone-core';
import cornerstoneWebImageLoader from 'cornerstone-web-image-loader';

console.log('Axios importé:', axios); // Vérifie si axios est bien défini

export function initializeImageLoader() {
  console.log('Initialisation du chargeur d’images personnalisé');
  cornerstoneWebImageLoader.external.cornerstone = cornerstone;

  cornerstone.registerImageLoader('http', loadImageFromImageLoader);
  cornerstone.registerImageLoader('https', loadImageFromImageLoader);
}

function loadImageFromImageLoader(imageId) {
  console.log('loadImageFromImageLoader appelé avec imageId:', imageId);
  if (!imageId) {
    console.error('imageId invalide:', imageId);
    return Promise.reject(new Error('imageId invalide'));
  }

  const token = localStorage.getItem('access_token'); // Vérifie la clé correcte
  if (!token) {
    console.error('Token d’authentification manquant');
    return Promise.reject(new Error('Token d’authentification manquant'));
  }

  let promise;
  try {
    promise = axios.get(imageId, {
      responseType: 'arraybuffer',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    console.log('Promesse créée:', promise); // Vérifie si la promesse est créée
  } catch (error) {
    console.error('Erreur lors de la création de la requête Axios:', error);
    return Promise.reject(error);
  }

  if (!promise || typeof promise.then !== 'function') {
    console.error('Axios n’a pas retourné une promesse valide:', promise);
    return Promise.reject(new Error('Axios n’a pas retourné une promesse valide'));
  }

  return promise.then((response) => {
    console.log('Réponse Axios reçue pour imageId:', imageId);
    const arrayBuffer = response.data;
    const blob = new Blob([arrayBuffer], { type: 'image/png' });
    const imageUrl = URL.createObjectURL(blob);

    return new Promise((resolve, reject) => {
      const img = new Image();
      img.src = imageUrl;
      img.onload = () => {
        console.log('Image chargée:', imageId);
        const image = cornerstoneWebImageLoader.createImage(
          img,
          imageId,
          {
            width: img.width,
            height: img.height,
            columns: img.width,
            rows: img.height,
            data: arrayBuffer,
          }
        );
        resolve(image);
      };
      img.onerror = (err) => {
        console.error('Erreur chargement image:', err);
        URL.revokeObjectURL(imageUrl);
        reject(err);
      };
    });
  }).catch((error) => {
    console.error('Erreur Axios:', error);
    return Promise.reject(error);
  });
}