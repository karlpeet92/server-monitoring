'use strict';
const {VueLoaderPlugin} = require('vue-loader');
const path = require('path');
module.exports = {
    mode: 'development',
    devtool: 'source-map',
    watch: true,
    watchOptions: {
        poll: true
      },
    resolve: {
        alias: {
            vue$: __dirname + '/node_modules/vue/dist/vue.common.js'
        },
        modules: [path.resolve(path.join(__dirname, 'node_modules'))]
    },
    entry: {
        app: path.resolve(path.join(__dirname, '/src/main.js'))
    },
    output: {
        path: path.resolve(path.join(__dirname, 'dist/js')),
        filename: '[name].min.js'
    },
    module: {
        rules: [
            {
                test: /\.(gif|png|jpe?g|svg)$/i,
                exclude: /fonts/ /* dont want svg fonts from fonts folder to be included */,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            name: '/img/[name].[ext]'
                        }
                    }
                ]
            },
            {
                test: /\.woff2?$|\.ttf$|\.eot|\.svg/,
                exclude: /img/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            name: '/fonts/[name].[ext]'
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
                test: /\.scss/,
                exclude: /node_modules/,
                use: [
                    // MiniCssExtractPlugin.loader,
                    {loader: 'css-loader', options: {sourceMap: true}},
                    //{loader: "postcss-loader", options: {}},
                    {loader: 'sass-loader', options: {sourceMap: true}}
                ]
            }
        ]
    },
    plugins: [
        new VueLoaderPlugin()
    ],
    externals: {
        jquery: 'jQuery',
        $: 'jQuery'
    }
};
