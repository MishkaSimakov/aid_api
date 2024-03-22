import json

from app.financial.ticker import Ticker


def test_main_page_returns_categories_data(client):
    response = client.post("/", data=json.dumps({"category": "profitability"}), headers={"Content-Type": "application/json"})
    assert response.status_code == 200
    assert len(response.json["items"]) != 0
    assert "SBER" in response.json["items"]
    assert "value" in response.json["items"]["SBER"]


def test_charts_page_returns_correctly(client):
    response = client.post("/tickers/SBER/chart", data=json.dumps({"period": "1H"}),
                           headers={"Content-Type": "application/json"})
    assert response.status_code == 200
    assert len(response.json["items"]) == 30
    assert "value" in response.json["items"][0]
    assert "begin" in response.json["items"][0]
    assert "end" in response.json["items"][0]


def test_values_page_returns_correctly(client):
    response = client.post("/tickers/SBER/values")
    assert response.status_code == 200

    assert response.json["ticker_full_name"] == "Сбербанк России ПАО ао"
    for category in Ticker.categories_list.keys():
        assert category in response.json["items"]
        assert "value" in response.json["items"][category]
        assert "postfix" in response.json["items"][category]
        assert "should_buy" in response.json["items"][category]
