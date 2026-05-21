# KOWRAP Project Definition

Last updated: 2026-05-21

## Public Name

KOWRAP is fixed as the public project name.

- English: Korean Wrapping and Rendering Analysis Project
- Korean: 한국어 줄바꿈·렌더링 분석 프로젝트
- CLI/package name: `kowrap`
- Repository: `msjang/kowrap`, private first
- License: Apache-2.0 for public code, documentation, and project-authored synthetic examples

## Working Thesis

보고서 작성에서 가장 비싼 일이 생각이 아니라 조판이 되는 현상은 개인의 숙련도 문제가 아니라, 한국어 텍스트 레이아웃을 기계가 재현 가능하게 다루지 못하는 인프라 문제다. KOWRAP은 한국어 긴 복합어와 행정·연구 문서 문체에서 안전한 줄바꿈 지점을 예측하고, 이를 HWPX/PDF/Web 렌더링 환경에서 검증 가능한 코드·데이터·표준 제안으로 만드는 프로젝트다.

## Origin Story

현장에서는 LLM이 초안을 쓰는 시대에도 HWP에 붙여넣고, `ㅁ/ㅇ/-/·`를 맞추고, `Alt+C`로 서식을 칠하고, 자간·장평을 수동으로 조절한다. 이 작업은 지식노동자의 판단을 쓰는 일이 아니라 렌더러와 폰트와 줄바꿈 규칙의 빈틈을 사람이 메우는 일에 가깝다.

사용자 증거:

> "연구계획서를 쓰고 있습니다. hwp에서 표를 고치고 있습니다. 뇌가 없어도 될 것 같습니다."
>
> 이제헌, 한국에너지기술연구원, 공개 게시물, 2024-01-26

## Evidence

`2026_0518_krigf_partial.pdf`의 3쪽과 5쪽을 렌더링하면 다음 문제가 드러난다.

- 3쪽: 영어권에는 Knuth-Liang 계열의 하이픈 알고리즘 전통이 있지만, 한국어 긴 합성어 내부의 의미 단위 줄바꿈을 다루는 실용 알고리즘·데이터·표준 레이어가 빈약하다.
- 3쪽: 한글 문장을 줄 안에 억지로 맞추기 위해 폰트 변경, 자간 조절, 수동 줄바꿈을 반복하면 어색한 지점과 표 레이아웃 붕괴가 발생한다.
- 5쪽: 같은 내용이 한컴 2010, 한컴 2020, 한컴독스 웹에서 서로 다른 줄간격, 장평, 자간, 줄바꿈으로 렌더링된다.

Rendered artifacts:

- `renders/krigf_p3-3.png`
- `renders/krigf_p5-5.png`

## Problem Statement

한국어 문서는 공백 기준 줄바꿈만으로 충분하지 않다. 특히 연구보고서, 행정문서, 법령문, 학술문서에는 띄어쓰기 없이 길게 이어지는 복합명사와 전문용어가 많다. 이 단어들이 줄 끝에 걸리면 다음 문제가 생긴다.

- 의미적으로 어색한 음절 단위 분절
- 양끝 정렬 시 과도한 공백 또는 강제 자간 압축
- HWPX, PDF, Web 렌더러 간 결과 불일치
- 폰트 메트릭 차이에 따른 줄바꿈 재현 실패
- 자동 문서 변환 파이프라인에서 사람이 수작업으로 조판을 보정해야 하는 병목

## Gap

영어권 조판에는 TeX의 Knuth-Liang hyphenation algorithm처럼 언어별 패턴 기반 줄바꿈 전통이 있다. 반면 한국어 긴 복합어 내부의 안전한 줄바꿈 위치를 다루는 공개 데이터셋, 벤치마크, 표준화된 구현체, 웹/HWPX 통합 레이어는 부족하다.

W3C의 Korean Layout Requirements 문서는 한국어 조판 요구사항을 정리하는 중요한 출발점이지만, 프로젝트가 필요로 하는 다음 레이어까지 제공하지는 않는다.

참고로 W3C 문서는 2026-03-21 기준 Group Note Draft로 재정리되어 있고 GitHub 피드백 경로도 열려 있다. 따라서 KOWRAP의 표준화 전략은 "문서가 없다"가 아니라 "요구사항 문서는 있으나, 긴 복합어 줄바꿈을 검증 가능한 구현·데이터·테스트 케이스로 내리는 층이 비어 있다"로 잡는다.

