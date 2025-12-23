import streamlit as st
import pandas as pd
import random
import os

# ====================================
# 페이지 설정
# ====================================
st.set_page_config(
    page_title="1인 가구 웰니스 상담 챗봇",
    page_icon="💬",
    layout="centered"
)

# ====================================
# CSS 스타일
# ====================================
st.markdown("""
<style>
    .main {max-width: 800px; margin: 0 auto;}
    .stChatMessage {border-radius: 15px; padding: 15px; margin: 10px 0;}
    h1 {text-align: center; color: #4A90E2; font-size: 1.8rem;}
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        font-size: 16px;
        font-weight: bold;
    }
    .password-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        font-size: 18px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ====================================
# 데이터셋 로드
# ====================================
@st.cache_data
def load_wellness_dataset():
    """웰니스 데이터셋 로드"""
    script_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else os.getcwd()
    
    possible_paths = [
        os.path.join(script_dir, 'aihub_counsel_pairs.csv'),
        'aihub_counsel_pairs.csv',
    ]
    
    df = None
    for path in possible_paths:
        if os.path.exists(path):
            try:
                df = pd.read_csv(path, encoding='utf-8')
                st.success(f"✅ 데이터 로드: {path} ({len(df):,}개)")
                break
            except:
                try:
                    df = pd.read_csv(path, encoding='cp949')
                    st.success(f"✅ 데이터 로드: {path} ({len(df):,}개)")
                    break
                except:
                    continue
    
    if df is None:
        st.info("💡 CSV 파일 없음 - 기본 응답 모드로 작동")
        return pd.DataFrame()
    
    # 컬럼명 정규화
    column_mapping = {
        '내담자': '유저', '상담사': '챗봇',
        'user': '유저', 'bot': '챗봇',
    }
    df = df.rename(columns=column_mapping)
    
    # 빈 데이터 제거
    if '유저' in df.columns and '챗봇' in df.columns:
        df = df[df['유저'].notna() & df['챗봇'].notna()]
        df = df[df['유저'].str.strip() != '']
        df = df[df['챗봇'].str.strip() != '']
        
        # 응답 길이 필터링 (너무 긴 응답 제외 - 100자 이하만)
        df = df[df['챗봇'].str.len() <= 100]
        
        # @NAME 등 불필요한 패턴 제거
        df = df[~df['챗봇'].str.contains('@NAME|@name', na=False)]
        df = df[~df['챗봇'].str.contains('님이|님은|님의', na=False)]
    
    return df

df = load_wellness_dataset()

# ====================================
# 30개 단체활동 데이터
# ====================================
ACTIVITIES = [
    {"name": "실내 클라이밍", "category": "스포츠", "difficulty": "중", "description": "함께 응원하며 성취감을 느낄 수 있어요"},
    {"name": "독서 토론", "category": "자기계발", "difficulty": "중", "description": "생각을 나누며 연결감을 느낄 수 있어요"},
    {"name": "보드게임 모임", "category": "취미", "difficulty": "초", "description": "가볍게 웃으며 사람들과 어울릴 수 있어요"},
    {"name": "명상 모임", "category": "라이프", "difficulty": "초", "description": "조용히 함께하며 마음의 안정을 찾아요"},
    {"name": "플라워 클래스", "category": "예술", "difficulty": "초", "description": "아름다운 것을 만들며 기분전환이 돼요"},
    {"name": "트레킹", "category": "아웃도어", "difficulty": "초", "description": "걸으며 자연스럽게 대화할 수 있어요"},
    {"name": "영화 모임", "category": "예술", "difficulty": "초", "description": "같이 보고 이야기 나누는 재미가 있어요"},
    {"name": "우쿨렐레", "category": "예술", "difficulty": "초", "description": "함께 연주하며 즐거움을 느껴요"},
    {"name": "캔들 공예", "category": "예술", "difficulty": "초", "description": "만들기에 집중하며 힐링할 수 있어요"},
    {"name": "맛집 탐방", "category": "미식", "difficulty": "초", "description": "맛있는 음식을 함께 즐길 수 있어요"},
    {"name": "반찬 나눔", "category": "라이프", "difficulty": "초", "description": "서로 챙기는 따뜻함을 느낄 수 있어요"},
    {"name": "봉사 활동", "category": "봉사", "difficulty": "초", "description": "누군가를 도우며 보람을 느껴요"},
    {"name": "노래방 모임", "category": "취미", "difficulty": "초", "description": "마음껏 노래하며 스트레스를 풀어요"},
    {"name": "피크닉", "category": "라이프", "difficulty": "초", "description": "야외에서 여유롭게 시간을 보내요"},
    {"name": "요가 클래스", "category": "스포츠", "difficulty": "초", "description": "함께 호흡하며 몸과 마음을 돌봐요"},
]

# ====================================
# 상담 질문 풀 (자연스러운 흐름)
# ====================================
QUESTION_POOL = [
    {"id": 1, "text": "혼자 지내면서 요즘 어떠세요?", "keywords": ["혼자", "요즘"], "phase": 1},
    {"id": 2, "text": "그게 언제부터 그러셨어요?", "keywords": ["언제", "시작"], "phase": 1},
    {"id": 3, "text": "그럴 때 어떻게 지내세요?", "keywords": ["어떻게", "보통"], "phase": 1},
    {"id": 4, "text": "요즘 하루 중에 가장 힘든 순간은 언제예요?", "keywords": ["하루", "힘든"], "phase": 2},
    {"id": 5, "text": "그런 기분이 들 때 어떤 생각이 드세요?", "keywords": ["기분", "생각"], "phase": 2},
    {"id": 6, "text": "주변에 이런 마음을 나눌 사람이 있으세요?", "keywords": ["주변", "사람"], "phase": 2},
    {"id": 7, "text": "요즘 잠은 잘 주무세요?", "keywords": ["잠", "수면"], "phase": 2},
    {"id": 8, "text": "밥은 잘 챙겨 드시고 계세요?", "keywords": ["밥", "식사"], "phase": 2},
    {"id": 9, "text": "쉬는 날에는 주로 뭐 하세요?", "keywords": ["쉬는 날", "주말"], "phase": 2},
    {"id": 10, "text": "예전에 사람들이랑 있을 때는 어땠어요?", "keywords": ["예전", "사람"], "phase": 3},
    {"id": 11, "text": "요즘은 사람 만나는 게 어떠세요?", "keywords": ["사람", "만나"], "phase": 3},
    {"id": 12, "text": "부담 없이 할 수 있는 활동이 있다면 해보고 싶으세요?", "keywords": ["활동", "해보고"], "phase": 3},
]

# ====================================
# 공감 응답 생성 (짧고 자연스럽게)
# ====================================
def generate_empathy_response(user_input):
    """사용자 입력에 대한 짧은 공감 응답"""
    user_lower = user_input.lower()
    
    # 키워드 기반 공감 (짧게)
    empathy_map = {
        '외로': ["외로우셨겠어요.", "혼자라는 느낌이 크셨겠네요.", "그 외로움이 느껴져요."],
        '혼자': ["혼자 지내는 게 쉽지 않죠.", "혼자라서 더 그러셨을 것 같아요."],
        '힘들': ["많이 힘드셨겠어요.", "그거 정말 힘들죠.", "힘든 시간을 보내고 계시네요."],
        '지치': ["많이 지치셨겠어요.", "그러면 지칠 수밖에 없어요."],
        '우울': ["기분이 가라앉으셨군요.", "마음이 무거우셨겠어요."],
        '불안': ["불안하셨겠어요.", "마음이 편하지 않으셨겠네요."],
        '무기력': ["의욕이 없으셨군요.", "그런 날이 있죠."],
        '답답': ["답답하셨겠어요.", "그 답답함이 느껴져요."],
        '걱정': ["걱정이 많으시네요.", "신경 쓰이는 게 많으셨겠어요."],
        '슬프': ["마음이 아프셨겠어요.", "슬프셨겠네요."],
        '짜증': ["짜증이 나셨겠어요.", "그러면 예민해질 수 있어요."],
        '화가': ["화가 나셨겠어요.", "그런 상황이면 화날 수 있어요."],
        '없어': ["그렇군요.", "그런 상황이시군요."],
        '못': ["그러셨군요.", "쉽지 않으셨겠어요."],
        '안': ["그렇군요.", "그런 느낌이 드셨군요."],
    }
    
    for keyword, responses in empathy_map.items():
        if keyword in user_lower:
            return random.choice(responses)
    
    # 기본 공감
    default = [
        "그렇군요.",
        "네, 들었어요.",
        "그런 마음이 드셨군요.",
        "이야기해주셔서 고마워요.",
    ]
    return random.choice(default)

# ====================================
# 다음 질문 선택
# ====================================
def select_next_question(asked_ids, current_phase):
    """현재 단계에 맞는 질문 선택"""
    # 현재 단계 질문 중 안 한 것
    remaining = [q for q in QUESTION_POOL 
                 if q['id'] not in asked_ids and q['phase'] <= current_phase + 1]
    
    if not remaining:
        return None
    
    # 현재 단계 우선
    current_phase_q = [q for q in remaining if q['phase'] == current_phase]
    if current_phase_q:
        return random.choice(current_phase_q)
    
    return random.choice(remaining)

# ====================================
# 사용자 상태 분석
# ====================================
def analyze_user_state(messages):
    """사용자 상태 분석"""
    full_text = " ".join([m['content'] for m in messages if m['role'] == 'user']).lower()
    
    state = {
        '고립감': 0, '우울감': 0, '저활동성': 0,
        '불안': 0, '사회적욕구': 0, '관계부담': 0
    }
    
    keywords = {
        '고립감': ['혼자', '외롭', '쓸쓸', '아무도', '적막', '허전'],
        '우울감': ['우울', '무기력', '힘들', '지쳐', '슬프', '답답'],
        '저활동성': ['집', '안나가', '누워', '방', '침대', '귀찮'],
        '불안': ['불안', '걱정', '두렵', '긴장', '초조'],
        '사회적욕구': ['사람', '친구', '만나', '모임', '대화', '함께'],
        '관계부담': ['부담', '피곤', '에너지', '피하']
    }
    
    for state_name, words in keywords.items():
        for word in words:
            if word in full_text:
                state[state_name] += 1
    
    return state

# ====================================
# 활동 추천
# ====================================
def recommend_activities(user_state):
    """사용자 상태에 맞는 활동 3개 추천"""
    scored = []
    
    for activity in ACTIVITIES:
        score = random.randint(1, 3)
        
        if user_state['고립감'] > 0 and activity['difficulty'] == '초':
            score += 2
        if user_state['관계부담'] > 0 and activity['difficulty'] == '초':
            score += 2
        if user_state['우울감'] > 0 and activity['category'] in ['예술', '아웃도어']:
            score += 1
            
        scored.append({'activity': activity, 'score': score})
    
    scored.sort(key=lambda x: x['score'], reverse=True)
    
    # 카테고리 다양하게
    recommendations = []
    used_categories = set()
    
    for item in scored:
        if len(recommendations) >= 3:
            break
        cat = item['activity']['category']
        if cat not in used_categories:
            recommendations.append(item['activity'])
            used_categories.add(cat)
    
    return recommendations

# ====================================
# 추천 메시지 생성
# ====================================
def generate_recommendation_message(recommendations, user_state, user_count):
    """추천 결과 메시지"""
    msg = "### 💭 이야기를 들어보니\n\n"
    
    if user_state['고립감'] > 0:
        msg += "혼자 지내는 시간이 길어지면서 외로움을 느끼고 계신 것 같아요.\n\n"
    elif user_state['우울감'] > 0:
        msg += "요즘 마음이 좀 가라앉아 계신 것 같아요.\n\n"
    else:
        msg += "혼자 지내면서 여러 생각이 드시는 것 같아요.\n\n"
    
    msg += "혼자 버티지 않아도 괜찮아요.\n\n"
    msg += f'<div class="stat-box">💡 지금 비슷한 상황의 사람들 {user_count}명이 함께하고 있어요</div>\n\n'
    
    msg += "### 🎯 이런 활동은 어떨까요?\n\n"
    
    for i, rec in enumerate(recommendations, 1):
        msg += f"**{i}. {rec['name']}**\n"
        msg += f"{rec['description']}\n\n"
    
    msg += "---\n\n"
    msg += "### 🚪 다음 단계\n\n"
    msg += "비슷한 상황의 분들이 모인 **카카오톡 채팅방**이 있어요.\n\n"
    msg += '<div class="password-box">🔐 입장 비밀번호: 1101</div>\n\n'
    msg += "준비되실 때 편하게 들어오세요 😊\n"
    
    return msg

# ====================================
# 세션 초기화
# ====================================
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.asked_question_ids = []
    st.session_state.question_count = 0
    st.session_state.counseling_done = False
    st.session_state.user_count = random.randint(150, 280)
    st.session_state.current_phase = 1
    
    initial_msg = "안녕하세요 🙂\n\n혼자 지내시면서 요즘 어떠세요?"
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": initial_msg
    })
    st.session_state.asked_question_ids.append(1)
    st.session_state.question_count = 1

# ====================================
# UI 렌더링
# ====================================
st.title("💬 1인 가구 웰니스 상담 챗봇")
st.caption("당신의 이야기를 들려주세요.")

# 대화 히스토리 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and ("stat-box" in message["content"] or "password-box" in message["content"]):
            st.markdown(message["content"], unsafe_allow_html=True)
        else:
            st.markdown(message["content"])

# 사용자 입력
if prompt := st.chat_input("메시지를 입력하세요"):
    user_input = prompt
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    if not st.session_state.counseling_done:
        user_msg_count = len([m for m in st.session_state.messages if m['role'] == 'user'])
        
        # 단계 업데이트
        if user_msg_count >= 3:
            st.session_state.current_phase = 2
        if user_msg_count >= 6:
            st.session_state.current_phase = 3
        
        # 10번 대화 후 추천
        if user_msg_count >= 10:
            user_state = analyze_user_state(st.session_state.messages)
            recommendations = recommend_activities(user_state)
            response = generate_recommendation_message(
                recommendations,
                user_state,
                st.session_state.user_count
            )
            st.session_state.counseling_done = True
        else:
            # 공감 + 질문
            empathy = generate_empathy_response(user_input)
            next_q = select_next_question(
                st.session_state.asked_question_ids,
                st.session_state.current_phase
            )
            
            if next_q:
                st.session_state.asked_question_ids.append(next_q['id'])
                st.session_state.question_count += 1
                response = f"{empathy}\n\n{next_q['text']}"
            else:
                response = f"{empathy}\n\n조금 더 이야기해주실 수 있을까요?"
    else:
        response = "추가로 이야기하고 싶은 게 있으시면 말씀해주세요 😊"
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        if "stat-box" in response or "password-box" in response:
            st.markdown(response, unsafe_allow_html=True)
        else:
            st.markdown(response)
    
    st.rerun()

# ====================================
# 사이드바
# ====================================
with st.sidebar:
    st.header("ℹ️ 서비스 안내")
    st.write(f"""
**고객상담 참여자**

👥 {st.session_state.user_count}명

---

**상담상담 상황**

📝 질문 {st.session_state.question_count}/10

---

**데이터 상태**

📋 웰니스 데이터: {len(df) if not df.empty else 0}개
📋 추천활동: {len(ACTIVITIES)}개
    """)
    
    if st.button("🔄 대화하기"):
        st.session_state.clear()
        st.rerun()