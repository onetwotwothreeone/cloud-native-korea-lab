# 73. GWAN Portfolio Demo Script Execution Check

## 1. 실습 제목

GWAN Portfolio Demo Script Execution Check

## 2. 목적

이번 단계는 GWAN StatefulSet portfolio demo script가 실제로 실행 가능한지 확인하는 단계다.

목표는 PostgreSQL StatefulSet 마이그레이션을 실행하는 것이 아니다.

목표는 README와 demo script만 보고도 새로운 사람이 GWAN 데모 흐름을 따라갈 수 있는지 확인하는 것이다.

## 3. HYEAN / GWAN 맥락

HYEAN은 이동식 인간 거주지를 위한 생존형 우주 지능 서비스다.

GWAN은 HYEAN 내부에서 관측, 해석, 점수화, 판단, 기억을 담당하는 핵심 엔진이다.

이번 데모는 GWAN이 위험한 PostgreSQL 인프라 변경을 바로 실행하지 않고, 안전 조건을 먼저 확인한다는 것을 보여준다.

## 4. 실행한 명령어

cd ~/cloud-native-korea-lab/hyean-gwan/simulation-integration

pwd
git status

kubectl config current-context
kubectl get ns hyean-gwan

ls -l scripts/k8s/statefulset_portfolio_demo_script.sh
ls -l scripts/k8s/statefulset_portfolio_demo_readiness_report.sh

chmod +x scripts/k8s/statefulset_portfolio_demo_script.sh
chmod +x scripts/k8s/statefulset_portfolio_demo_readiness_report.sh

NAMESPACE=hyean-gwan ROOT="$PWD" ./scripts/k8s/statefulset_portfolio_demo_script.sh

cat .local/demo-reports/statefulset-portfolio-demo-script.md

## 5. 확인한 Kubernetes 상태

확인된 상태는 다음과 같다.

kubectl context: docker-desktop
namespace: hyean-gwan
deployment/gwan-api: available
deployment/postgres: available
pod/gwan-api: Running
pod/postgres: Running
service/gwan-api: exists
service/postgres: exists
persistentvolumeclaim/postgres-data: Bound
secret/gwan-postgres-secret: exists
configmap/gwan-api-config: exists

## 6. StatefulSet 안전 확인

현재 active PostgreSQL StatefulSet은 존재하지 않는다.

STATEFULSET_STATUS=NOT_CREATED

이는 정상이다.

이번 단계는 실제 마이그레이션 실행 단계가 아니라, 마이그레이션이 아직 차단되어 있는지 확인하는 단계다.

## 7. 승인 게이트 확인

최종 승인 게이트는 여전히 차단되어 있다.

CURRENT_DECISION=NO_GO
FINAL_DECISION=NO_GO
APPROVED_BY_OPERATOR=false
OPERATOR_FINAL_APPROVAL_STATUS=NOT_APPROVED
FINAL_APPROVAL_GATE_STATUS=BLOCKED

## 8. 마이그레이션 실행 여부

실제 마이그레이션은 실행되지 않았다.

MIGRATION_EXECUTION_ALLOWED=false
REAL_MIGRATION_EXECUTED=false
SECRET_VALUES_EXPORTED=false

이 결과는 안전하다.

DB 변경은 operator approval이 없으면 실행되면 안 된다.

## 9. 생성된 데모 리포트

아래 파일이 생성되었다.

.local/demo-reports/statefulset-portfolio-demo-script.md

이 파일은 포트폴리오 데모에서 설명할 수 있는 내용을 담고 있다.

핵심 메시지는 다음과 같다.

The important point is not that migration was executed.
The important point is that the system knows when not to execute.

## 10. 결과 해석

이번 검증은 성공이다.

성공 이유는 다음과 같다.

- demo script executed successfully
- Kubernetes resources were checked
- PostgreSQL remained Deployment + PVC
- active PostgreSQL StatefulSet was not created
- final approval gate remained blocked
- migration execution remained blocked
- Secret values were not exported
- portfolio demo report was created

## 11. 포트폴리오 의미

이 단계는 GWAN이 단순히 기능을 실행하는 시스템이 아니라, 위험한 인프라 변경을 안전하게 멈출 수 있는 예방형 운영 흐름을 갖고 있음을 보여준다.

HYEAN/GWAN의 핵심은 단순 자동화가 아니다.

중요한 것은 생존에 위험한 결정을 아무 때나 실행하지 않고, 조건과 승인 상태를 확인한 뒤 필요한 경우 멈추는 것이다.

## 12. 현재 결정

Step 73은 성공적으로 완료되었다.

현재 PostgreSQL은 여전히 Deployment + PVC 상태로 유지한다.

StatefulSet 마이그레이션은 아직 실행하지 않는다.

## 13. 다음 단계

다음 단계는 아래와 같다.

74. GWAN Portfolio Demo README Final Review

이 단계에서는 README와 demo report를 기준으로, 포트폴리오를 보는 사람이 GWAN의 목적과 Kubernetes 안전 설계를 쉽게 이해할 수 있는지 최종 점검한다.
