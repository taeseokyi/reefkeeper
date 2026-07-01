# project-bt-rf-reconnect

> HC-06 블루투스 SPP RF 순단 진단과 measure_kh_once.py 4계층 대응(연결확인·재연결·재시도·모터정지+keepalive)

---

측정(measure_kh_once.py)은 **COM9 = 인텔 내장 BT(Dual Band Wireless-AC 8265)의 SPP 링크**로 HC-06과 통신한다(USB CSR 동글 VID_0A12는 미사용·Unknown). 2026-06-23 진단·해결.

**증상:** RF 링크가 간헐적으로 끊김(버스트성, 몰릴 때 몰리고 없을 때 없음). 펌웨어는 살아있고, **드롭은 대개 '명령 보낼 때 이미 끊겨 있음'(통신 중엔 잘 안 끊김)**, 재연결하면 금방 붙고 재페어링·COM 변경 없음. 6/23 05:00 자동측정이 첫 tank 측정에서 `[START]` 후 침묵→실패(수동 재실행 성공). 원인=RF 마진 부족 아님(바로 옆에서도 끊김)=주변 2.4GHz 간섭 추정.

**호스트측 조치(적용):** WiFi 어댑터·BT 네트워크 장치 "사용 안 함"(유선랜 사용), **USB 선택적 절전 OFF**(`powercfg ... 48e6b7a6... 0`, AC/DC). WiFi는 같은 콤보칩이라 미연결이어도 스캔이 BT를 방해할 수 있어 끔.

**코드 대응 = send() 4계층(사용자 설계):** ①모든 명령 송신 전 연결확인(`ensure_link`=부작용없는 status 핑) ②끊겼으면 `reconnect()`(close→open+status 검증) ③보낸 뒤 연결문제(송신/수신 예외·응답 미수신)면 재연결 후 재시도 ④재시도 `SEND_RETRY_MAX=3`까지 ⑤**모터는 재시도 시 먼저 정지(`mNs`→`[Mn] 정지`) 후 재송신**(미전달이든 진행중이든 펌프 중복 구동 방지). + **예방 keepalive**: 유휴(측정 30s·모터 60~85s) 중 `KEEPALIVE_SECS=12`마다 빈 줄(`\r\n`, 펌웨어 line 544 무시) 송신→HC-06 ~20초 유휴 타임아웃 드롭 예방. calkh·calref(--setref) 모두 같은 send() 경로라 동일 적용.

관련 상수(measure_kh_once.py, 실전값): RECONNECT_TRIES=5, RECONNECT_BACKOFF=(1,1,2,2,3), SEND_RETRY_MAX=3, KEEPALIVE_SECS=12, MEAS_READ_TIMEOUT=20, LINK_PING_TIMEOUT=3. 매직넘버를 상수로 뺀 건 테스트 패치용(=[feedback-regression-test-simulator](feedback-regression-test-simulator.md)).

검증: 시뮬레이터 12시나리오 58 PASS([feedback-regression-test-simulator](feedback-regression-test-simulator.md)). 배포 완료(C:\dkh\work). 펌웨어는 `m1s~m4s` 개별 정지 지원. 관련 [project-measure-kh-script](project-measure-kh-script.md) [reference-bluetooth-hc06](reference-bluetooth-hc06.md) [project-windows-files](project-windows-files.md)
