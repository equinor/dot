FROM node:18.16.1-slim@sha256:02632fa826cdbdaa5fba25032bd2931fc79348c60110fefea2edf3fc480f39c5

COPY ./web /home/web
WORKDIR /home/web

RUN npm install

CMD ["npm", "start"]
