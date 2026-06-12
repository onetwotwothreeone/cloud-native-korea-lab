# GitHub Actions Docker Image Build Lab

## 1. 실습 제목

GitHub Actions에서 FastAPI 테스트 통과 후 Docker 이미지 자동 빌드하기

## 2. 실습 목표

FastAPI Mini Platform의 테스트가 GitHub Actions에서 통과하면 Docker 이미지를 자동으로 빌드한다.

## 3. 전체 프로젝트에서의 역할

Cloud Native AI Docs Agent를 실제 클라우드 네이티브 방식으로 운영하려면 코드 변경 후 자동 테스트와 이미지 빌드가 필요하다.

이번 실습은 CI/CD 흐름 중 아래 단계에 해당한다.

```text
코드 변경
→ 자동 테스트
→ Docker 이미지 자동 빌드
→ 이미지 저장소 push
→ Kubernetes 배포
```

## 4. 추가한 workflow 구조

```text
FastAPI CI
├── test-fastapi
└── build-docker-image
```

## 5. 핵심 설정

```yaml
build-docker-image:
  runs-on: ubuntu-latest
  needs: test-fastapi
```

`needs: test-fastapi`는 테스트가 통과해야 Docker 이미지 빌드가 실행된다는 뜻이다.

쉽게 말하면 테스트가 실패하면 Docker 이미지 빌드는 실행되지 않는다.

## 6. 실행한 명령어

```bash
cd ~/cloud-native-korea-lab

git add .github/workflows/fastapi-ci.yml
git commit -m "Add Docker image build job to FastAPI CI"
git pull --rebase origin main
git push origin main
```

## 7. 성공 확인 결과

- GitHub Actions에서 `test-fastapi` 성공
- GitHub Actions에서 `build-docker-image` 성공
- `python -m pytest` 실행 확인
- `docker build -t cnkl-fastapi-mini-platform:ci .` 실행 확인
- FastAPI CI workflow 초록 체크 확인

## 8. 오늘 배운 점

1. GitHub Actions는 테스트뿐 아니라 Docker 이미지 빌드도 자동화할 수 있다.
2. `needs`를 사용하면 job 실행 순서를 정할 수 있다.
3. 테스트가 실패하면 Docker 이미지 빌드를 막을 수 있다.
4. CI/CD는 작은 자동화 단계를 하나씩 연결하면서 만들어진다.
5. 내 MacBook에서 직접 `docker build` 하지 않아도 GitHub가 Docker 이미지를 만들 수 있다.

## 9. 다음 실습

Docker 이미지를 GitHub Container Registry에 push한다.
