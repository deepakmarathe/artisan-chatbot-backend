
response=$(bash ../user/login.sh)
#{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTcyNDk1NTQ5Mn0.Y3YIxkLLtaOXMMR5sXN9wGn5jX2B-DoZ711wwQX9XDM","token_type":"bearer"}%
ACCESS_TOKEN=$(echo $response | jq -r '.access_token')

curl -X DELETE "http://localhost:8003/messages/1" -H "Authorization: Bearer $ACCESS_TOKEN"