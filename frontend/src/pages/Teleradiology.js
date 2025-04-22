import React from 'react';
import DicomViewer from '../components/DicomViewer';
import { Container, Typography, Box } from '@mui/material';

const Teleradiology = () => {
  // URL de l'image DICOM via l'API Django avec barre oblique finale
  const imageId = 'wadouri:http://localhost:8000/api/orthanc/instances/1.2.826.0.1.3680043.8.1055.1.20111103111202067.15191801.69178937/file/';

  return (
    <Container maxWidth="lg" sx={{ padding: '20px', backgroundColor: '#f0f4f8', minHeight: '100vh' }}>
      <Typography variant="h4" color="#1e3a8a" gutterBottom>
        Plateforme de Télé-radiologie
      </Typography>
      <Box sx={{ display: 'flex', justifyContent: 'center', marginTop: '20px' }}>
        <DicomViewer imageId={imageId} />
      </Box>
    </Container>
  );
};

export default Teleradiology;