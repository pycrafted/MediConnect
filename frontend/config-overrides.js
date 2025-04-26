const { override } = require('customize-cra');

module.exports = override(
  (config) => {
    // Personnaliser les options du devServer
    config.devServer = {
      ...config.devServer,
      setupMiddlewares: (middlewares, devServer) => {
        if (!devServer) {
          throw new Error('WebpackDevServer is not configured');
        }
        // Ajouter des middlewares personnalisés si nécessaire
        return middlewares;
      },
    };
    return config;
  }
);