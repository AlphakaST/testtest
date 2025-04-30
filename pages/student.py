# .streamlit/secrets.toml 예시:
# [openai]
# api_key = "YOUR_OPENAI_API_KEY"
#
# [mysql]
# host = "YOUR_MYSQL_HOST"
# user = "YOUR_MYSQL_USER"
# password = "YOUR_MYSQL_PASSWORD"
# database = "YOUR_DATABASE_NAME"
# port = 3306

# MySQL 테이블 생성 명령어 (워크벤치에서 실행):
# CREATE TABLE test1 (
#     student_id VARCHAR(5) NOT NULL,
#     answer1 TEXT,
#     answer2 TEXT,
#     answer3 TEXT,
#     answer4 TEXT,
#     answer5 TEXT,
#     feedback1 TEXT,
#     feedback2 TEXT,
#     feedback3 TEXT,
#     feedback4 TEXT,
#     feedback5 TEXT,
#     submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     PRIMARY KEY (student_id, submitted_at)
# );

import streamlit as st
import os
import openai
import mysql.connector
from mysql.connector import Error

st.title("과학 서술형 평가")


# 비밀 정보 로드
openai.api_key = st.secrets["openai"]["api_key"]
mysql_conf = st.secrets["mysql"]

# MySQL 연결 함수
def get_mysql_connection():
    try:
        return mysql.connector.connect(
            host=mysql_conf["host"],
            user=mysql_conf["user"],
            password=mysql_conf["password"],
            database=mysql_conf["database"],
            port=mysql_conf.get("port", 3306)
        )
    except Error as e:
        st.error(f"MySQL 연결 오류: {e}")
        return None


# -----------------------------------------
# 사용자 정의 영역: 문항, 그림, 예시 답안, 채점 기준
question_texts = [
    "문제 1) 다음은 정전기 유도 현상을 알아보기 위한 실험이다. (가)의 금속박에 대전된 전하의 종류(2점)를 쓰고, [결과]에서 금속박이 벌어진 이유(5점)에 대해 <조건>을 모두 포함하여 서술하시오.",
    "문제 2) 다음은 알루미늄박을 스탠드에 실로 매달아 가만히 놓은 후 음(-)전하로 대전되어 있는 PVC 막대를 알루미늄박에 가까이 하였더니 알루미늄박이 끌여와 PVC막대와 접촉한 것을 나타낸 것이다. 접촉한 이유, PVC막대와 알루미늄박은 서로 미는지 또는 당기는지 쓰고(2점), 그 이유(5점)에 대해 <조건>을 모두 포함하여 설명하시오.",
    "문제 3) (가)는 사람의 몸에 전류가 흐를 때 나타나는 효과를, (나)는 사람 몸의 상태에 따른 저항을 나타낸 것이다. (가)와 (나)를 이용하여 젖은 손으로 전기기구를 만지면 위험한 이유를 <조건>에 맞게 서술하시오.",
    "문제 4) 다음은 어떤 학생이 수행한 탐구 활동의 과정과 결과의 일부이다. A, B는 각각 전압계와 전류계 중의 하나이다. 물음에 답하시오. A와 B 중에 어떤 것이 전압계인지 쓰고, 그 이유를 서술하시오.",
    "문제 5) 다른 조건은 그대로 하고, 짧은 니크롬선을 긴 니크롬선으로 바꾸어 위 실험을 실행하였을 때, 니크롬선의 길이가 길어지면 저항의 크기가 어떻게 변하는지 쓰고 <그래프2>의 기울기가, 짧은 니크롬선으로 실험하였을 때와 비교하여 어떻게 달라지는지 서술하시오."
]

image_paths = [
    "images/q1.png",
    "images/q2.png",
    "images/q3.png",
    "images/q4.png",
    "images/q5.png"
]

