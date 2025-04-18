import React, { useEffect } from 'react';
import { Container, Typography, Button } from '@mui/material';
import './App.css';

function App() {
  // Log pour vérifier que le composant est chargé
  useEffect(() => {
    console.log('[App.js] Composant App chargé');
    console.log('[App.js] Vérification environnement :', {
      nodeEnv: process.env.NODE_ENV,
      reactVersion: React.version,
    });
  }, []);

  return (
    <Container maxWidth="sm" style={{ marginTop: '2rem', textAlign: 'center' }}>
      <Typography variant="h4" color="primary" gutterBottom>
        Bienvenue sur MediConnect
      </Typography>
      <Typography variant="body1" color="textSecondary">
        Plateforme médicale pour la gestion des patients et des données DICOM.
      </Typography>
      <Button
        variant="contained"
        color="primary"
        style={{ marginTop: '1rem' }}
        onClick={() => {
          console.log('[App.js] Bouton Test cliqué');
          alert('Bouton de test cliqué !');
        }}
      >
        Test
      </Button>
    </Container>
  );
}

export default App;