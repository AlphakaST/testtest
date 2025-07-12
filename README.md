# testtest

# GPT와 함께하는 **서술형 평가 자동 채점 & 실시간 피드백**  
중학교 과학 수업용 AI-기반 평가·피드백 시스템
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-%F0%9F%90%9B-red)
![OpenAI GPT](https://img.shields.io/badge/OpenAI-GPT4o-11A37F)
![MySQL](https://img.shields.io/badge/MySQL-8.x-orange)

> **교사 채점 부담 ↓ , 학생 맞춤 피드백 ↑**  
> GPT API·Streamlit·MySQL만으로 손쉽게 구축한 ‘에세이 자동 채점 + 대시보드’ 예제입니다.

---

## 📚 프로젝트 개요
| 구분 | 내용 |
|------|------|
| 목적 | **서술형 평가**의 높은 교육적 효과를 살리면서도 교사 채점‧피드백 부담을 최소화 |
| 대상 | 중학교 2학년 과학 - ‘물질의 구성’ 단원 <br>→ 단원·과목 변경도 코드만 수정하면 가능 |
| 특징 | 1. **GPT-4o**가 모범 답안·채점 기준을 바탕으로 1차 채점 & 초안 피드백<br>2. **교사 대시보드**에서 오답·환각 여부 2차 확인<br>3. **MySQL**에 모든 기록 자동 저장 → 학습 분석·포트폴리오 활용<br>4. **Streamlit** 웹 앱으로 학생·교사 모두 설치 없이 접속 |

---

## 🏗️ 기술 스택
| Layer            | Tech / Lib                     | 역할 |
|------------------|--------------------------------|------|
| UI / Front       | **Streamlit 1.35**             | 문제 제시·작성, 피드백 팝업, 교사용 대시보드 |
| AI Engine        | **OpenAI GPT-4o**              | 서술형 답안 채점·피드백 생성 |
| DB               | **MySQL 8.x** / MariaDB 호환   | 답안·점수·피드백 영구 저장 |
| Dev Ops & Deploy | **Docker (optional)**<br>Streamlit Community Cloud | 로컬 개발·테스트 / 1-Click 배포 |

---

## 🗂️ 디렉터리 구조
```text
.
├── app/                 # Streamlit 소스
│   ├── pages/           # (선택) 여러 페이지 분할
│   ├── components/      # 공통 컴포넌트
│   └── main.py          # 앱 진입점
├── sql/                 # DB 스키마 & 예시 쿼리
│   └── init_schema.sql
├── docs/                # PDF 매뉴얼, 발표자료 등
├── requirements.txt     # Python 의존성
├── .streamlit/          # config.toml (테마, email 등)
└── .env.example         # OPENAI_KEY / DB 접속 정보 예시
