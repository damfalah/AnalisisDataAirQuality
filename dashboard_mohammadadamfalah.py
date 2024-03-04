#Mengimport library
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore

#Side bar
with st.sidebar:
    st.markdown(
        "<div style='display: flex; justify-content: center; align-items: center; background-color: #1E90FF; padding: 20px; border-radius: 10px;'>"
        "<img src='https://media.licdn.com/dms/image/C4E03AQEOxY7VmZoN0w/profile-displayphoto-shrink_400_400/0/1642706331770?e=1715212800&v=beta&t=PePWpy4w8bl3M1_b4QfXtb5PLdusnG5GBLvTpZqFxTE' style='width: 80px; height: 80px; border-radius: 50%; margin-right: 20px;'>"
        "<div>"
        "<h1 style='color: white; margin-bottom: 5px;'>Mohammad Adam Falah</h1>"
        "<p style='color: white; margin: 0;'>Universitas Gunadarma</p>"
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )
    st.write('')
    st.text("Email    : m.adamfalah12@gmail.com")
    st.text("GitHub   : https://github.com/damfalah")
    st.text("LinkedIn : https://www.linkedin.com/in/adamfalah/")
    
st.title("Proyek Analisis Data: Air Quality Dataset")
st.write("- **Nama:** Mohammad Adam Falah")
st.write("- **Email:** m.adamfalah12@gmail.com")
st.write("- **ID:** 7385665")

#Pengolahan data-----------------------------------------------------------------------------------------------

# Mengambil data
aotizhongxin = pd.read_csv("D:\AnalisisDataAirQuality\dataset\PRSA_Data_Aotizhongxin_20130301-20170228.csv")
changping = pd.read_csv("D:\AnalisisDataAirQuality\dataset\PRSA_Data_Changping_20130301-20170228.csv")
dingling = pd.read_csv("D:\AnalisisDataAirQuality\dataset\PRSA_Data_Dingling_20130301-20170228.csv")
dongsi = pd.read_csv("D:\AnalisisDataAirQuality\dataset\PRSA_Data_Dongsi_20130301-20170228.csv")
guanyuan = pd.read_csv("D:\AnalisisDataAirQuality\dataset\PRSA_Data_Guanyuan_20130301-20170228.csv")
gucheng = pd.read_csv("D:\AnalisisDataAirQuality\dataset\PRSA_Data_Gucheng_20130301-20170228.csv")
huairou = pd.read_csv("D:\AnalisisDataAirQuality\dataset\PRSA_Data_Huairou_20130301-20170228.csv")
nongzhanguan = pd.read_csv("D:\AnalisisDataAirQuality\dataset\PRSA_Data_Nongzhanguan_20130301-20170228.csv")
shunyi = pd.read_csv("D:\AnalisisDataAirQuality\dataset\PRSA_Data_Shunyi_20130301-20170228.csv")
tiantan = pd.read_csv("D:\AnalisisDataAirQuality\dataset\PRSA_Data_Tiantan_20130301-20170228.csv")
wanliu = pd.read_csv("D:\AnalisisDataAirQuality\dataset\PRSA_Data_Wanliu_20130301-20170228.csv")
wanshouxigong = pd.read_csv("D:\AnalisisDataAirQuality\dataset\PRSA_Data_Wanshouxigong_20130301-20170228.csv")

#Menggabungkan data
data_frames = [aotizhongxin, changping, dingling, dongsi, guanyuan, gucheng, huairou, nongzhanguan, shunyi, tiantan, wanliu, wanshouxigong]
df = pd.concat(data_frames, axis=0)

#Mengisi missing value
#dengan mean
numerical_columns = df.select_dtypes(include=['number']).columns
df[numerical_columns] = df[numerical_columns].fillna(df[numerical_columns].mean())

#dengan modus pada kolom wd
wd_mode = df['wd'].mode()[0]
df['wd'].fillna(wd_mode, inplace=True)

#menghapus kolom yang tidak diperlukan
kolom_tidak_digunakan = ['PM10', "PRES", "DEWP", "wd", "WSPM"]
df_cleaned = df.drop(kolom_tidak_digunakan, axis=1)

