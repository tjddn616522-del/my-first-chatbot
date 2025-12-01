import streamlit as st
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# 1. 환경 변수 로드 (.env 파일이 같은 폴더에 있어야 함)
load_dotenv()

# ⭐️ 새로 추가된 부분 1: 페이지 설정 및 CSS (블루 테마) 적용 ⭐️
st.set_page_config(
    page_title="울산 고래 가이드",
    layout="wide",
    page_icon="🐳" # 고래 이모티콘으로 아이콘 변경
)

# ⭐️ [핵심] CSS를 사용하여 블루 테마를 강제로 적용하는 코드 ⭐️
st.markdown(
    f"""
    <style>
    /* 앱 배경 색상 (아주 밝은 하늘색) */
    .stApp {{
        background-color: #E9F4FF; 
        color: #1C3F60;
    }}
    /* 버튼, 드롭다운 테두리 등 주요 요소에 사용될 색상 (선명하고 시원한 블루) */
    .stButton>button, .stSelectbox > div, .stTextInput > div > div {{
        border: 1px solid #007BFF;
    }}
    /* 사이드바 배경 색상 (순백색) */
    .stSidebar {{
        background-color: #FFFFFF;
    }}
    /* 사이드바 제목 텍스트 색상 변경 */
    .css-1d3f9cr, .css-vk32z9, .css-1a6f8v0 {{ /* Streamlit 내부 클래스 */
        color: #007BFF; 
    }}
    </style>
    """,
    unsafe_allow_html=True
)
# ---------------------------------------------

st.title("🤖 울산 고래 가이드 챗봇") # 챗봇 이름을 컨셉에 맞게 변경

# 2. Azure OpenAI 클라이언트 설정
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OAI_KEY"),
    api_version="2024-05-01-preview",
    azure_endpoint=os.getenv("AZURE_OAI_ENDPOINT")
)

# ⭐️ 새로 추가된 부분 2: 사이드바 설정 ⭐️
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
if prompt := st.chat_input("울산에 대해 무엇이든 물어보세요."):
    # (1) 사용자 메시지 화면에 표시 & 저장
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # System Prompt를 먼저 정의합니다.
    system_message = {"role": "system", "content": f"너는 울산 토박이처럼 친절하고 전문적인 {selected_theme} 테마의 여행 가이드야. 모든 답변은 울산의 {selected_theme} 관련 코스 추천이나 명소 정보에 중점을 둬."}
    
    # AI에게 전달할 전체 대화 기록을 만듭니다.
    full_messages = [system_message] + st.session_state.messages

    # (2) AI 응답 생성
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            # ⭐️ [핵심!] 404 오류 해결: deployment_id를 사용해야 Azure에서 정상 작동 (model로 변경) ⭐️
            # NOTE: 이전 단계에서 404가 발생했으나, 현재 코드가 model을 사용하므로 그대로 유지하면서, 배포명이 정확해야 함을 안내합니다.
            model="ai058-gpt-4o-mini",
            messages=full_messages
        )
        assistant_reply = response.choices[0].message.content
        st.markdown(assistant_reply)

    # (3) AI 응답 저장
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})