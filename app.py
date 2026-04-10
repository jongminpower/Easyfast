import streamlit as st
import requests  # 👈 이건 에러가 절대 안 납니다!
import json

# 1. 힐링 테마 설정 (심리적 안정감을 주는 디자인)
st.set_page_config(page_title="정선식 세법 힐링센터", page_icon="🌿")

st.markdown("""
    <style>
    .stApp { background-color: #fdfdfa; }
    .stButton > button { background-color: #a3d9c9; color: white; border-radius: 20px; border: none; font-weight: bold; }
    .stButton > button:hover { background-color: #8dcabd; }
    </style>
    """, unsafe_allow_value=True)

# 2. 사이드바 - 열쇠(API 키) 입력
with st.sidebar:
    st.title("🗝️ 시스템 연결")
    api_key = st.text_input("Gemini API Key를 넣어주세요", type="password")
    st.caption("라이브러리 없이 직접 연결하는 보안 모드입니다.")

# 3. 메인 화면
st.title("🌿 정선식 세법 힐링센터")
st.subheader("본부장님, 에러의 주범인 '두 번째 줄'을 아예 삭제했습니다.")
st.write("---")

# 세션 상태 초기화
if 'query' not in st.session_state:
    st.session_state.query = ""

# 4. 단순화된 퀵 버튼
st.write("💡 궁금한 주제를 선택하세요.")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🚛 타사업장 반출"): st.session_state.query = "타사업장 반출"
with col2:
    if st.button("🏠 간주임대료"): st.session_state.query = "간주임대료"
with col3:
    if st.button("💰 매입세액 공제"): st.session_state.query = "매입세액 공제"

# 5. 사용자 입력창
query = st.text_input("지금 어떤 세법 용어가 당신을 괴롭히나요?", value=st.session_state.query)

# 6. AI 로직 (라이브러리 없이 직접 호출)
if query and api_key:
    try:
        # 구글 AI 서버 주소로 직접 메시지를 보냅니다.
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"너는 '정선식 세법 힐링 멘토'다. '{query}'를 다음 4단계로 다정하게 설명해줘. 1.공감 2.법의본질 3.정선식비유(경선식스타일) 4.한줄요약"
                }]
            }]
        }
        
        with st.spinner('본부장님, 최적의 비유를 가져오는 중입니다... ☕'):
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            result = response.json()
            
            # AI의 답변만 쏙 골라냅니다.
            answer = result['candidates'][0]['content']['parts'][0]['text']
            st.success("해석이 완료되었습니다!")
            st.markdown(answer)

    except Exception as e:
        st.error("연결에 문제가 있거나 API 키가 잘못되었습니다. 키를 확인해 주세요.")

