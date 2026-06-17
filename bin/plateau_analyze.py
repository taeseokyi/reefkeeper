import csv, math

rows=[]
with open('/mnt/c/dkh/work/aeration_plateau.csv') as f:
    for r in csv.DictReader(f):
        rows.append((float(r['elapsed_s']), float(r['pH'])))
T=[x[0] for x in rows]; P=[x[1] for x in rows]
TRUE=P[-1]
print(f"데이터 {len(rows)}점, t=0~{int(T[-1])}s, pH {P[0]:.3f}→{P[-1]:.3f}, 진짜평형(최종)={TRUE:.3f}\n")

def linfit_exp(ts,ps,tau):
    xs=[math.exp(-t/tau) for t in ts]; n=len(xs)
    sx=sum(xs); sy=sum(ps); sxx=sum(x*x for x in xs); sxy=sum(xs[i]*ps[i] for i in range(n))
    d=n*sxx-sx*sx
    if abs(d)<1e-15: return None
    slope=(n*sxy-sx*sy)/d; inter=(sy-slope*sx)/n
    ybar=sy/n; sst=sum((p-ybar)**2 for p in ps); ssr=sum((ps[i]-(inter+slope*xs[i]))**2 for i in range(n))
    r2=1-ssr/sst if sst>0 else 0
    return inter,slope,r2  # inter = pH_eq

def best_exp(ts,ps):
    best=None
    for tau in range(120,3001,20):
        f=linfit_exp(ts,ps,tau)
        if f and (best is None or f[2]>best[2]): best=(f[0],tau,f[2])
    return best  # pH_eq, tau, r2

print("=== ① 현재 방식: 연속 Δ ≤ 0.002 (CONV_EPS) ===")
for i in range(1,len(P)):
    if abs(P[i]-P[i-1])<=0.002:
        print(f"  latch @ t={int(T[i])}s, 값={P[i]:.3f}, 진짜평형과 오차={P[i]-TRUE:+.3f}")
        break

print("\n=== ② 윈도우 평탄도: 최근 4점 (max-min) ≤ 0.002 ===")
K=4
for i in range(K-1,len(P)):
    w=P[i-K+1:i+1]
    if max(w)-min(w)<=0.002:
        print(f"  latch @ t={int(T[i])}s, 값={P[i]:.3f}, 오차={P[i]-TRUE:+.3f}")
        break

print("\n=== ③ 지수 최소제곱 외삽: 그 시점까지 데이터로 pH_eq 예측 (온라인) ===")
print(f"  {'t(s)':>6} {'점수':>4} {'pH_eq예측':>9} {'오차':>7} {'τ(s)':>6} {'R2':>7}")
prev_eq=None; stable_since=None; first_good=None
for k in range(4,len(P)):           # 최소 5점부터
    ts=T[:k+1]; ps=P[:k+1]
    b=best_exp(ts,ps)
    if not b: continue
    eq,tau,r2=b; err=eq-TRUE
    flag=""
    # 안정: 직전 예측과 ±0.002 이내가 연속되면
    if prev_eq is not None and abs(eq-prev_eq)<=0.002:
        if stable_since is None: stable_since=T[k]
    else:
        stable_since=None
    prev_eq=eq
    if abs(err)<=0.002 and first_good is None: first_good=T[k]
    if k%2==0 or k>=len(P)-3:
        print(f"  {int(T[k]):6d} {k+1:4d} {eq:9.3f} {err:+7.3f} {int(tau):6d} {r2:7.4f}")
print(f"\n  → 예측이 진짜평형 ±0.002 안에 처음 든 시점: t={int(first_good) if first_good else -1}s")
print(f"  → 예측이 ±0.002로 안정되기 시작한 시점: t={int(stable_since) if stable_since else -1}s")
