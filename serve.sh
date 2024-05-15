cd client
npm install
npm run build
cd ..

source .venv/bin/activate
pip install -r requirements/common.txt
flask --app server.py run --port 8000