#cd client
#npm run build
#cd ..

source .venv/bin/activate
pip install -r requirements/common.txt
flask --app server.py --debug run --port 8000