# Corona infections tracking application

The microservice is running on Docker Droplet of cloud.digitalocean.com and uses docker image semenovalexander/corona-inzidenz (https://hub.docker.com/repository/docker/semenovalexander/corona-inzidenz)

## Data Usage
Data sources are https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html and https://infogram.com/coronafallzahlen2-1hdw2jwlnqxp4l0

# App Usage
to make the Telegram bot work, you will need the token. You can create a new bot using @BotFather. You will need a simple docker-compose.yml to fill the ENV (environmental variables) of Dockerfile. No addtional configuration needed. 

## Docker-compose
Here is how a docker-compose.yml can look like
```bash
version: '3'
services:
  corona-inzidenz:
    image: semenovalexander/corona-inzidenz:3
    environment:
      TOKEN: <yourtoken>
    restart: always
```

## Notice
The application is currently only privatly used. So, feel free to try it out on your own. I plan to improve the interface and usability for the bot interaction. After that, I will make it public in form of a telegram group. 