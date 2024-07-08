all: stop start

clean:
	docker ps -a -q | docker rm 
	docker images -q | xargs docker rmi 

build:
	make -C SIPp
	make -C nginx

start:
	docker-compose up -d

stop:
	docker-compose down

full:
	make stop
	make -i clean
	make build
	make start
