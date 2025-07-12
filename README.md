# testtest

````markdown
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
````

---

## ⚡ 빠른 시작 (로컬)

1. **사전 준비**

   * Python ≥ 3.10 - 권장 3.11
   * MySQL 8.x 실행 중 (Docker Compose 예시 제공)
   * OpenAI API Key

2. **클론 & 가상환경**

   ```bash
   git clone https://github.com/your-org/essay-auto-grading.git
   cd essay-auto-grading
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **환경 변수 설정**

   ```bash
   cp .env.example .env        # 편집하여 KEY·DB 비밀번호 입력
   ```

4. **DB 스키마 생성**

   ```bash
   mysql -u root -p < sql/init_schema.sql
   ```

5. **앱 실행**

   ```bash
   streamlit run app/main.py
   ```

   브라우저가 자동 열리며 `/?role=student` 또는 `/dashboard` URL로 접근합니다.

---

## 🚀 배포 가이드

### Streamlit Community Cloud

1. 레포지토리를 **Public** 으로 설정
2. Streamlit Cloud → New App → Git URL 지정
3. **Secrets** 탭에 환경 변수 추가
4. **Deploy** 클릭 후 즉시 공유 URL 발급

### Docker Compose (학교 서버)

```yaml
version: "3"
services:
  db:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: rootpw
      MYSQL_DATABASE: essay
    volumes: [ "./dbdata:/var/lib/mysql" ]
  app:
    build: .
    env_file: .env
    ports: [ "8501:8501" ]
    depends_on: [ db ]
```

```bash
docker compose up -d
```

---

## 🖥️ 사용법

| 대상     | 행동 흐름                                                                                  |
| ------ | -------------------------------------------------------------------------------------- |
| **학생** | ① 학번 입력 → ② 5문항 작성 → ③ `제출` → ④ 즉시 GPT 피드백 확인                                          |
| **교사** | ① `/dashboard` 접속 → ② 학생별 점수·GPT 피드백 확인 → ③ 필요 시 코멘트 보정 → ④ `확정` 클릭 시 학생 화면에 최종 피드백 반영 |

---

## 📝 주요 코드 스니펫

```python
# GPT 채점 함수를 한눈에
def grade_answer(prompt, answer, rubric):
    messages = [
        {"role": "system", "content": "You are a strict science teacher."},
        {"role": "user", "content": f"{prompt}\n\n학생 답안: {answer}\n\n[채점 기준]\n{rubric}"},
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=messages
    )
    return response.choices[0].message.content
```

---

## 🙋 FAQ

| 질문                  | 답변                                                              |
| ------------------- | --------------------------------------------------------------- |
| **학생답안 최대 글자수?**    | 기본 1 문항 1000자 · `st.text_area(max_chars=…)`로 조정                 |
| **DB 대신 CSV로도 가능?** | 예. `pandas.to_csv` 로컬 저장 ↔ 추후 업로드 가능하지만 동시성·분실 위험               |
| **OpenAI 비용은?**     | GPT-4o mini 기준 \~\~￦0.59 / 1K tokens. 5문항·80명 → 1차시 약 ₩1,000 미만 |

---

## 🤝 Contributing

1. **Fork** → 2. 새 브랜치 생성(`feature/awesome`) → 3. PR

   * 문서·UI 한국어/영어 번역, 채점 룰 추가 모두 환영
2. Issue 템플릿에 따라 버그·제안 남겨주세요 🙏

---

## 🪪 License

[MIT](LICENSE) — 자유롭게 수정·배포 가능하나, 학습 데이터(학생 답안)는 학교 내부 정책을 준수하세요.

---

## 📄 참고 문헌 & 자료

* \<GPT와 함께하는 서술형 평가 자동 채점 및 피드백.pdf> — 시스템 설계 & 수업 사례
* <전기와 자기 서논술형 평가.pdf>, <서술형 채점 기준표.pdf> — 예시 문항 & 루브릭
* Bloom, B. S. (1984), **“The Search for Methods of Group Instruction as Effective as One-to-One Tutoring”**

```
```
