import {FinancialApi} from "@/api/api";
import {LoadingState} from "@/components/loading/LoadingState";

const state = {
    tickers: {},
    indices: [],
    updated_at: Date.now(),
    postfix: "",

    loadingState: LoadingState.READY_TO_LOAD,
};

const getters = {};

const actions = {
    fetchData({commit, state}) {
        if (state.loadingState !== LoadingState.READY_TO_LOAD) {
            return;
        }

        commit('setLoadingState', LoadingState.LOADING);

        FinancialApi.fetchTickersData()
            .then(apiData => {
                commit('setApiData', apiData);
                commit('setLoadingState', LoadingState.SUCCESS);
            })
            .catch(error => {
                commit('setLoadingState', LoadingState.ERROR);
            });
    }
};

const mutations = {
    setApiData(state, apiData) {
        state.indices = Object.keys(apiData.indices).map(indexId => {
            return {
                id: indexId,
                name: apiData.indices[indexId].name,
            };
        });

        state.tickers = {};

        state.indices.forEach(index => {
            let tickers = apiData.indices[index.id].tickers;
            state.tickers[index.id] = [];

            Object.keys(tickers).forEach(tickerName => {
                let ticker = apiData.tickers[tickerName];
                if (ticker === undefined || ticker.value === null) {
                    return;
                }

                state.tickers[index.id].push({
                    name: tickerName,
                    value: apiData.tickers[tickerName].value,
                    index: index.id,
                    weight: tickers[tickerName]
                });
            });
        });

        state.updated_at = Date.parse(apiData.updated_at);
        state.postfix = apiData.postfix;
    },
    setLoadingState(state, loadingState) {
        state.loadingState = loadingState;
    }
};

export default {
    namespaced: true,

    state,
    getters,
    actions,
    mutations
}
