# Dockerfile for Cloud Native Korea Lab Mini Platform
# This file will be completed in the Dockerfile lab.

FROM node:20-alpine

WORKDIR /app

COPY app/package*.json ./
RUN npm install

COPY app/server.js ./

EXPOSE 3000

CMD ["npm", "start"]
