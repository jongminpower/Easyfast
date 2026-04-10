import streamlit as st
import google.generativeai as genai

# 1. 힐링 테마 설정
st.set_page_config(page_title="정선식 세법 힐링센터", page_icon="🌿")

st.markdown("""
    <style>
    .stApp { background-color: #fdfdfa; }
    .stButton > button { background-color: #a3d9c9; color: white; border-radius: 20px; }
    </style>
    """, unsafe_allow_value=True)

# 2. 사이드바 API 키 입력
with st.sidebar:
    st.title("🗝️ 연결 엔진")
    api_key = st.text_input("Gemini API Key를 넣어주세요", type="password")

# 3. 메인 화면
st.title("🌿 정선식 세법 힐링센터")
st.info("본부장님, requirements.txt 파일을 만드셨다면 이제 정상 작동할 겁니다.")

# 세션 상태 초기화
if 'query' not in st.session_state:
    st.session_state.query = ""

# 퀵 버튼
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🚛 타사업장 반출"): st.session_state.query = "타사업장 반출"
with col2:
    if st.button("🏠 간주임대료"): st.session_state.query = "간주임대료"
with col3:
    if st.button("💰 매입세액 공제"): st.session_state.query = "매입세액 공제"

# 입력창
query = st.text_input("궁금한 용어를 입력하세요", value=st.session_state.query)

if query and api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"너는 정선식 세법 힐링 멘토다. '{query}'를 공감-본질-비유-요약 순으로 다정하게 설명해줘."
        
        with st.spinner('해석 중...'):
            response = model.generate_content(prompt)
            st.markdown(response.text)
    except Exception as e:
        st.error(f"에러 발생: {e}")

