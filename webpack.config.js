const path = require('path');
const Dotenv = require('dotenv-webpack');

// Ruta de imágenes en .JS -> /static/assets/...
// Ruta de imágenes en .SCSS -> /aitenea_api/frontend/static/assets/...

module.exports = {
  entry: path.resolve(__dirname, 'aitenea_api/frontend/src/index.js'),
  watchOptions: {
    ignored: [
      '/node_modules/'
    ]
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader'
        }
      },
      {
        test: /\.(scss|sass|css)$/,
          use: [
            'style-loader',
            'css-loader',
            'resolve-url-loader',
            {
              loader: 'sass-loader',
              options: {
                sourceMap: true,  // <-- IMPORTANT!
              }
            }
          ]
      },
      {
        test: /\.(jpg|jpeg|png|gif|ico)$/,
        type: 'asset/resource'
      },
      {
        test: /\.(svg|ttf|eot|woff|woff2)$/,
        type: 'asset/resource'
      },

    ]
  },
  output: {
    path: path.resolve(__dirname, 'aitenea_api/frontend/static/build'),
    filename: '[name].bundle.js'
  },
  devtool: false,
  performance: {
    maxEntrypointSize: 10512000,
    maxAssetSize: 10512000
  },
  plugins: [
    new Dotenv({
      path: path.resolve(__dirname, '.env'), // load this now instead of the ones in '.env'
      safe: true, // load '.env.example' to verify the '.env' variables are all set. Can also be a string to a different file.
      systemvars: true, // load all the predefined 'process.env' variables which will trump anything local per dotenv specs.
      silent: true, // hide any errors
      defaults: false // load '.env.defaults' as the default values if empty.
    })
  ]
};
