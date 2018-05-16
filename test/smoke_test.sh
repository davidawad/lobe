#!/bin/bash
set -e

: '
This is a very quick smoke test to determine if the server is keeping basic functionality
Just a convenient tool for local development
'

curl -X GET "localhost:8000/messaging/fbmessenger"

printf "\\n"

curl -X POST 'localhost:8000/messaging/fbmessenger' -H "Content-Type: application/json" --data @../test/message_request.json
