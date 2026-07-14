import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="JAWARA DATA Sempurna", page_icon="🏆", layout="wide")

# --- 2. INISIALISASI DATABASE SEMENTARA (SESSION STATE) ---
if 'energy_data' not in st.session_state:
    dates = pd.date_range(start="2026-06-01", periods=30, freq="D")
    base_kwh = np.linspace(200, 150, 30) + np.random.normal(0, 10, 30)
    base_sampah = np.random.randint(2, 12, 30) # Data Adiwiyata: Kg Sampah terdaur ulang
    st.session_state['energy_data'] = pd.DataFrame({
        'Tanggal': dates,
        'Pemakaian Listrik (kWh)': np.round(base_kwh, 2),
        'Jejak Karbon (Kg CO2)': np.round(base_kwh * 0.85, 2),
        'Sampah Daur Ulang (Kg)': base_sampah
    })

if 'student_data' not in st.session_state:
    st.session_state['student_data'] = pd.DataFrame({
        'ID Siswi': ['SRI-001', 'SRI-002', 'SRI-003', 'SRI-004'],
        'Nama': ['Siti (Contoh)', 'Ayu (Contoh)', 'Rina (Contoh)', 'Desi (Contoh)'],
        'Status Ekonomi': ['Pra-Sejahtera', 'Menengah', 'Pra-Sejahtera', 'Menengah'],
        'Minat Utama': ['Web Development', 'Digital Marketing', 'Data Science', 'Content Creator'],
        'Literasi Awal': [45, 50, 40, 55],
        'Literasi Akhir': [88, 92, 85, 90],
        'Kehadiran (%)': [95, 100, 90, 98],
        'Peluang Karir': ['Front-End Developer', 'Social Media Specialist', 'Data Analyst', 'Video Editor / Kreator']
    })

# --- 3. SIDEBAR & NAVIGASI ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2103/2103254.png", width=80)
st.sidebar.title("Navigasi JAWARA DATA")
menu = st.sidebar.radio("Pilih Modul Sistem:", [
    "🏠 Beranda Eksekutif", 
    "✍️ Input Data Manual", 
    "🌍 Adiwiyata & Go Green", 
    "👩‍💻 GESI & Minat Karir", 
    "🤖 AI Automations"
])
st.sidebar.markdown("---")
st.sidebar.caption("© 2026 - Mendukung Visi Banten Cerdas & Lulusan Siap Kerja")

# --- 4. LOGIKA MODUL HALAMAN ---

if menu == "🏠 Beranda Eksekutif":
    st.title("🏆 JAWARA DATA (Sistem Terpadu)")
    st.markdown("Integrasi Pemantauan Adiwiyata, Inklusi Sosial, dan Penyaluran Karir Berbasis Kecerdasan Buatan.")
    
    col1, col2, col3, col4 = st.columns(4)
    df_e = st.session_state['energy_data']
    df_s = st.session_state['student_data']
    
    col1.metric("Total Pemakaian Listrik", f"{df_e['Pemakaian Listrik (kWh)'].sum():,.0f} kWh")
    col2.metric("Total Sampah Didaur Ulang", f"{df_e['Sampah Daur Ulang (Kg)'].sum()} Kg", "Poin Adiwiyata")
    col3.metric("Total Siswi Terbina", f"{len(df_s)} Srikandi")
    col4.metric("Siap Masuk Industri", f"{len(df_s[df_s['Literasi Akhir'] >= 85])} Siswi", "Siap Magang")
    
    st.info("👈 Silakan navigasi ke menu 'Input Data Manual' untuk memasukkan catatan harian, atau 'AI Automations' untuk prediksi.")

