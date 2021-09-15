const path = require('path');

const NodePolyfillPlugin = require("node-polyfill-webpack-plugin");

module.exports = {
  mode: 'development',
  entry: './src/my.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'static'),
  },
  plugins: [
    new NodePolyfillPlugin()
  ],
  resolve: {
    fallback: {
        "fs": false
    },
  }
};