example_answers = [
    "양(+) 전하, 금속박에서 금속판으로 음(-)전하(또는 전자)가 이동하기 때문이다.",
    "밀어낸다(민다), PVC막대에 있는 음(-)전하가 알루미늄박으로 이동하여 알루미늄박이 음(-)전하로 대전되기 때문이다.",
    "젖은 손이 마른 손보다 저항값이 작아 전기기구를 만질 경우, 몸에 강한(높은) 전류가 흐를 수 있어 위험하다.",
    "A이다. A와 B 중에서 니크롬선(저항)에 병렬로 연결된 장치는 A이므로 A가 전압계이다.",
    "긴 니크롬선은 짧은 니크롬선보다 저항값이 크다. 저항값이 커지면 같은 전압에서 회로에 흐르는 전류의 세기가 작아지므로, 그래프의 기울기가 작아진다."
]

grading_criteria = [
    "양(+) 전하, 금속박에서 금속판으로 음(-)전하(또는 전자)가 이동하기 때문이다. 만약 '양(+) 전하, 금속박에서 금속판으로 음(-)전하(또는 전자)가 이동하기 때문이다.'라고 했다면 조금 더 보완할 필요가 있는 답안입니다.",
    "전자가 알루미늄박으로 이동하여 알루미늄박이 음(-)전하로 대전되기 때문이다.",
    "젖은 손이 저항값이 작다는 것과 전류가 많이 흐른다는 점을 모두 옳게 언급한 경우.",
    "A와 B 중에서 A가 전압계라고 쓰고, 그 이유가 저항에 병렬로 연결되어 있기 때문임을 서술한 경우.",
    "긴 니크롬선의 저항값이 짧은 니크롬선보다 크고, 회로의 저항값이 크면, 같은 전압에서 회로에 흐르는 전류의 세기가 작아지므로, 그래프의 기울기가 작아진다고 기술한 경우."
]
# -----------------------------------------

# 학생 학번 입력
student_id = st.text_input("학번을 입력하세요 (예: 30101)", max_chars=5)

# 학생 답안을 저장할 리스트
answers = []
# 문항 표시 및 답안 입력
for idx, question in enumerate(question_texts):
    st.markdown(f"### 문제 {idx+1}")
    path = image_paths[idx]
    if path and os.path.exists(path):
        st.image(path, use_container_width=True)
    answers.append(st.text_area(label="답안을 입력하세요.", key=f"answer_{idx}", height=150))

st.markdown("---")

# 제출 및 채점/저장
if st.button("제출"):
    # 유효성 검사
    if not (student_id.isdigit() and len(student_id)==5):
        st.error("유효한 5자리 학번을 입력해주세요.")
    elif any(not ans.strip() for ans in answers):
        st.error("모든 문항에 답안을 작성해야 제출할 수 있습니다.")
    else:
        grades = []
        with st.spinner("채점 중입니다..."):
            for idx, ans in enumerate(answers):
                prompt = (
                    f"예시 답안: {example_answers[idx]}\n"
                    f"채점 기준: {grading_criteria[idx]}\n"
                    f"학생 답안: {ans}\n\n"
                    "200자 이내로 친절한 어조로 평가 결과를 요약해주세요."
                )
                try:
                    resp = openai.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role":"system","content":"당신은 학생들에게 친절하게 피드백을 제공하는 과학 교사입니다."},
                            {"role":"user","content":prompt}
                        ],
                        max_tokens=150, temperature=0.7
                    )
                    grades.append(resp.choices[0].message.content.strip())
                except Exception as e:
                    grades.append(f"채점 오류: {e}")

        # MySQL 저장
        conn = get_mysql_connection()
        if conn:
            cursor = conn.cursor()
            sql = (
                "INSERT INTO test1 (student_id, answer1, answer2, answer3, answer4, answer5,"
                " feedback1, feedback2, feedback3, feedback4, feedback5)"
                " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            )
            try:
                cursor.execute(sql, [student_id]+answers+grades)
                conn.commit()
                st.success("제출 및 저장 완료되었습니다.")
            except Error as e:
                st.error(f"DB 저장 오류: {e}")
            finally:
                cursor.close(); conn.close()

        # 결과 표시
        st.markdown(f"**학번:** {student_id}")
        for idx, (ans, fb) in enumerate(zip(answers, grades)):
            st.markdown(f"#### 문제 {idx+1}")
            st.write(f"**학생 답안:** {ans}")
            st.write(f"**피드백:** {fb}")
