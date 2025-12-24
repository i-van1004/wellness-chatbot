# -*- coding: utf-8 -*-
import streamlit as st
import random
import time

# ====================================
# 페이지 설정
# ====================================
st.set_page_config(
    page_title="1인 가구 웰니스 상담",
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
    
    .summary-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
        border-radius: 20px;
        padding: 28px;
        margin: 24px 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    }
    
    .summary-card h3 {
        color: #2d3748;
        font-size: 18px;
        margin-bottom: 16px;
    }
    
    .summary-text {
        color: #4a5568;
        font-size: 15px;
        line-height: 1.7;
    }
    
    .summary-encourage {
        color: #667eea;
        font-size: 14px;
        margin-top: 16px;
    }
    
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px 28px;
        border-radius: 16px;
        text-align: center;
        margin: 24px 0;
        font-size: 16px;
        font-weight: 600;
    }
    
    .activity-card {
        background: white;
        border-radius: 16px;
        padding: 20px 24px;
        margin: 16px 0;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border-left: 4px solid #667eea;
    }
    
    .activity-name {
        font-size: 16px;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 8px;
    }
    
    .activity-desc {
        font-size: 14px;
        color: #4a5568;
        margin-bottom: 12px;
    }
    
    .activity-effect {
        display: inline-block;
        background: #edf2f7;
        color: #4a5568;
        font-size: 12px;
        padding: 6px 12px;
        border-radius: 20px;
        margin-right: 8px;
    }
    
    .activity-detail {
        font-size: 13px;
        color: #718096;
        margin-top: 12px;
        padding-top: 12px;
        border-top: 1px solid #e2e8f0;
    }
    
    .kakao-section {
        background: #fafbfc;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 28px;
        margin: 28px 0;
    }
    
    .kakao-title {
        font-size: 16px;
        color: #4a5568;
        font-weight: 500;
        margin-bottom: 12px;
    }
    
    .kakao-desc {
        font-size: 14px;
        color: #718096;
        line-height: 1.7;
        margin-bottom: 20px;
    }
    
    .kakao-fit {
        font-size: 13px;
        color: #a0aec0;
        margin-bottom: 20px;
        padding: 16px;
        background: white;
        border-radius: 12px;
    }
    
    .kakao-password {
        display: inline-block;
        background: white;
        border: 1px dashed #cbd5e0;
        padding: 10px 20px;
        border-radius: 8px;
        font-size: 14px;
        color: #4a5568;
    }
    
    .kakao-note {
        font-size: 12px;
        color: #a0aec0;
        margin-top: 16px;
    }
    
    .counseling-section {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 24px;
        margin: 24px 0;
    }
    
    .counseling-title {
        font-size: 15px;
        color: #4a5568;
        font-weight: 500;
        margin-bottom: 12px;
    }
    
    .counseling-item {
        font-size: 14px;
        color: #4a5568;
        margin: 10px 0;
    }
    
    .crisis-section {
        background: linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%);
        border: 1px solid #feb2b2;
        border-radius: 16px;
        padding: 28px;
        margin: 24px 0;
    }
    
    .crisis-title {
        font-size: 17px;
        color: #c53030;
        font-weight: 600;
        margin-bottom: 12px;
    }
    
    .crisis-item {
        font-size: 15px;
        color: #742a2a;
        margin: 12px 0;
        padding: 12px 16px;
        background: white;
        border-radius: 10px;
    }
    
    .closing-text {
        text-align: center;
        color: #a0aec0;
        font-size: 14px;
        margin-top: 32px;
        padding-top: 24px;
        border-top: 1px solid #e2e8f0;
    }
    
    .divider {
        height: 1px;
        background: #e2e8f0;
        margin: 28px 0;
    }
    
    .encourage-box {
        background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 100%);
        border-radius: 16px;
        padding: 24px;
        margin: 24px 0;
        border-left: 4px solid #00acc1;
    }
    
    .encourage-title {
        font-size: 16px;
        color: #00838f;
        font-weight: 600;
        margin-bottom: 12px;
    }
    
    .encourage-text {
        font-size: 14px;
        color: #006064;
        line-height: 1.8;
    }
    
    .tip-box {
        background: #fffbeb;
        border-radius: 12px;
        padding: 16px;
        margin: 16px 0;
        border-left: 4px solid #f59e0b;
    }
    
    .tip-text {
        font-size: 14px;
        color: #92400e;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# ====================================
# 단체활동 데이터
# ====================================
ACTIVITIES = [
    {"name": "명상 모임", "category": "라이프", "difficulty": "초",
     "description": "조용히 함께하며 마음의 안정을 찾아요",
     "effect": "불안↓, 마음 안정, 조용한 연대감",
     "effect_detail": "말을 많이 하지 않아도 함께 있다는 느낌이 위로가 돼요."},
    {"name": "트레킹", "category": "아웃도어", "difficulty": "초",
     "description": "걸으며 자연스럽게 대화할 수 있어요",
     "effect": "기분 전환, 체력 향상, 자유로운 대화",
     "effect_detail": "자연 속에서 걷다 보면 마음이 열려요."},
    {"name": "보드게임 모임", "category": "취미", "difficulty": "초",
     "description": "가볍게 웃으며 사람들과 어울릴 수 있어요",
     "effect": "긴장↓, 웃음↑, 친해지기 쉬움",
     "effect_detail": "게임이라는 공통 목표가 있어 어색함이 줄어요."},
    {"name": "플라워 클래스", "category": "예술", "difficulty": "초",
     "description": "아름다운 것을 만들며 기분전환이 돼요",
     "effect": "집중·몰입, 성과물 보람, 감성 충전",
     "effect_detail": "손으로 무언가를 만드는 과정이 마음을 차분하게 해요."},
    {"name": "요가 클래스", "category": "스포츠", "difficulty": "초",
     "description": "함께 호흡하며 몸과 마음을 돌봐요",
     "effect": "불안↓, 마음 안정, 조용한 연대감",
     "effect_detail": "호흡에 집중하다 보면 복잡한 생각이 정리돼요."},
    {"name": "독서 토론", "category": "자기계발", "difficulty": "중",
     "description": "생각을 나누며 연결감을 느낄 수 있어요",
     "effect": "대화·공감↑, 고립감↓, 사고 정리",
     "effect_detail": "다른 시각을 접하며 생각이 확장돼요."},
    {"name": "맛집 탐방", "category": "미식", "difficulty": "초",
     "description": "맛있는 음식을 함께 즐길 수 있어요",
     "effect": "여유↑, 대화 촉진, 세련된 만남",
     "effect_detail": "좋은 음식 앞에서는 누구나 기분이 좋아져요."},
    {"name": "영화 모임", "category": "문화", "difficulty": "초",
     "description": "같이 보고 이야기 나누는 재미가 있어요",
     "effect": "문화 생활↑, 대화 소재↑, 부담 없는 만남",
     "effect_detail": "영화라는 공통 경험이 대화의 물꼬를 터요."},
    {"name": "러닝 크루", "category": "스포츠", "difficulty": "중",
     "description": "함께 뛰며 건강해지는 느낌이에요",
     "effect": "체력↑, 성취감, 활력",
     "effect_detail": "같이 뛰는 사람들이 있으면 더 오래 달릴 수 있어요."},
    {"name": "사진 산책", "category": "아웃도어", "difficulty": "초",
     "description": "걸으며 사진 찍고 공유해요",
     "effect": "관찰력↑, 현재 집중, 소소한 기쁨",
     "effect_detail": "일상을 다르게 보는 눈이 생겨요."},
]

# ====================================
# 상담 질문 40개 (맥락 기반)
# ====================================
QUESTIONS = {
    # Phase 1: 마음 열기 (1~8)
    "opening": [
        "요즘 하루 보내는 느낌은 어때요?",
        "오늘 기분은 어떠세요?",
        "요즘 어떻게 지내세요?",
        "최근에 어떤 일이 있으셨어요?",
        "그런 느낌이 언제부터 드셨어요?",
        "하루 중에 그나마 괜찮은 시간대도 있나요?",
        "아침에 눈 뜨면 어떤 기분이 들어요?",
        "요즘 하루가 길게 느껴져요, 짧게 느껴져요?",
    ],
    
    # Phase 2: 일상/활동 (9~18)
    "daily": [
        "집에 있을 때랑 밖에 나갈 때 중에 어느 쪽이 더 편해요?",
        "요즘 쉬는 날엔 보통 뭐 하면서 보내세요?",
        "밥은 잘 챙겨 드시고 계세요?",
        "요즘 잠은 잘 주무세요?",
        "집 밖에 나가는 게 요즘 어떻게 느껴져요?",
        "뭔가 하고 싶은 마음은 있는데 몸이 안 따라준 적 있어요?",
        "요즘 가장 오래 하는 일이 뭐예요?",
        "최근에 뭔가 새로 시작한 게 있어요?",
        "요즘 운동이나 산책은 하세요?",
        "하루 중 가장 좋아하는 시간이 있어요?",
    ],
    
    # Phase 3: 관계/사람 (19~28)
    "relationship": [
        "사람 만나는 건 요즘 어떤 편이에요?",
        "누군가 만나고 나면 기운이 생기는 편이에요, 빠지는 편이에요?",
        "연락 오면 반가워요, 아니면 좀 부담스러워요?",
        "요즘 대화 나눌 사람이 있어요?",
        "혼자 있는 시간이 편해요, 아니면 좀 외로워요?",
        "누군가랑 있을 때 어떤 게 제일 편해요?",
        "가까운 사람한테 요즘 마음 이야기한 적 있어요?",
        "사람들 사이에 있으면 어떤 느낌이 들어요?",
        "요즘 자주 연락하는 사람이 있어요?",
        "누군가한테 기대고 싶을 때가 있어요?",
    ],
    
    # Phase 4: 감정/마음 (29~38)
    "emotion": [
        "요즘 '이건 좀 버겁다' 싶은 게 있어요?",
        "그 버거움이 몸 쪽에 더 와요, 마음 쪽에 더 와요?",
        "혼자서 넘기려는 편이에요, 풀어보려는 편이에요?",
        "예전에는 스트레스 풀 때 뭘 많이 했어요?",
        "요즘 그나마 위로가 되는 게 있어요?",
        "기분이 안 좋을 때 어떻게 보내세요?",
        "요즘 가장 많이 드는 생각이 뭐예요?",
        "마음이 복잡할 때 어떻게 하세요?",
        "요즘 나한테 필요한 게 뭘까요?",
        "스스로한테 '잘하고 있어'라고 말해준 적 있어요?",
    ],
    
    # Phase 5: 마무리/희망 (39~40)
    "closing": [
        "지금 상태에서 '이건 해볼 수 있을지도' 싶은 건 어느 정도예요?",
        "요즘 생활에서 뭐 하나 바꿀 수 있다면 뭘 바꾸고 싶어요?",
    ],
}

# 키워드 → Phase 매핑
KEYWORD_PHASE = {
    "daily": ["집", "밥", "잠", "아침", "저녁", "하루", "일상", "생활", "운동", "산책", "쉬"],
    "relationship": ["사람", "친구", "가족", "연락", "만나", "혼자", "외로", "대화", "같이", "누구"],
    "emotion": ["힘들", "지치", "우울", "불안", "걱정", "스트레스", "버겁", "무기력", "슬프", "답답", "짜증", "화", "마음"],
    "closing": ["바꾸", "시작", "해보", "노력", "괜찮", "좋아", "나아"],
}

def select_next_question(messages, asked_questions):
    """대화 맥락에 맞는 다음 질문 선택"""
    
    user_msgs = [m['content'] for m in messages if m['role'] == 'user']
    last_answer = user_msgs[-1].lower() if user_msgs else ""
    all_answers = " ".join(user_msgs).lower()
    
    asked_count = len(asked_questions)
    
    # Phase 결정
    if asked_count < 2:
        phase = "opening"
    elif asked_count < 4:
        # 답변 키워드에 따라 분기
        for p, keywords in KEYWORD_PHASE.items():
            if any(k in last_answer for k in keywords):
                phase = p
                break
        else:
            phase = "daily"
    elif asked_count < 7:
        for p, keywords in KEYWORD_PHASE.items():
            if any(k in last_answer for k in keywords):
                phase = p
                break
        else:
            phase = "relationship"
    elif asked_count < 9:
        phase = "emotion"
    else:
        phase = "closing"
    
    # 해당 phase에서 안 한 질문 선택
    available = [q for q in QUESTIONS[phase] if q not in asked_questions]
    
    if not available:
        for p in ["daily", "relationship", "emotion", "closing", "opening"]:
            available = [q for q in QUESTIONS[p] if q not in asked_questions]
            if available:
                break
    
    return random.choice(available) if available else None

# ====================================
# 공감 응답 (짧고 자연스럽게)
# ====================================
def get_empathy(user_input):
    text = user_input.lower()
    
    if any(w in text for w in ['외로', '혼자']):
        return random.choice(["외로우셨겠어요.", "혼자라는 느낌이 크셨겠네요."])
    if any(w in text for w in ['힘들', '지치', '피곤']):
        return random.choice(["많이 힘드셨겠어요.", "지치셨겠어요."])
    if any(w in text for w in ['우울', '무기력', '의욕']):
        return random.choice(["기분이 가라앉으셨군요.", "그런 날이 있죠."])
    if any(w in text for w in ['불안', '걱정', '두렵']):
        return random.choice(["불안하셨겠어요.", "걱정이 많으시네요."])
    if any(w in text for w in ['짜증', '화', '답답']):
        return random.choice(["답답하셨겠어요.", "그럴 수 있어요."])
    if any(w in text for w in ['슬프', '울', '눈물']):
        return random.choice(["마음이 아프셨겠어요.", "슬프셨겠네요."])
    if any(w in text for w in ['좋', '괜찮', '나아']):
        return random.choice(["다행이네요.", "그건 좋은 것 같아요."])
    if any(w in text for w in ['싫', '귀찮', '하기']):
        return random.choice(["그럴 때 있죠.", "그렇군요."])
    
    return "그렇군요."

# ====================================
# 사용자 상태 분석
# ====================================
def analyze_state(messages):
    text = " ".join([m['content'] for m in messages if m['role'] == 'user']).lower()
    
    state = {
        '고립감': 0, 
        '우울감': 0, 
        '저활동성': 0, 
        '불안': 0, 
        '관계부담': 0,
        '긍정신호': 0
    }
    
    # 키워드 카운트
    if any(w in text for w in ['혼자', '외롭', '쓸쓸', '허전', '아무도']):
        state['고립감'] += 1
    if any(w in text for w in ['우울', '무기력', '힘들', '슬프', '지치']):
        state['우울감'] += 1
    if any(w in text for w in ['집', '안나가', '누워', '귀찮', '못']):
        state['저활동성'] += 1
    if any(w in text for w in ['불안', '걱정', '두렵', '긴장']):
        state['불안'] += 1
    if any(w in text for w in ['부담', '피곤', '피하', '싫']):
        state['관계부담'] += 1
    if any(w in text for w in ['좋', '괜찮', '나아', '해보', '시작']):
        state['긍정신호'] += 1
    
    return state

# ====================================
# 맞춤 응원 메시지 생성
# ====================================
def get_encouragement(state):
    messages = []
    tips = []
    
    if state['고립감'] > 0:
        messages.append("혼자 지내는 시간이 길어지면 마음이 움츠러들 수 있어요. 하지만 지금 이렇게 대화를 나눈 것만으로도 한 걸음 내딛은 거예요.")
        tips.append("💡 하루에 5분만이라도 밖에 나가보세요. 편의점이라도 괜찮아요.")
    
    if state['우울감'] > 0:
        messages.append("마음이 무거운 날들을 보내고 계시는군요. 그런 와중에도 여기까지 오신 거, 정말 대단해요.")
        tips.append("💡 작은 것 하나만 해보세요. 샤워하기, 커튼 열기, 물 한 잔 마시기. 그것만으로 충분해요.")
    
    if state['저활동성'] > 0:
        messages.append("몸이 잘 안 움직여지는 시기가 있어요. 괜찮아요, 천천히 해도 돼요.")
        tips.append("💡 침대에서 일어나기 힘들면, 일단 앉아만 있어보세요. 그것도 움직임이에요.")
    
    if state['불안'] > 0:
        messages.append("걱정이 많으시군요. 불안한 마음을 안고 하루를 버티는 것도 쉽지 않은 일이에요.")
        tips.append("💡 심호흡 3번만 해보세요. 4초 들이쉬고, 7초 내쉬고. 몸이 조금 편해질 거예요.")
    
    if state['관계부담'] > 0:
        messages.append("사람 만나는 게 에너지가 드는 시기가 있어요. 억지로 안 만나도 괜찮아요.")
        tips.append("💡 부담 없는 연결부터 시작해보세요. 온라인 모임이나 짧은 산책 모임 같은 거요.")
    
    if state['긍정신호'] > 0:
        messages.append("긍정적인 신호가 보여요! 지금 이 마음을 잘 붙잡고 계세요.")
        tips.append("💡 지금 느끼는 좋은 감정을 기록해두세요. 힘들 때 다시 꺼내볼 수 있어요.")
    
    # 기본 메시지
    if not messages:
        messages.append("오늘 이야기 나눠주셔서 고마워요. 당신은 혼자가 아니에요.")
        tips.append("💡 오늘 하루, 나한테 '수고했어'라고 말해주세요.")
    
    return messages, tips

# ====================================
# 활동 추천
# ====================================
def recommend(user_state):
    scored = []
    for act in ACTIVITIES:
        score = random.randint(1, 3)
        if user_state['고립감'] > 0 and act['difficulty'] == '초':
            score += 2
        if user_state['관계부담'] > 0 and act['difficulty'] == '초':
            score += 2
        if user_state['저활동성'] > 0 and act['category'] == '아웃도어':
            score += 2
        if user_state['우울감'] > 0 and act['category'] in ['예술', '라이프']:
            score += 1
        scored.append((act, score))
    
    scored.sort(key=lambda x: x[1], reverse=True)
    
    result = []
    categories = set()
    for act, _ in scored:
        if len(result) >= 3:
            break
        if act['category'] not in categories:
            result.append(act)
            categories.add(act['category'])
    
    return result

# ====================================
# 결과 메시지 생성
# ====================================
def make_result(recs, state, count, is_crisis):
    # 상태 요약
    parts = []
    if state['고립감'] > 0:
        parts.append("혼자 보내는 시간이 많으셨던 것 같아요")
    if state['우울감'] > 0:
        parts.append("마음이 좀 가라앉아 계신 것 같아요")
    if state['저활동성'] > 0:
        parts.append("몸을 움직이기가 어려우셨던 것 같아요")
    if state['불안'] > 0:
        parts.append("걱정이 많으셨던 것 같아요")
    if state['관계부담'] > 0:
        parts.append("사람 만나는 게 부담스러우셨던 것 같아요")
    
    summary = ". ".join(parts[:2]) + "." if parts else "여러 생각이 드시는 것 같아요."
    
    # 맞춤 응원 메시지
    encouragements, tips = get_encouragement(state)

    msg = f"""
<div class="summary-card">
    <h3>📋 이야기를 들어보니</h3>
    <p class="summary-text">{summary}</p>
    <p class="summary-encourage">이야기를 나눠주신 것만으로도 큰 용기예요.</p>
</div>

<div class="encourage-box">
    <div class="encourage-title">💪 당신에게 전하고 싶은 말</div>
    <div class="encourage-text">
"""
    
    for enc in encouragements:
        msg += f"{enc}<br><br>"
    
    msg += """
    </div>
</div>
"""

    # 맞춤 팁
    for tip in tips[:2]:
        msg += f"""
<div class="tip-box">
    <div class="tip-text">{tip}</div>
</div>
"""

    msg += f"""
<div class="stat-box">💡 비슷한 상황의 사람들 {count}명이 함께하고 있어요</div>

<h3>🎯 이런 활동은 어떨까요?</h3>
<p style="color: #718096; margin-bottom: 20px;">부담 없이 시작할 수 있는 활동들을 골라봤어요.</p>
"""

    for i, rec in enumerate(recs, 1):
        effects = rec['effect'].split(', ')
        tags = ''.join([f'<span class="activity-effect">{e}</span>' for e in effects])
        
        msg += f"""
<div class="activity-card">
    <div class="activity-name">{i}. {rec['name']}</div>
    <div class="activity-desc">{rec['description']}</div>
    <div>{tags}</div>
    <div class="activity-detail">💬 {rec['effect_detail']}</div>
</div>
"""

    msg += '<div class="divider"></div>'

    msg += """
<div class="kakao-section">
    <div class="kakao-title">📍 혼자가 아닌 공간</div>
    <div class="kakao-desc">비슷한 상황의 분들이 느슨하게 모여 있는 곳이에요.<br>꼭 말할 필요 없고, 있기만 해도 괜찮아요.</div>
    <div class="kakao-fit">
        · 누군가 있으면 좋겠는데 깊은 대화는 부담스러운 분<br>
        · 가끔 안부 정도만 나누고 싶은 분<br>
        · 혼자 지내지만 연결은 놓고 싶지 않은 분
    </div>
    <a href="https://open.kakao.com/o/xxxxxxxx" target="_blank" style="color: #667eea;">👉 1인가구 모임방 둘러보기</a>
    <br><br>
    <span class="kakao-password">🔐 입장 비밀번호: 1101</span>
    <div class="kakao-note">준비되실 때 편하게 들어오시면 돼요.</div>
</div>
"""

    msg += '<div class="divider"></div>'

    if is_crisis:
        msg += """
<div class="crisis-section">
    <div class="crisis-title">🆘 지금 바로 이야기 나눌 수 있어요</div>
    <p style="color: #742a2a; margin-bottom: 16px;">혼자 감당하기 힘든 마음이 느껴지셨나요?<br>지금 이 순간, 당신의 이야기를 들어줄 전문가가 24시간 대기하고 있어요.</p>
    <div class="crisis-item"><strong>📞 1393</strong> — 자살예방 상담전화 (24시간, 무료)</div>
    <div class="crisis-item"><strong>📞 1577-0199</strong> — 정신건강위기 상담전화</div>
    <div class="crisis-item"><strong>📞 112 / 119</strong> — 긴급상황</div>
    <p style="color: #9b2c2c; font-size: 13px; margin-top: 16px;">전화가 어렵다면, 카카오톡에서 "마음이음"을 검색해보세요.</p>
</div>
"""
    else:
        msg += """
<div class="counseling-section">
    <div class="counseling-title">📞 전문 상담이 필요하시다면</div>
    <p style="color: #718096; margin-bottom: 16px;">대화만으로는 해결되지 않는 마음의 무게가 있을 수 있어요.</p>
    <div class="counseling-item"><strong>📞 1393</strong> — 자살예방 상담전화 (24시간, 무료)</div>
    <div class="counseling-item"><strong>📞 1577-0199</strong> — 정신건강위기 상담전화</div>
    <div class="counseling-item"><strong>📞 112 / 119</strong> — 긴급상황</div>
    <p style="color: #a0aec0; font-size: 13px; margin-top: 16px;">💡 전화가 부담스러워도 괜찮아요. 상담사분들은 그런 마음도 다 이해해요.</p>
</div>
"""

    msg += """
<div class="closing-text">
    오늘 이야기 나눠주셔서 감사해요.<br>
    당신은 충분히 잘하고 있어요. 응원할게요 💙<br>
    언제든 다시 찾아오세요 😊
</div>
"""
    return msg

# ====================================
# 세션 초기화
# ====================================
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.asked_questions = []
    st.session_state.done = False
    st.session_state.user_count = random.randint(150, 280)
    st.session_state.user_state = {}
    
    first_q = QUESTIONS["opening"][0]
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"안녕하세요 🙂\n\n{first_q}"
    })
    st.session_state.asked_questions.append(first_q)

