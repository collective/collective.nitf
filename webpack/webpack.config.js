var ExtractTextPlugin = require('extract-text-webpack-plugin');
module.exports = {
  entry: './app/nitf.js',
  output: {
    filename: 'nitf.js',
    path: __dirname + '/../src/collective/nitf/static',
    libraryTarget: 'umd',
    publicPath: '++resource++collective.nitf/',
    library: 'collective.nitf'
  },
  module: {
    rules: [{
      test: /\.js$/,
      exclude: /(\/node_modules\/|test\.js$|\.spec\.js$)/,
      use: 'babel-loader',
    }, {
      test: /\.less$/,
      exclude: /node_modules/,
      loader: ExtractTextPlugin.extract({
        fallback: 'style-loader',
        use: [
          {
            loader: 'css-loader',
            options: {
              importLoaders: 1
            }
          },
          'postcss-loader',
          'less-loader'
        ]
      })
    }, {
      test: /.*\.(gif|png|jpe?g)$/i,
      loaders: [
        'file-loader?name=[path][name].[ext]&context=app/',
        {
          loader: 'image-webpack-loader',
          query: {
            progressive: true,
            pngquant: {
              quality: '65-90',
              speed: 4
            },
            gifsicle: {
              interlaced: false
            },
            optipng: {
              optimizationLevel: 7
            }
          }
        }
      ]
    }, {
      test: /\.svg/,
      exclude: /node_modules/,
      use: 'svg-url-loader'
    }]
  },
  devtool: 'source-map',
  plugins: [
    new ExtractTextPlugin({
      filename: 'nitf.css',
      disable: false,
      allChunks: true
    })
  ]
}
