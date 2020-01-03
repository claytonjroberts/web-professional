var path = require('path');
var path = require('path');
var glob = require("glob");

const webpack = require('webpack');
const VueLoaderPlugin = require('vue-loader/lib/plugin')


// Get entry points for Vue files
// var entry_vue = {};
// glob.sync("./src/templates/vue/*.vue").reduce(function(obj,
//     x) {
//     console.log("obj", obj);
//     console.log("x", x);
//     entry_vue["vue_" + x.match(
//         /(?:\/)([A-z_]+)(?:\.vue)/)[1]] = x;
//     return;
// }, null);

// console.log(entry_vue);

module.exports = {
    mode: 'development',

    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js',
            // '@fortawesome/fontawesome-free$': '@fortawesome/fontawesome-free-solid/shakable.es.js'
        },
        extensions: ['*', '.js', '.vue', '.json']
    },

    entry: {
        "index": path.resolve(__dirname, 'src/scripts/index.js'),
    },
    output: {
        filename: '[name].js',
        // filename: (chunkData) => {     return chunkData.chunk.name === 'main' ?
        // '[name].js'         : '[name]/[name].js'; },
        path: path.resolve(__dirname, 'static/dist')
    },
    module: {
        rules: [{ test: /\.vue$/, use: 'vue-loader' },
            {
                test: /\.scss$/,
                use: [
                    "style-loader", // creates style nodes from JS strings
                    "css-loader", // translates CSS into CommonJS
                    "sass-loader", // compiles Sass to CSS, using Node Sass by default
                    // "url-loader",,,,,,,,,,,,,,,
                ]
            }, {
                test: /\.m?js$/,
                exclude: /(node_modules|bower_components)/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env']
                    }
                }
            }, {
                test: /\.less$/,
                loader: "less-loader",
            }, {
                test: /\.woff2?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                // Limiting the size of the woff fonts breaks font-awesome ONLY for the extract
                // text plugin loader: "url?limit=10000"
                loader: "url-loader"
            }, {
                test: /\.(ttf|eot|svg)(\?[\s\S]+)?$/,
                loader: 'file-loader'
            },
            // {     test: /\.woff2?(\?v=[0-9]\.[0-9]\.[0-9])?$/,      Limiting the size of
            // the woff fonts breaks font-awesome ONLY for the extract text plugin loader:
            // "url?limit=10000"     loader: "url-loader" }, {     test:
            // /\.(ttf|eot|svg)(\?[\s\S]+)?$/,     loader: 'file-loader' },  {      test:
            // /\.woff2?(\?v=[0-9]\.[0-9]\.[0-9])?$/,       Limiting the size of the woff
            // fonts breaks font-awesome ONLY for the extract text plugin       loader:
            // "url?limit=10000"      loader: "url-loader"  }, {     test:
            // /\.(ttf|eot|svg)(\?[\s\S]+)?$/,     loader: 'file-loader' }, {     test:
            // /(eot|woff|woff2|ttf|svg|png|jpe?g|gif)(\?\S*)?$/,     loader: 'url-loader',
            // use: {          loader: 'url-loader',          options: {              name:
            // '[name].[ext]',              outputPath: 'fonts/'          }      }
            // },,,,,,,,,,,,,,,
        ]
    },
    watchOptions: {
        ignored: /node_modules/
    },
    watch: true,

    plugins: [
        new VueLoaderPlugin(), new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            Vue: 'vue',
        })
    ],
    // optimization: {
    //     // We no not want to minimize our code.
    //     minimize: false
    // },
    // target: 'web',
    //
    // mode: slsw.lib.webpack.isLocal ? "development" : "production",

    // node: {
    //     fs: 'empty'
    //     // ^ Fixes can't resolve 'fs' when bundle with webpack error
    // }
    // node: { global: true, fs: 'empty' }
    node: {
        fs: 'empty'
    }

    // resolve: {     alias: {         'vue$': 'vue/dist/vue.esm.js'     },
    // extensions: ['*', '.js', '.vue', '.json'] },,,,,,,,,,,,,,,
};