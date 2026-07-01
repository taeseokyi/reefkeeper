# project-pump-timings

> "연동펌프 동작시간(초) — 헹굼·측정이송 모두 60/68, m1f80/m1b92(긴 호스)"

---

연동(peristaltic) 펌프 동작 시간 설정값 (`measure_kh_once.py` 기준, 단위 초):

| 동작 | forward | back(백) | 비고 |
|------|---------|----------|------|
| 헹굼 (KCl 스윕/참조 헹굼, m2/m4) | 60 | 68 | back +8 |
| 측정 이송 (채움/배출, m2/m4/m3) | 60 | 68 | back +8 |
| m1 (수조수, 호스 김) | 80 | 92 | back +12 |

**규칙:** back(백)이 forward보다 8초 길다. 호스가 긴 m1만 12초 길다.
**Why:** back을 더 길게 둬서 호스 안의 액체를 모두 비우기 위함. m1은 수조수 호스가 길어 더 김.
헹굼은 처음 30/38(반만 적심)이었으나, 측정컵을 완전히 적셔야 잔막이 헹궈지므로 채움과 동일한 60/68 풀 사이클로 변경(2026-06-14). m3 호스는 m2/m4와 길이 비슷.
**How to apply:** 펌프/호스 길이 바뀌면 이 값 조정. [project-measure-kh-script](project-measure-kh-script.md) [project-symmetric-kh-redesign](project-symmetric-kh-redesign.md)

주의: 2026-06-14 대화에서 사용자는 "m1b 90"이라 말했으나 "12초 깁니다" 규칙(80+12)과 코드는 모두 92. 92로 확정 가정.
