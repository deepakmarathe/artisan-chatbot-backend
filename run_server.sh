#uvicorn main:app --reload --host 0.0.0.0 --port 8002 --log-level debug

pip3.9 install -r requirements.txt

# Replace <port_number> with the actual port number you want to check
PORT=8003
# Find the process ID using the specified port
lsof -i :$PORT -t | xargs kill -9

python3.9 chatbot/main.py

uvicorn chatbot.main:app --reload --port 8003 --host 0.0.0.0 --log-level debug
