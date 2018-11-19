var path = require('path');


module.exports = {
    mode: 'development',

    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js'
        }
    },

    // context: path.resolve(__dirname, 'src'),
    // entry: './static/src/index.js',
    entry: path.resolve(__dirname, 'static/src/index.js'),
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'static/dist')
    },
    module: {
        rules: [{
                test: /\.scss$/,
                use: [
                    "style-loader", // creates style nodes from JS strings
                    "css-loader", // translates CSS into CommonJS
                    "sass-loader" // compiles Sass to CSS, using Node Sass by default
                ]

            },
            {
                test: /\.m?js$/,
                exclude: /(node_modules|bower_components)/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env']
                    }
                }
            },
            {
                test: /\.(eot|svg|ttf|woff|woff2)$/,
                use: {
                    loader: 'url-loader',
                    options: {
                        name: '[name].[ext]',
                        outputPath: 'fonts/'
                    }
                }
            },

        ]
    },
    watchOptions: {
        ignored: /node_modules/
    },
    watch: true,

    // resolve: {
    //     alias: {
    //         'vue$': 'vue/dist/vue.esm.js'
    //     },
    //     extensions: ['*', '.js', '.vue', '.json']
    // },
};