# Mendefinisikan fungsi untuk membersihkan outlier berdasarkan z-score
def remove_outliers(df, threshold=3):
    z_scores = zscore(df.select_dtypes(include='number'))
    abs_z_scores = np.abs(z_scores)
    filtered_entries = (abs_z_scores < threshold).all(axis=1)
    return df[filtered_entries]

# Membersihkan outlier dari DataFrame df_cleaned
df_cleaned_no_outliers = remove_outliers(df_cleaned)

# Mengelompokkan data dan menghitung rata-rata tingkat polusi
meanPolutan = df_cleaned_no_outliers.groupby(by="station").agg({
    "SO2": ["mean"],
    "NO2": ["mean"],
    "CO": ["mean"],
    "O3": ["mean"]
})

# Menambahkan kolom untuk tingkat polusi rata-rata
meanPolutan["kadar_polusi"] = meanPolutan.mean(axis=1)

#--------------------------------------------------------------------------------------------------------------
#Pertanyaan 1--------------------------------------------------------------------------------------------------

# Dimana stasiun yang curah hujannya paling tinggi?
st.subheader("Dimana stasiun yang curah hujannya paling tinggi?")

rain_levels = df_cleaned.groupby('station')['RAIN'].mean().sort_values()

fig, ax = plt.subplots(figsize=(12, 6))
rain_levels.plot(kind='bar', color='lightblue', ax=ax)
ax.set_title('Rata-rata nilai Curah Hujan per Stasiun')
ax.set_xlabel('Stasiun')
ax.set_ylabel('Nilai Rata-rata Curah Hujan')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Menampilkan plot menggunakan Streamlit
st.pyplot(fig)

# Teks penjelasan analisis1
penjelasan1 = """
Penjelasan Analisis:

Berdasarkan grafik diatas dapat diambil analisis bahwa nilai rata-rata curah hujan tertinggi di stasiun Wanliu
"""
st.markdown(penjelasan1)

#--------------------------------------------------------------------------------------------------------------
#Pertanyaan 2--------------------------------------------------------------------------------------------------


#Stasiun mana yang memiliki suhu terendah dan suhu tertinggi?
st.subheader("Stasiun mana yang memiliki suhu terendah dan suhu tertinggi?")

volume_mean = df_cleaned_no_outliers.groupby(by="station").agg({
    "TEMP": ["max", "min"]
})

stations = volume_mean.index
maxTemp = volume_mean['TEMP']['max']
minTemp = volume_mean['TEMP']['min']

bar_width = 0.35

r1 = range(len(stations))
r2 = [x + bar_width for x in r1]

fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(r1, maxTemp, color='red', width=bar_width, edgecolor='grey', label='Max Temperature')
ax.bar(r2, minTemp, color='skyblue', width=bar_width, edgecolor='grey', label='Min Temperature')

ax.set_xlabel('Stasiun', fontsize=14)
ax.set_ylabel('Nilai Temperatur', fontsize=14)
ax.set_title('Nilai Maksimum Minimum Temperatur per Stasiun', fontsize=16)

ax.set_xticks([r + bar_width/2 for r in range(len(stations))])
ax.set_xticklabels(stations, rotation=45, ha='right')

# Menambahkan legenda
ax.legend()

# Menampilkan plot menggunakan Streamlit
st.pyplot(fig)

# Teks penjelasan analisis2
penjelasan2 = """
Penjelasan Analisis:

Berdasarkan grafik diatas dapat disimpulkan bahwa stasiun dengan Temperatur tertinggi adalah Gucheng dan stasiun dengan Temperatur terendah adalah Huairou
"""
st.markdown(penjelasan2)

#--------------------------------------------------------------------------------------------------------------
#Pertanyaan 3--------------------------------------------------------------------------------------------------

# Apakah ada hubungan antara suhu udara dengan konsentrasi CO?
st.subheader("Apakah ada hubungan antara suhu udara dengan konsentrasi CO?")

correlation_matrix = df_cleaned_no_outliers[["TEMP", "CO"]].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f") # Matrix heatmap
plt.title("Korelasi Temperatur dan CO")

# Menampilkan plot menggunakan Streamlit
st.pyplot(plt)

