import axios from 'axios';
import cornerstone from 'cornerstone-core';
import cornerstoneWebImageLoader from 'cornerstone-web-image-loader';

export function initializeImageLoader() {
  console.log('Initialisation du chargeur d’images personnalisé');
  cornerstoneWebImageLoader.external.cornerstone = cornerstone;

  cornerstone.registerImageLoader('http', loadImageFromImageLoader);
}

function loadImageFromImageLoader(imageId) {
  console.log('loadImageFromImageLoader appelé avec imageId:', imageId);
  if (!imageId) {
    console.error('imageId invalide:', imageId);
    return Promise.reject(new Error('imageId invalide'));
  }

  const token = localStorage.getItem('access_token');
  if (!token) {
    console.error('Token d’authentification manquant');
    return Promise.reject(new Error('Token d’authentification manquant'));
  }

  return axios
    .get(imageId, {
      responseType: 'arraybuffer',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
    .then((response) => {
      console.log('Réponse Axios reçue pour imageId:', imageId);
      const arrayBuffer = response.data;
      const blob = new Blob([arrayBuffer], { type: 'image/png' });
      const imageUrl = URL.createObjectURL(blob);

      return new Promise((resolve, reject) => {
        const img = new Image();
        img.src = imageUrl;

        img.onload = () => {
          console.log('Image chargée:', imageId);
          const image = {
            imageId: imageId,
            minPixelValue: 0,
            maxPixelValue: 255,
            slope: 1,
            intercept: 0,
            windowCenter: 127,
            windowWidth: 256,
            getPixelData: () => {
              const canvas = document.createElement('canvas');
              canvas.width = img.width;
              canvas.height = img.height;
              const ctx = canvas.getContext('2d');
              ctx.drawImage(img, 0, 0);
              const imageData = ctx.getImageData(0, 0, img.width, img.height);
              return imageData.data;
            },
            rows: img.height,
            columns: img.width,
            height: img.height,
            width: img.width,
            color: false,
            columnPixelSpacing: 1,
            rowPixelSpacing: 1,
            invert: false,
            sizeInBytes: arrayBuffer.byteLength,
          };
          URL.revokeObjectURL(imageUrl);
          resolve(image);
        };

        img.onerror = (err) => {
          console.error('Erreur lors du chargement de l’image:', err);
          URL.revokeObjectURL(imageUrl);
          reject(err);
        };
      });
    })
    .catch((error) => {
      console.error('Erreur Axios:', error);
      throw error;
    });
}