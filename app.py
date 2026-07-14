import streamlit as st
import pandas as pd
import numpy as np

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="JAWARA DATA v3", page_icon="🚀", layout="wide")

# --- 2. GENERASI DATA DUMMY (Realistis) ---
@st.cache_data
def generate_energy_data():
    np.random.seed(42)
    dates = pd.date_range(start="2026-01-01", periods=180, freq="D")
    base_kwh = np.linspace(250, 150, 180) + np.random.normal(0, 15, 180)
    carbon_footprint = base_kwh * 0.85 # Asumsi 1 kWh = 0.85 Kg CO2
    
    df = pd.DataFrame({
        'Tanggal': dates,
        'Pemakaian Listrik (kWh)': np.round(base_kwh, 2),
        'Jejak Karbon (Kg CO2)': np.round(carbon_footprint, 2)
    })
    return df

@st.cache_data
def generate_student_data():
    return pd.DataFrame({
        'ID Siswi': ['SRI-001', 'SRI-002', 'SRI-003', 'SRI-004', 'SRI-005', 'SRI-006', 'SRI-007', 'SRI-008'],
        'Nama': ['Siti', 'Ayu', 'Rina', 'Desi', 'Wati', 'Nia', 'Fitri', 'Lestari'],
        'Kelas': ['X-TKJ', 'X-RPL', 'XI-TKJ', 'XI-RPL', 'X-RPL', 'XI-TKJ', 'X-TKJ', 'XI-RPL'],
        'Literasi Data Awal': [45, 50, 40, 55, 48, 42, 52, 49],
        'Literasi Data Akhir': [88, 92, 85, 95, 89, 87, 94, 91],
        'Proyek Selesai': [3, 4, 3, 5, 4, 3, 5, 4],
        'Status Ekonomi': ['Pra-Sejahtera', 'Menengah', 'Pra-Sejahtera', 'Menengah', 'Pra-Sejahtera', 'Pra-Sejahtera', 'Menengah', 'Pra-Sejahtera']
    })

df_energy = generate_energy_data()
df_students = generate_student_data()

# --- 3. SIDEBAR NAVIGASI ---
st.sidebar.title("🚀 Navigasi Sistem")
st.sidebar.markdown("Pilih Modul Analitik:")
menu = st.sidebar.radio("", [
    "📊 Pantau Energi (Go Green)", 
    "👩‍💻 Profil Srikandi Data (GESI)", 
    "🤖 Prediksi AI Jejak Karbon"
])

st.sidebar.markdown("---")
st.sidebar.caption("Sistem didukung oleh infrastruktur PT. Boyang Digital Nusantara - Banten")

# --- 4. LOGIKA ROUTING HALAMAN ---

if menu == "📊 Pantau Energi (Go Green)":
    st.title("🌱 Dasbor Analitik Efisiensi Energi Sekolah")
    st.markdown("Pemantauan *real-time* penggunaan daya listrik dan kalkulasi jejak karbon operasional harian.")
    
    # Metrik Utama
    col1, col2, col3, col4 = st.columns(4)
    total_kwh = df_energy['Pemakaian Listrik (kWh)'].sum()
    total_co2 = df_energy['Jejak Karbon (Kg CO2)'].sum()
    rata_harian = df_energy['Pemakaian Listrik (kWh)'].mean()
    
    col1.metric("Total Pemakaian (6 Bulan)", f"{total_kwh:,.0f} kWh")
    col2.metric("Total Jejak Karbon", f"{total_co2:,.0f} Kg")
    col3.metric("Rata-rata Harian", f"{rata_harian:.1f} kWh", "-12.5% dari target")
    col4.metric("Status Zonasi", "Aman", "Rekomendasi aktif")

    st.markdown("---")
    
    # Grafik Utama
    st.subheader("Tren Pemakaian Listrik Harian (Januari - Juni 2026)")
    st.line_chart(df_energy.set_index('Tanggal')['Pemakaian Listrik (kWh)'], color="#17B169")
    
    # Tabel Data
    st.subheader("Log Data Harian")
    st.dataframe(df_energy.sort_values(by="Tanggal", ascending=False).head(10), use_container_width=True)
    
    # Fitur Download Laporan
    csv_energy = df_energy.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Unduh Laporan Energi (CSV)",
        data=csv_energy,
        file_name='laporan_energi_sekolah.csv',
        mime='text/csv',
    )

