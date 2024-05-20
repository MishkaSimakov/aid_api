import MainView from "@/views/MainView.vue";
import TickerView from "@/views/TickerView.vue";

import {createRouter, createWebHistory} from "vue-router";

const routes = [
    {path: '/', component: MainView},
    {path: '/tickers/:ticker', component: TickerView},
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router
