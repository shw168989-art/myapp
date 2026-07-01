import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="팀 예산 관리 시스템", layout="wide", initial_sidebar_state="collapsed")

# CSS를 통한 Pretendard 폰트 및 스타일 적용 (기존 테마 유지)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Pretendard', sans-serif;
        background-color: #f8fafc;
    }
    div[data-testid="stMetric"] {
        background-color: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# 1. 시크릿 파일(Secrets)에서 앱스 스크립트 URL 가져오기
if "WEBAPP_URL" in st.secrets:
    API_URL = st.secrets["WEBAPP_URL"]
else:
    st.error("스트림릿 Secrets에 'WEBAPP_URL'이 설정되지 않았습니다. 로컬 환경이라면 .streamlit/secrets.toml을 확인하세요.")
    st.stop()

# 데이터 불러오기 함수
def load_data():
    try:
        response = requests.get(API_URL)
        if response.status_size != 0:
            return pd.DataFrame(response.json())
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    return pd.DataFrame(columns=["id", "member", "month", "category", "amount"])

# 데이터 업로드 함수
def save_data(entry):
    try:
        res = requests.post(API_URL, json=entry)
        return res.json().get("status") == "success"
    except Exception as e:
        st.error(f"데이터 저장 중 오류 발생: {e}")
        return False

# 헤더 영역
st.markdown("<h1 style='text-align: center; color: #1e293b; font-weight:700;'>📊 팀 예산 관리 시스템</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>부장님 보고용 월별 예산 취합 및 대시보드</p>", unsafe_allow_html=True)
st.write("---")

# 네비게이션 탭 (기존 데이터 입력 / 전체 대시보드 구조 재현)
tab_input, tab_dashboard = st.tabs(["📝 데이터 입력", "📈 전체 대시보드"])

# 데이터 로드
df = load_data()

# --- 데이터 입력 탭 ---
with tab_input:
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.markdown("### 📝 내역 입력")
        with st.form("budget_form", clear_on_submit=True):
            member = st.selectbox("팀원 선택", ["부장님", "팀원1", "팀원2", "팀원3", "팀원4"])
            month = st.date_input("해당 월", datetime.now()).strftime("%Y-%m")
            category = st.selectbox("예산 항목", ["수선유지비", "비품", "개량공사"])
            amount = st.number_input("사용 금액 (원)", min_value=0, step=1000, format="%d")
            
            submit_button = st.form_submit_button("기록 저장하기", use_container_width=True)
            
            if submit_button:
                if amount <= 0:
                    st.warning("금액을 정확히 입력해 주세요.")
                else:
                    new_entry = {
                        "id": int(datetime.now().timestamp() * 1000),
                        "member": member,
                        "month": month,
                        "category": category,
                        "amount": amount
                    }
                    if save_data(new_entry):
                        st.success("예산 데이터가 정상적으로 기록되었습니다.")
                        st.rerun()
                    else:
                        st.error("저장에 실패했습니다.")
                        
    with col2:
        st.markdown("### 📂 최근 입력 내역")
        if not df.empty:
            # 보기 좋은 컬럼명으로 변경하여 출력
            display_df = df[["month", "member", "category", "amount"]].copy()
            display_df["amount"] = display_df["amount"].apply(lambda x: f"{int(x):,}원")
            display_df.columns = ["날짜", "팀원", "항목", "금액"]
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info("등록된 데이터가 없습니다.")

# --- 대시보드 탭 ---
with tab_dashboard:
    if df.empty:
        st.info("대시보드를 표시할 데이터가 없습니다. 먼저 데이터를 입력해 주세요.")
    else:
        df["amount"] = df["amount"].astype(int)
        
        # 상단 핵심 지표 (Cards)
        total_amount = df["amount"].sum()
        data_count = len(df)
        
        # 이번 달 최대 사용 항목 계산
        current_month = datetime.now().strftime("%Y-%m")
        current_month_df = df[df["month"] == current_month]
        if not current_month_df.empty:
            top_cat = current_month_df.groupby("category")["amount"].sum().idxmax()
            top_cat_val = current_month_df.groupby("category")["amount"].sum().max()
            top_cat_str = f"{top_cat} ({top_cat_val:,}원)"
        else:
            top_cat_str = "이번 달 데이터 없음"
            
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric(label="전체 누적 사용액", value=f"{total_amount:,}원")
        with m_col2:
            st.metric(label="이번 달 최대 사용 항목", value=top_cat_str)
        with m_col3:
            st.metric(label="데이터 건수", value=f"{data_count}건")
            
        st.write(" ")
        
        # 차트 영역 (기존 Doughnut, Bar 차트 구현)
        c_col1, c_col2 = st.columns(2, gap="large")
        
        with c_col1:
            st.markdown("##### 🏠 항목별 예산 분포")
            cat_df = df.groupby("category")["amount"].sum().reset_index()
            fig_pie = px.pie(cat_df, values="amount", names="category", hole=0.6,
                             color_discrete_sequence=['#3b82f6', '#10b981', '#8b5cf6'])
            fig_pie.update_traces(textinfo='percent+label')
            fig_pie.update_layout(showlegend=False, margin=dict(t=10, b=10, l=10, r=10), height=300)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with c_col2:
            st.markdown("##### 👥 팀원별 누적 사용액")
            mem_df = df.groupby("member")["amount"].sum().reset_index()
            fig_bar = px.bar(mem_df, x="member", y="amount", labels={"member": "팀원", "amount": "사용 금액"})
            fig_bar.update_traces(marker_color='#60a5fa')
            fig_bar.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=300, yaxis={'visible': True, 'showgrid': False})
            st.plotly_chart(fig_bar, use_container_width=True)
            
        # 월별/항목별 요약 테이블 (취합본 피벗 테이블)
        st.markdown("### 📅 월별/항목별 요약 테이블 (취합본)")
        
        # 피벗 테이블 생성
        pivot_df = df.pivot_table(index="month", columns="category", values="amount", aggfunc="sum", fill_value=0)
        
        # 기존 HTML에 있던 모든 항목 열이 안전하게 생성되도록 보장
        for col in ["수선유지비", "비품", "개량공사"]:
            if col not in pivot_df.columns:
                pivot_df[col] = 0
                
        # 합계 열 추가 및 정렬
        pivot_df["합계"] = pivot_df.sum(axis=1)
        pivot_df = pivot_df.sort_index(ascending=False) # 최신 연월이 위로
        
        # 천단위 콤마 포맷팅 변환
        style_df = pivot_df.copy()
        for col in style_df.columns:
            style_df[col] = style_df[col].apply(lambda x: f"{x:,}")
            
        st.table(style_df)
