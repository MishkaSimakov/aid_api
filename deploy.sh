# install all updates on server and restart website

source ~/aid/bin/activate
pip install -r requirements.txt
touch .restart-app

# calculate data for main page in case storage is empty
python3 <<HEREDOC
from moex_api.tickers_data_loader import tickers_data_loader
tickers_data_loader()
HEREDOC