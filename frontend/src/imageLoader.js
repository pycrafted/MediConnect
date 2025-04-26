import cornerstone from 'cornerstone-core';
import cornerstoneWebImageLoader from 'cornerstone-web-image-loader';
import axios from 'axios';

export function initializeImageLoader() {
  console.log('Initialisation du chargeur d’images personnalisé');
  cornerstoneWebImageLoader.external.cornerstone = cornerstone;

  cornerstone.registerImageLoader('http', (imageId) => {
    console.log('loadImageFromImageLoader appelé avec imageId:', imageId);
    if (!imageId || !imageId.startsWith('http')) {
      console.error('imageId invalide:', imageId);
      return Promise.reject(new Error('imageId invalide'));
    }

    return new Promise((resolve, reject) => {
      axios
        .get(imageId, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
          responseType: 'blob',
        })
        .then((response) => {
          console.log('Réponse Axios reçue:', imageId);
          const blob = response.data;
          if (blob.type !== 'image/png') {
            console.error('Type de réponse inattendu:', blob.type);
            throw new Error('Réponse non-PNG reçue');
          }
          const imgUrl = URL.createObjectURL(blob);
          const img = new Image();
          img.src = imgUrl;
          img.onload = () => {
            console.log('Image chargée:', imageId);
            const image = cornerstoneWebImageLoader.createImage(img, imageId);
            resolve(image);
            URL.revokeObjectURL(imgUrl);
          };
          img.onerror = (err) => {
            console.error('Erreur chargement image:', err);
            reject(new Error(`Erreur chargement image: ${err.message}`));
            URL.revokeObjectURL(imgUrl);
          };
        })
        .catch((err) => {
          console.error('Erreur Axios:', err.message);
          reject(err);
        });
    });
  });
}