# ====================================
# UI
# ====================================
st.title("💬 1인 가구 웰니스 상담")
st.caption("편하게 이야기해주세요.")

# 대화 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if any(x in msg["content"] for x in ["summary-card", "stat-box", "activity-card", "kakao-section", "crisis-section", "counseling-section", "encourage-box", "tip-box"]):
            st.markdown(msg["content"], unsafe_allow_html=True)
        else:
            st.markdown(msg["content"])

# 입력
if prompt := st.chat_input("메시지를 입력하세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    if not st.session_state.done:
        user_count = len([m for m in st.session_state.messages if m['role'] == 'user'])
        
        if user_count >= 10:
            # 분석 중 메시지 표시
            with st.chat_message("assistant"):
                analysis_placeholder = st.empty()
                analysis_placeholder.markdown("""
                <div style="text-align: center; padding: 40px;">
                    <div style="font-size: 18px; color: #667eea; margin-bottom: 16px;">
                        🔍 상담 분석중...
                    </div>
                    <div style="font-size: 14px; color: #a0aec0;">
                        잠시만 기다려주세요
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                time.sleep(4)
                analysis_placeholder.empty()
            
            state = analyze_state(st.session_state.messages)
            st.session_state.user_state = state
            recs = recommend(state)
            is_crisis = state['우울감'] >= 2 or state['불안'] >= 2
            response = make_result(recs, state, st.session_state.user_count, is_crisis)
            st.session_state.done = True
        else:
            empathy = get_empathy(prompt)
            next_q = select_next_question(st.session_state.messages, st.session_state.asked_questions)
            
            if next_q:
                st.session_state.asked_questions.append(next_q)
                response = f"{empathy}\n\n{next_q}"
            else:
                response = f"{empathy}\n\n조금 더 이야기해주실 수 있을까요?"
    else:
        response = "추가로 이야기하고 싶은 게 있으시면 말씀해주세요 😊"
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    with st.chat_message("assistant"):
        if any(x in response for x in ["summary-card", "stat-box", "activity-card", "kakao-section", "encourage-box", "tip-box"]):
            st.markdown(response, unsafe_allow_html=True)
        else:
            st.markdown(response)
    
    st.rerun()

# ====================================
# 사이드바
# ====================================
with st.sidebar:
    st.header("ℹ️ 서비스 안내")
    
    st.markdown("---")
    
    # 참여자 수
    st.markdown("**👥 상담 참여자**")
    st.markdown(f"<div style='font-size: 24px; font-weight: bold; color: #667eea;'>{st.session_state.user_count}명</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 상담 진행 상황
    st.markdown("**📝 상담 진행 상황**")
    user_msgs = len([m for m in st.session_state.messages if m['role'] == 'user'])
    progress = min(user_msgs / 10, 1.0)
    
    st.progress(progress)
    st.markdown(f"<div style='text-align: center; color: #666;'>질문 <strong>{user_msgs}</strong> / 10</div>", unsafe_allow_html=True)
    
    if user_msgs < 10:
        remaining = 10 - user_msgs
        st.markdown(f"<div style='text-align: center; font-size: 12px; color: #999;'>{remaining}개 더 대화하면 결과가 나와요</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='text-align: center; font-size: 12px; color: #667eea;'>✅ 상담 완료</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 현재 단계 표시
    st.markdown("**🎯 현재 단계**")
    if user_msgs < 2:
        stage = "마음 열기"
        stage_icon = "💭"
    elif user_msgs < 5:
        stage = "일상 파악"
        stage_icon = "🏠"
    elif user_msgs < 8:
        stage = "관계/감정 탐색"
        stage_icon = "💬"
    else:
        stage = "마무리"
        stage_icon = "🎁"
    
    st.markdown(f"<div style='text-align: center; padding: 10px; background: #f0f4ff; border-radius: 8px;'>{stage_icon} {stage}</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 데이터셋 정보
    st.markdown("**📊 Dataset Info**")
    
    total_questions = sum(len(q) for q in QUESTIONS.values())
    
    st.code(f"""
QUESTIONS_POOL = {total_questions}
├── opening: {len(QUESTIONS['opening'])}
├── daily: {len(QUESTIONS['daily'])}
├── relationship: {len(QUESTIONS['relationship'])}
├── emotion: {len(QUESTIONS['emotion'])}
└── closing: {len(QUESTIONS['closing'])}

ACTIVITIES = {len(ACTIVITIES)}
KEYWORDS = {sum(len(v) for v in KEYWORD_PHASE.values())}

state_variables:
├── 고립감: int
├── 우울감: int
├── 저활동성: int
├── 불안: int
├── 관계부담: int
└── 긍정신호: int
    """, language="python")
    
    # 현재 분석 상태 (상담 완료 시)
    if st.session_state.done and st.session_state.user_state:
        st.markdown("---")
        st.markdown("**🔬 분석 결과**")
        state = st.session_state.user_state
        st.code(f"""
user_state = {{
    '고립감': {state.get('고립감', 0)},
    '우울감': {state.get('우울감', 0)},
    '저활동성': {state.get('저활동성', 0)},
    '불안': {state.get('불안', 0)},
    '관계부담': {state.get('관계부담', 0)},
    '긍정신호': {state.get('긍정신호', 0)}
}}
        """, language="python")
    
    st.markdown("---")
    
    if st.button("🔄 처음부터 다시하기", use_container_width=True):
        st.session_state.clear()
        st.rerun()