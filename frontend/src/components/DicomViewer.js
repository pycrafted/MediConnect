import React, { useEffect, useRef } from 'react';
import cornerstone from '../utils/cornerstoneSetup';

const DicomViewer = ({ imageId }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const element = canvasRef.current;
    cornerstone.enable(element);

    cornerstone.loadImage(imageId).then((image) => {
      cornerstone.displayImage(element, image);
    }).catch((error) => {
      console.error('Erreur lors du chargement de l’image DICOM:', error);
    });

    return () => {
      cornerstone.disable(element);
    };
  }, [imageId]);

  return (
    <div>
      <div
        ref={canvasRef}
        style={{ width: '512px', height: '512px', background: 'black' }}
      />
    </div>
  );
};

export default DicomViewer;