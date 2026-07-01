# project-measure-kh-script

> "KH 측정 파이썬 스크립트 — once(V4 본 측정)/test 진단, dkh.dat 기록, Windows COM 포트(블루투스 재페어링 시 바뀜, 2026-06-20 현재 COM9). measure_kh_loop.py는 2026-06-22 삭제(미사용)"

---

KH 측정 스크립트 (모두 `bin/`):

**⚠️ COM 포트는 블루투스 페어링에 묶임.** 한 번 연결되면 포트는 **계속 유지**되고, 장치를 **삭제(제거)한 뒤 다시 연결할 때만** 번호가 바뀜(매 연결마다 바뀌는 게 아님). 재페어링했으면 실제 포트 확인 후 스크립트 `PORT` 갱신 필요. (2026-06-14: COM15였음 → **2026-06-20 재페어링으로 COM9.** 스크립트 기본 `PORT`도 COM9로 갱신됨.)

| 파일 | 동작 | 기록 |
|------|------|------|
| `measure_kh_once.py` | **V4 본 측정** — 1회 실행 후 종료(스케줄러 정시용). 인자 없으면 calkh, `--setref <수조dKH>`면 calref(ref dKH 역산·저장, dkh.dat 미기록). 자세히 [project-kh-v4-firmware-state](project-kh-v4-firmware-state.md) | dkh.dat ✓ (calref 제외) |
| `test_aeration_plateau.py` / `test_aeration_plateau_ref.py` | 평형곡선 진단(V4 평탄 기준) | 없음 |
| `test_pump.py` | 펌프/배관 시험용 순서 1회 | 없음, 화면 출력만 |

**★2026-06-22 `measure_kh_loop.py` 삭제** (repo + `C:\dkh\work` + 문서). 전혀 사용 안 함(once+스케줄러로 대체). 구 방식=매 정시 무한 반복·고정 폭기시간.

**★2026-06-22 calref(`--setref`) 검증 완료·실전 투입 가능:** 프로덕션 펌웨어(.ino) 응답 포맷을 모사한 mock 시리얼로 calkh/calref 양쪽 흐름 end-to-end 실행 → **19/19 PASS**. 확인: setref 측정 전 선전송, tank/ref 측정 시퀀스가 calkh==calref(setref·cal만 차이), calref 자동 EEPROM 저장(추가 setref 불요, .ino calcRefDKH line 423-424), 새refDKH=knownTank·10^(-(tankPH-refPH))는 calkh 역산. 배포본==저장소 동기화. 구버전 시뮬레이터 `firmware/test/`(calckh/seq 잔존, calref 없음) 삭제. **운영 주의: 스케줄러 `ExecutionTimeLimit` 55분이면 4h 상한 측정 잘림 → 270분 상향 확인**(PHASE_MAX 7200×2phase=4h, [project-kh-v4-firmware-state](project-kh-v4-firmware-state.md)).

**dkh.dat 형식 (공백 구분):**
```
HH ref_pH tank_pH ref_kh tank_kh temp
22 4.064 4.053 8.448 8.239 27.0
```
- 오류/타임아웃 시 `HH 0.000 0.000 0.000 0.000 0.0` 기록(에러 래치)
- tank_kh 음수=평탄 미도달 표식(V4)
- 파일은 열고→쓰고→즉시 닫기 (다른 프로그램과 공유)

**V4 once 핵심 상수**(구 STABLE/CONV/AIR_SECS 폐기, 평탄 추종으로 대체): `FLAT_SPAN_N=4/FLAT_SPAN_MPH=2` + `FLAT_NET_N=8/FLAT_NET_MPH=1`(B1), `MEAS_INTERVAL=30`, `PHASE_MAX_SECS=7200`(2h)/`MEAS_MAX=240`/`FAIL_MAX=5`, `BAUD=9600`. 상세 [project-kh-v4-firmware-state](project-kh-v4-firmware-state.md).

**Why:** 수조 dKH 추세 모니터링용 장기 데이터 수집. test_*는 배관/펌프/평형곡선 확인용.

**How to apply:** 블루투스 재페어링했으면 현재 할당된 COM 포트 확인 → 스크립트 `PORT` 갱신 또는 인자로 명시(평소엔 유지되므로 그대로). [reference-bluetooth-hc06](reference-bluetooth-hc06.md)
