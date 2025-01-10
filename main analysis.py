import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rc


import platform
if platform.system() == 'Darwin':  # macOS
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows':  # Windows
    rc('font', family='Malgun Gothic')
else:  # Linux 등 기타
    rc('font', family='NanumGothic')

# 그래프에서 마이너스 기호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False

# pandas 출력 글자 크기 설정
pd.set_option('display.max_columns', None)  # 모든 열 출력
pd.set_option('display.max_rows', None)  # 모든 행 출력
pd.set_option('display.width', 1000)  # 출력 너비 설정
pd.set_option('display.max_colwidth', 200)  # 열의 최대 너비 설정
pd.set_option('display.float_format', '{:,.2f}'.format)  # 실수 포맷 설정
pd.set_option('display.max_seq_item', None)  # 긴 시퀀스 출력

# 데이터 로드
file_path = r"C:\src\netflix_titles.csv"  # 데이터 파일 경로
df = pd.read_csv(file_path)

# 데이터 확인
print(df.head())  # 첫 5행 출력
print(df.info())  # 데이터 정보 출력

# NaN 값 처리
df['listed_in'] = df['listed_in'].fillna('')  # 장르 결측값을 빈 문자열로 대체
df['country'] = df['country'].fillna('Unknown')  # 국가 결측값을 "Unknown"으로 대체

# ----------------------------------------
# 1. 영화와 TV 쇼의 비율 비교
# ----------------------------------------

# (1) 영화와 TV 쇼의 비율 비교
type_counts = df['type'].value_counts()
plt.figure(figsize=(6, 4))
type_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['skyblue', 'orange'])
plt.title('영화와 TV 프로그램(show)의 비율 (Netflix)', fontsize=14)
plt.ylabel('', fontsize=12)
plt.show()

# (2) 영화와 TV 쇼의 출시 연도 비교
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='release_year', hue='type', kde=False, bins=20, palette='pastel')
plt.title('출시 연도별 TV 프로그램(show) 분포', fontsize=14)
plt.xlabel('출시 연도', fontsize=12)
plt.ylabel('개수', fontsize=12)
plt.legend(title='타입', labels=['영화', 'TV 쇼'], fontsize=12)
plt.tight_layout()  # 레이아웃 자동 조정
plt.show()

# (3) 영화와 TV 쇼의 장르 비교
movies_genres = df[df['type'] == 'Movie']['listed_in'].str.split(', ').explode()
tv_genres = df[df['type'] == 'TV Show']['listed_in'].str.split(', ').explode()

# 상위 장르 추출
top_movie_genres = movies_genres.value_counts().head(10)
top_tv_genres = tv_genres.value_counts().head(10)

# 시각화
plt.figure(figsize=(12, 6))
plt.bar(top_movie_genres.index, top_movie_genres.values, label='영화', color='skyblue', alpha=0.7)
plt.bar(top_tv_genres.index, top_tv_genres.values, label='TV 쇼', color='orange', alpha=0.7)
plt.title('영화와 TV 프로그램(show)에서 인기 있는 장르', fontsize=14)
plt.xlabel('장르', fontsize=12)
plt.ylabel('개수', fontsize=12)
plt.xticks(rotation=45, fontsize=10)  # x축 라벨 회전
plt.legend(fontsize=12)
plt.tight_layout()  # 레이아웃 자동 조정
plt.show()

# ----------------------------------------
# 4. 장르 트렌드 분석
# ----------------------------------------

# (1) 출시 연도별 인기 장르 변화
genres_by_year = df.explode('listed_in').groupby(['release_year', 'listed_in']).size().reset_index(name='count')
top_genres = genres_by_year.groupby('release_year').apply(lambda x: x.nlargest(5, 'count')).reset_index(drop=True)

# 시각화
plt.figure(figsize=(6, 4))  # 그래프 크기 조정
for genre in top_genres['listed_in'].unique():
    subset = top_genres[top_genres['listed_in'] == genre]
    plt.plot(subset['release_year'], subset['count'], label=genre)

plt.title('연도별 인기 장르 변화', fontsize=14)
plt.xlabel('출시 연도', fontsize=12)
plt.ylabel('개수', fontsize=12)
plt.legend(title='장르', fontsize=12, bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()  # 레이아웃 자동 조정
plt.subplots_adjust(right=0.8)  # 여백을 조정하여 텍스트가 잘리지 않게 함
plt.show()

# (2) 장르와 국가의 연관성 분석
country_genres = df[['country', 'listed_in']].dropna()
country_genres = country_genres.explode('listed_in')

# 상위 국가별 장르 분석
top_countries = country_genres['country'].value_counts().head(10).index
filtered_data = country_genres[country_genres['country'].isin(top_countries)]

# 시각화
plt.figure(figsize=(12, 6))  # 그래프 크기 조정
sns.countplot(data=filtered_data, y='country', hue='listed_in', palette='pastel', order=top_countries)
plt.title('주요 국가별 인기 장르', fontsize=14)
plt.xlabel('개수', fontsize=12)
plt.ylabel('국가', fontsize=12)

# 범례 위치 조정: 그래프 밖으로 이동
plt.legend(title='장르', fontsize=12, bbox_to_anchor=(1.05, 1), loc='upper left')

# 레이아웃 자동 조정 및 여백 조정
plt.tight_layout()  # 레이아웃 자동 조정
plt.subplots_adjust(right=0.8)  # 여백을 조정하여 텍스트가 잘리지 않게 함
plt.show()