elif menu == "✍️ Input Data Manual":
    st.title("✍️ Modul Input Data Manual")
    
    tab1, tab2 = st.tabs(["🌱 Input Log Adiwiyata", "🎓 Registrasi & Minat Siswi"])
    
    with tab1:
        with st.form("form_energi", clear_on_submit=True):
            st.subheader("Catat Indikator Lingkungan Hari Ini")
            tgl_input = st.date_input("Tanggal Pencatatan")
            kwh_input = st.number_input("Pemakaian Listrik (kWh)", min_value=0.0, value=150.0, step=1.5)
            sampah_input = st.number_input("Volume Sampah Organik/Non-Organik Didaur Ulang (Kg)", min_value=0.0, value=5.0, step=0.5)
            submit_energi = st.form_submit_button("Simpan Data Adiwiyata")
            
            if submit_energi:
                co2_calc = round(kwh_input * 0.85, 2)
                new_e_data = pd.DataFrame({
                    'Tanggal': [pd.to_datetime(tgl_input)],
                    'Pemakaian Listrik (kWh)': [kwh_input],
                    'Jejak Karbon (Kg CO2)': [co2_calc],
                    'Sampah Daur Ulang (Kg)': [sampah_input]
                })
                st.session_state['energy_data'] = pd.concat([st.session_state['energy_data'], new_e_data], ignore_index=True)
                st.success(f"Data tanggal {tgl_input} berhasil disimpan!")

    with tab2:
        with st.form("form_siswi", clear_on_submit=True):
            st.subheader("Pemetaan Profil & Minat Bakat Baru")
            nama_input = st.text_input("Nama Siswi")
            ekonomi_input = st.selectbox("Status Ekonomi", ["Pra-Sejahtera", "Menengah", "Mampu"])
            minat_input = st.selectbox("Minat Bakat Utama", ["Web Development", "Digital Marketing", "Data Science", "Content Creator", "Networking"])
            lit_awal = st.slider("Nilai Literasi Awal (Pre-Test)", 0, 100, 50)
            lit_akhir = st.slider("Nilai Literasi Akhir (Post-Test)", 0, 100, 85)
            hadir = st.slider("Kehadiran Pelatihan (%)", 0, 100, 95)
            
            # Mapping Karir Sederhana Berdasarkan Minat
            karir_map = {
                "Web Development": "Front-End Developer",
                "Digital Marketing": "Social Media Specialist",
                "Data Science": "Data Analyst",
                "Content Creator": "Video Editor / Kreator",
                "Networking": "Teknisi Jaringan"
            }
            
            submit_siswi = st.form_submit_button("Simpan Pemetaan Karir")
            
            if submit_siswi:
                new_id = f"SRI-{len(st.session_state['student_data']) + 1:03d}"
                new_s_data = pd.DataFrame({
                    'ID Siswi': [new_id], 'Nama': [nama_input], 'Status Ekonomi': [ekonomi_input],
                    'Minat Utama': [minat_input], 'Literasi Awal': [lit_awal], 
                    'Literasi Akhir': [lit_akhir], 'Kehadiran (%)': [hadir],
                    'Peluang Karir': [karir_map[minat_input]]
                })
                st.session_state['student_data'] = pd.concat([st.session_state['student_data'], new_s_data], ignore_index=True)
                st.success(f"Profil {nama_input} tersimpan. Rekomendasi Karir AI: {karir_map[minat_input]}")

elif menu == "🌍 Adiwiyata & Go Green":
    st.title("🌍 Dasbor Adiwiyata & Penurunan Karbon")
    df_e = st.session_state['energy_data'].sort_values('Tanggal')
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Tren Pemakaian Listrik")
        st.line_chart(df_e.set_index('Tanggal')['Pemakaian Listrik (kWh)'], color="#FFC300")
    with col2:
        st.subheader("Grafik Sampah Didaur Ulang (Kg)")
        st.bar_chart(df_e.set_index('Tanggal')['Sampah Daur Ulang (Kg)'], color="#17B169")
        
    st.dataframe(df_e, use_container_width=True)

elif menu == "👩‍💻 GESI & Minat Karir":
    st.title("👩‍💻 Pemetaan Karir Masa Depan Srikandi Data")
    df_s = st.session_state['student_data']
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Distribusi Minat Siswi")
        minat_count = df_s['Minat Utama'].value_counts()
        st.bar_chart(minat_count)
    with col2:
        st.subheader("Proyeksi Penyaluran Industri")
        karir_count = df_s['Peluang Karir'].value_counts()
        st.bar_chart(karir_count, color="#900C3F")
        
    st.subheader("Database Talenta Siap Kerja")
    st.dataframe(df_s[['ID Siswi', 'Nama', 'Minat Utama', 'Peluang Karir', 'Literasi Akhir']], use_container_width=True)

