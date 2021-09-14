const path = require('path');

module.exports = {
  mode: 'development',
  entry: './src/my.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'static'),
  }
};