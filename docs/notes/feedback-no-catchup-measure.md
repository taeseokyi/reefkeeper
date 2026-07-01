# feedback-no-catchup-measure

> 밀린(놓친) KH 측정 보충은 불필요 — StartWhenAvailable 추가하지 말 것

---

Measure KH 작업에 **놓친 정시 측정의 보충(catch-up) 기능은 추가하지 않는다.** 사용자가 "밀린 것을 할 필요는 없다"고 명시.

즉 `StartWhenAvailable=true`를 추가하지 말 것. 노트북이 꺼져 있던 시간대의 측정 공백은 그대로 두고, 부팅·로그인 후 다음 정시부터 재개되는 현재 동작이 의도된 정상 상태.

**Why:** KH는 매시간 추세만 보면 되므로, 꺼져 있던 시간의 데이터 포인트를 굳이 메울 필요가 없다고 사용자가 판단.

**How to apply:** 시간별 스케줄 신뢰성 관련 질문/개선 시, catch-up(StartWhenAvailable)은 제안하지 않는다. 현재 트리거(매일 00:00 + PT1H/P1D, 절대 정시 고정)는 재부팅해도 스케줄이 안 깨지므로 그대로 유지. 관련: [project-windows-files](project-windows-files.md)
