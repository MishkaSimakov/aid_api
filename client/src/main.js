import {createApp} from 'vue'
import App from './App.vue'

import "bootstrap/dist/css/bootstrap.min.css"
import "./scss/borders.scss"

import store from "@/store";
import router from "@/router";

createApp(App).use(store).use(router).mount('#app')
