# FastAPI Mini Platform

Cloud Native Korea Lab의 `mini-platform`은 공식 문서 기반 **Cloud Native AI Docs Agent**로 발전시키기 위한 FastAPI 실습 프로젝트입니다.

이 README는 다른 컴퓨터에서도 프로젝트를 그대로 실행할 수 있도록 만든 **실행 안내서**입니다.

---

## 1. 이 프로젝트가 무엇인지

이 프로젝트의 목표는 작은 FastAPI 애플리케이션을 기준으로 클라우드 네이티브 운영 흐름을 단계적으로 실습하는 것입니다.

```text
FastAPI 앱 만들기
→ 로컬 Python 실행
→ Docker 이미지로 포장
→ Docker Compose로 로컬 컨테이너 실행
→ Kubernetes에 배포
→ Kustomize로 환경별 manifest 관리
→ GitHub Actions, GHCR, Argo CD, Monitoring, Terraform으로 확장
```

쉽게 말하면, 이 프로젝트는 **클라우드 네이티브를 배우기 위한 작은 실습용 기준 앱**입니다.

핵심 문장:

```text
클라우드 네이티브를 설명하는 AI를 클라우드 네이티브 방식으로 운영한다.
```

현재 단계에서는 실제 AI/RAG를 연결하기 전, FastAPI 기반 API와 운영 기반을 먼저 만듭니다.

---

## 2. 필요한 도구

다른 컴퓨터에서 실행하려면 아래 도구가 필요합니다.

| 도구 | 용도 |
| --- | --- |
| Git | GitHub 저장소를 복사하기 위해 사용 |
| Python 3.13 | FastAPI 앱을 로컬에서 실행 |
| pip | Python 패키지 설치 |
| Docker | 컨테이너 이미지 빌드와 실행 |
| Docker Compose | 여러 컨테이너 실행 구성을 관리 |
| kubectl | Kubernetes 클러스터에 배포 |
| Kubernetes Cluster | Docker Desktop Kubernetes, kind, minikube 등 |
| curl | API 정상 동작 확인 |

권장 버전:

```text
Python: 3.13.x
Docker Desktop: 최신 안정 버전
Kubernetes: Docker Desktop Kubernetes 또는 로컬 실습용 클러스터
```

설치 확인:

```bash
git --version
python --version
docker --version
docker compose version
kubectl version --client
```

Mac에서 `python` 명령어가 동작하지 않으면 아래 명령어를 사용합니다.

```bash
python3 --version
```

---

## 3. 실행 전 준비

먼저 GitHub 저장소를 복사합니다.

```bash
git clone https://github.com/onetwotwothreeone/cloud-native-korea-lab.git
cd cloud-native-korea-lab/mini-platform
```

현재 폴더가 `mini-platform`인지 확인합니다.

```bash
pwd
ls
```

정상이라면 대략 아래 파일들이 보여야 합니다.

```text
README.md
app
compose
k8s
tests
Dockerfile
requirements.txt
pytest.ini
```

프로젝트 구조:

```text
mini-platform
├── README.md
├── app
│   ├── __init__.py
│   └── main.py
├── tests
│   └── test_main.py
├── requirements.txt
├── pytest.ini
├── Dockerfile
├── .dockerignore
├── compose
│   └── docker-compose.yml
└── k8s
    ├── base
    │   ├── kustomization.yaml
    │   ├── deployment.yaml
    │   └── service.yaml
    └── overlays
        └── dev
            └── kustomization.yaml
```

---

## 4. 로컬 Python 실행 방법

이 방식은 Docker 없이 Python으로 직접 앱을 실행하는 방법입니다.

### 4-1. 가상환경 생성

macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

만약 `python` 명령어가 안 되면:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4-2. 패키지 설치

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4-3. FastAPI 앱 실행

```bash
uvicorn app.main:app --reload
```

정상 실행되면 기본 주소는 아래와 같습니다.

```text
http://localhost:8000
```

