import streamlit as st
import time

# 새로운 질문 리스트
questions = [
    "1. 다양한 AI 도구(ChatGPT, DALL-E, Midjourney 등)를 사용해 본 경험이 있나요?",
    "2. AI를 활용하여 업무나 학습 효율성을 높인 경험이 있나요?",
    "3. AI의 한계와 잠재적 위험성에 대해 얼마나 이해하고 있나요?",
    "4. AI 기술의 최신 트렌드를 얼마나 자주 확인하시나요?",
    "5. AI 윤리와 관련된 이슈에 대해 얼마나 관심을 가지고 있나요?",
    "6. AI를 이용한 창작 활동(글쓰기, 이미지 생성 등)을 해본 적이 있나요?",
    "7. AI 관련 뉴스나 연구 논문을 얼마나 자주 읽으시나요?",
    "8. AI 기술이 미래 사회에 미칠 영향에 대해 얼마나 생각해 보셨나요?",
    "9. AI 프로그래밍이나 머신러닝에 대한 기초 지식이 있나요?",
    "10. AI를 활용한 개인 프로젝트나 업무 프로젝트를 진행해 본 적이 있나요?"
]

# 답변 옵션
options = [
    "전혀 아니다",
    "가끔 그렇다",
    "보통이다",
    "자주 그렇다",
    "매우 그렇다"
]

def calculate_score(answers):
    return sum([options.index(answer) + 1 for answer in answers])

def get_level(score):
    if score <= 10:
        return "초보자 레벨"
    elif score <= 20:
        return "기초 레벨"
    elif score <= 30:
        return "중급 레벨"
    elif score <= 40:
        return "고급 레벨"
    else:
        return "전문가 레벨"

def start_test():
    st.session_state.page = 1
    st.session_state.start_time = time.time()
    st.session_state.answers = []

def next_question():
    if len(st.session_state.answers) < st.session_state.page:
        st.session_state.answers.append(st.session_state.current_answer)
    st.session_state.page += 1

def prev_question():
    st.session_state.page -= 1
    if st.session_state.answers:
        st.session_state.answers.pop()

def main():
    st.set_page_config(page_title="AI 활용 지수 레벨 테스트", page_icon="🤖")
    
    st.title("AI 활용 지수 레벨 테스트")
    st.write("AI 도구 사용 경험을 바탕으로 당신의 AI 활용 수준을 측정합니다!")

    if 'page' not in st.session_state:
        st.session_state.page = 0

    if st.session_state.page == 0:
        st.write("테스트를 시작하려면 '시작' 버튼을 클릭하세요. (제한 시간: 5분)")
        st.button("시작", on_click=start_test)

    elif 1 <= st.session_state.page <= len(questions):
        # 시간 제한 체크
        elapsed_time = time.time() - st.session_state.start_time
        remaining_time = max(300 - int(elapsed_time), 0)  # 5분 = 300초
        st.info(f"남은 시간: {remaining_time}초")
        
        if elapsed_time > 300:
            st.warning("제한 시간이 초과되었습니다. 결과 페이지로 이동합니다.")
            st.session_state.page = len(questions) + 1
        else:
            question_index = st.session_state.page - 1
            st.write(questions[question_index])
            st.session_state.current_answer = st.radio("답변을 선택하세요:", options, key=f"question_{question_index}")

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("이전", on_click=prev_question, disabled=(st.session_state.page == 1)):
                    pass
            
            with col3:
                if st.button("다음", on_click=next_question):
                    pass

    elif st.session_state.page > len(questions):
        if len(st.session_state.answers) == len(questions):
            score = calculate_score(st.session_state.answers)
            level = get_level(score)
            
            st.success("테스트가 완료되었습니다!")
            st.write(f"당신의 점수: {score}점")
            st.write(f"당신의 AI 활용 레벨: {level}")
        else:
            st.warning("모든 질문에 답하지 않았습니다. 테스트를 다시 시작해주세요.")
        
        if st.button("테스트 다시 하기"):
            st.session_state.page = 0
            st.session_state.answers = []
            st.session_state.start_time = None

if __name__ == "__main__":
    main()