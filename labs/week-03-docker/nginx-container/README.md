# Docker Nginx Container Lab

## 실습 목표

MacBook에서 Docker Desktop 설치 상태를 확인하고, Nginx 컨테이너를 실행한 뒤 브라우저에서 접속한다.

## 실습 환경

- OS: macOS
- Device: MacBook
- Docker Desktop: 설치 완료
- Docker Engine: running
- Image: nginx:latest
- Port: 8080:80

## 실행 명령어

```bash
docker --version
docker info
docker run hello-world
docker run -d --name cnkl-nginx -p 8080:80 nginx:latest
docker ps
curl -I http://localhost:8080
docker logs cnkl-nginx
