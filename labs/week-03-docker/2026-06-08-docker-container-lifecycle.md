# Docker 컨테이너 상태 관리

## Date

2026-06-08

## Topic

Docker / Container Lifecycle

## Lab Title

Docker 컨테이너 상태 관리 실습

## Goal

Docker 컨테이너를 단순히 실행하는 것에서 끝내지 않고, 실행 상태를 확인하고, 멈추고, 다시 시작하고, 로그를 확인하고, 삭제하는 흐름을 익힌다.

이번 실습의 핵심은 컨테이너에도 생명주기가 있다는 것을 이해하는 것이다.

## Environment

- OS: macOS
- Device: MacBook
- Tool: Docker Desktop
- Terminal: zsh
- Cloud Provider: None

## Background

첫 번째 실습에서는 Docker로 Nginx 컨테이너를 실행하고 `localhost:8080`에서 정상 접속을 확인했다.

두 번째 실습에서는 실행된 컨테이너를 어떻게 관리하는지 확인했다.

쉽게 말하면 첫 번째 실습이 “컨테이너를 켜는 방법”이었다면, 이번 실습은 “컨테이너를 확인하고, 멈추고, 다시 켜고, 기록을 보고, 정리하는 방법”이다.

## Commands

### 1. 실행 중인 컨테이너 확인

```bash
docker ps
```

설명:
현재 실행 중인 컨테이너 목록을 확인한다.

### 2. 전체 컨테이너 확인

```bash
docker ps -a
```

설명:
실행 중인 컨테이너뿐 아니라 중지된 컨테이너까지 모두 확인한다.

### 3. 컨테이너 중지

```bash
docker stop 컨테이너이름
```

예시:

```bash
docker stop cloud-native-nginx
```

설명:
실행 중인 컨테이너를 멈춘다.

### 4. 컨테이너 다시 시작

```bash
docker start 컨테이너이름
```

예시:

```bash
docker start cloud-native-nginx
```

설명:
중지된 컨테이너를 다시 실행한다.

### 5. 컨테이너 로그 확인

```bash
docker logs 컨테이너이름
```

예시:

```bash
docker logs cloud-native-nginx
```

설명:
컨테이너 안에서 발생한 기록을 확인한다.

### 6. 컨테이너 삭제

```bash
docker rm 컨테이너이름
```

예시:

```bash
docker rm cloud-native-nginx
```

설명:
중지된 컨테이너를 삭제한다.

## Success Check

아래 흐름을 완료하면 성공으로 본다.

1. `docker ps`로 실행 중인 컨테이너를 확인했다.
2. `docker ps -a`로 전체 컨테이너 목록을 확인했다.
3. `docker stop`으로 컨테이너를 중지했다.
4. `docker start`로 컨테이너를 다시 실행했다.
5. `docker logs`로 컨테이너 로그를 확인했다.
6. `docker rm`으로 중지된 컨테이너를 삭제했다.

## Errors / Troubleshooting

이번 기록에서는 구체적인 에러 메시지를 별도로 남기지 않았다.

다만 초보자가 헷갈리기 쉬운 부분은 아래와 같다.

| 헷갈린 점 | 쉬운 설명 | 확인 방법 |
|---|---|---|
| `docker ps`와 `docker ps -a` 차이 | `docker ps`는 실행 중인 컨테이너만 보여주고, `docker ps -a`는 멈춘 컨테이너까지 보여준다. | 두 명령어를 각각 실행해 비교한다. |
| 실행 중인 컨테이너 삭제 | 실행 중인 컨테이너는 바로 삭제되지 않을 수 있다. 먼저 stop 후 rm 한다. | `docker stop 컨테이너이름` 후 `docker rm 컨테이너이름` 실행 |
| 로그 확인 시 이름 입력 | 컨테이너 이름이나 ID를 정확히 입력해야 한다. | `docker ps -a`로 이름 확인 |

## What I Learned

1. 컨테이너는 실행, 중지, 재시작, 삭제라는 생명주기를 가진다.
2. `docker ps`는 현재 실행 중인 컨테이너를 확인하는 명령어다.
3. `docker ps -a`는 중지된 컨테이너까지 포함해 전체 컨테이너를 확인하는 명령어다.
4. `docker logs`는 컨테이너 내부에서 발생한 기록을 확인할 때 사용한다.
5. 컨테이너를 삭제하기 전에는 먼저 중지 상태인지 확인하는 습관이 필요하다.

## Related Concepts

- Docker
- Container
- Container Lifecycle
- Process
- Log
- Port
- Nginx
- Kubernetes Pod

## Connection to Kubernetes

Docker에서 컨테이너의 상태를 확인하고 관리하는 경험은 Kubernetes의 Pod를 이해하는 기초가 된다.

Docker에서는 사용자가 직접 `docker stop`, `docker start`를 실행하지만, Kubernetes에서는 Deployment와 Controller가 Pod 상태를 감시하고 원하는 상태로 유지하려고 한다.

즉, 이번 실습은 나중에 Kubernetes의 Pod, Deployment, ReplicaSet을 이해하기 위한 기초 실습이다.

## Community Post Summary

[오늘의 클라우드 네이티브] Docker 컨테이너 상태 관리

오늘은 Docker 컨테이너를 실행한 뒤, 그 컨테이너를 확인하고, 멈추고, 다시 시작하고, 로그를 확인하고, 삭제하는 방법을 실습했다.

오늘 사용한 명령어는 `docker ps`, `docker ps -a`, `docker stop`, `docker start`, `docker logs`, `docker rm`이다.

핵심은 컨테이너도 실행 상태를 계속 관리해야 한다는 점이다.

질문:
Docker를 처음 배울 때 `docker ps`와 `docker ps -a`의 차이가 헷갈리셨나요?

## Next Lab

다음 실습 주제는 Docker 이미지 관리다.

다음 실습에서 다룰 명령어:

```bash
docker images
docker pull nginx
docker image inspect nginx
docker rmi 이미지ID
```

다음 실습의 핵심 질문:

이미지와 컨테이너는 무엇이 다를까?
