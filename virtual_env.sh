python3.9 -m venv .venv
source .venv/bin/activate
python3.9 -m pip install -r requirements.txt

#python3 -m pytest /Users/deepakmarathe/Documents/code/artisan/artisan-app-backend/tests/test_crud.py
python3.9 -m pytest tests/test_crud.py
