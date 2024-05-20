import {FinancialApi} from "@/api/api";
import {LoadingState} from "@/components/loading/LoadingState";
import {TickerChartPeriod} from "@/api/TickerChartPeriod";

const state = {
    identifier: "",
    shortName: "",
    fullName: "",
    chartData: [],
    chartLoadingState: LoadingState.READY_TO_LOAD,
    indicatorsLoadingState: LoadingState.READY_TO_LOAD,
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
                }),
                cubicInterpolationMode: 'monotone',
                tension: 0.4
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
        if (state.loadingState === LoadingState.LOADING) {
            return;
        }

        commit('setChartLoadingState', LoadingState.LOADING);

        FinancialApi.fetchTickerChart(state.identifier, state.selectedPeriod.alias)
            .then(chartData => {
                commit('setChartData', chartData);
                commit('setChartLoadingState', LoadingState.SUCCESS);
            })
            .catch(() => {
                commit('setChartLoadingState', LoadingState.ERROR);
            });
    },
    fetchIndicatorsData({commit, state}) {
        if (state.indicatorsLoadingState !== LoadingState.READY_TO_LOAD) {
            return;
        }

        commit('setIndicatorsLoadingState', LoadingState.LOADING);

        FinancialApi.fetchTickerIndicators(state.identifier)
            .then(indicatorsData => {
                commit('setIndicatorsData', indicatorsData);
                commit('setIndicatorsLoadingState', LoadingState.SUCCESS);
            })
            .catch(() => {
                commit('setIndicatorsLoadingState', LoadingState.ERROR);
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
    setChartLoadingState(state, isLoading) {
        state.chartLoadingState = isLoading;
    },
    setIndicatorsLoadingState(state, isLoading) {
        state.indicatorsLoadingState = isLoading;
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
    }
};

export default {
    namespaced: true,

    state,
    getters,
    actions,
    mutations
}
