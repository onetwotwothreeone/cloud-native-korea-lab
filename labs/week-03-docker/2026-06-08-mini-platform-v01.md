# Mini Platform v0.1 Lab

## Summary

Created a tiny Node.js web app for Cloud Native Korea Lab.

## Files

- mini-platform/package.json
- mini-platform/server.js

## Endpoints

- GET / : main page
- GET /health : app status check
- GET /version : app version check

## Commands

- node -v
- npm -v
- npm start
- curl http://localhost:3000/
- curl http://localhost:3000/health
- curl http://localhost:3000/version

## Result

The app runs locally on port 3000.

## Learning Points

1. A small Node.js server can become the base of a cloud native practice project.
2. Health check endpoints help platforms check whether the app is alive.
3. Version endpoints help verify deployments and trace problems.

## Next Lab

Containerize Mini Platform v0.1 with Docker.
