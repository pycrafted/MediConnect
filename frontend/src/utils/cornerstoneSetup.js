import cornerstone from 'cornerstone-core';
import cornerstoneWADOImageLoader from 'cornerstone-wado-image-loader';
import dicomParser from 'dicom-parser';

// Configurer le chargeur d'images WADO
cornerstoneWADOImageLoader.external.cornerstone = cornerstone;
cornerstoneWADOImageLoader.external.dicomParser = dicomParser;

// Initialiser le chargeur
cornerstoneWADOImageLoader.configure({
  useWebWorkers: true,
});

export default cornerstone;