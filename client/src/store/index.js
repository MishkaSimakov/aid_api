import {createStore} from "vuex";
import companies from "./companies";
import ticker from "@/store/ticker";

export default new createStore({
    modules: {
        companies: companies,
        ticker: ticker
    }
});
