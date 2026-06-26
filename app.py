import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. 페이지 레이아웃 설정
st.set_page_config(page_title="광주광역시 버스 대시보드", layout="wide")

st.title("🚌 광주광역시 버스 정류장별 이용 현황")
st.markdown("깃허브 저장소에 업로드된 광주광역시 버스 데이터를 기반으로 작동하는 실시간 대시보드입니다.")

# 💡 [핵심 수정] app.py 파일이 있는 '진짜 절대 경로'를 기준으로 삼습니다.
current_dir = os.path.dirname(os.path.abspath(__file__))
all_files = os.listdir(current_dir)

# 🔍 사이드바에 서버 내부 파일 상태를 보여주는 디버깅 창 활성화
st.sidebar.header("⚙️ 서버 시스템 확인")
st.sidebar.write("📂 현재 서버가 보는 폴더:", current_dir)
st.sidebar.write("📄 폴더 안의 전체 파일:", all_files)

# CSV 파일만 골라내기 (대소문자 무관하게 .csv, .CSV 모두 찾음)
csv_files = [f for f in all_files if f.lower().endswith('.csv')]

# 지정하고자 하는 파일명
TARGET_FILE = "20260331.csv"

# 파일 존재 여부 체크
if TARGET_FILE in all_files:
    target_csv = TARGET_FILE
    is_ready = True
elif len(csv_files) > 0:
    # 20260331.csv는 없지만 다른 CSV 파일이 있다면 그거라도 읽음
    target_csv = csv_files[0]
    is_ready = True
else:
    is_ready = False

if not is_ready:
    st.error(f"❌ 깃허브 저장소에서 CSV 파일을 찾을 수 없습니다.")
    st.warning(f"위의 '폴더 안의 전체 파일' 목록에 실제로 [{TARGET_FILE}]이(가) 들어있는지 확인해 주세요!")
else:
    # 3. 데이터 로드 (인코딩 에러 방지 및 캐싱 적용)
    @st.cache_data
    def load_data(file_path):
        try:
            return pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            return pd.read_csv(file_path, encoding='cp949')

    # 전체 절대 경로로 파일 읽기
    full_path = os.path.join(current_dir, target_csv)
    bus = load_data(full_path)

    # 4. 데이터 검증 및 시각화 진행
    required_columns = ['정류장명', '권종', '거래건수']
    if all(col in bus.columns for col in required_columns):
        
        st.success(f"📂 성공적으로 **[{target_csv}]** 파일을 로드했습니다.")
        
        # 상단 요약 화면 구성 (Metric)
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("📊 광주 데이터 통계")
            st.metric("총 거래건수", f"{bus['거래건수'].sum():,} 건")
            st.metric("분석 대상 정류장 수", f"{bus['정류장명'].nunique():,} 개")
        with col2:
            st.subheader("📋 데이터 미리보기")
            st.dataframe(bus.head(5), use_container_width=True)
            
        st.divider()

        # [사용자 기존 분석 로직 수행]
        agg_df = bus.groupby(['정류장명', '권종'])['거래건수'].sum().reset_index()
        top_stations = agg_df.groupby('정류장명')['거래건수'].sum().nlargest(10).index
        filtered_agg_df = agg_df[agg_df['정류장명'].isin(top_stations)]

        color_palette = {'어린이': 'red', '일반': 'yellow', '청소년': 'blue'}

        # 5. Plotly 기반 차트 시각화
        st.subheader("📈 정류장별 권종별 거래건수 상위 10개 정류장 (광주광역시)")
        
        fig = px.bar(
            filtered_agg_df,
            x='정류장명',
            y='거래건수',
            color='권종',
            barmode='group',
            color_discrete_map=color_palette
        )
        
        fig.update_layout(
            xaxis_title="Station Name (정류장명)",
            yaxis_title="Transaction Count (거래건수)",
            legend_title="Ticket Type (권종)",
            font=dict(size=13),
            xaxis={'categoryorder': 'total descending'},
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📥 가공된 상위 10개 정류장 상세 데이터 보기"):
            st.dataframe(filtered_agg_df, use_container_width=True)
            
    else:
        st.error(f"❌ CSV 구조 불일치: 파일 내에 {required_columns} 컬럼이 모두 포함되어 있는지 확인해주세요.")
