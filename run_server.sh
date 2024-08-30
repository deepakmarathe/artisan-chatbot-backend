
# Replace <port_number> with the actual port number you want to check
PORT=8000
# Find the process ID using the specified port
lsof -i :$PORT -t | xargs kill -9

PORT=8000
lsof -i :$PORT -t | xargs kill -9

nohup uvicorn chatbot.main:app --reload --port $PORT --host 0.0.0.0 --log-level debug  > server.log 2>&1 &
