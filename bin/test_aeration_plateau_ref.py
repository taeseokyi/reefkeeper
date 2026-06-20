#!/usr/bin/env python3
"""
폭기 평형(plateau) 테스트 — ★참조수(ref) 버전.

test_aeration_plateau.py(=tank/측정챔버 본수조수)의 ref 대응판.
측정 챔버에 **참조수**(5L 김치통 → 홀딩 → 측정챔버)를 채우고 ron 으로 계속 폭기하며
일정 간격으로 pH 를 반복 측정해 시간-pH 곡선을 기록한다.
최근 PLATEAU_N개 정수 milli-pH 의 span ≤ PLATEAU_SPAN_MPH **AND** net(양끝차) ≤ PLATEAU_NET_MPH
이면 진짜 평형으로 보고 종료(net 게이트 = 단조 드리프트 꼬리 조기 latch 차단).

목적: tank 버전이 같은 폐루프에서 7.850 에 평탄해진 것과 비교 —
  · ref 도 ~7.85 → 헤드스페이스 천장 공통(차동 상쇄 OK)
  · ref 가 ~7.92 → tank·ref 가 같은 루프서 갈라짐(널 깨짐/헤드스페이스 비공통 = 새벽 dip 진짜 원인)

배관(사용자 지정): 채움 m4f:60(참조수→홀딩) → m2f:60(홀딩→측정챔버),
                  배출 역순 m2b:68 → m4b:68, KCl 소크 백(m3b) 먼저·끝나면 소크(m3f).
액체 이동 전 반드시 airoff→ton(수조ON), 폭기는 ron(참조ON). (production measure_kh_once 와 동일)

실행:  /mnt/c/dkh/python313/python.exe -X utf8 test_aeration_plateau_ref.py [COM포트]
중단:  Ctrl+C — 정리(시료 배출 + KCl 채움)까지 수행 후 종료
"""

import serial
import time
import re
import sys
import os
from datetime import datetime

PORT = 'COM9'
BAUD = 9600

DO_PREP           = True   # True면 KCl 배출 후 참조수 채움(테스트라 헹굼·기포청소 생략)
FILL_HOLD_SECS    = 60     # m4f: 참조수 → 홀딩
FILL_CHAMBER_SECS = 60     # m2f: 홀딩 → 측정 챔버
LOG_INTERVAL      = 30     # pH 재측정 간격(초)
MAX_DURATION      = 3600   # 최대 폭기·기록 시간(초)
PLATEAU_N        = 4    # 최근 N개 읽기로 판정 (윈도우)
PLATEAU_SPAN_MPH = 2    # 최근 N개 max−min ≤ 2 milli-pH (흔들림 폭). 정수 비교(float 지터 회피)
PLATEAU_NET_MPH  = 1    # ★net 게이트: 최근 N개 양끝 |win[-1]-win[0]| ≤ 1 mpH (단조 드리프트 꼬리 차단)

CSV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'aeration_plateau_ref.csv')


def read_until(ser, stop, timeout=20.0):
    lines = []
    deadline = time.time() + timeout
    while time.time() < deadline:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8', errors='replace').strip()
            if line:
                lines.append(line)
                if stop in line:
                    return lines
        else:
            time.sleep(0.02)
    return lines


def send(ser, cmd, stop=None, timeout=5.0):
    ser.write((cmd + '\r\n').encode())
    if stop:
        return read_until(ser, stop, timeout)
    time.sleep(0.3)
    out = []
    while ser.in_waiting:
        line = ser.readline().decode('utf-8', errors='replace').strip()
        if line:
            out.append(line)
    return out


def motor(ser, idx, cmd):
    m = re.search(r':(\d+)$', cmd)
    dur = int(m.group(1)) if m else 60
    return send(ser, cmd, stop=f'[모터{idx}] 완료', timeout=dur + 15)


def measure_ph(ser):
    """tank 1회 측정 → (pH, V, T). 폭기 켠 상태에서 호출. (펌웨어 'tank' 명령이 현재 측정챔버 pH 읽음)"""
    lines = send(ser, 'tank', stop='[OK]', timeout=20)
    ph = v = t = None
    for ln in lines:
        m = re.search(r'\[수조수\] V:([\d.]+) pH:([\d.]+) T:([\d.]+)', ln)
        if m:
            v, ph, t = float(m.group(1)), float(m.group(2)), float(m.group(3))
    return ph, v, t


def cleanup_ref(ser):
    """모든 종료 경로(정상/Ctrl+C/오류)에서 호출 — 참조수 배출(역순) 후 KCl 용액 채움(프로브 소크), airoff.
    프로브를 절대 KCl 없이 두지 않기 위함. (production measure_kh_once 정리와 동일)"""
    try:
        send(ser, 'airoff', stop='OFF')
        send(ser, 'ton', stop='수조ON')
        print("\n[정리] 참조수 배출 → 홀딩 → 위즈수조 (역순)")
        motor(ser, 2, 'm2b:68')
        motor(ser, 4, 'm4b:68')
        print("[정리] KCl 용액 공급(프로브 소크 복원)")
        motor(ser, 3, 'm3f:60')
        send(ser, 'airoff', stop='OFF')
    except Exception as e:
        print(f"[정리 오류] {e} — KCl 채움 실패, 수동 확인 필요!")


