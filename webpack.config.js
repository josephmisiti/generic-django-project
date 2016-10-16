var path = require('path'),
    webpack = require('webpack');

var staticPath = path.join(__dirname, '{{cookiecutter.repo_name}}', 'static_local', 'src');
var buildPath = path.join(__dirname, '{{cookiecutter.repo_name}}', 'static_local', 'build');

var entry = {
    'bundle-app': path.join(staticPath, 'index.js'),
}

var config = {
    entry: entry,
    output: {
        path: buildPath,
        filename: '[name].js',
    },
    module: {
        loaders: [
            {
              test: /\.js$/,
              loader: 'babel-loader',
              include: staticPath,
              exclude: /(node_modules)/,
            },
        ]
    }
}

module.exports = config;
