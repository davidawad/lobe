


curl -X GET "localhost:8000/messaging/fb_messenger"

curl -X POST 'localhost:8000/messaging/fb_messenger' -H "Content-Type: application/json" --data @../test/message_request.json
