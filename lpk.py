import streamlit as st

# Fungsi untuk mengkonversi satuan konsentrasi ke mg/Nm³
def konversi_konsentrasi(konsentrasi, satuan):
    konversi = {
        'µg/m³': konsentrasi / 1000,  # µg/m³ ke mg/m³
        'mg/m³': konsentrasi,
        'ppm': konsentrasi * 1.96  # Asumsi untuk konversi kasar
    }
    return konversi.get(satuan, konsentrasi)

# Fungsi untuk mengkonversi satuan debit ke m³/jam
def konversi_debit(debit, satuan):
    konversi = {
        'm³/jam': debit,
        'L/detik': debit * 3.6,
        'L/menit': debit * 0.06,
        'm³/hari': debit / 24,
        'm³/menit': debit * 60,
        'm³/detik': debit * 3600
    }
    return konversi.get(satuan, debit)

# Fungsi untuk mengkonversi satuan beban emisi ke berat/waktu
def konversi_beban_emisi(beban_emisi, satuan):
    konversi = {
        'mg/jam': beban_emisi,
        'mg/detik': beban_emisi / 3600,
        'g/jam': beban_emisi / 1000,
        'kg/jam': beban_emisi / 1_000_000,
        'ton/tahun': beban_emisi / 1_000_000_000 * 24 * 365  # Asumsi beban emisi dalam mg/jam untuk 1 tahun
    }
    return konversi.get(satuan, beban_emisi)

# Fungsi untuk menghitung beban emisi
def hitung_beban_emisi(konsentrasi, debit):
    return konsentrasi * debit

# Fungsi untuk membandingkan konsentrasi dengan baku mutu emisi udara
def cek_baku_mutu(konsentrasi, parameter):
    baku_mutu = {
        'PM10': 90,    # mg/Nm³
        'SO2': 550,    # mg/Nm³
        'NO2': 300,    # mg/Nm³
        'CO': 150      # mg/Nm³
    }
    return konsentrasi <= baku_mutu.get(parameter, float('inf'))

# Streamlit UI
st.set_page_config(page_title="Perhitungan Beban Emisi Udara", page_icon=":factory:", layout="centered")

st.markdown("""
<style>
    body {
        background-color: #f0f2f6;
    }
    .main {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .footer {
        text-align: center;
        padding: 20px;
        margin-top: 20px;
        font-size: 14px;
        color: #888;
    }
    .sidebar .sidebar-content {
        background-color: #4CAF50;
        color: white;
    }
    .sidebar .sidebar-content a {
        color: white;
    }
    .sidebar .sidebar-content a:hover {
        color: #e6e6e6;
    }
</style>
""", unsafe_allow_html=True)

st.title('Perhitungan Beban Emisi Udara :factory:')

# Halaman awal
menu = ["Perkenalan", "Perhitungan Beban Emisi"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Perkenalan":
    st.header("Perkenalan")
    st.write("""
    Selamat datang di aplikasi Perhitungan Beban Emisi Udara. Aplikasi ini dirancang untuk membantu Anda menghitung beban emisi udara berdasarkan konsentrasi dan debit aliran.

    ### Apa itu Beban Emisi Udara?
    Beban emisi udara adalah jumlah total polutan yang dilepaskan ke atmosfer dalam jangka waktu tertentu. Perhitungan ini penting untuk memastikan bahwa emisi yang dihasilkan tidak melebihi batas yang ditetapkan oleh baku mutu.

    ### Baku Mutu Emisi Udara
    Berikut adalah baku mutu emisi udara yang digunakan dalam aplikasi ini sesuai dengan *PermenLHK No. 15 Tahun 2019*:
    - PM10: 90 mg/Nm³
    - SO2: 550 mg/Nm³
    - NO2: 300 mg/Nm³
    - CO: 150 mg/Nm³

    ### Cara Menggunakan Aplikasi
    1. Pilih menu "Perhitungan Beban Emisi" dari sidebar.
    2. Masukkan data konsentrasi polutan dan debit aliran.
    3. Pilih satuan untuk masing-masing parameter.
    4. Klik "Hitung Beban Emisi" untuk mendapatkan hasil.
    5. Hasil perhitungan akan menampilkan apakah konsentrasi memenuhi baku mutu serta nilai beban emisi.
    
    Beban emisi yang dihitung adalah hasil dari cerobong industri.
    """)

elif choice == "Perhitungan Beban Emisi":
    st.sidebar.header('Masukkan Data')
    st.sidebar.write('Silakan masukkan data konsentrasi dan debit.')

    # Input form untuk konsentrasi dan debit
    with st.sidebar.form(key='input_form'):
        konsentrasi = st.number_input('Konsentrasi', min_value=0.0, step=0.1, help='Masukkan konsentrasi polutan dalam udara')
        satuan_konsentrasi = st.selectbox('Satuan Konsentrasi', ['µg/m³', 'mg/m³', 'ppm'], help='Pilih satuan konsentrasi')
        debit = st.number_input('Debit', min_value=0.0, step=0.1, 
        help='Masukkan debit aliran udara') satuan_debit
