#uvicorn main:app --reload --host 0.0.0.0 --port 8002 --log-level debug

#pip3.9 install -r requirements.txt
#sudo python3.9 -m pip install -r requirements.txt

# Replace <port_number> with the actual port number you want to check
#python3.9 chatbot/main.py

PORT=8000 
lsof -i :$PORT -t | xargs kill -9

uvicorn chatbot.main:app --reload --port $PORT --host 0.0.0.0 --log-level debug &
