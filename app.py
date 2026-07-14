import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="JAWARA DATA Ultimate", page_icon="🏆", layout="wide")

# --- 2. INISIALISASI DATABASE SEMENTARA (SESSION STATE) ---
# Ini memungkinkan input manual tersimpan selama aplikasi berjalan
if 'energy_data' not in st.session_state:
    # Data awal (Baseline)
    dates = pd.date_range(start="2026-06-01", periods=30, freq="D")
    base_kwh = np.linspace(200, 150, 30) + np.random.normal(0, 10, 30)
    st.session_state['energy_data'] = pd.DataFrame({
        'Tanggal': dates,
        'Pemakaian Listrik (kWh)': np.round(base_kwh, 2),
        'Jejak Karbon (Kg CO2)': np.round(base_kwh * 0.85, 2)
    })

if 'student_data' not in st.session_state:
    st.session_state['student_data'] = pd.DataFrame({
        'ID Siswi': ['SRI-001', 'SRI-002', 'SRI-003'],
        'Nama': ['Siti (Contoh)', 'Ayu (Contoh)', 'Rina (Contoh)'],
        'Status Ekonomi': ['Pra-Sejahtera', 'Menengah', 'Pra-Sejahtera'],
        'Literasi Awal': [45, 50, 40],
        'Literasi Akhir': [88, 92, 85],
        'Kehadiran (%)': [95, 100, 90]
    })

# --- 3. SIDEBAR & NAVIGASI ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2103/2103254.png", width=80)
st.sidebar.title("Navigasi JAWARA DATA")
menu = st.sidebar.radio("Pilih Modul Sistem:", [
    "🏠 Beranda Eksekutif", 
    "✍️ Input Data Manual", 
    "🌍 Pantau Energi (Go Green)", 
    "👩‍💻 Analisis Srikandi (GESI)", 
    "🤖 AI Automation (Auto-Predict)"
])
st.sidebar.markdown("---")
st.sidebar.caption("© 2026 - Dikembangkan untuk Kompetisi Inovasi Pendidikan Banten")

# --- 4. LOGIKA MODUL HALAMAN ---

if menu == "🏠 Beranda Eksekutif":
    st.title("🏆 JAWARA DATA (Versi Ultimate)")
    st.markdown("Sistem Pemantauan Jejak Karbon & Inklusi Sosial Terintegrasi AI Automations.")
    
    col1, col2, col3 = st.columns(3)
    df_e = st.session_state['energy_data']
    df_s = st.session_state['student_data']
    
    col1.metric("Total Pemakaian Energi Tercatat", f"{df_e['Pemakaian Listrik (kWh)'].sum():,.0f} kWh")
    col2.metric("Total Jejak Karbon", f"{df_e['Jejak Karbon (Kg CO2)'].sum():,.0f} Kg CO2")
    col3.metric("Total Siswi Terbina (GESI)", f"{len(df_s)} Orang")
    
    st.info("👈 Gunakan navigasi di sebelah kiri untuk menginput data baru secara manual atau menjalankan eksekusi AI.")

elif menu == "✍️ Input Data Manual":
    st.title("✍️ Modul Input Data Manual")
    st.markdown("Masukkan data operasional sekolah harian atau data siswi baru di sini. Data akan langsung terhubung dengan mesin AI.")
    
    tab1, tab2 = st.tabs(["⚡ Input Listrik Harian", "👩‍🎓 Registrasi Siswi Baru"])
    
    with tab1:
        with st.form("form_energi", clear_on_submit=True):
            st.subheader("Catat Penggunaan Daya Hari Ini")
            tgl_input = st.date_input("Tanggal Pencatatan")
            kwh_input = st.number_input("Pemakaian Listrik (kWh)", min_value=0.0, value=150.0, step=1.5)
            submit_energi = st.form_submit_button("Simpan Data Energi")
            
            if submit_energi:
                co2_calc = round(kwh_input * 0.85, 2)
                new_e_data = pd.DataFrame({
                    'Tanggal': [pd.to_datetime(tgl_input)],
                    'Pemakaian Listrik (kWh)': [kwh_input],
                    'Jejak Karbon (Kg CO2)': [co2_calc]
                })
                st.session_state['energy_data'] = pd.concat([st.session_state['energy_data'], new_e_data], ignore_index=True)
                st.success(f"Data tanggal {tgl_input} berhasil disimpan! Jejak Karbon: {co2_calc} Kg CO2.")

    with tab2:
        with st.form("form_siswi", clear_on_submit=True):
            st.subheader("Registrasi Srikandi Data Baru")
            nama_input = st.text_input("Nama Siswi")
            ekonomi_input = st.selectbox("Status Ekonomi Keluarga", ["Pra-Sejahtera", "Menengah", "Mampu"])
            lit_awal = st.slider("Nilai Pre-Test (Literasi Awal)", 0, 100, 50)
            lit_akhir = st.slider("Nilai Post-Test (Literasi Akhir)", 0, 100, 85)
            hadir = st.slider("Persentase Kehadiran (%)", 0, 100, 95)
            submit_siswi = st.form_submit_button("Simpan Profil Siswi")
            
            if submit_siswi:
                new_id = f"SRI-{len(st.session_state['student_data']) + 1:03d}"
                new_s_data = pd.DataFrame({
                    'ID Siswi': [new_id], 'Nama': [nama_input], 'Status Ekonomi': [ekonomi_input],
                    'Literasi Awal': [lit_awal], 'Literasi Akhir': [lit_akhir], 'Kehadiran (%)': [hadir]
                })
                st.session_state['student_data'] = pd.concat([st.session_state['student_data'], new_s_data], ignore_index=True)
                st.success(f"Siswi {nama_input} berhasil diregistrasi dengan ID {new_id}!")