elif menu == "🤖 AI Automations":
    st.title("🤖 Eksekusi AI Automations")
    
    tab_ai1, tab_ai2 = st.tabs(["♻️ Prediksi Poin Adiwiyata (Regresi)", "🎯 AI Klasifikasi Peluang Karir"])
    
    with tab_ai1:
        st.subheader("AI Prediksi Pengurangan Karbon & Sampah (7 Hari Kedepan)")
        df_e = st.session_state['energy_data'].copy()
        
        if len(df_e) > 5:
            df_e['Hari_Ke'] = np.arange(len(df_e))
            X = df_e[['Hari_Ke']]
            y_listrik = df_e['Pemakaian Listrik (kWh)']
            y_sampah = df_e['Sampah Daur Ulang (Kg)']
            
            model_l = LinearRegression().fit(X, y_listrik)
            model_s = LinearRegression().fit(X, y_sampah)
            
            future_days = np.arange(len(df_e), len(df_e) + 7).reshape(-1, 1)
            pred_listrik = model_l.predict(future_days)
            pred_sampah = model_s.predict(future_days)
            
            future_dates = [df_e['Tanggal'].max() + timedelta(days=int(i)) for i in range(1, 8)]
            df_pred = pd.DataFrame({
                'Tanggal': future_dates, 
                'Prediksi Listrik (kWh)': np.round(pred_listrik, 2),
                'Prediksi Sampah Daur Ulang (Kg)': np.round(pred_sampah, 1)
            })
            
            st.dataframe(df_pred, use_container_width=True)
            st.info("Kecerdasan Buatan membaca tren bahwa program Adiwiyata sekolah berhasil meningkatkan volume daur ulang sampah setiap minggunya.")
        else:
            st.error("Data kurang. Input minimal 5 data harian di menu Manual Input.")
            
    with tab_ai2:
        st.subheader("AI Klasifikasi Penempatan Industri")
        st.markdown("Algoritma *Decision Tree Classifier* akan mencocokkan profil nilai dan minat siswi ke posisi pekerjaan di agensi digital/industri lokal.")
        
        df_s = st.session_state['student_data'].copy()
        
        if len(df_s) >= 4:
            # Encoding kategori teks menjadi angka untuk Machine Learning
            le_minat = LabelEncoder()
            df_s['Minat_Code'] = le_minat.fit_transform(df_s['Minat Utama'])
            
            X_clf = df_s[['Minat_Code', 'Literasi Akhir', 'Kehadiran (%)']]
            y_clf = df_s['Peluang Karir']
            
            # Melatih Model Klasifikasi
            clf_model = DecisionTreeClassifier(random_state=42)
            clf_model.fit(X_clf, y_clf)
            
            st.markdown("### Simulasi Talenta Baru")
            col_a, col_b, col_c = st.columns(3)
            sim_minat = col_a.selectbox("Minat Calon Siswi", le_minat.classes_)
            sim_nilai = col_b.slider("Estimasi Nilai Kelulusan", 50, 100, 85)
            sim_hadir = col_c.slider("Estimasi Kehadiran", 50, 100, 95)
            
            if st.button("Eksekusi Klasifikasi Karir"):
                minat_encoded = le_minat.transform([sim_minat])[0]
                prediksi_karir = clf_model.predict([[minat_encoded, sim_nilai, sim_hadir]])[0]
                
                st.success(f"🎯 **Hasil Keputusan Mesin (AI):** Berdasarkan pola data talenta sebelumnya, siswi ini sangat direkomendasikan untuk disalurkan pada karir: **{prediksi_karir}**.")
        else:
            st.error("Sistem membutuhkan minimal 4 data siswi untuk melatih algoritma klasifikasi.")
