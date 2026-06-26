"""예방 레이어 (Prevention Layer) v0.1.

흐름(추세·균형·조기신호·회복여력) 기반 예방 판단. 순간 위험(severity)과 별개 축이며
severity 를 import 하지 않고 값으로만 약한 참조한다(SPEC 3절).

구조(Unix 1모듈 1역할 + 규칙 정의/실행 분리):
  - models.py : 데이터 형태
  - rules.py  : 규칙 '정의'(상수) — DEFAULT_RULESET
  - engine.py : 규칙 '실행'(절차) — assess_prevention

공개 API:
  from app.services.prevention import assess_prevention, DEFAULT_RULESET
"""

from .engine import assess_prevention
from .models import (
    FlowAxis,
    HolisticState,
    PreventionAssessment,
    PreventionInput,
    PreventionReading,
    PreventionStatus,
)
from .rules import DEFAULT_RULESET, PreventionRuleSet

__all__ = [
    "assess_prevention",
    "DEFAULT_RULESET",
    "PreventionRuleSet",
    "PreventionInput",
    "PreventionReading",
    "PreventionAssessment",
    "PreventionStatus",
    "HolisticState",
    "FlowAxis",
]
