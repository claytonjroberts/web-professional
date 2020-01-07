import JQuery from 'jquery';
import $ from 'jquery';
import Bootstrap from 'bootstrap';
import _ from 'lodash';
import markdown from 'markdown';
import axios from 'axios';
import Vue from 'vue';
import VueAxios from 'vue-axios';
import VueScrollTo from 'vue-scrollto';
import VueMarkdown from 'vue-markdown';

Vue.use(VueScrollTo);
Vue.use(VueMarkdown);



window.Vue = Vue;
window.VueMarkdown = VueMarkdown;
window.$ = $;
window._ = _;


var showdown = require('showdown');
window.mdconverter = new showdown.Converter();

Vue.filter('from_markdown_to_html', function(val) {
    // Global filter function
    return mdconverter.makeHtml(val);
})

import "../styles/index.scss";
import "../templates/vue/test.vue";