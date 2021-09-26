# Corona-inzidenz

The microservice is running on Docker Droplet of cloud.digitalocean.com and uses docker image semenovalexander/corona-inzidenz (https://hub.docker.com/repository/docker/semenovalexander/corona-inzidenz)

## Data Usage
Data sources are https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html and https://infogram.com/coronafallzahlen2-1hdw2jwlnqxp4l0

# App Usage
to make the Telegram bot work, you will need the token. You can create a new bot using @BotFather. You will need a simple docker-compose.yml to fill the ENV (environmental variables) of Dockerfile. No addtional configuration needed. 
