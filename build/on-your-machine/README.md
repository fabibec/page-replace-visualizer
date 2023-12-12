## Run on your local machine

This section contains the ```docker-compose.yml``` file that is needed to run an instance of the website on your personal machine. 

#### Perquisites  
- [docker](https://docs.docker.com/compose/install/)
- [docker-compose](https://docs.docker.com/compose/install/)

#### Running
Get a copy of the ```docker-compose.yml``` file for example by using the wget command. 
The file uses port 8080 as default port, if you have another service running on your machine please change the host port. 
Then just execute 
```docker
docker compose up -d
```
to run the image