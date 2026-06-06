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

## Troubleshooting

이번 실습에서는 Docker 미설치, Docker Engine 상태, heredoc 입력 모드, Git 저장소 경로 문제를 경험했다.  
각 문제를 해결하면서 Docker CLI, Docker Engine, 컨테이너 포트 매핑, Git 저장소 구조를 함께 이해할 수 있었다.
