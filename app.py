import streamlit as st
import requests  # 이건 파이썬 기본이라 에러가 안 납니다.
import json

# 1. 힐링 테마 설정
st.set_page_config(page_title="정선식 세법 힐링센터", page_icon="🌿")

st.markdown("""
    <style>
    .stApp { background-color: #fdfdfa; }
    .stButton > button { background-color: #a3d9c9; color: white; border-radius: 20px; border: none; font-weight: bold; }
    .stButton > button:hover { background-color: #8dcabd; }
    </style>
    """, unsafe_allow_value=True)

# 2. 사이드바 API 키 입력
with st.sidebar:
    st.title("🗝️ 연결 엔진")
    api_key = st.text_input("Gemini API Key를 넣어주세요", type="password")
    st.caption("라이브러리 없이 직접 연결하는 보안 모드입니다.")

# 3. 메인 화면
st.title("🌿 정선식 세법 힐링센터")
st.subheader("본부장님, 이제 '그 줄'은 없습니다. 바로 시작하시죠.")
st.write("---")

# 세션 상태 초기화
if 'query' not in st.session_state:
    st.session_state.query = ""

# 4. 단순화된 퀵 버튼 (UX)
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

# 6. AI 로직 (라이브러리 없이 직접 호출하는 방식)
if query and api_key:
    try:
        # 구글 AI 서버에 직접 편지를 보냅니다 (API 호출)
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
            
            # 결과물 출력
            answer = result['candidates'][0]['content']['parts'][0]['text']
            st.success("해석이 완료되었습니다!")
            st.markdown(answer)

    except Exception as e:
        st.error("연결에 문제가 있습니다. API 키를 확인하시거나 잠시 후 다시 시도해주세요.")

