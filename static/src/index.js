import './index.scss';
import JQuery from 'jquery';
import $ from 'jquery';
import Bootstrap from 'bootstrap';
import Vue from 'vue';
import _ from 'lodash';
import markdown from 'markdown';
import axios from 'axios';
import VueAxios from 'vue-axios';
import VueScrollTo from 'vue-scrollto';
import VueMarkdown from 'vue-markdown';


// import FontAwesome from 'fontawesome-free';
// require("~@fortawesome/fontawesome-free/all.js");
// require("font-awesome-webpack"); require("font-awesome-loader");
// require("font-awesome-webpack"); import "font-awesome-loader"; import
// "font-awesome";

// import Vuex from 'vuex';
// import all from '@fortawesome/fontawesome-free/js/'
// require("~@fortawesome/fontawesome-free/js/all.js");

import showdown from 'showdown';
var mdconverter = new showdown.Converter();

// console.log(mdconverter.makeHtml("**hello**"));

Vue.filter('fromMarkdownToHTML', function(value) {
    return window.mdconverter.makeHtml(value);
});

Vue.use(VueScrollTo);
Vue.use(VueMarkdown);
Vue.use(VueAxios, axios);


window.$ = $;
window.jQuery = $;
window.Vue = Vue;
window.VueMarkdown = VueMarkdown;
window.VueScrollTo = VueScrollTo;
window.mdconverter = mdconverter;






// window.$ = $;
// import fontawesome; const Vue =
// require('node_modules/vue');
//