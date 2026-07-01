import streamlit as st
import time
from datetime import datetime

# 1. 페이지 기본 설정 및 스타일 정의
st.set_page_config(
    page_title="동물 캐릭터로 알아보는 나의 스트레스 대처 유형",
    page_icon="🦁",
    layout="centered"
)

# 커스텀 CSS 주입 (기존 HTML/CSS 감성 재현)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    
    /* 전체 폰트 및 배경 스타일링 */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Noto Sans KR', sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* 카드 래퍼 스타일 */
    .card-wrapper {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
    }
    
    /* 배지 및 타이틀 */
    .badge {
        display: inline-block;
        background: #e1f5fe;
        color: #0288d1;
        padding: 0.3rem 0.8rem;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .success-badge {
        background: #e8f5e9;
        color: #2e7d32;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1a1a;
        line-height: 1.3;
        margin-bottom: 1rem;
    }
    .subtitle {
        color: #666;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }
    
    /* 애니메이션 이모지 그룹 */
    .emoji-group {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        font-size: 3rem;
        margin: 2rem 0;
    }
    
    /* 결과 카드 */
    .result-animal-card {
        text-align: center;
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid #eee;
        margin-bottom: 1.5rem;
    }
    .result-emoji {
        font-size: 4.5rem;
        display: block;
        margin-bottom: 0.5rem;
    }
    .result-animal-name {
        font-size: 1.6rem;
        font-weight: 700;
        color: #333;
        margin-bottom: 0.5rem;
    }
    .result-tagline {
        font-style: italic;
        color: #555;
        font-size: 1rem;
    }
    
    /* 상세 섹션 */
    .detail-section {
        margin-bottom: 1.5rem;
        padding: 1rem;
    }
    .detail-section h4 {
        margin-top: 0;
        color: #222;
        font-size: 1.1rem;
        font-weight: 600;
    }
    .highlight-box {
        background: #fff9db;
        border-left: 4px solid #fab005;
        border-radius: 4px;
    }
    
    /* 히스토리 아이템 */
    .history-item {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.8rem;
        border-left: 4px solid #0288d1;
    }
</style>
""", unsafe_allow_html=True)

# 2. 질문 데이터셋 정의 (8개 질문)
QUESTIONS = [
    {"q": "중요한 발표를 앞두고 극심한 스트레스를 받을 때 나는?", "a": "자료를 처음부터 끝까지 다시 검토하며 완벽히 준비한다.", "b": "친구에게 전하해서 수다를 떨거나 매운 음식을 먹으며 푼다."},
    {"q": "회사나 학교에서 억울한 상황에 직면했을 때 나는?", "a": "상황의 원인을 이성적으로 파악하고 정면으로 따진다.", "b": "일단 상황을 피하고 혼자만의 시간을 가지며 마음을 추스른다."},
    {"q": "스트레스가 가득 찬 주말, 내가 선택할 휴식은?", "a": "침대 밖은 위험해! 하루 종일 넷플릭스를 보며 잠을 잔다.", "b": "당장 밖으로 나가서 운동을 하거나 새로운 액티비티를 즐긴다."},
    {"q": "예상치 못한 문제가 발생해 계획이 틀어졌을 때 나는?", "a": "플랜 B를 즉각 가동하여 문제를 즉시 해결하려고 움직인다.", "b": "조금 멘붕이 오지만 '어떻게든 되겠지' 하며 흐름에 맡긴다."},
    {"q": "타인과의 갈등으로 마음이 답답할 때 나는?", "a": "내 감정과 생각을 솔직하게 다 털어놓고 대화로 푼다.", "b": "갈등이 깊어지는 게 싫어서 적당히 맞춰주거나 참는다."},
    {"q": "요즘 나를 가장 지치게 하는 스트레스의 성격은?", "a": "해야 할 일이 너무 많고 정리가 안 되는 업무적/학업적 스트레스", "b": "사람 관계에서 오는 신경전과 감정 소모성 스트레스"},
    {"q": "스트레스를 받으면 나의 신체적 변화는?", "a": "두통이 오거나 심장이 뛰고 온몸에 긴장감이 든다.", "b": "무기력해지고 온종일 잠이 쏟아지거나 의욕이 사라진다."},
    {"q": "힘든 시기를 겪고 있는 나에게 가장 필요한 위로는?", "a": "현실적인 해결책이나 '너는 능력이 있으니 잘할 거야'라는 확신", "b": "따뜻한 공감과 '그동안 고생 많았어'라는 감정적 위로"}
]

# 3. 결과 데이터셋 정의 (A/B 성향 조합에 따른 대표 동물)
# A 선택 개수에 따라 결과 매칭 (0~8개)
RESULTS = {
    "high_a": { # A가 6개 이상 (주도적/해결 중심)
        "name": "용감한 사자형", "emoji": "🦁",
        "tagline": '"정면 돌파! 문제를 직면하고 해결해야 직성이 풀리는 스타일"',
        "desc": "스트레스 원인을 정확히 분석하고 통제하려는 성향이 강합니다. 어려운 과제가 주어질수록 승부욕이 자극되기도 합니다.",
        "prescription": "가끔은 모든 것을 내가 통제할 수 없음을 인정하세요. '내려놓기' 연습과 충분한 신체적 휴식이 필요합니다."
    },
    "mid_a": { # A가 4~5개 (균형/전략 중심)
        "name": "똑똑한 여우형", "emoji": "🦊",
        "tagline": '"전략적 대처! 상황에 따라 유연하게 머리를 쓰는 스타일"',
        "desc": "이성적인 대처와 감정적인 환기의 밸런스가 좋습니다. 위험 요소를 미리 파악하고 영리하게 피해 갈 줄 압니다.",
        "prescription": "생각이 너무 많아지면 행동이 늦어질 수 있습니다. 고민의 시간을 줄이고 단순하게 행동해 보세요."
    },
    "mid_b": { # A가 2~3개 (관계/힐링 중심)
        "name": "다정한 돌고래형", "emoji": "🐬",
        "tagline": '"감정 교류! 주변 사람들과 소통하며 스트레스를 녹이는 스타일"',
        "desc": "혼자 앓기보다는 신뢰하는 사람들과 감정을 나누며 에너지를 얻습니다. 공감 능력이 뛰어나 주변을 잘 챙깁니다.",
        "prescription": "타인의 감정에 지나치게 몰입하다 보면 정작 내 마음이 방전될 수 있습니다. '나 감정 우선주의' 세션이 필요합니다."
    },
    "high_b": { # A가 0~1개 (평화/수용 중심)
        "name": "여유로운 코알라형", "emoji": "🐨",
        "tagline": '"유유자적! 스트레스 상황에서 한 발짝 물러서 평정을 찾는 스타일"',
        "desc": "갈등을 최소화하고 내면의 평화를 지키는 것이 중요합니다. 주로 수면, 취미 생활 등 혼자만의 동굴 속에서 에너지를 충전합니다.",
        "prescription": "회피가 길어지면 근본적인 문제가 쌓일 수 있습니다. 아주 작은 문제부터 직접 마주하고 해결하는 성공 경험을 쌓아보세요."
    }
}

# 4. 세션 상태(Session State) 초기화
if "screen" not in st.session_state:
    st.session_state.screen = "home"
if "current_idx" not in st.session_state:
    st.session_state.current_idx = 0
if "answers" not in st.session_state:
    st.session_state.answers = []
if "history" not in st.session_state:
    st.session_state.history = []

# 5. 로직 함수들
def get_result_data(answers):
    a_count = answers.count("A")
    if a_count >= 6: return RESULTS["high_a"]
    elif a_count >= 4: return RESULTS["mid_a"]
    elif a_count >= 2: return RESULTS["mid_b"]
    else: return RESULTS["high_b"]

# --- 화면 렌더링 시작 ---

# [1. 홈 스크린]
if st.session_state.screen == "home":
    st.markdown('<div class="card-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="badge">Psychology Test</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">나의 스트레스<br>대처 동물은?</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">단 8개의 질문으로 알아보는 나의 스트레스 극복 성향과 마음의 날씨</p>', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="emoji-group">
        <span>🦁</span><span>🐨</span><span>🐬</span><span>🦊</span>
    </div>
    ''', unsafe_allow_html=True)
    
    # 버튼 액션 그룹
    if st.button("🚀 테스트 시작하기", use_container_width=True, type="primary"):
        st.session_state.current_idx = 0
        st.session_state.answers = []
        st.session_state.screen = "test"
        st.rerun()
        
    # 이어서 진행하기 (진행 중인 데이터가 있을 때만 노출)
    if 0 < st.session_state.current_idx < len(QUESTIONS):
        if st.button("⏳ 이어서 진행하기", use_container_width=True):
            st.session_state.screen = "test"
            st.rerun()
            
    if st.button("📂 지난 결과 보기", use_container_width=True):
        st.session_state.screen = "history"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# [2. 검사 진행 스크린]
elif st.session_state.screen == "test":
    idx = st.session_state.current_idx
    q_data = QUESTIONS[idx]
    
    st.markdown('<div class="card-wrapper">', unsafe_allow_html=True)
    
    # 상단 헤더 (이전 버튼 및 프로그레스 바)
    col1, col2 = st.columns([1, 6])
    with col1:
        if st.button("⬅️", help="이전 단계로"):
            if idx > 0:
                st.session_state.current_idx -= 1
                st.session_state.answers.pop()
                st.rerun()
            else:
                st.session_state.screen = "home"
                st.rerun()
    with col2:
        progress_val = (idx + 1) / len(QUESTIONS)
        st.progress(progress_val)
        st.write(f"**질문 {idx + 1} / {len(QUESTIONS)}**")
        
    st.markdown("---")
    
    # 질문 내용
    st.markdown(f"### {q_data['q']}")
    st.write("")
    
    # 옵션 버튼 카드 형식 제공
    if st.button(f"🅰️ {q_data['a']}", use_container_width=True, key=f"opt_a_{idx}"):
        st.session_state.answers.append("A")
        if idx + 1 < len(QUESTIONS):
            st.session_state.current_idx += 1
        else:
            # 최종 결과 계산 및 기록 저장
            res = get_result_data(st.session_state.answers)
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            st.session_state.history.append({"date": now_str, "name": res["name"], "emoji": res["emoji"]})
            st.session_state.screen = "result"
        st.rerun()
        
    if st.button(f"🅱️ {q_data['b']}", use_container_width=True, key=f"opt_b_{idx}"):
        st.session_state.answers.append("B")
        if idx + 1 < len(QUESTIONS):
            st.session_state.current_idx += 1
        else:
            res = get_result_data(st.session_state.answers)
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            st.session_state.history.append({"date": now_str, "name": res["name"], "emoji": res["emoji"]})
            st.session_state.screen = "result"
        st.rerun()
        
    st.markdown('</div>', unsafe_allow_html=True)

# [3. 결과 분석 스크린]
elif st.session_state.screen == "result":
    res = get_result_data(st.session_state.answers)
    
    st.markdown('<div class="card-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="badge success-badge">진단 완료</div>', unsafe_allow_html=True)
    st.markdown('<h2>당신의 스트레스 대처 유형은...</h2>', unsafe_allow_html=True)
    
    # 동물 카드 섹션
    st.markdown(f'''
    <div class="result-animal-card">
        <span class="result-emoji">{res["emoji"]}</span>
        <h3 class="result-animal-name">{res["name"]}</h3>
        <p class="result-tagline">{res["tagline"]}</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # 세부 정보 특징 섹션
    st.markdown(f'''
    <div class="detail-section">
        <h4>💡 나의 대처 방식 특징</h4>
        <p>{res["desc"]}</p>
    </div>
    <div class="detail-section highlight-box">
        <h4>🎯 마인드셋 추천 처방</h4>
        <p>{res["prescription"]}</p>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 액션 그룹
    if st.button("🔗 결과 링크 복사하기 (클립보드)", use_container_width=True):
        st.toast("📋 결과 링크가 복사되었습니다! (Streamlit 시뮬레이션)")
        
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 다시 테스트하기", use_container_width=True, type="primary"):
            st.session_state.current_idx = 0
            st.session_state.answers = []
            st.session_state.screen = "test"
            st.rerun()
    with col2:
        if st.button("🏠 홈으로", use_container_width=True):
            st.session_state.screen = "home"
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)

# [4. 지난 기록(History) 스크린]
elif st.session_state.screen == "history":
    st.markdown('<div class="card-wrapper">', unsafe_allow_html=True)
    st.markdown('<h2>지난 테스트 기록</h2>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">로컬 세션에 저장된 나의 스트레스 관리 여정</p>', unsafe_allow_html=True)
    
    if not st.session_state.history:
        st.markdown('''
        <div style="text-align:center; padding: 3rem 0; color:#888;">
            <span style="font-size:3rem;">📂</span>
            <p style="margin-top:1rem;">저장된 테스트 기록이 없습니다.<br>첫 테스트를 시작해 보세요!</p>
        </div>
        ''', unsafe_allow_html=True)
    else:
        for i, item in enumerate(reversed(st.session_state.history)):
            st.markdown(f'''
            <div class="history-item">
                <span style="font-size:0.85rem; color:#888;">{item['date']}</span>
                <div style="font-size:1.1rem; font-weight:600; margin-top:0.3rem;">
                    {item['emoji']} {item['name']}
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
    st.markdown("---")
    
    # 푸터 버튼들
    if st.session_state.history:
        if st.button("🗑️ 모든 기록 삭제", use_container_width=True):
            st.session_state.history = []
            st.toast("기록이 모두 삭제되었습니다.")
            st.rerun()
            
    if st.button("🏠 홈으로 돌아가기", use_container_width=True, type="primary"):
        st.session_state.screen = "home"
        st.rerun()
        
    st.markdown('</div>', unsafe_allow_html=True)
