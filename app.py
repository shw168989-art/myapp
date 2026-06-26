import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. 페이지 설정 및 한글 폰트 설정
st.set_page_config(page_title="버스 정류장 분석 대시보드", layout="wide")

# (중요) Streamlit Cloud(리눅스) 환경에서는 나눔폰트 등이 설치되어 있지 않아 
# 한글이 깨질 수 있습니다. 이를 방지하기 위해 제목 등을 영어로 쓰거나, 
# 아래와 같이 폰트 설정을 시도합니다.
plt.rcParams['font.family'] = 'sans-serif' # 기본 폰트 설정
plt.rcParams['axes.unicode_minus'] = False

st.title("🚌 버스 정류장별 권종별 이용 현황")

# 2. 파일 업로드 기능
uploaded_file = st.sidebar.file_uploader("버스 데이터(CSV)를 업로드하세요", type=["csv"])

if uploaded_file is not None:
    # 데이터 로드
    bus = pd.read_csv(uploaded_file)
    
    st.subheader("📋 데이터 미리보기")
    st.write(bus.head())

    # 3. 데이터 전처리 (제공해주신 로직)
    # 정류장명, 권종별 거래건수 합계 계산
    agg_df = bus.groupby(['정류장명', '권종'])['거래건수'].sum().reset_index()

    # 사이드바에서 상위 N개 선택 가능하게 설정 (기존 10개에서 확장)
    top_n = st.sidebar.slider("상위 몇 개의 정류장을 볼까요?", 5, 30, 10)

    # 상위 정류장 추출
    top_stations = agg_df.groupby('정류장명')['거래건수'].sum().nlargest(top_n).index
    filtered_agg_df = agg_df[agg_df['정류장명'].isin(top_stations)]

    # 4. 시각화 (Seaborn)
    st.subheader(f"📊 상위 {top_n}개 정류장 권종별 이용 분석")
    
    color_palette = {'어린이': 'red', '일반': 'yellow', '청소년': 'blue'}
    
    # Matplotlib 객체 생성
    fig, ax = plt.subplots(figsize=(15, 8))
    sns.barplot(data=filtered_agg_df, x='정류장명', y='거래건수', hue='권종', palette=color_palette, ax=ax)
    
    # 한글 깨짐 대비: Streamlit Cloud에서는 제목에 한글이 안 나올 수 있어 영문 병기 추천
    ax.set_title(f'Top {top_n} Stations by Ticket Type', fontsize=15)
    ax.set_xlabel('Station Name', fontsize=12)
    ax.set_ylabel('Transaction Count', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    
    # 스트림릿에 그래프 출력
    st.pyplot(fig)

    # 5. 상세 데이터 표 출력
    with st.expander("상세 데이터 보기"):
        st.dataframe(filtered_agg_df)

else:
    st.info("왼쪽 사이드바에서 CSV 파일을 업로드해주세요.")
    # 테스트용 데이터가 없을 때 보여줄 예시 설명
    st.warning("데이터에는 '정류장명', '권종', '거래건수' 컬럼이 반드시 포함되어야 합니다.")