elif menu == "🌍 Pantau Energi (Go Green)":
    st.title("🌍 Dasbor Go Green & Jejak Karbon")
    df_e = st.session_state['energy_data'].sort_values('Tanggal')
    
    st.line_chart(df_e.set_index('Tanggal')['Pemakaian Listrik (kWh)'], color="#17B169")
    st.dataframe(df_e, use_container_width=True)
    
    csv_e = df_e.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Unduh Laporan Lingkungan (CSV)", csv_e, "laporan_gogreen.csv", "text/csv")

elif menu == "👩‍💻 Analisis Srikandi (GESI)":
    st.title("👩‍💻 Analisis Kesetaraan Gender & Inklusi Sosial")
    df_s = st.session_state['student_data']
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Data Peserta Didik Perempuan")
        st.dataframe(df_s, use_container_width=True)
    with col2:
        st.subheader("Distribusi Status Ekonomi (Inklusi)")
        st.bar_chart(df_s['Status Ekonomi'].value_counts())
        
    csv_s = df_s.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Unduh Laporan GESI (CSV)", csv_s, "laporan_gesi.csv", "text/csv")

elif menu == "🤖 AI Automation (Auto-Predict)":
    st.title("🤖 Eksekusi AI Automations")
    st.markdown("Mesin *Machine Learning* (Regresi Linear) akan membaca data historis yang telah Anda input dan mengeksekusi prediksi secara otomatis.")
    
    tab_ai1, tab_ai2 = st.tabs(["⚡ Auto-Predict Tagihan Listrik", "🎓 Auto-Predict Potensi Siswi"])
    
    with tab_ai1:
        st.subheader("AI Prediksi Pemakaian Energi 7 Hari Kedepan")
        df_e = st.session_state['energy_data'].copy()
        
        if len(df_e) > 5:
            # AI ML Training on the fly
            df_e['Hari_Ke'] = np.arange(len(df_e))
            X = df_e[['Hari_Ke']]
            y = df_e['Pemakaian Listrik (kWh)']
            
            model = LinearRegression()
            model.fit(X, y)
            
            # Memprediksi 7 hari ke depan
            future_days = np.arange(len(df_e), len(df_e) + 7).reshape(-1, 1)
            predictions = model.predict(future_days)
            
            last_date = df_e['Tanggal'].max()
            future_dates = [last_date + timedelta(days=int(i)) for i in range(1, 8)]
            
            df_pred = pd.DataFrame({'Tanggal': future_dates, 'Prediksi kWh': np.round(predictions, 2)})
            
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(df_pred, use_container_width=True)
            with col2:
                st.line_chart(df_pred.set_index('Tanggal')['Prediksi kWh'], color="#FF0000")
                st.warning("⚠️ Berdasarkan algoritma, jika tren naik, segera lakukan efisiensi AC!")
        else:
            st.error("Data energi belum cukup. Silakan input minimal 5 hari data di menu 'Input Data Manual'.")
            
    with tab_ai2:
        st.subheader("AI Prediksi Kemampuan Siswi Baru")
        st.markdown("Masukkan nilai tes awal (Pre-Test) siswi baru, AI akan memprediksi hasil kelulusan akhirnya berdasarkan pola belajar Srikandi sebelumnya.")
        
        sim_pre_test = st.number_input("Input Nilai Pre-Test (AI Simulation)", min_value=0, max_value=100, value=50)
        
        if st.button("Jalankan AI Analitik Siswi"):
            df_s = st.session_state['student_data']
            if len(df_s) > 2:
                # ML Training
                X_s = df_s[['Literasi Awal']]
                y_s = df_s['Literasi Akhir']
                model_s = LinearRegression()
                model_s.fit(X_s, y_s)
                
                pred_akhir = model_s.predict([[sim_pre_test]])[0]
                st.success(f"🎯 **Hasil Eksekusi AI:** Jika siswi ini mendapatkan pelatihan intensif, nilai post-test diprediksi akan mencapai **{pred_akhir:.1f}**.")
            else:
                st.error("Butuh lebih banyak data siswi untuk menjalankan AI.")
