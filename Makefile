all:
		docker build -t lobe .

test:
		time curl -X GET  -H "Content-Type: application/json" -d '{"keyword":"murder"}' '0.0.0.0:8000/search'

run:
	docker run -p 8000:8000 lobe