- 현대 문서 렌더러별 줄바꿈 재현 벤치마크
- 긴 복합어 내부 분절 데이터셋
- HWPX/PDF/Web을 잇는 구현 가능한 알고리즘
- 기관별 문체와 용어를 반영하는 모델 버전 관리
- 표준 문서에 반영 가능한 테스트 케이스와 참조 구현

## Goals

1. 한국어 긴 복합어와 전문용어의 안전한 줄바꿈 지점을 정의한다.
2. 공개 가능한 말뭉치와 비공개 기관 말뭉치를 분리해 학습·평가 파이프라인을 설계한다.
3. 규칙 기반, 통계 기반, 경량 ML 기반 모델을 같은 평가 체계에서 비교한다.
4. HWPX/PDF/Web 렌더링 차이를 재현 가능한 이미지와 수치 지표로 측정한다.
5. 오픈소스 라이브러리, 논문, 특허, 표준화 제안을 서로 보강하는 구조로 만든다.

## Non-Goals

- 한컴오피스 렌더러 전체를 재구현하지 않는다.
- 모든 한국어 타이포그래피 문제를 한 번에 해결하지 않는다.
- 초기 버전부터 LLM, PPO, 브라우저 엔진 패치를 전제로 삼지 않는다.
- 내부 문서 원문을 공개 데이터로 섞지 않는다.
- 폰트 라이선스가 불명확한 파일을 배포 산출물에 포함하지 않는다.

## Research Questions

- RQ1: 한국어 긴 복합어 내부의 줄바꿈 가능 지점은 형태소, 음절, 통계적 결합도, 문서 도메인 정보를 조합해 얼마나 안정적으로 예측할 수 있는가?
- RQ2: `keep-all`, 음절 단위 분절, 수동 `<br>`, 자간 조절 대비 제안 모델은 시각적 품질과 편집 비용을 얼마나 줄이는가?
- RQ3: HWPX/PDF/Web 렌더러 차이를 흡수하는 최소 공통 표현은 무엇인가?
- RQ4: 기관별 용어와 문체에 맞춘 모델을 어떻게 버전 관리하고 교체할 수 있는가?
- RQ5: 여러 내부 줄바꿈 후보가 있을 때 의미 점수, 남은 줄 폭, 자간/장평 조정 비용, 다음 줄 영향을 결합해 어떤 후보를 선택해야 하는가?
- RQ6: 표준 문서가 받아들일 수 있는 테스트 케이스와 요구사항 문장으로 어떻게 환원할 수 있는가?

## Expected Outputs

- Code: Korean wrapping library, CLI, renderer test harness, HWPX/PDF/Web adapters.
- Dataset: 공개 가능 예제, 비공개 기관용 fine-tuning 포맷, synthetic test cases.
- Benchmark: line-break quality, visual layout stability, renderer reproducibility, latency.
- Paper: 문제정의, 데이터셋, 알고리즘, 평가, 오픈소스 구현.
- Patent: 렌더링 환경·문서 도메인·모델 점수를 결합한 한국어 줄바꿈 제어 방법.
- Standardization: W3C `klreq` issue/PR, Korean layout test cases, 가능한 경우 KS/공공문서 가이드 제안.

## Repository and Collaboration

The initial repository is `msjang/kowrap` on GitHub and should remain private until the evidence pack, disclosure boundary, and first baseline are stable enough for external collaborators.

First collaboration target:

- KONI / KISTI internal AI collaboration

Later collaboration targets:

- HWPX/open-source maintainers
- W3C `klreq`
- browser and document-layout implementers
- public-sector document automation users

## IP and Open Source Posture

The default posture is Apache-2.0 open source. If KISTI wants to file a patent or manage institutional IP, the desired shape is a defensive/open-source-compatible route: commercial proprietary implementers can be licensed explicitly, while open-source implementers can use the public implementation freely under Apache-2.0.

Until the institutional IP boundary is clarified, public materials should emphasize the problem, evidence, benchmark, and high-level architecture. Exact scoring formulas, model compression details, domain adaptation method, and render-aware optimization loop should be held back from public issue trackers and slide uploads.

## Product Surface

초기 사용자는 연구자, 문서 자동화 개발자, HWPX 변환기 메인테이너, 공공기관 보고서 작성자다. 첫 제품 표면은 다음 순서로 만든다.

