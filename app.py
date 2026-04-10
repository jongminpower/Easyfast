import streamlit as st
import google.generativeai as genai  # 두 번째 줄, 다시 확실히 잡았습니다!

# 1. 페이지 설정 (심리적 안정감을 주는 컬러)
st.set_page_config(page_title="정선식 세법 힐링센터", page_icon="🌿", layout="centered")

# --- 🎨 본부장님 전용 힐링 디자인 (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #fdfdfa; }
    h1, h2, h3, p { color: #4a4a4a !important; }
    .stButton > button {
        background-color: #a3d9c9;
        color: white;
        border-radius: 20px;
        border: none;
        font-weight: bold;
    }
    .stButton > button:hover { background-color: #8dcabd; }
    </style>
    """, unsafe_allow_value=True)

# 2. 사이드바 API 설정
with st.sidebar:
    st.markdown("### 🗝️ 시스템 연결")
    api_key = st.text_input("Gemini API Key를 입력하세요", type="password")

# 3. 메인 화면
st.title("🌿 정선식 세법 힐링센터")
st.subheader("본부장님, 이제 에러 없이 편안하게 시작하세요.")
st.write("---")

# 4. 단순화된 퀵 버튼 (UX 개선)
st.write("💡 궁금한 주제를 선택하거나 입력하세요.")
col1, col2, col3 = st.columns(3)

# 버튼 클릭 시 입력창에 들어갈 수 있도록 세션 스테이트 활용
if 'query' not in st.session_state:
    st.session_state.query = ""

with col1:
    if st.button("🚛 타사업장 반출"):
        st.session_state.query = "타사업장 반출"
with col2:
    if st.button("🏠 간주임대료"):
        st.session_state.query = "간주임대료"
with col3:
    if st.button("💰 매입세액 공제"):
        st.session_state.query = "매입세액 공제"

# 5. 사용자 입력창
query = st.text_input("지금 어떤 세법 용어가 당신을 괴롭히나요?", value=st.session_state.query)

# 6. AI 로직
if query and api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        너는 '정선식 세법 힐링 멘토'다. 
        '{query}'라는 용어를 다음 원칙으로 설명해.
        1. [공감]: 다정한 위로로 시작.
        2. [본질]: 왜 이 법이 생겼는지 아주 쉽게.
        3. [정선식 비유]: 경선식 스타일의 직관적 사례.
        4. [한줄 요약]: 핵심 암기 포인트.
        """
        
        with st.spinner('최적의 비유를 찾는 중... ☕'):
            response = model.generate_content(prompt)
            st.success("해석이 완료되었습니다!")
            st.markdown(response.text)

    except Exception as e:
        st.error(f"연결 에러가 발생했습니다. API 키를 확인해 주세요: {e}")
