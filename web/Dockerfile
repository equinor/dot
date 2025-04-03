FROM node:20-alpine AS build

RUN mkdir -p /home/node/app/node_modules \
    && chown -R node:node /home/node/app
WORKDIR /home/node/app
COPY package*.json ./

RUN npm ci

COPY . .
RUN npm run build

FROM node:20-alpine AS deployment

RUN deluser --remove-home node \
    && addgroup -S node -g 1001 \
    && adduser -S -G node -u 1001 node

WORKDIR /home/node/app

COPY deployment .
RUN npm install

COPY --from=build /home/node/app/build ./build
RUN chown -R node:node /home/node/app/*
RUN chmod -R 755 /home/node/app/*

USER 1001
EXPOSE 3000

CMD ["node","app.js"]