elif menu == "👩‍💻 Profil Srikandi Data (GESI)":
    st.title("👩‍💻 Analitik Kompetensi Siswi (Fokus GESI)")
    st.markdown("Rekam jejak peningkatan literasi *Data Science* pada siswi perempuan kelompok rentan di Pandeglang.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Sebaran Peningkatan Kemampuan")
        df_students['Peningkatan (%)'] = ((df_students['Literasi Data Akhir'] - df_students['Literasi Data Awal']) / df_students['Literasi Data Awal']) * 100
        st.dataframe(df_students[['Nama', 'Kelas', 'Literasi Data Awal', 'Literasi Data Akhir', 'Peningkatan (%)']], use_container_width=True)
    
    with col2:
        st.subheader("Komparasi Literasi (Pre vs Post)")
        chart_data = df_students[['Nama', 'Literasi Data Awal', 'Literasi Data Akhir']].set_index('Nama')
        st.bar_chart(chart_data)

    st.markdown("---")
    st.subheader("Korelasi Proyek Diselesaikan vs Status Ekonomi")
    st.markdown("Sistem memprioritaskan siswi dari keluarga pra-sejahtera untuk memimpin proyek industri nyata.")
    
    # Tampilan kartu profil terbaik
    top_student = df_students.sort_values(by="Literasi Data Akhir", ascending=False).iloc[0]
    st.info(f"🏆 **Performa Tertinggi Bulan Ini:** {top_student['Nama']} ({top_student['Kelas']}) - Menyelesaikan {top_student['Proyek Selesai']} Proyek Analitik. Status: {top_student['Status Ekonomi']}.")

elif menu == "🤖 Prediksi AI Jejak Karbon":
    st.title("🤖 Simulasi Prediksi (*Machine Learning*)")
    st.markdown("Gunakan model *forecasting* ini untuk melihat potensi penghematan anggaran dan penurunan karbon jika kebijakan *Go Green* diterapkan lebih agresif.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Parameter Kebijakan")
        jam_pemangkasan = st.slider("Pemangkasan Jam AC/Hari (Jam)", 0, 5, 2)
        lampu_led = st.radio("Migrasi 100% Lampu LED?", ["Ya", "Belum"])
        
        # Logika Prediksi Sederhana
        penghematan_base = jam_pemangkasan * 15.5
        if lampu_led == "Ya":
            penghematan_base += 20.0
            
    with col2:
        st.subheader("Hasil Prediksi 30 Hari Kedepan")
        prediksi_kwh = (150 * 30) - (penghematan_base * 30)
        prediksi_co2 = prediksi_kwh * 0.85
        estimasi_rupiah = prediksi_kwh * 1444 # Tarif dasar listrik asumsi
        
        st.success(f"⚡ **Proyeksi Pemakaian:** {prediksi_kwh:,.0f} kWh / bulan")
        st.success(f"🌍 **Proyeksi Jejak Karbon:** {prediksi_co2:,.0f} Kg CO2 / bulan")
        st.success(f"💰 **Estimasi Tagihan:** Rp {estimasi_rupiah:,.0f}")
        
        st.markdown(f"**Insight AI:** Dengan kebijakan pemangkasan AC selama {jam_pemangkasan} jam dan status migrasi LED '{lampu_led}', sekolah diprediksi akan menghemat anggaran hingga **Rp {(penghematan_base * 30 * 1444):,.0f}** bulan depan.")
