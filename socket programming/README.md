# Socket programing 
run the server and client program:

	python server.py
	python client.py
	
and then proceed to run prometheus, remember to add the 8000 target to the targets in prometheus, the sample prometheus config file could be found here.

# Docker

use the files in the networking folder to build images and start the containers:
	docker-compose up -d --build