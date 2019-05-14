import './index.scss';
import JQuery from 'jquery';
import Bootstrap from 'bootstrap';
import Vue from 'vue';
import _ from 'lodash';
// import FontAwesome from 'fontawesome-free';
// require("~@fortawesome/fontawesome-free/all.js");
// require("font-awesome-webpack"); require("font-awesome-loader");
// require("font-awesome-webpack"); import "font-awesome-loader"; import
// "font-awesome";
import VueScrollTo from 'vue-scrollto';
import VueMarkdown from 'vue-markdown';
import showdown from 'showdown';
var mdconverter = new showdown.Converter();
window.mdconverter = mdconverter;

// console.log(mdconverter.makeHtml("**hello**"));

Vue.filter('fromMarkdownToHTML', function(value) {
    return window.mdconverter.makeHtml(value);
});

Vue.use(VueScrollTo);
Vue.use(VueMarkdown);
window.Vue = Vue;
window.VueMarkdown = VueMarkdown;
// import Vuex from 'vuex'; Vue.use(Vuex) import fontawesome; const Vue =
// require('node_modules/vue');
//