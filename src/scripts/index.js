import JQuery from 'jquery';
import $ from 'jquery';
import Bootstrap from 'bootstrap';
import _ from 'lodash';
import markdown from 'markdown';
import Vue from 'vue';
import VueScrollTo from 'vue-scrollto';
// import VueMarkdown from 'vue-markdown';

Object.defineProperty(Vue.prototype, '$_', { value: _ });
// See https://stackoverflow.com/questions/37694243/using-lodash-in-all-of-vue-component-template
// Above adds lodash to all Vue objects, accssable as this.$_

Vue.use(VueScrollTo);
// Vue.use(VueMarkdown);


window.Vue = Vue;
// window.VueMarkdown = VueMarkdown;
window.$ = $;
window._ = _;


var showdown = require('showdown');
window.mdconverter = new showdown.Converter();

Vue.filter('from_markdown_to_html', function(val) {
    // Global filter function
    return mdconverter.makeHtml(val);
})

import "../styles/index.scss";

import vue_exp from "../templates/vue/experience.vue";
import vue_skill from "../templates/vue/skill.vue";

Vue.component("exp", vue_exp);
Vue.component("skill", vue_skill);