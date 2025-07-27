import streamlit as st
from utils import (
    tampilkan_header,
    display_pendapatan_infographic,
    display_belanja_kl_chart,
    display_tkd_chart,
    display_belanja_negara_chart,
    display_umi_kur_chart,
    display_digitalisasi_chart,
    display_transfer_daerah_wilayah_chart,
    generate_press_release,
    display_kopdes_mbg_chart
)

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    layout="wide",
    page_title="Dashboard APBN | KPPN Lhokseumawe",
    page_icon="🏠"
)

# --- SIDEBAR ---
st.sidebar.info("Anda berada di laman **Ringkasan Utama**.", icon="🏠")
st.sidebar.markdown("- KPPN Lhokseumawe")

# --- PANGGIL FUNGSI HEADER (LOGO) ---
tampilkan_header()

# --- JUDUL UTAMA DENGAN ANIMASI ---
st.markdown("""
<style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .title-box {
        background: linear-gradient(135deg, #005FAC, #006ac1); /* Warna Biru DJPb */
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeIn 1s ease-out;
    }
    .title-box h1 {
        margin-bottom: 0.5rem;
        font-size: 2.2rem;
    }
    .title-box h2 {
        margin-top: 0;
        font-size: 1.5rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="title-box">
    <h1>KINERJA APBN 2025</h1>
    <h2>LINGKUP KPPN LHOKSEUMAWE</h2>
</div>
""", unsafe_allow_html=True)

# --- GAYA KARTU YANG LEBIH MODERN DAN INTERAKTIF ---
st.markdown("""
<style>
    /* Style untuk container kartu */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="stVerticalBlock"] > div:first-child[data-testid="stContainer"][style*="border"] {
        min-height: 450px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        border-radius: 15px !important;
        padding: 15px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 2px solid #e0e0e0 !important;
        background-color: white;
        margin-bottom: 2rem; /* Menambahkan jarak antar kartu */
    }

    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="stVerticalBlock"] > div:first-child[data-testid="stContainer"][style*="border"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.15);
        border-color: #005FAC !important; /* Warna Biru DJPb saat hover */
    }

    /* Menerapkan gaya visual baru ke komponen st.page_link */
    .page-link-box {
        display: block;
        background: linear-gradient(135deg, #005FAC, #006ac1); /* Warna Biru DJPb */
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        text-decoration: none !important;
        color: white;
        font-weight: bold;
        font-size: 1.1rem;
        border: none;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }

    .page-link-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: 0.5s;
    }

    .page-link-box:hover::before {
        left: 100%;
    }

    .page-link-box:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
    }

    /* Mengatur teks di dalam st.page_link */
    a[data-testid="stPageLink-Label"] p {
        color: white !important;
        font-weight: bold;
        font-size: 1.1rem;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Animasi chart */
    @keyframes chartFadeIn {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }
    .chart-container {
        animation: chartFadeIn 0.8s ease-out;
        flex-grow: 1; /* Memastikan chart mengisi ruang yang tersedia */
    }
</style>
""", unsafe_allow_html=True)

# --- TATA LETAK UTAMA MENJADI 2 KOLOM ---
col_kiri, col_kanan = st.columns(2, gap="large")

# --- KOLOM KIRI ---
with col_kiri.container(height=500):
    # 1. KINERJA PENDAPATAN APBN
    with st.container(border=True):
        st.markdown('<div class="page-link-box">KINERJA PENDAPATAN APBN</div>', unsafe_allow_html=True)
        st.page_link(
            "pages/2_Kinerja_Pendapatan_APBN.py",
            label="Klik untuk melihat detail",
            help="Klik untuk melihat detail Kinerja Pendapatan APBN"
        )
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        display_pendapatan_infographic()
        st.markdown('</div>', unsafe_allow_html=True)

with col_kiri.container(height=500):
    # 2. CAPAIAN PENYALURAN TKD
    with st.container(border=True):
        st.markdown('<div class="page-link-box">CAPAIAN PENYALURAN TKD</div>', unsafe_allow_html=True)
        st.page_link(
            "pages/4_Capaian_Penyaluran_TKD.py",
            label="Klik untuk melihat detail",
            help="Klik untuk melihat detail Capaian Penyaluran TKD"
        )
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        display_tkd_chart()
        st.markdown('</div>', unsafe_allow_html=True)

with col_kiri.container(height=500):
    # 3. PENYALURAN PEMBIAYAAN UMi & KUR
    with st.container(border=True):
        st.markdown('<div class="page-link-box">PENYALURAN PEMBIAYAAN UMi & KUR</div>', unsafe_allow_html=True)
        st.page_link(
            "pages/6_Penyaluran_Pembiayaan_UMi_KUR.py",
            label="Klik untuk melihat detail",
            help="Klik untuk melihat detail Penyaluran Pembiayaan UMi & KUR"
        )
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        display_umi_kur_chart()
        st.markdown('</div>', unsafe_allow_html=True)


