import {FinancialApi, TickerChartPeriod} from "@/api/api";

const state = {
    identifier: "",
    shortName: "",
    fullName: "",
    chartData: [],
    isLoading: true,
    indicators: [],
    selectedPeriod: TickerChartPeriod.YEAR
};

const getters = {
    imageURL(state) {
        return FinancialApi.getTickerImageURL(state.identifier);
    },
    preparedChartData(state) {
        return {
            datasets: [{
                data: state.chartData.map(candle => {
                    return {
                        x: candle.begin,
                        y: candle.open
                    }
                })
            }]
        };
    },
    preparedIndicatorsData(state) {
        let filteredIndicators = state.indicators.filter(
            indicator => indicator.verdict != null && indicator.value != null
        );

        return {
            buy: filteredIndicators.filter(indicator => indicator.verdict > 0),
            neutral: filteredIndicators.filter(indicator => indicator.verdict === 0),
            sell: filteredIndicators.filter(indicator => indicator.verdict < 0)
        }
    },
    notEnoughData(state) {
        return state.chartData.length < 10;
    }
};

const actions = {
    selectPeriod({state, dispatch}, period) {
        if (state.selectedPeriod === period) {
            return;
        }

        state.selectedPeriod = period;
        dispatch('fetchData');
    },
    fetchData({commit, state}) {
        commit('setLoadingState', true);

        FinancialApi.fetchTickerChart(state.identifier, state.selectedPeriod)
            .then(chartData => {
                commit('setChartData', chartData, state.selectedPeriod);
                commit('setLoadingState', false);
            })
            .catch(() => {
                commit('setLoadingState', false);
            });
    },
    fetchIndicatorsData({commit, state}) {
        commit('setLoadingState', true);

        FinancialApi.fetchTickerIndicators(state.identifier)
            .then(indicatorsData => {
                commit('setIndicatorsData', indicatorsData);
                commit('setLoadingState', false);
            })
            .catch(() => {
                commit('setLoadingState', false);
            });
    }
};

const mutations = {
    setIdentifier(state, identifier) {
        state.identifier = identifier;
    },
    setChartData(state, chartData) {
        state.chartData = chartData.items;
    },
    setLoadingState(state, isLoading) {
        state.isLoading = isLoading;
    },
    setIndicatorsData(state, indicatorsData) {
        state.shortName = indicatorsData.shortName;
        state.fullName = indicatorsData.fullName;
        state.indicators = [];

        Object.keys(indicatorsData.items).forEach(key => {
            state.indicators.push({
                id: key,
                ...indicatorsData.items[key]
            });
        });

        console.log(state.indicators);
    }
};

export default {
    namespaced: true,

    state,
    getters,
    actions,
    mutations
}