1. `kowrap` CLI: 텍스트를 입력하면 후보 줄바꿈 지점과 점수를 출력한다.
2. Web demo: 같은 문단을 `keep-all`, 음절 분절, KOWRAP으로 비교 렌더링한다.
3. HWPX adapter: HWPX 문서의 문단 텍스트와 스타일을 읽어 줄바꿈 위험 지점을 리포트한다.
4. Benchmark runner: 여러 렌더러와 폰트 조합에서 PNG/PDF 결과를 비교한다.

## Algorithmic Core

KOWRAP separates Korean compound wrapping into two layers.

Layer 1 scores word-internal break candidates. For `과학기술유공자`, candidates include `과학|기술유공자` and `과학기술|유공자`. The latter is normally preferred because `과학기술` is a strong compound and `유공자` is a natural unit.

Layer 2 chooses the actual line break under renderer constraints. If the current line has enough width for `과학기술`, KOWRAP can choose `과학기술\n유공자`. If only `과학` fits, KOWRAP should compare earlier line breaks, moving the whole eojeol to the next line, small 자간/장평 adjustment, and the weaker `과학\n기술유공자` option.

One explicit subproblem is semantic-preserving microcompression. If the renderer would otherwise produce `과학기|술유공자`, KOWRAP can compare the cost of the bad semantic split with the cost of a small negative letter-spacing or modest glyph-width reduction that permits `과학기술|유공자`.

The line-level decision minimizes:

```text
total_cost =
  layout_badness
+ semantic_break_penalty
+ typography_adjustment_penalty
+ lookahead_penalty
+ renderer_instability_penalty
```

Details live in `docs/break-selection.md`.

## Model Versioning

모델은 알고리즘과 말뭉치의 시간성을 분리해 관리한다.

- `kowrap-rule-YYYYMM`: 규칙 기반 기준선.
- `kowrap-stat-YYYYMM`: PMI, branching entropy, 빈도 기반 모델.
- `kowrap-light-YYYYMM`: 경량 ML 모델.
- `kowrap-domain-ORG-YYYYMM`: 기관별 용어와 문체에 맞춘 사내 fine-tuned 모델.

각 모델은 model card를 갖는다.

- 학습 데이터 출처와 공개 가능 여부
- 도메인
- 평가 세트
- 알려진 실패 사례
- 추론 속도와 크기
- 라이선스와 배포 범위

## Evaluation Metrics

- Break accuracy: 사람이 표시한 안전 분절 지점과의 precision, recall, F1.
- Bad break rate: 의미적으로 부적절한 위치에서 줄이 끊긴 비율.
- Preferred break accuracy: 여러 후보 중 사람이 선호한 의미 단위 후보를 고른 비율.
- Layout-aware choice quality: 남은 폭과 다음 줄 영향을 고려했을 때 총비용이 낮은 후보를 선택한 비율.
- Microcompression benefit: 의미 보존을 위해 제한된 자간/장평 축소를 사용했을 때 bad break가 얼마나 줄어드는지.
- Layout stability: 폰트, 폭, 렌더러 변화에 따른 줄바꿈 edit distance.
- Visual quality: 과도한 공백, 자간 압축, 표 영역 넘침, widows/orphans.
- Human effort: 수동 `<br>`, 자간 조정, 폰트 변경 횟수.
- Latency: 브라우저/CLI에서 문단당 추론 시간.

## Baselines

- CSS `word-break: keep-all`
- 음절 단위 임의 분절
- 수동 `<br>` 삽입
- 형태소 분석기 기반 휴리스틱
- PMI/branching entropy 기반 통계 모델
- Google BudouX류 phrase break 접근법의 한국어 적용 가능성 검토

## Risks

- 내부 보고서 데이터는 개인정보, 보안, 저작권 문제가 있을 수 있다.
- 폰트 라이선스가 연구 재현성을 제한할 수 있다.
- HWPX 렌더링 차이를 완전히 설명하려 하면 프로젝트가 너무 커진다.
- LLM 기반 방법은 비용과 재현성 문제가 있다.
- 표준화는 속도가 느리므로 코드와 테스트 케이스가 먼저 살아 있어야 한다.

## Source Links

- W3C Korean Layout Requirements: https://www.w3.org/TR/klreq/
- W3C `klreq` GitHub repository: https://github.com/w3c/klreq/
- Knuth-Liang hyphenation background: https://tug.org/docs/liang/
