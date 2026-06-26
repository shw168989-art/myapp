import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 페이지 기본 설정
st.set_page_config(page_title="California Housing Dashboard", layout="wide")

# 대시보드 제목
st.title("🏠 캘리포니아 주택 데이터 대시보드")

# 1. 데이터 로드 (캐싱을 사용하여 속도 최적화)
@st.cache_data
def load_data():
    # 구글에서 공식 제공하는 안정적인 데이터셋 URL로 변경
    url = "https://download.mlcc.google.com/mledu-datasets/california_housing_train.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

# 2. 데이터프레임 미리보기
st.subheader("📊 데이터프레임 미리보기")
st.write("데이터의 첫 5행을 확인합니다.")
st.dataframe(df.head())

st.divider() # 구분선

# 3. 특정 컬럼 간의 관계 시각화 (Scatter Plot)
st.subheader("💰 중간 소득 vs 중간 주택 가격")
fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.scatter(df['median_income'], df['median_house_value'], alpha=0.5, color='cornflowerblue')
ax1.set_title('Median Income vs Median House Value')
ax1.set_xlabel('Median Income')
ax1.set_ylabel('Median House Value')
ax1.grid(True)
st.pyplot(fig1)

st.divider()

# 4. 주택 연식 분포 시각화 (Histogram)
st.subheader("🏢 주택 연식 분포")
fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.hist(df['housing_median_age'], bins=30, edgecolor='black', color='lightcoral')
ax2.set_title('Distribution of Housing Median Age')
ax2.set_xlabel('Housing Median Age')
ax2.set_ylabel('Frequency')
ax2.grid(True)
st.pyplot(fig2)
