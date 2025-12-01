import streamlit as st
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# 1. 환경 변수 로드 (.env 파일이 같은 폴더에 있어야 함)
load_dotenv()

st.title("🤖 나의 첫 AI 챗봇")

# 2. Azure OpenAI 클라이언트 설정
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OAI_KEY"),
    api_version="2024-05-01-preview",
    azure_endpoint=os.getenv("AZURE_OAI_ENDPOINT")
)

# ⭐️ 새로 추가된 부분 1: 사이드바 설정 ⭐️
with st.sidebar:
    st.header("✨ 울산 테마 선택")
    selected_theme = st.selectbox("어떤 여행 테마를 원하세요?", ["전체", "자연/힐링", "역사/문화", "맛집/미식"])
# ---------------------------------------------

# 3. 대화기록(Session State) 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. 화면에 기존 대화 내용 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 사용자 입력 받기
if prompt := st.chat_input("무엇을 도와드릴까요?"):
    # (1) 사용자 메시지 화면에 표시 & 저장
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # ⭐️ [핵심] System Prompt를 포함한 새로운 messages 리스트 생성 (문법 오류 해결) ⭐️
    # System Prompt를 먼저 정의합니다.
    system_message = {"role": "system", "content": f"너는 울산 토박이처럼 친절하고 전문적인 {selected_theme} 테마의 여행 가이드야. 모든 답변은 울산의 {selected_theme} 관련 코스 추천이나 명소 정보에 중점을 둬."}
    
    # AI에게 전달할 전체 대화 기록을 만듭니다. (System Message + 기존 대화)
    # 이 방식으로 리스트를 합쳐야 문법 오류가 나지 않습니다.
    full_messages = [system_message] + st.session_state.messages

    # (2) AI 응답 생성
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            # ⭐️ 배포명은 "ai058-gpt-4o-mini"로 가정하고 진행합니다. ⭐️
            model="ai058-gpt-4o-mini",
            messages=full_messages # ⭐️ 오류 없는 full_messages 사용 ⭐️
        )
        assistant_reply = response.choices[0].message.content
        st.markdown(assistant_reply)

    # (3) AI 응답 저장
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})