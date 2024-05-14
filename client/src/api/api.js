const API_URL = 'http://localhost:8000'

const TickerChartPeriod = {
    HOUR: 'H',
    DAY: 'D',
    WEEK: 'W',
    MONTH: 'M',
    YEAR: 'Y',
    ALL_TIME: 'A'
}

export const FinancialApi = {
    getAbsoluteURL(relative_url) {
        return new URL(relative_url, API_URL);
    },

    fetch(url, method, payload = {}) {

        let absoluteUrl = FinancialApi.getAbsoluteURL(url);

        return fetch(absoluteUrl, {
            signal: AbortSignal.timeout(5000),
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
    },

    fetchJSON(url, payload) {
        return FinancialApi.fetch(url, 'POST', payload)
            .then(result => result.json());
    },

    fetchTickersData() {
        return FinancialApi.fetchJSON('/', {
            'category': 'ema100'
        });
    },

    fetchTickerChart(tickerName, period) {
        return FinancialApi.fetchJSON(`/tickers/${tickerName}/chart`, {
            'period': period
        });
    },

    fetchTickerIndicators(tickerName) {
        return FinancialApi.fetchJSON(`/tickers/${tickerName}/values`);
    },

    getTickerImageURL(tickerName) {
        return FinancialApi.getAbsoluteURL(`/images/${tickerName}.png`)
            .toString();
    },

    fetchCategories() {
        return FinancialApi.fetchJSON(`/categories`);
    }
};

export {TickerChartPeriod};
