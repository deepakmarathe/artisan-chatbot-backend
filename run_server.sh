# Find the process ID using the specified port
PORT=8000
lsof -i :$PORT -t | xargs kill -9

nohup uvicorn chatbot.main:app --reload --port $PORT --host 0.0.0.0 --log-level debug  > server.log 2>&1 &