# Teks penjelasan analisis3
penjelasan3 = """
Penjelasan Analisis:

Terlihat bahwa Temperatur dan CO memiliki nilai korelasi yang negatif, yang berarti korelasi antara keduanya lemah
"""
st.markdown(penjelasan3)

#--------------------------------------------------------------------------------------------------------------
#Pertanyaan 4--------------------------------------------------------------------------------------------------

# Apakah meningkat atau menurunnya konsentrasi SO2 dapat ditentukan berdasarkan jam?
st.subheader("Apakah meningkat atau menurunnya konsentrasi SO2 dapat ditentukan berdasarkan jam?")

plt.figure(figsize=(12, 6))
sns.lineplot(data=df_cleaned_no_outliers, x="hour", y="SO2")
plt.title("SO2 Concentration by Hour")
plt.xlabel("Jam")
plt.ylabel("Konsentrasi SO2")
plt.grid(True)

# Menampilkan plot menggunakan Streamlit
st.pyplot(plt)

# Teks penjelasan analisis4
penjelasan4 = """
Penjelasan Analisis:

Dilihat dari grafik SO2 dapat ditentukan berdasarkan jam, yang mana pada pagi hingga ke siang konsentrasi SO2 akan meningkat. Kemudian pada siang hari hingga pagi konsentrasi SO2 akan menurun
"""
st.markdown(penjelasan4)

#--------------------------------------------------------------------------------------------------------------
#Pertanyaan 5--------------------------------------------------------------------------------------------------

#Pada stasiun mana konsentrasi polusi tertinggi dan terendah dengan melihat secara keseluruhan polutan?
st.subheader("Pada stasiun mana konsentrasi polusi tertinggi dan terendah dengan melihat secara keseluruhan polutan?")

stations = meanPolutan.index
nilaiMeanPolutan = meanPolutan["kadar_polusi"]

plt.figure(figsize=(10, 6))
plt.bar(stations, nilaiMeanPolutan, color="skyblue")

plt.xlabel("Stasiun")
plt.ylabel("Nilai Mean Polusi")
plt.title("Nilai Mean Polusi per Stasiun")
plt.xticks(rotation=45, ha="right")

plt.tight_layout()

# Displaying the plot using Streamlit
st.pyplot(plt)

# Teks penjelasan analisis5
penjelasan5 = """
Penjelasan Analisis:

Terlihat bahwa konsentrasi polusi tertinggi terdapat pada stasiun Wanshouxigong dan konsentrasi polusi terendah terdapat pada stasiun Dingling
"""
st.markdown(penjelasan5)

#--------------------------------------------------------------------------------------------------------------

# Conclusion Section
st.header("Conclusion")
st.markdown("""
1. **Dimana stasiun yang curah hujannya paling tinggi?**
    > Walaupun tidak jauh berbeda nilainya, tetapi curah hujan tertinggi berada di stasiun Wanliu dengan nilai curah hujan 0.068261

2. **Berapa lama rata-rata pengiriman paket pengiriman paket terlama ? dari mana ke mana?**
    > Stasiun yang memiliki suhu terendah adalah stasiun Huairou dengan nilai 41.6, dan stasiun yang memiliki suhu tertinggi adalah stasiun Guchen dengan niali -19.9

3. **Bagian hari apa yang sering digunakan oleh pembeli untuk melakukan transaksi?**
    > Suhu udara atau temperatur memiliki korelasi yang lemah terhadap CO yang bernilai -0.26, dan berkorelasi negatif

4. **Berapa rata-rata payment value dari tiap tipe transaksi? dan transaksi tipe apa yang paling sering digunakan?**
    > Iya, Konsetrasi SO2 dapat ditentukan berdasarkan jam. Yang mana konsentrasi SO2 akan meningkat saat pagi hingga siang (jam 5 pagi hingga jam 11 siang), dan konsentrasi SO2 akan menurun saat siang hingga pagi (jam 11 siang hingga jam 5 pagi)

5. **Bagaimana perbandingan penjualan tahun 2017 dan 2018?**
    > Stasiun yang memiliki konsentrasi polusi tertinggi adalah stasiun Wanshouxigong dengan nilai rata-rata konsentrasi polusi 321.80, dan stasiun yang memiliki konsentrasi polusi terendah adalah stasiun Dingling dengan nilai rata-rata konsentrasi polusi 240.05
""")