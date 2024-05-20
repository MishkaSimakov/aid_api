const API_URL = 'http://localhost:8000'

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
        return FinancialApi.fetchJSON('/api', {
            'category': 'ema100'
        });
    },

    fetchTickerChart(tickerName, period) {
        return FinancialApi.fetchJSON(`api/tickers/${tickerName}/chart`, {
            'period': period
        });
    },

    fetchTickerIndicators(tickerName) {
        return FinancialApi.fetchJSON(`api/tickers/${tickerName}/values`);
    },

    getTickerImageURL(tickerName) {
        return FinancialApi.getAbsoluteURL(`/images/${tickerName}.png`)
            .toString();
    },

    fetchCategories() {
        return FinancialApi.fetchJSON(`/api/categories`);
    }
};
