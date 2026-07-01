# 연구 노트 (측정 대장 참조용)

> 관련 문서: [측정 대장](../measurement-ledger.md) | [프로젝트 개요 (README)](../../README.md)

[측정 대장](../measurement-ledger.md) 본문에서 인용하는 세부 진단·검증 노트 모음이다. KH 측정 정확도를 다듬어 온 과정에서 나온 작업 메모를 시점 스냅샷으로 옮겨 놓았다 — 이후 실측으로 갱신되었을 수 있으니, 최신 결론은 항상 측정 대장 본문을 기준으로 본다.

- [feedback-no-catchup-measure](feedback-no-catchup-measure.md) — 밀린(놓친) KH 측정 보충은 불필요 — StartWhenAvailable 추가하지 말 것
- [feedback-one-change-at-a-time](feedback-one-change-at-a-time.md) — KH 측정 시스템 튜닝/실험은 한 번에 하나씩만 변경하고 효과 측정 후 다음으로
- [feedback-regression-test-simulator](feedback-regression-test-simulator.md) — measure_kh_once.py 등 측정/BT 로직 변경은 배포 전 항상 시뮬레이터(bin/test_measure_sim.py)로 회귀 검증
- [feedback-run-windows-py-from-wsl](feedback-run-windows-py-from-wsl.md) — WSL에서 Windows Python 스크립트(test_pump 등) 실행하는 정해진 방법 (-X utf8 필수)
- [feedback-validation-independent-replication](feedback-validation-independent-replication.md) — 보정(영점 등) 적용 전, 비독립 소표본을 독립 재현으로 검증 — 일정 vs 우연을 먼저 가른다
- [project-accuracy-target](project-accuracy-target.md) — KH 측정 목표 오차 = ±0.5 dKH 허용 / ±0.25 dKH 희망. 다일 널(n=13): 편향 −0.13 실재(σ0.061), 온도·KCl 원인 아님=액간전위. 목표는 여전히 충족
- [project-bt-rf-reconnect](project-bt-rf-reconnect.md) — HC-06 블루투스 SPP RF 순단 진단과 measure_kh_once.py 4계층 대응(연결확인·재연결·재시도·모터정지+keepalive)
- [project-dkh-temp-column-is-sealed-box](project-dkh-temp-column-is-sealed-box.md) — dkh.dat 온도 컬럼=밀폐 측정챔버 내부 수온(참조수·수조수 평형온도), 실제 메인 리프수조 수온의 대리값 아님
- [project-firmware-kh-calc](project-firmware-kh-calc.md) — 펌웨어 dKH 차동 계산식과 ref_pH/tank_pH 상승=전극 드리프트 진단
- [project-kh-offset-aeration-test](project-kh-offset-aeration-test.md) — KH 널테스트 ΔpH 오프셋 튜닝 — 부피·시간상수 비대칭(5L ref가 느려 방CO₂ 과도 추종 못 함) 진단과 대응
- [project-kh-v4-firmware-state](project-kh-v4-firmware-state.md) — KH 측정 상태 스냅샷 — V4 평형추종 측정 + 신펌웨어(트림평균) + dkh.dat 규약
- [project-measure-kh-script](project-measure-kh-script.md) — KH 측정 파이썬 스크립트 — once(V4 본 측정)/test 진단, dkh.dat 기록, Windows COM 포트
- [project-pump-timings](project-pump-timings.md) — 연동펌프 동작시간(초) — 헹굼·측정이송 모두 60/68, m1f80/m1b92(긴 호스)
- [project-symmetric-kh-redesign](project-symmetric-kh-redesign.md) — KH 측정 대칭화 재설계 확정안 — 저장수조 직접 폭기, tank 우선, KCl 스윕=tank 헹굼, 3M KCl 보관
- [project-windows-files](project-windows-files.md) — Windows 작업 폴더 파일 현황 및 작업 스케줄러 설정
- [reference-aeration-equilibrium](reference-aeration-equilibrium.md) — 폭기 화학 — 대기평형이 pH 상한, "과폭기" 불가, 폭기 부족(비대칭)만 dKH 오차 유발
- [reference-aeration-literature](reference-aeration-literature.md) — 해수 폭기/CO₂ 평형 시간의 학술 문헌값 — 화학완화 16초 vs 물리 가스교환 15분, 소부피화 근거
- [reference-aquawiz-overseas-cases](reference-aquawiz-overseas-cases.md) — 해외 상용 AquaWiz 커뮤니티 오차 분석(reef2reef 등) — 방CO₂·기포 오차구조가 우리 진단과 일치
- [reference-bluetooth-hc06](reference-bluetooth-hc06.md) — HC-06 블루투스 WSL 연결 방법 — rfcomm, MAC 주소
