# reference-aeration-literature

> "해수 폭기/CO₂ 평형 시간의 학술 문헌값 — 화학완화 16초 vs 물리 가스교환 15분, 소부피화 근거"

---

해수 폭기(CO₂ 탈기·대기평형)는 두 층위로 나뉘며 둘 다 문헌 정량값이 있음. 폭기시간 튜닝의 학술 근거.

## 1. 화학 평형(완화시간) ≈ 16초 — 율속 아님
- CO₂+H₂O⇌H⁺+HCO₃⁻ 내부평형 완화시간 **≈15.9s** (25°C, S=35, pH8.2). 율속단계=CO₂ 수화 k_CO₂≈0.037 s⁻¹.
- Johnson 1982, *CO₂ hydration/dehydration kinetics in seawater*, Limnol. Oceanogr. 27(5):849 (DOI 10.4319/lo.1982.27.5.0849)
- Soli & Byrne (CO₂ system hydration/dehydration kinetics); 이론서 Zeebe & Wolf-Gladrow 2001, *CO₂ in Seawater: Equilibrium, Kinetics, Isotopes* (Elsevier Ocean. Ser. 65)
- → 물속 화학반응은 ~16초면 끝. 폭기를 길게 하는 이유는 화학이 아님.

## 2. 물리적 가스교환(대기평형)=진짜 율속, 방식별 시간
- **직접 버블링(가스 디스퍼서): CO₂ 평형 15분**(공기 ~20분 순환) — Takahashi, *Methods for measurement of pCO₂/TCO₂ in seawater*. ※아쿠아위즈 "버블 15분/총 20분"과 정확히 일치(우연 아님)
- 버블 평형기 폐루프 ~10분; **막(멤브레인) 평형기 시간상수 ~2분**; 분광 소부피계 <10분(대부분 첫 2분).

## 3. 아쿠아위즈식 차동측정의 학술근거 (가장 중요)
- **Fleger, Liu, Berelson, Adkins 외 2025, *Total alkalinity measurements in small samples: methods based on CO₂ equilibration and spectrophotometric pH*, Analytica Chimica Acta** (DOI 10.1016/j.aca.2025.344432)
- "AT는 AT·pCO₂·분광pH의 단순 선형관계로 결정" = 차동식(ΔpH→KH) 동일 원리. 온도보정상수 E(T)로 절대 CO₂농도 불필요(=ref·tank 동일폭기시 절대 pCO₂ 상쇄 논리와 동일). **직접버블링 0.5mL 소부피까지 가능**, 정밀도 ±1~2 µmol/kg.

## 4. 부피 vs 평형시간 정량 (2026-06-16 검색)
- 폭기 평형은 **1차 지수**: C(t)−C* = (C₀−C*)e^(−t/τ). 가스 스트리핑 문헌이 `ln(C₀/Cₜ)` ∝ `φ/V`(누적가스부피/액부피) 직선으로 확증(기울기=헨리상수).
- **시간상수 τ = V/(K_H·Q_gas) × β.** 지배 무차원군 = **Q_gas/V (=VVM, 분당 액부피당 가스부피)**. τ ∝ 1/VVM.
- **같은 폭기(같은 Q): τ ∝ V → 1L가 100mL보다 ~10배 느림.** 1L를 100mL만큼 빠르게 = 가스유량 10배(같은 VVM).
- **단서(중요):** τ∝V 선형은 "기포 포화(가스측 한계)" 영역 한정. 액막 한계에선 τ=1/(kₗa), a=계면적/부피 → 같은 기포기로 높이만 늘리면 a≈일정해 τ가 부피에 둔감. 실제는 "10배"와 "1배" 사이, 진짜 손잡이=**a(계면적/부피)**.
- **β = 해수 CO₂ 버퍼/화학 인자**: 스트립 가능한 건 CO₂(aq) 미량뿐(대부분 HCO₃⁻/CO₃²⁻) → Revelle ~8~15배만큼 τ↑(+수화 16초). **β는 τ를 곱으로 늘리나 V/Q 스케일링은 보존.** 출처: 가스스트리핑(ScienceDirect S0045653512015184, Roberts2005 GRL, NIST), kLa(AIP PoF, BioProcessIntl VVM), Revelle(Egleston2010 GBC), CO₂평형시간(Zeebe&Wolf-Gladrow).
- **함의:** 5L→500mL/150mL = τ ~10~33배↓ → tank 챔버와 시간상수 일치 → 방CO₂ 과도 동반추종 → ΔpH 비대칭 소멸. 부피 못 줄이면 참조수 폭기유량↑로 VVM 일치도 등가. 실측 권장=참조수 pH(t) 곡선으로 τ 직접 측정.

## 프로젝트 함의
- 폭기 15분은 과하지 않음(직접버블링 표준값). 줄였다가 비대칭오차 본 것과 정합.
- **참조수 5L→150mL 소부피화가 정공법**: 막/소부피는 평형 2분으로 단축, Fleger 0.5mL가 강력 지지. 부피 스케일링(위 §4)이 정량 근거. [project-kh-offset-aeration-test](project-kh-offset-aeration-test.md)
- 율속은 가스교환(버블 표면적·유량·부피)이지 화학 아님, 화학완화 16초가 하한. [reference-aeration-equilibrium](reference-aeration-equilibrium.md) [project-firmware-kh-calc](project-firmware-kh-calc.md) [project-symmetric-kh-redesign](project-symmetric-kh-redesign.md)
