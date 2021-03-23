# RestApiEndpoint

The aim of this project is to provide service which keeps track game users' data by using provided endpoint.

### SETUP
- Python
- Redis
- Docker

##### Run Dockerized Services

The project uses custom backend and Redis services as docker containers. Run "docker-compose up" command in order to start containerized services.
-Note: "docker-compose down" command can be used for stop services.

### Usage

Client can sent RESTApi requests in JSON format in order to create new user, submit user's new score and get leaderboard or leaderboard by country. 
Example requests can be seen below:

GET localhost:5000 and GET localhost:5000/leaderboard
Response:
![image](https://user-images.githubusercontent.com/45763123/112211000-70920700-8c2c-11eb-9025-0da23fc5a143.png)

GET localhost:5000/{country_iso_code}
Response:
![image](https://user-images.githubusercontent.com/45763123/112211327-d2527100-8c2c-11eb-847b-eceb8537d541.png)

GET localhost:5000/user/profile/{guid}
Response:
![image](https://user-images.githubusercontent.com/45763123/112211841-54db3080-8c2d-11eb-97ff-c71a805c523a.png)

POST localhost:5000/score/submit  (Requires user id and score worth)
Response:
![image](https://user-images.githubusercontent.com/45763123/112212166-b3a0aa00-8c2d-11eb-8b6d-3c1cce825cd7.png)

POST localhost:5000/user/create (Requires country)
Response:
![image](https://user-images.githubusercontent.com/45763123/112211567-1c3b5700-8c2d-11eb-9b9d-010e8307f88f.png)

###PROJECT STRUCTURE

For Request
![image](https://user-images.githubusercontent.com/45763123/112214738-9a4d2d00-8c30-11eb-88c8-617f3b6e33ab.png)

For Response
![image](https://user-images.githubusercontent.com/45763123/112215960-07ad8d80-8c32-11eb-8f65-35ae09db2fa3.png)




