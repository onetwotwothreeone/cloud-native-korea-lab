# GitHub Actions GHCR Push Lab

## 1. 실습 제목

Docker 이미지를 GitHub Container Registry에 push하기

## 2. 실습 목표

GitHub Actions에서 FastAPI 테스트가 통과하면 Docker 이미지를 자동으로 빌드하고 GitHub Container Registry에 push한다.

## 3. 전체 프로젝트에서의 역할

Cloud Native AI Docs Agent를 실제 클라우드 네이티브 방식으로 운영하려면 Docker 이미지를 이미지 저장소에 보관해야 한다.

이번 실습은 CI/CD 흐름 중 아래 단계에 해당한다.

```text
코드 변경
→ 자동 테스트
→ Docker 이미지 자동 빌드
→ GitHub Container Registry push
→ Kubernetes 배포
```

## 4. 사용한 이미지 이름

```text
ghcr.io/onetwotwothreeone/cnkl-fastapi-mini-platform:latest
ghcr.io/onetwotwothreeone/cnkl-fastapi-mini-platform:<commit-sha>
```

## 5. 추가한 핵심 설정

```yaml
permissions:
  contents: read
  packages: write
```

`packages: write`는 GitHub Actions가 GHCR에 Docker 이미지를 push할 수 있게 해주는 권한이다.

## 6. workflow 구조

```text
FastAPI CI
├── test-fastapi
└── build-and-push-docker-image
```

`build-and-push-docker-image` job은 `needs: test-fastapi`를 사용한다.

즉, 테스트가 성공해야 Docker 이미지 빌드와 GHCR push가 실행된다.

## 7. 실행한 명령어

```bash
cd ~/cloud-native-korea-lab

git add mini-platform/Dockerfile
git add .github/workflows/fastapi-ci.yml

git commit -m "Push FastAPI Docker image to GHCR"
git pull --rebase origin main
git push origin main
```

## 8. 성공 확인 결과

- GitHub Actions에서 `test-fastapi` 성공
- GitHub Actions에서 `build-and-push-docker-image` 성공
- Docker image build 성공
- GHCR push 성공
- GitHub Packages에서 `cnkl-fastapi-mini-platform` package 확인

## 9. 오늘 배운 점

1. GitHub Actions는 Docker 이미지를 빌드할 뿐 아니라 GHCR에 push할 수도 있다.
2. GHCR은 GitHub에서 Docker 이미지를 저장하는 Container Registry다.
3. `GITHUB_TOKEN`과 `packages: write` 권한으로 workflow repository와 연결된 package를 publish할 수 있다.
4. `latest` 태그는 최신 이미지를 가리킨다.
5. commit SHA 태그는 특정 커밋으로 만든 이미지를 추적할 수 있게 해준다.
6. 테스트가 통과한 이미지만 저장소에 올리면 배포 안정성이 좋아진다.

## 10. 다음 실습

Kubernetes manifest의 image 값을 GHCR 이미지로 변경한다.
