
var webpack = require('webpack');
var path = require("path");
const ExtractTextWebpackPlugin = require("extract-text-webpack-plugin");



module.exports = {
    watch: true,
    entry: {
        'home': path.join(__dirname, 'main', 'project', 'core', 'blueprints', 'home', 'static', 'index.js'),
        'admin': path.join(__dirname, 'main', 'project', 'core', 'blueprints', 'admin', 'static', 'index.js')
    },
    output: {
        filename: '[name]_bundle.js',
        path: path.resolve(__dirname, 'main', 'project', 'core', 'static')
    },
    resolve: {
        "extensions": [".js", ".jsx", ".css"]
    },
    module: {
        rules: [
            {
                "test": /\.jsx?/,
                "exclude": "/node_modules/",
                loader: "babel-loader"
            },
            {
                "test": /\.css$/,
                use: ExtractTextWebpackPlugin.extract({
                    use: 'css-loader',
                    fallback: 'style-loader'
                })
            }
        ]
    },
    plugins: [
        new ExtractTextWebpackPlugin("[name]_bundle.css"),
    ],





};