#!/usr/bin/env python3
"""dkh.dat 을 읽어 tank/ref dKH 추세 그래프를 그린다.

dkh.dat 형식(공백 구분, 한 줄에 하나): HH ref_pH tank_pH ref_kh tank_kh temp
  - 5개 값 전부 0.000  → 에러 표식(측정 실패/타임아웃/KCl 소크 실패), 스킵
  - tank_kh 가 음수    → 평탄(평형) 미도달 표식. 크기는 유지되므로 abs() 로 값만 취하고 따로 표시
  - 파일에 날짜가 없다(시각 HH만 기록) → 가로축은 파일에 적힌 순서(행 순번)이고,
    눈금에는 HH를 함께 표기한다. 절대 날짜가 필요하면 docs/measurement-ledger.md 의
    타임스탬프와 대조해야 한다(이 파일만으로는 복원 불가).
"""
import argparse
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

matplotlib.rcParams["font.family"] = "NanumGothic"
matplotlib.rcParams["axes.unicode_minus"] = False


def load(path):
    rows = []  # (idx, hh, ref_kh, tank_kh, temp, is_flat)
    with open(path) as f:
        for line in f:
            parts = line.split()
            if len(parts) < 5:
                continue
            hh, _ref_ph, _tank_ph, ref_kh, tank_kh, *rest = parts
            temp = float(rest[0]) if rest else float("nan")
            ref_kh_v = float(ref_kh)
            tank_kh_v = float(tank_kh)
            if ref_kh_v == 0.0 and tank_kh_v == 0.0:
                continue  # 에러 표식(전부 0) — 스킵
            is_flat = tank_kh_v >= 0
            rows.append((int(hh), ref_kh_v, abs(tank_kh_v), temp, is_flat))
    return rows


def plot(rows, out_path):
    if not rows:
        print("표시할 데이터가 없습니다(전부 에러 표식이거나 파일이 비어있음).", file=sys.stderr)
        sys.exit(1)

    idx = list(range(len(rows)))
    hh = [r[0] for r in rows]
    ref_kh = [r[1] for r in rows]
    tank_kh = [r[2] for r in rows]
    temp = [r[3] for r in rows]
    flat_idx = [i for i, r in enumerate(rows) if r[4]]
    not_flat_idx = [i for i, r in enumerate(rows) if not r[4]]

    fig, ax1 = plt.subplots(figsize=(max(8, len(rows) * 0.12), 5))

    ax1.plot(idx, tank_kh, "-", color="tab:blue", linewidth=1, alpha=0.6, zorder=1)
    ax1.scatter([idx[i] for i in flat_idx], [tank_kh[i] for i in flat_idx],
                color="tab:blue", label="tank dKH (평탄)", zorder=2, s=18)
    if not_flat_idx:
        ax1.scatter([idx[i] for i in not_flat_idx], [tank_kh[i] for i in not_flat_idx],
                    color="tab:red", marker="x", label="tank dKH (평탄 미도달)", zorder=3, s=30)
    ax1.plot(idx, ref_kh, "--", color="tab:gray", linewidth=1, label="ref dKH(앵커)")

    ax1.set_ylabel("dKH")
    ax1.set_xlabel("측정 순번 (파일에 날짜가 없어 순번 기준; 눈금=HH시)")

    step = max(1, len(rows) // 20)
    ax1.set_xticks(idx[::step])
    ax1.set_xticklabels([f"{hh[i]:02d}" for i in idx[::step]], rotation=45, fontsize=8)

    ax2 = ax1.twinx()
    ax2.plot(idx, temp, ":", color="tab:orange", linewidth=1, alpha=0.7, label="온도(°C)")
    ax2.set_ylabel("온도 (°C, 밀폐챔버 내부)")

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="best", fontsize=8)

    ax1.set_title(f"KH 측정 대장 (dkh.dat) — {len(rows)}건")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    print(f"저장: {out_path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("dat_file", nargs="?", default="/mnt/c/dkh/work/dkh.dat",
                     help="dkh.dat 경로 (기본: Windows 원본, WSL에서 /mnt/c 경유)")
    ap.add_argument("-o", "--out", default="dkh_trend.png", help="출력 PNG 경로")
    args = ap.parse_args()

    rows = load(args.dat_file)
    plot(rows, args.out)
