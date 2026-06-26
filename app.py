import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. 스트림릿 페이지 레이아웃 설정
st.set_page_config(page_title="광주광역시 버스 대시보드", layout="wide")

st.title("🚌 광주광역시 버스 정류장별 권종별 이용 현황")
st.markdown("깃허브 저장소에 업로드된 광주광역시 버스 데이터를 분석한 실시간 대시보드입니다.")

# 🔥 [중요] 깃허브에 올리신 광주 CSV 파일명과 정확히 똑같이 적어주세요!
# 예: 파일명이 'gwangju_bus_data.csv' 라면 아래를 수정해야 합니다.
CSV_FILE_NAME = "gwangju_bus.csv" 

# 2. 데이터 로드 함수 (캐싱 적용)
@st.cache_data
def load_local_data(file_name):
    if os.path.exists(file_name):
        try:
            # 한글 인코딩 오류 방지 (UTF-8 우선, 실패 시 CP949)
            return pd.read_csv(file_name, encoding='utf-8')
        except UnicodeDecodeError:
            return pd.read_csv(file_name, encoding='cp949')
    return None

bus = load_local_data(CSV_FILE_NAME)

# 3. 데이터가 정상적으로 로드되었을 때만 시각화 실행
if bus is not None:
    st.success(f"✅ 저장소에서 '{CSV_FILE_NAME}' 데이터를 성공적으로 불러왔습니다.")
    
    # 데이터 기본 검증
    required_columns = ['정류장명', '권종', '거래건수']
    if all(col in bus.columns for col in required_columns):
        
        # 상단 요약 지표 및 데이터 미리보기
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("📊 광주 버스 데이터 통계")
            st.metric("총 거래건수", f"{bus['거래건수'].sum():,} 건")
            st.metric("분석 대상 정류장 수", f"{bus['정류장명'].nunique():,} 개")
        with col2:
            st.subheader("📋 데이터 미리보기")
            st.dataframe(bus.head(5), use_container_width=True)
            
        st.divider()
        
        # [기존 데이터 분석 가공 로직 적용]
        # Aggregate transaction count by '정류장명' and '권종'
        agg_df = bus.groupby(['정류장명', '권종'])['거래건수'].sum().reset_index()

        # Get top 10 stations by total transaction count for better visualization
        top_stations = agg_df.groupby('정류장명')['거래건수'].sum().nlargest(10).index
        filtered_agg_df = agg_df[agg_df['정류장명'].isin(top_stations)]

        # Define a custom color palette
        color_palette = {'어린이': 'red', '일반': 'yellow', '청소년': 'blue'}

        # 4. 시각화 구현 (Streamlit Cloud 한글 깨짐 방지를 위해 Plotly Express 사용)
        st.subheader("📈 정류장별 권종별 거래건수 상위 10개 정류장 (광주광역시)")
        
        fig = px.bar(
            filtered_agg_df, 
            x='정류장명', 
            y='거래건수', 
            color='권종',
            barmode='group',
            color_discrete_map=color_palette
        )
        
        # 레이아웃 스타일 설정 (기존 plt 설정 반영)
        fig.update_layout(
            xaxis_title="Station Name (정류장명)",
            yaxis_title="Transaction Count (거래건수)",
            legend_title="Ticket Type (권종)",
            font=dict(size=13),
            xaxis={'categoryorder':'total descending'}, # 거래건수 높은 정류장 순으로 정렬
            height=600
        )
        
        # 스트림릿 화면에 인터랙티브 차트 출력
        st.plotly_chart(fig, use_container_width=True)
        
        # 가공 데이터 확인 및 다운로드 기능
        with st.expander("📥 상위 10개 정류장 가공 데이터 보기"):
            st.dataframe(filtered_agg_df, use_container_width=True)
            
    else:
        st.error(f"❌ CSV 파일 구조 오류: 파일 내에 {required_columns} 컬럼이 모두 포함되어 있는지 확인해주세요.")
else:
    st.error(f"❌ 깃허브 저장소에서 '{CSV_FILE_NAME}' 파일을 찾을 수 없습니다.")
    st.info("💡 **해결 방법**: 현재 깃허브에 올리신 광주 데이터 파일명과 코드 상단의 `CSV_FILE_NAME = \"...\"` 부분이 대소문자 및 확장자까지 완벽히 일치하는지 확인 후 수정해 주세요.")
