# 1. 프로젝트 개요 (Project Overview)

* **연구 제목**: 한글 형태-통사적 언어 구조 정보의 온디바이스 증류를 통한 반응형 웹 동적 타이포그래피 레이아웃 최적화 시스템 및 이의 실시간 제어 방법
* **핵심 문제 (Pain Point)**:
* 한국어 웹/모바일 환경에서 단순 공백(Whitespace) 기준 줄바꿈이나 `word-break: keep-all` 적용 시 발생하는 **양끝 정렬 붕괴(River of space) 및 가독성 저하**.


* 특히 한국어 행정·법률·학술 문서의 특징인 '띄어쓰기 없이 길게 뭉쳐진 복합명사/합성어'가 줄 끝에 걸칠 때 발생하는 조판 붕괴 현상.
* 실무자들은 이를 해결하기 위해 자간/장평 단축키(`Alt+Shift+N/W`, `J/K` 등)로 눈물겨운 수동 압축 조판(Alt+Shift 노가다)을 수행하고 있음.


* **연구의 비전**: 이 수동 미세 조판(Micro-typography) 프로세스를 **초경량 온디바이스 신경망 지식 증류 기술**과 **실시간 가독성 손실 함수 제어**를 통해 웹 렌더링 표준 엔진 단에서 실시간 자동화함.

---

## 2. 핵심 기술 아키텍처 (Technical Architecture)

### A. 형태-통사적 결합 스코어 증류 (Teacher-Student KD Pipeline)

1. **교사 모델 (Teacher, $T$)**: 한국어 의존 구문 및 형태소 이해도가 높은 고성능 LLM(예: K-독파모 프로젝트 모델 등 ). 입력 문장에 대해 형태-통사적으로 가장 안전한 줄바꿈 분할 경계 스코어 $P(b_i\mid S) \in $를 계산.


2. **학생 모델 (Student, $S_{light}$)**: 클라이언트 단독 구동을 위해 20KB 이하로 최적화된 에이다부스트(AdaBoost) 기반 초경량 이진 분류기. 타겟 경계 전후 3음절 크기의 슬라이딩 윈도우 특징 벡터와 결합하여 고속 추론(추론 지연 < 2.5ms).

### B. 실시간 가독성 손실 함수 (Layout Loss Function)

뷰포트 가로폭 변동 및 모바일 Dynamic Type 확대 설정 에 능동 대응하기 위해, 렌더링 엔진 단에서 자간 변위치($\Delta\text{Sp}$)와 장평 변위치($\Delta\text{Ar}$)를 결정 변수로 하는 실시간 최적화 조판 손실 함수 $E$를 구동.

$$E = w_1 \cdot \sum_{j=1}^{M} \left( 1 - S_{light}(b_{break, j}) \right) + w_2 \cdot D_{justify} + w_3 \cdot \left( \Delta\text{Sp}^2 + \Delta\text{Ar}^2 \right)$$

* **제약 조건 (Constraints)**: 자간 조절 범위 $[-10\%, +5\%]$, 장평 조절 범위 $[95\%, 105\%]$ 내외로 제한하여 가독용 글자 형태 훼손 방지.

---

## 3. 실측 데이터 확보 및 전처리 전략 (Data Sourcing Strategy)

1. **HWP 10년치 내부 문서 자산 활용 (역발상 전처리)**:
* 한컴의 미공개 렌더링 규격(`lineseg` 등)을 파싱하는 대신, HWP 문서들을 **PDF로 일괄 변환(Export)**.
* 변환된 PDF는 한글 조판 엔진이 최종 확정한 시각적 결과물이므로, 행(Line) 단위로 텍스트를 추출하여 "실제 행정 문서에서 완벽하게 줄바꿈된 형태-통사 경계선 정보(Ground Truth)"를 수만 건 확보.


2. **NTIS 연구보고서(PDF) 활용**: `LayoutLM` 등 문서 레이아웃 분석 도구로 본문 영역만 추출한 뒤, 조판원이 수동으로 쪼갠 합성어 경계선 데이터를 정제하여 OOD(Out-of-Distribution) 챌린지셋으로 활용.
3. **법령 데이터 활용**: 국가법령정보 DB 텍스트에서 뭉쳐진 긴 명사구들을 추출하여 PMI(Pointwise Mutual Information) 및 분기 엔트로피(Branching Entropy) 기반의 통계적 결합성 분석으로 1차 의미 경계를 자동 마킹.

---

## 4. 3x NVIDIA RTX A6000 분산 실험 설계 (GPU Pipeline Setup)

단일 노드 내 48GB VRAM GPU 3장(NVLink 안되어 있음)을 비대칭 파이프라인으로 구성하여 병목 없는 고속 수렴 달성.


* **GPU 0 (Teacher 미세 조정)**: KoELECTRA-Large 등 국산 파운데이션 모델의 구문 분석 성능 극대화 파인튜닝.
* **GPU 1 (Soft-Labeling 데이터 가공)**: 완성된 교사 가중치를 동결하고, 일반 텍스트 말뭉치 1,500만 자에 대해 $P(b_i\mid S)$ 분포를 초고속 병렬 추론하여 로컬 NVMe SSD로 스트리밍.
* **GPU 2 (Student Distillation & Simulation)**: 학생 모델을 훈련함과 동시에, Puppeteer/Playwright 헤드리스 브라우저 환경에서 실시간 렌더링 루프를 시뮬레이션. 최적의 레이아웃 가중치 파라미터($w_1, w_2, w_3$)를 정책 구동하기 위해 PPO(Proximal Policy Optimization) 강화학습 적용 시도.



---

## 5. 선행 기술 비교 및 특허 전략 (Patent Position)

* **W3C KLREQ (한글 조판 요구사항)**: 양끝 정렬 기본 원칙 및 미세 조정(Inter-character spacing) 원칙을 수립했으나, 현대 반응형 웹 환경에 대한 동적 제어 표준 및 오픈소스 구현체가 부재함.


* **Google BudouX**: 한국어는 단순 `keep-all`만으로 충분하다는 오판 하에 한글 학습 모델을 배제함. 좁은 화면에서 가독성 붕괴(River of Space) 유발.


* **US11170154B1 (Cascade Reading)**: 의존성/구문 분석을 통해 줄바꿈 및 계단식 들여쓰기를 실행하나, 일반적인 블록형 그리드 배치를 깨뜨려 커머스/뉴스 등의 웹 UI에 이식이 불가능하고 연산 오버헤드가 과도함.


* **본 발명의 차별성 (청구항 1 핵심)**: 텍스트 레이아웃 구조를 깨뜨리지 않으면서, 온디바이스 초경량 예측 모델 스코어($S_{light}$)와 브라우저 컨테이너 가로폭($W_{container}$), Dynamic Type 설정을 결합하여 **자간과 장평을 실시간 픽셀 스케일로 미세 변형 제어하는 하이브리드 최적화 기술**.

---

## 6. 학술적 기여 (ICML/Top-tier CS Conference Targeting)

1. **Weight-to-Table Distillation**: 고차원 연속 신경망 임베딩 공간의 맥락을 수십 KB 수준의 이산적인 문자열 득점표(Score table) 구조로 정보 손실 없이 투영해낸 수학적 방법론 규명.
2. **Predictive Stream-to-Layout Compression**: 텍스트가 타이핑되는 동안 문장 마무리를 예측하여 실시간으로 앞선 어절들의 자간/장평을 가변 조절하여 지면 낭비를 제어하는 동적 알고리즘 증명.