확인:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/version
```

예상 결과:

```json
{"status":"ok"}
```

```json
{"version":"0.1.0","language":"Python","framework":"FastAPI"}
```

FastAPI 자동 문서:

```text
http://localhost:8000/docs
```

---

## 5. Docker 실행 방법

이 방식은 FastAPI 앱을 Docker 이미지로 만든 뒤 컨테이너로 실행하는 방법입니다.

쉽게 말하면, 앱과 실행 환경을 하나의 박스처럼 포장해서 실행합니다.

### 5-1. Docker 이미지 빌드

`mini-platform` 폴더에서 실행합니다.

```bash
docker build -t cnkl-fastapi-mini-platform:0.1.0 .
```

### 5-2. Docker 컨테이너 실행

```bash
docker run --rm --name cnkl-fastapi-mini-platform -p 8001:8000 cnkl-fastapi-mini-platform:0.1.0
```

여기서 포트 의미는 아래와 같습니다.

```text
내 컴퓨터 8001번 포트 → 컨테이너 내부 8000번 포트
```

확인:

```bash
curl http://localhost:8001/health
curl http://localhost:8001/version
```

---

## 6. Docker Compose 실행 방법

이 방식은 `compose/docker-compose.yml` 파일에 적힌 설정으로 컨테이너를 실행하는 방법입니다.

Docker Compose는 쉽게 말해 **컨테이너 실행 설명서**입니다.

`mini-platform` 폴더에서 실행합니다.

```bash
docker compose -f compose/docker-compose.yml up -d --build
```

실행 상태 확인:

```bash
docker compose -f compose/docker-compose.yml ps
```

로그 확인:

```bash
docker compose -f compose/docker-compose.yml logs -f
```

API 확인:

```bash
curl http://localhost:8001/health
```

종료:

```bash
docker compose -f compose/docker-compose.yml down
```

---

## 7. Kubernetes 실행 방법

이 방식은 FastAPI 앱을 Kubernetes에 직접 배포하는 방법입니다.

Kubernetes는 쉽게 말해 **컨테이너를 자동으로 관리하는 운영 관리자**입니다.

실행 전 Kubernetes 클러스터가 켜져 있어야 합니다.

확인:

```bash
kubectl config current-context
kubectl get nodes
```

### 7-1. 기본 manifest 배포

`mini-platform` 폴더에서 실행합니다.

```bash
kubectl apply -f k8s/base/deployment.yaml
kubectl apply -f k8s/base/service.yaml
```

### 7-2. 배포 상태 확인

```bash
kubectl get deployment
kubectl get pods
kubectl get service
```

또는 라벨 기준으로 확인합니다.

```bash
kubectl get deployment,pod,svc -l app=fastapi-mini-platform
```

### 7-3. 로컬에서 접속하기

Service는 기본적으로 `ClusterIP` 타입이라 클러스터 내부에서만 접근됩니다.

내 컴퓨터에서 확인하려면 `port-forward`를 사용합니다.

```bash
kubectl port-forward svc/fastapi-mini-platform-service 8001:80
```

새 터미널을 열고 확인합니다.

```bash
curl http://localhost:8001/health
curl http://localhost:8001/version
```

---

## 8. Kustomize 실행 방법

이 방식은 `k8s/base`의 공통 설정을 기준으로 `k8s/overlays/dev` 개발 환경 설정을 덧씌워 배포하는 방법입니다.

쉽게 말하면:

```text
base = 기본 김밥
overlay/dev = dev 토핑
final manifest = dev 환경용 완성 김밥
```

### 8-1. dev 환경 배포

`mini-platform` 폴더에서 실행합니다.

```bash
kubectl apply -k k8s/overlays/dev
```

### 8-2. dev 환경 리소스 확인

```bash
kubectl get deployment,pod,svc -l environment=dev
```

Kustomize dev 환경은 이름 뒤에 `-dev`가 붙습니다.

예시:

```text
fastapi-mini-platform-dev
fastapi-mini-platform-service-dev
```

### 8-3. dev 환경 접속 확인

```bash
kubectl port-forward svc/fastapi-mini-platform-service-dev 8001:80
```

새 터미널에서 확인합니다.

```bash
curl http://localhost:8001/health
curl http://localhost:8001/version
```

### 8-4. 실제 생성될 manifest 미리 보기

적용하기 전에 결과를 확인하고 싶으면 아래 명령어를 사용합니다.

```bash
kubectl kustomize k8s/overlays/dev
```

---

## 9. 테스트 실행 방법

이 프로젝트는 `pytest`로 FastAPI API를 테스트합니다.

### 9-1. 테스트 실행

`mini-platform` 폴더에서 실행합니다.

```bash
python -m pytest
```

### 9-2. 현재 테스트 대상

```text
GET  /health
GET  /version
POST /ask
```

정상이라면 아래처럼 테스트가 통과해야 합니다.

```text
3 passed
```

---

## 10. 정상 실행 확인 방법

실행 방식에 따라 포트가 다릅니다.

| 실행 방식 | 확인 주소 |
| --- | --- |
| 로컬 Python | http://localhost:8000 |
| Docker | http://localhost:8001 |
| Docker Compose | http://localhost:8001 |
| Kubernetes port-forward | http://localhost:8001 |
| Kustomize dev port-forward | http://localhost:8001 |

### 10-1. Health Check

```bash
curl http://localhost:8001/health
```

로컬 Python 실행이면 아래를 사용합니다.

```bash
curl http://localhost:8000/health
```

예상 결과:

```json
{"status":"ok"}
```

### 10-2. Version Check

```bash
curl http://localhost:8001/version
```

예상 결과:

```json
{"version":"0.1.0","language":"Python","framework":"FastAPI"}
```

### 10-3. Ask API Check

```bash
curl -X POST http://localhost:8001/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Kubernetes에서 Service는 왜 필요한가요?"}'
```

예상 결과에는 아래 필드가 포함됩니다.

```json
{
  "question": "Kubernetes에서 Service는 왜 필요한가요?",
  "answer": "아직 실제 AI/RAG는 연결하지 않았습니다. 현재는 Python FastAPI 기반 예시 응답입니다.",
  "source": "sample-response"
}
```

### 10-4. FastAPI 문서 확인

브라우저에서 확인합니다.

```text
http://localhost:8000/docs
```

Docker, Docker Compose, Kubernetes port-forward 사용 중이면:

```text
http://localhost:8001/docs
```

---

## 11. 자주 나는 에러

### 11-1. `python: command not found`

뜻:

```text
컴퓨터가 python 명령어를 찾지 못한다는 뜻입니다.
```

해결:

```bash
python3 --version
python3 -m venv .venv
```

또는 Python 3.13을 설치합니다.

---

### 11-2. `ModuleNotFoundError: No module named 'fastapi'`

뜻:

```text
FastAPI 패키지가 현재 Python 환경에 설치되어 있지 않다는 뜻입니다.
```

해결:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

### 11-3. `Address already in use`

뜻:

```text
이미 8000번 또는 8001번 포트를 다른 프로그램이 사용 중이라는 뜻입니다.
```

해결 방법 1: 사용 중인 프로세스 확인

```bash
lsof -i :8000
lsof -i :8001
```

해결 방법 2: 다른 포트 사용

```bash
uvicorn app.main:app --reload --port 8002
```

Docker에서는 포트 매핑을 바꿉니다.

```bash
docker run --rm -p 8002:8000 cnkl-fastapi-mini-platform:0.1.0
```

---

### 11-4. `Cannot connect to the Docker daemon`

뜻:

```text
Docker Desktop 또는 Docker daemon이 실행 중이 아니라는 뜻입니다.
```

해결:

```bash
docker info
```

Docker Desktop을 실행한 뒤 다시 시도합니다.

---

### 11-5. `kubectl` 연결 실패

예시:

```text
The connection to the server localhost:8080 was refused
```

뜻:

```text
kubectl이 연결할 Kubernetes 클러스터를 찾지 못했다는 뜻입니다.
```

확인:

```bash
kubectl config current-context
kubectl get nodes
```

해결:

Docker Desktop Kubernetes, kind, minikube 중 하나를 실행합니다.

---

### 11-6. `ImagePullBackOff`

뜻:

```text
Kubernetes가 컨테이너 이미지를 가져오지 못했다는 뜻입니다.
```

확인:

```bash
kubectl describe pod <pod-name>
```

가능한 원인:

```text
1. 이미지 이름이 틀림
2. 이미지 태그가 없음
3. GHCR 이미지가 private 상태임
4. 네트워크 문제로 이미지를 가져오지 못함
```

---

### 11-7. `services "fastapi-mini-platform-service" not found`

뜻:

```text
port-forward 하려는 Service 이름이 현재 클러스터에 없다는 뜻입니다.
```

확인:

```bash
kubectl get svc
```

주의:

```text
기본 Kubernetes 배포 Service 이름: fastapi-mini-platform-service
Kustomize dev 배포 Service 이름: fastapi-mini-platform-service-dev
```

---

## 12. 정리 명령어

실습 후 리소스를 정리할 때 사용합니다.

### 12-1. 로컬 Python 종료

터미널에서 실행 중인 `uvicorn`을 종료합니다.

```bash
Ctrl + C
```

가상환경 비활성화:

```bash
deactivate
```

---

### 12-2. Docker 컨테이너 정리

실행 중인 컨테이너 확인:

```bash
docker ps
```

컨테이너 중지:

```bash
docker stop cnkl-fastapi-mini-platform
```

이미지는 필요할 때만 삭제합니다.

```bash
docker image rm cnkl-fastapi-mini-platform:0.1.0
```

---

### 12-3. Docker Compose 정리

```bash
docker compose -f compose/docker-compose.yml down
```

---

### 12-4. Kubernetes 기본 배포 정리

```bash
kubectl delete -f k8s/base/service.yaml
kubectl delete -f k8s/base/deployment.yaml
```

---

### 12-5. Kustomize dev 배포 정리

```bash
kubectl delete -k k8s/overlays/dev
```

---

## Learning Connection

이 프로젝트에서 각 기술은 아래 역할을 합니다.

| 기술 | 이 프로젝트에서의 역할 |
| --- | --- |
| FastAPI | AI Docs Agent의 API 서버 |
| `/ask` | 사용자의 클라우드 네이티브 질문을 받는 입구 |
| `/health` | Docker, Kubernetes가 앱 상태를 확인하는 기준 |
| Docker | 앱을 어디서든 실행 가능한 이미지로 포장 |
| Docker Compose | 로컬 컨테이너 실행 설정 관리 |
| Kubernetes | 컨테이너 앱을 운영 환경처럼 배포하고 관리 |
| Kustomize | Kubernetes manifest를 환경별로 관리 |
| GitHub Actions | 테스트와 빌드를 자동화 |
| GHCR | Docker 이미지를 저장하는 GitHub Container Registry |
| Helm | Kubernetes 설정을 패키지화 |
| Argo CD | Git 기준으로 배포 상태 유지 |
| Prometheus / Grafana | 앱 상태 관찰 |
| Terraform | 클라우드 인프라를 코드로 관리 |

---

## Next Steps

앞으로 이 README는 실습이 추가될 때마다 함께 업데이트합니다.

다음 후보:

```text
1. GitHub Actions에서 GHCR push 결과 확인 방법 추가
2. Kubernetes image tag 업데이트 방법 추가
3. ConfigMap / Secret 실습 추가
4. Helm Chart 실행 방법 추가
5. Argo CD 배포 방법 추가
6. Prometheus / Grafana 모니터링 방법 추가
7. Terraform으로 클라우드 인프라 생성 방법 추가
```

---

## Vision

FastAPI Mini Platform은 단순한 예제 앱이 아니라, 공식 문서 기반 Cloud Native AI Docs Agent로 발전하기 위한 시작점입니다.

이 프로젝트를 통해 클라우드 네이티브를 직접 실습하고, 그 과정을 한국어 교육 콘텐츠와 커뮤니티 자료로 전환합니다.
