const webpack = require('webpack');
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CssMinimizerWebpackPlugin = require('css-minimizer-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const WorkboxPlugin = require('workbox-webpack-plugin');
const config = require('./env.config');

const { NODE_ENV: env } = process.env;
const getFilename = filetype => `assets/[name].[contenthash].${filetype}`;

/* rules */
const scriptsRule = envConfig => ({
  exclude: /node_modules/,
  test: /\.(js|jsx)$/,
  type: 'javascript/auto',
  use: {
    loader: 'babel-loader',
    options: {
      presets: [
        ['@babel/preset-env'],
        ['@babel/preset-react', { development: envConfig.isDev }],
      ],
      plugins: [
        'babel-plugin-react-scoped-css',
      ],
    },
  },
});

const stylesRule = envConfig => ({
  test: /\.s?css$/i,
  type: 'javascript/auto',
  use: [
    !envConfig.isDev ? MiniCssExtractPlugin.loader : 'style-loader',
    'css-loader',
    'scoped-css-loader',
    'sass-loader',
  ],
});

const sourceMapsRule = envConfig => {
  if (!envConfig.isDev) {
    return {};
  }

  return {
    enforce: 'pre',
    exclude: /node_modules/,
    use: 'source-map-loader',
    test: /\.js$/,
  };
};

const imagesRule = {
  test: /\.(png|svg|jpe?g|gif|ico)$/i,
  type: 'asset/resource',
  generator: {
    filename: 'assets/images/[name][ext]',
  },
};

const fontsRule = {
  generator: {
    filename: 'assets/fonts/[name][ext]',
  },
  test: /\.(woff|woff2|eot|ttf|otf)$/i,
  type: 'asset/resource',
};

/* optimization */
const optimization = envConfig => {
  const result = {
    splitChunks: {
      chunks: 'all',
    },
    runtimeChunk: {
      name: 'runtime',
    },
  };

  if (!envConfig.isDev) {
    result.minimize = true;
    result.minimizer = [
      '...',
      new CssMinimizerWebpackPlugin(),
    ];
  }

  return result;
};

/* plugins */
const cleanWebpack = envConfig => new CleanWebpackPlugin({ verbose: !envConfig.isDev });
const extractHtml = envConfig => new HtmlWebpackPlugin({
  minify: !envConfig.isDev,
  meta: {
    description: envConfig.html.description,
    'theme-color': '#000000',
    viewport: 'width=device-width, initial-scale=1',
  },
  template: path.resolve(__dirname, 'src/assets/templates/index.html'),
  title: envConfig.html.title,
});
const includeAppDefinitions = envConfig => new webpack.DefinePlugin({
  ...Object.keys(envConfig.appDefinitions).reduce((acc, key) => {
    acc[key] = JSON.stringify(envConfig.appDefinitions[key]);

    return acc;
  }, {}),
  __BUILT_AT__: webpack.DefinePlugin.runtimeValue(
    Date.now,
    [path.resolve(__dirname, 'env.config.js')],
  ),
});
const extractCss = new MiniCssExtractPlugin({ filename: getFilename('css') });
const extractFiles = new CopyWebpackPlugin({ patterns: ['src/assets/public'] });

const envConfig = config(env);

module.exports = {
  entry: path.join(__dirname, 'src', 'index.jsx'),
  output: {
    filename: getFilename('js'),
    path: path.resolve(__dirname, 'dist'),
    publicPath: '/',
  },
  mode: envConfig.mode,
  module: {
    rules: [
      scriptsRule(envConfig),
      stylesRule(envConfig),
      sourceMapsRule(envConfig),
      imagesRule,
      fontsRule,
    ],
  },
  optimization: optimization(envConfig),
  plugins: [
    cleanWebpack(envConfig),
    includeAppDefinitions(envConfig),
    extractHtml(envConfig),
    extractCss,
    extractFiles,
    new WorkboxPlugin.GenerateSW({
      maximumFileSizeToCacheInBytes: 25_000_000,
      clientsClaim: true,
      skipWaiting: true,
    }),
  ],
  resolve: {
    extensions: ['.js', '.jsx'],
  },
  ...envConfig.isDev && { devtool: 'source-map' },
  devServer: {
    allowedHosts: 'all',
    historyApiFallback: true,
  },
};
