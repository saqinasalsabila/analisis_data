import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

# Load dataset (gantilah dengan path file CSV yang sesuai)
file_path = "https://raw.githubusercontent.com/saqinasalsabila/analisis_data/main/day_bike.csv"

df_day = pd.read_csv(file_path)

# Set judul aplikasi
st.title("Bike Rental Analysis with Streamlit")

# Pilihan pertanyaan
selected_tab = st.sidebar.radio("Select Question", ["Bike Rentals by Month", "Peak Day Rentals", "Season, Weather, and Rentals", "Holiday vs Weekday Rentals"])

# Analisis pertanyaan berdasarkan tab yang dipilih
if selected_tab == "Bike Rentals by Month":
    # Menampilkan filter tahun
    selected_year = st.selectbox("Select Year", df_day['year'].unique())

    # Filter dataframe berdasarkan tahun yang dipilih
    filtered_df = df_day[df_day['year'] == selected_year]

    # Urutkan bulan
    months_order = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "oktober", "november", "desember"]
    filtered_df.loc[:, 'month'] = pd.Categorical(filtered_df['month'], categories=months_order, ordered=True)

    # Urutkan DataFrame berdasarkan bulan
    filtered_df = filtered_df.sort_values('month')

    # Visualisasi distribusi peminjaman sepeda berdasarkan bulan
    monthly_stats = filtered_df.groupby('month', observed=False)['count'].agg(['sum']).reset_index()
    st.bar_chart(monthly_stats.set_index('month'))

elif selected_tab == "Peak Day Rentals":
    # Visualisasi rata-rata jumlah peminjaman sepeda berdasarkan hari
    st.header("Peak Day Rentals")
    weekday_counts = df_day.groupby('weekday')['count'].agg(['mean']).reset_index()
    st.bar_chart(weekday_counts.set_index('weekday'))

elif selected_tab == "Season, Weather, and Rentals":
    # Pilih musim
    selected_season = st.selectbox("Select Season", df_day['season'].unique())

    # Pilih cuaca
    selected_weather = st.selectbox("Select Weather", df_day['weather'].unique())

    # Filter dataframe berdasarkan musim dan cuaca yang dipilih
    filtered_df = df_day[(df_day['season'] == selected_season) & (df_day['weather'] == selected_weather)]

    # Agregasi data untuk mendapatkan total peminjaman berdasarkan musim dan cuaca
    aggregated_df = filtered_df.groupby(['season', 'weather'])['count'].sum().reset_index()

    # Tampilkan chart menggunakan altair
    chart = alt.Chart(aggregated_df).mark_bar().encode(
        x='season:N',
        y='count:Q',
        color='weather:N',
        tooltip=['season:N', 'weather:N', 'count:Q']
    ).properties(
        width=500,
        height=300
    )

    st.altair_chart(chart, use_container_width=True)

elif selected_tab == "Holiday vs Weekday Rentals":
    # Visualisasi perbedaan jumlah peminjaman sepeda pada hari libur dan hari kerja dalam persentase
    st.header("Difference in Bike Rentals on Holidays and Weekdays (Percentage)")

    # Menghitung total peminjaman pada hari libur dan hari kerja
    total_holidays = df_day[df_day['holiday'] == 1]['count'].sum()
    total_weekdays = df_day[df_day['holiday'] == 0]['count'].sum()

    # Menghitung persentase peminjaman pada hari libur dan hari kerja
    percentage_holidays = (total_holidays / (total_holidays + total_weekdays)) * 100
    percentage_weekdays = (total_weekdays / (total_holidays + total_weekdays)) * 100

    # Menampilkan hasil dalam bentuk bar chart
    holiday_weekday_stats = pd.DataFrame({
        'Category': ['Holidays', 'Weekdays'],
        'Percentage': [percentage_holidays, percentage_weekdays]
    })

    st.bar_chart(holiday_weekday_stats.set_index('Category'))