# --- KOLOM KANAN ---
with col_kanan.container(height=500):
    # 5. REALISASI BELANJA K/L
    with st.container(border=True):
        st.markdown('<div class="page-link-box">REALISASI BELANJA K/L</div>', unsafe_allow_html=True)
        st.page_link(
            "pages/3_Realisasi_Belanja_KL.py",
            label="Klik untuk melihat detail",
            help="Klik untuk melihat detail Realisasi Belanja K/L"
        )
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        display_belanja_kl_chart()
        st.markdown('</div>', unsafe_allow_html=True)

with col_kanan.container(height=500):
    # 6. REALISASI BELANJA NEGARA
    with st.container(border=True):
        st.markdown('<div class="page-link-box">REALISASI BELANJA NEGARA</div>', unsafe_allow_html=True)
        st.page_link(
            "pages/5_Realisasi_Belanja_Negara.py",
            label="Klik untuk melihat detail",
            help="Klik untuk melihat detail Realisasi Belanja Negara"
        )
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        display_belanja_negara_chart()
        st.markdown('</div>', unsafe_allow_html=True)

with col_kanan.container(height=500):
    # 7. MONITORING KOPDES DAN MBG
    with st.container(border=True):
        st.markdown('<div class="page-link-box">MONITORING KOPDES DAN MBG</div>', unsafe_allow_html=True)
        st.page_link(
            "pages/7_Monitoring_KOPDES_dan_MBG.py",
            label="Klik untuk melihat detail",
            help="Klik untuk melihat detail monitoring KOPDES dan MBG"
        )
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        display_kopdes_mbg_chart()
        st.markdown('</div>', unsafe_allow_html=True)

# --- BARIS PENUH UNTUK DIGITALISASI (TINGGI 300) ---
with st.container(height=300):
    with st.container(border=True):
        st.markdown('<div class="page-link-box">CAPAIAN DIGITALISASI PEMBAYARAN</div>', unsafe_allow_html=True)
        st.page_link(
            "pages/8_Capaian_Digitalisasi_Pembayaran.py",
            label="Klik untuk melihat detail",
            help="Klik untuk melihat detail Capaian Digitalisasi Pembayaran"
        )
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        display_digitalisasi_chart()
        st.markdown('</div>', unsafe_allow_html=True)


# --- BARIS PENUH DENGAN 2 KOLOM UNTUK PRESS RELEASE DAN ANTI KORUPSI ---
col_pr, col_ak = st.columns(2, gap="large")

with col_pr.container(height=200):
    # PRESS RELEASE
    with st.container(border=True):
        st.markdown('<div class="page-link-box">PRESS RELEASE</div>', unsafe_allow_html=True)
        st.page_link(
            "pages/9_Press_Release.py",
            label="Klik untuk melihat detail",
            help="Klik untuk melihat detail Press Release"
        )
        # Kosongkan konten utama
        st.markdown('<div class="chart-container" style="display: flex; justify-content: center; align-items: center; height: 150px;">', unsafe_allow_html=True)
        st.markdown("Klik judul untuk melihat press release lengkap")
        st.markdown('</div>', unsafe_allow_html=True)

with col_ak.container(height=200):
    # ANTI KORUPSI
    with st.container(border=True):
        st.markdown('<div class="page-link-box">ANTI KORUPSI</div>', unsafe_allow_html=True)
        st.page_link(
            "pages/10_Anti_Korupsi.py",
            label="Klik untuk melihat detail",
            help="Klik untuk melihat detail Komitmen Anti Korupsi"
        )
        # Kosongkan konten utama
        st.markdown('<div class="chart-container" style="display: flex; justify-content: center; align-items: center; height: 150px;">', unsafe_allow_html=True)
        st.markdown("Klik judul untuk melihat layanan anti korupsi")
        st.markdown('</div>', unsafe_allow_html=True)


# --- PEMISAH AKHIR DENGAN EFEK GRADIENT ---
st.markdown("""
<style>
    .gradient-divider {
        height: 3px;
        background: linear-gradient(90deg, #005FAC, #D4AF37, #005FAC); /* Biru DJPb dan Emas Kemenkeu */
        margin: 2rem 0;
        border-radius: 3px;
        opacity: 0.7;
    }
</style>
<div class="gradient-divider"></div>
""", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem; margin-top: 1rem;">
    © 2025 KPPN Lhokseumawe | Dashboard APBN
</div>
""", unsafe_allow_html=True)
