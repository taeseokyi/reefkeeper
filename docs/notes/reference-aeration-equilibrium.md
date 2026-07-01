# reference-aeration-equilibrium

> "폭기 화학 — 대기평형이 pH 상한, \"과폭기\" 불가, 폭기 부족(비대칭)만 dKH 오차 유발"

---

폭기는 물의 pCO₂를 방 공기(~400ppm)와 **평형**시키는 과정. 평형 도달 시 pCO₂(물)=pCO₂(공기)가 되어 **더 폭기해도 pH가 안 올라감 — 대기평형 pH가 천장**. 따라서 "과폭기로 ΔpH가 평형을 넘어 틀어진다"는 메커니즘은 **없다**(사용자 지적 맞음, 2026-06-15). 폭기가 dKH를 틀어뜨리는 건 오직 **부족(ref·tank 비대칭)**일 때 — 한쪽에 CO₂가 잔류하면 그쪽 pH가 부당히 낮아져 가짜 ΔpH.

차동식 `KH_tank = 8.448 × 10^(−(pH_ref−pH_tank))`([project-firmware-kh-calc](project-firmware-kh-calc.md))가 순수 KH차를 반영하려면 **ref·tank의 pCO₂가 같아야** 함. 그래서 측정 시퀀스는 ref(5L 김치통)+tank(챔버) **동시 폭기**로 양쪽을 같은 평형에 맞춤([project-symmetric-kh-redesign](project-symmetric-kh-redesign.md)). 양쪽 평형 후 남는 ΔpH = 진짜 KH차 + 전극 노이즈(±0.005~0.01). 민감도 ≈19.5 dKH/pH(0.01 pH = 0.19 dKH)라 작은 ΔpH도 dKH로 증폭됨. 평형 도달이 안 되면(부피 큼) 시간이 율속 — 5L는 8h에도 잔차 0.020, 소부피(~150mL)면 20분 1회로 완전평형. 관련 [project-kh-offset-aeration-test](project-kh-offset-aeration-test.md)

**부피 대칭 불필요(2026-06-15 사용자 정정)**: 평형 pH = f(AT, pCO₂, T, S)이고 **부피 항 없음**(헨리법칙 [CO₂]aq=K_H·pCO₂는 부피 무관). 따라서 수조수 100mL vs 참조수 1L처럼 **부피가 달라도 둘 다 완전 평형이면 ΔpH 오차 0** — 부피는 상쇄됨. "같은 부피라야 대칭"은 부분평형(미완)일 때만 성립(부피 다르면 평형곡선상 다른 지점). 즉 관건은 부피 일치가 아니라 **둘 다 완전 평형 도달 + ref/tank의 pCO₂·온도 일치**. 율속은 느린 쪽(부피 큰 ref) → 폭기시간을 그 기준으로. ref를 상시 폭기로 늘 평형 유지하면 매 측정 때 100mL 수조수만 평형시키면 됨(소부피라 빠름). 완전평형 도달의 실측 증거 = 수렴판정 plateau(45s/0.005). 1L·20분이면 마진 충분([reference-aeration-literature](reference-aeration-literature.md) Takahashi 직접버블링 15분).