def main():
    port = sys.argv[1] if len(sys.argv) > 1 else PORT
    print(f"폭기 평형 테스트 [참조수] — {port} @ {BAUD}baud, 간격 {LOG_INTERVAL}s, 최대 {MAX_DURATION}s")
    print(f"평형 판정: 최근 {PLATEAU_N}개 span ≤ {PLATEAU_SPAN_MPH}mpH AND net ≤ {PLATEAU_NET_MPH}mpH (정수, net=양끝차=드리프트)")
    print(f"CSV: {CSV_FILE}\n")

    with serial.Serial(port, BAUD, timeout=1) as ser:
        plateaued = False
        try:
            time.sleep(2)
            ser.reset_input_buffer()

            # ── 준비: KCl 배출 → 참조수 채움 (m4f 홀딩 → m2f 측정챔버) ──
            if DO_PREP:
                send(ser, 'airoff', stop='OFF')
                send(ser, 'ton', stop='수조ON')
                print("[준비] KCl 배출(소크 백)")
                motor(ser, 3, 'm3b:68')
                print("[준비] 참조수 → 홀딩")
                motor(ser, 4, f'm4f:{FILL_HOLD_SECS}')
                print("[준비] 홀딩 → 측정 챔버")
                motor(ser, 2, f'm2f:{FILL_CHAMBER_SECS}')

            # ── 폭기 ON, 시간-pH 기록 ──
            send(ser, 'airoff', stop='OFF')
            send(ser, 'ron', stop='참조ON')
            print("[폭기] ON — 참조수 시간별 pH 기록 시작\n")
            print(f"{'t(s)':>6} {'pH':>7} {'ΔpH':>7} {'V(mV)':>9} {'T':>5}")

            with open(CSV_FILE, 'w') as f:
                f.write("elapsed_s,pH,dPH,V_mV,T_C,span_mph,net_mph,clock\n")

            t0 = time.time()
            prev = None         # 표시·CSV용 직전 pH
            win = []            # 최근 PLATEAU_N개 정수 milli-pH
            old_rule_at = None  # 기존(span만) 규칙이라면 처음 latch했을 지점 — 비교용 1회 기록
            while True:
                elapsed = int(time.time() - t0)
                ph, v, t = measure_ph(ser)
                if ph is None:
                    print(f"{elapsed:6d}  [측정 실패]")
                else:
                    d = (ph - prev) if prev is not None else 0.0   # 표시·CSV용(float)
                    win.append(round(ph * 1000))                   # 정수 milli-pH (지터 회피)
                    if len(win) > PLATEAU_N:
                        win.pop(0)
                    if len(win) >= PLATEAU_N:
                        span = max(win) - min(win)
                        net  = abs(win[-1] - win[0])               # ★양끝 차 = 방향성 드리프트
                    else:
                        span = net = None
                    sstr = f"{span}" if span is not None else "-"
                    nstr = f"{net}" if net is not None else "-"
                    print(f"{elapsed:6d} {ph:7.3f} {d:+7.3f} {v:9.3f} {t:5.1f}  span{PLATEAU_N}:{sstr}mpH net:{nstr}mpH")
                    with open(CSV_FILE, 'a') as f:
                        f.write(f"{elapsed},{ph:.3f},{d:+.3f},{v:.3f},{t:.1f},"
                                f"{sstr},{nstr},{datetime.now():%H:%M:%S}\n")
                    prev = ph
                    # 기존 규칙(span만) 처음 만족 지점 — 멈추진 않고 비교용으로 1회 표시
                    if span is not None and span <= PLATEAU_SPAN_MPH and old_rule_at is None:
                        old_rule_at = (elapsed, ph)
                        print(f"       └─ [기존규칙(span≤{PLATEAU_SPAN_MPH})이라면 여기서 latch했을 것: "
                              f"@{elapsed}s pH={ph:.3f}, net={net}mpH 이동중] — net 게이트로 계속 측정")
                    # ★신규 규칙: span AND net 둘 다 만족해야 진짜 평형
                    if span is not None and span <= PLATEAU_SPAN_MPH and net <= PLATEAU_NET_MPH:
                        print(f"\n[평형] 최근{PLATEAU_N} span={span}≤{PLATEAU_SPAN_MPH} AND net={net}≤{PLATEAU_NET_MPH} "
                              f"→ pH 진짜 평탄(평형 도달) @ {elapsed}s, pH={ph:.3f}")
                        if old_rule_at:
                            gap = abs(round(ph * 1000) - round(old_rule_at[1] * 1000))
                            print(f"       (기존규칙은 @{old_rule_at[0]}s pH={old_rule_at[1]:.3f}에 멈췄을 것 "
                                  f"= {gap}mpH 일찍·낮게 latch했을 것)")
                        plateaued = True
                        break
                if time.time() - t0 >= MAX_DURATION:
                    print(f"\n[종료] 최대 {MAX_DURATION}s 도달 — net≤{PLATEAU_NET_MPH} 미달(아직 이동중). 곡선은 CSV에 전부 기록됨.")
                    break
                time.sleep(LOG_INTERVAL)
        except KeyboardInterrupt:
            print("\n[중단] 사용자 인터럽트 — 정리 후 종료")
        finally:
            cleanup_ref(ser)   # ★어떤 경로로 끝나든(정상/Ctrl+C/오류) 참조수 배출 + KCl 소크

        print(f"\n완료. CSV 저장: {CSV_FILE}  (평형도달={'O' if plateaued else 'X'})")


if __name__ == '__main__':
    main()
