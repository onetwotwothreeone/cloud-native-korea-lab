# Mini Platform v0.1 Docker Compose Lab

## 1. 실습 제목

Mini Platform v0.1을 Docker Compose로 실행하기

## 2. 실습 목표

긴 docker run 명령어 대신 docker-compose.yml 파일로 Mini Platform 실행 설정을 관리한다.

## 3. 사용한 파일

```text
mini-platform
├── app
│   ├── package.json
│   └── server.js
├── docker
│   └── Dockerfile
└── compose
    └── docker-compose.yml
