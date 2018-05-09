


curl -X GET "localhost:8000/messaging/fbmessenger"

curl -X POST 'localhost:8000/messaging/fbmessenger' -H "Content-Type: application/json" --data @../test/message_request.json
