# import semua library yang digunakan
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import math
from babel.numbers import format_currency
sns.set(style='white')

df = pd.read_csv("https://raw.githubusercontent.com/sanitrisna/projek/main/Dashboard/main_data.csv")

datetime_columns = ["dteday"]
df.sort_values(by="dteday", inplace=True)
df.reset_index(inplace=True)
 
for column in datetime_columns:
    df[column] = pd.to_datetime(df[column])

min_date = df["dteday"].min()
max_date = df["dteday"].max()
 
 # Membuat sidebar
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://png.pngtree.com/png-clipart/20220306/original/pngtree-cartoon-boy-riding-a-bike-png-image_7411085.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    # Membuat filter dengan option season dan weathersit
    filter = st.selectbox(
        label="Pilih flter berdasarkan :",
        options=('season', 'weathersit')
    )

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

filter_date = df[(df["dteday"]>= start_date) & (df["dteday"]<= end_date) ]

# Memberikan judul dashboard
st.title('Dashboard Bike Sharing Dataset')
# Membuat tab
tab1, tab2, tab3 = st.tabs(["Diagram Batang", "Diagram Garis", "About"])
 
with tab1:
    st.header("Diagram Batang")
    # Membuat widget
    
    def calculate_cnt(filter):
        if filter == 'season':
            total_season_1 = filter_date[filter_date["season"] == 1]["cnt"].sum()
            total_season_2 = filter_date[filter_date["season"] == 2]["cnt"].sum()
            total_season_3 = filter_date[filter_date["season"] == 3]["cnt"].sum()
            total_season_4 = filter_date[filter_date["season"] == 4]["cnt"].sum()
            return total_season_1, total_season_2, total_season_3, total_season_4
        elif filter == 'weathersit':
            total_weathersit_1 = filter_date[filter_date["weathersit"] == 1]["cnt"].sum()
            total_weathersit_2 = filter_date[filter_date["weathersit"] == 2]["cnt"].sum()
            total_weathersit_3 = filter_date[filter_date["weathersit"] == 3]["cnt"].sum()
            total_weathersit_4 = filter_date[filter_date["weathersit"] == 4]["cnt"].sum()
            return total_weathersit_1, total_weathersit_2, total_weathersit_3, total_weathersit_4

    # Menghitung jumlah cnt pada filter yang diipilih
    if filter:
        if filter == 'season':
            total_season_1, total_season_2, total_season_3, total_season_4 = calculate_cnt(filter)
            # Tampilkan metric
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Season 1 (Springer)", value=total_season_1)
                st.metric("Total Season 2 (Summer)", value=total_season_2)
            with col2:
                st.metric("Total Season 3 (Fall)", value=total_season_3)
                st.metric("Total Season 4 (Winter)", value=total_season_4)
        elif filter == 'weathersit':
            total_weathersit_1, total_weathersit_2, total_weathersit_3, total_weathersit_4 = calculate_cnt(filter)
            # Tampilkan metric
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Weathersit 1", value=total_weathersit_1)
                st.metric("Total Weathersit 2", value=total_weathersit_2)
            with col2:
                st.metric("Total Weathersit 3", value=total_weathersit_3)
                st.metric("Total Weathersit 4", value=total_weathersit_4)

    # Membuat bar chart
                
    import seaborn as sns
    import pandas as pd

    # Menghitung jumlah 'cnt', 'registered', dan 'casual'
    total_counts = filter_date.groupby(filter)[['cnt', 'registered', 'casual']].sum().reset_index()

    # Melting DataFrame untuk menjadikan 'cnt', 'registered', dan 'casual' menjadi baris baru
    melted_df = total_counts.melt(id_vars=filter, value_vars=['cnt', 'registered', 'casual'], var_name='variable', value_name='total_value')

    # Membuat bar plot menggunakan seaborn
    fig, ax = plt.subplots()
    sns.barplot(data=melted_df, x=filter, y="total_value", hue="variable")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))
    st.pyplot(fig)

    # Menambahkan keterangan
    if filter == "season":
        st.caption("""
        - 1: Springer
        - 2: Summer
        - 3: Fall
        - 4: Winter
        """)
    elif filter == "weathersit" :
        st.caption("""
        - 1: Clear, Few clouds, Partly cloudy, Partly cloudy
        - 2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist
        - 3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds
        - 4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog
        """)
    # Menambahkan caption
    st.caption('Diagram batang jumlah peminjam sepeda berdasarkan ' + str(filter))

with tab2:
    st.header("Diagram Garis")
    # Membuat widget rata-rata peminjaman
    # Menghitung rata-rata
    average_cnt = math.ceil(filter_date["cnt"].mean())
    average_registered = math.ceil(filter_date["registered"].mean())
    average_casual = math.ceil(filter_date["casual"].mean())

    # Tampilkan metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Rata-rata cnt", value=average_cnt)
        st.metric("Rata-rata registered", value=average_registered)
        st.metric("Rata-rata casual", value=average_casual)
        
    # Membuat diagram garis
    fig, ax = plt.subplots(figsize=(16, 8))

    # Plot cnt
    ax.plot(filter_date["dteday"], filter_date["cnt"], label='cnt', marker='o', linewidth=2, color="#90CAF9")
    # Plot registered
    ax.plot(filter_date["dteday"], filter_date["registered"], label='registered', marker='o', linewidth=2, color="#FFA726")
    # Plot casual
    ax.plot(filter_date["dteday"], filter_date["casual"], label='casual', marker='o', linewidth=2, color="#4CAF50")

    # Pengaturan plot
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    ax.legend(fontsize=15)
    ax.set_xlabel('Tanggal', fontsize=20)
    ax.set_ylabel('Jumlah Peminjam Sepeda', fontsize=20)
    ax.set_title('Plot Harian Jumlah Peminjam Sepeda', fontsize=25)

    plt.xticks(rotation=45)

    # Menampilkan diagram menggunakan st.pyplot()
    st.pyplot(fig)

    # Menambahkan caption
    st.caption('Diagram garis jumlah peminjam sepeda berdasarkan ' + str(filter))

with tab3:
    st.header("About Dashboard")
    st.caption('Dashboard sederhana yang menyajikan visualisasi dari Bike Sharing Dataset. Dashboard ini dibuat untuk memvisulisasikan jumlah peminjam sepeda berdasarkan musim dan cuacanya, dengan tujuan agar mudah dipahami oleh orang awam dan untuk keperluan bisnis peminjaman sepeda')