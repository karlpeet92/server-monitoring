const {VueLoaderPlugin} = require("vue-loader");
const path = require('path');
const Dotenv = require('dotenv-webpack');
module.exports = {
    mode: "production",
    resolve: {
        alias: {
            vue$: __dirname + '/node_modules/vue/dist/vue.common.js',
            '@': path.resolve('src')
        },
    },
    entry: {
        app: "./src/main.js"
    },

    output: {
        path: __dirname + "/../static/js/",
        filename: "[name].js"
    },
    module: {
        rules: [
            {
                test: /\.s(c|a)ss$/,
                use: [
                    'vue-style-loader',
                    'css-loader',
                    {
                        loader: 'sass-loader',
                        options: {
                            implementation: require('sass'),
                            fiber: require('fibers')
                        }
                    }
                ]
            },
            {
                test: /\.vue$/,
                use: 'vue-loader'
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader']
            },
            {
                test: /\.js$/,

                exclude: '/node_modules/',
                use: {
                    loader: 'babel-loader'
                }
            },
            {
                test: /\.html$/,
                exclude: /node_modules|public/,
                use: {loader: 'html-loader'}
            },
            {
                test: /\.(woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            name: '[name].[ext]',
                            outputPath: './static/js/fonts/',
                            publicPath: './static/js/fonts/'
                        }
                    }
                ]
            }
        ]
    },
    plugins: [
        new VueLoaderPlugin(),
        new Dotenv()
    ]
};