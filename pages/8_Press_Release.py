import streamlit as st
from utils import tampilkan_header, generate_press_release
from datetime import datetime

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Siaran Pers Kinerja APBN",
    page_icon="📰",
    layout="wide"
)

# Custom CSS untuk perbaikan tampilan
st.markdown("""
<style>
    /* Gaya utama untuk siaran pers */
    .press-release {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.8;
        text-align: justify;
        color: #333;
    }

    .press-release h2 {
        color: #003366;
        border-bottom: 2px solid #003366;
        padding-bottom: 8px;
        margin-top: 1.5em;
    }

    .press-release h3 {
        color: #00509e;
        margin-top: 1.2em;
    }

    .press-release ul, .press-release ol {
        padding-left: 1.5em;
        margin-bottom: 1.5em;
    }

    .press-release li {
        margin-bottom: 0.8em;
    }

    .press-release p {
        margin-bottom: 1.2em;
    }

    /* Container styling */
    .press-container {
        background-color: #f8fafc;
        border-radius: 10px;
        padding: 2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
    }

    /* Tombol styling */
    .stButton>button {
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    /* Header styling */
    .press-header {
        text-align: center;
        margin-bottom: 1.5rem;
    }

    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 0.35em 0.65em;
        font-size: 0.75em;
        font-weight: 700;
        line-height: 1;
        text-align: center;
        white-space: nowrap;
        vertical-align: baseline;
        border-radius: 0.375rem;
    }

    .badge-primary {
        color: #fff;
        background-color: #0d6efd;
    }

    .badge-secondary {
        color: #fff;
        background-color: #6c757d;
    }
</style>
""", unsafe_allow_html=True)

# Header dengan logo
tampilkan_header()

# --- Judul Halaman ---
st.markdown("""
<div class="press-header">
    <h1 style="color: #003366; margin-bottom: 0.5rem;">📰 Siaran Pers Kinerja APBN</h1>
    <p style="color: #6c757d; font-size: 1.1rem;">
        Laporan Otomatis Kinerja Anggaran Pendapatan dan Belanja Negara
    </p>
</div>
""", unsafe_allow_html=True)

# --- Manajemen State ---
if 'press_release' not in st.session_state:
    st.session_state.press_release = generate_press_release()

# --- Tombol Aksi Utama ---
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    st.markdown("""
    <div style="font-size: 0.95rem; color: #4a5568;">
        Siaran pers ini dihasilkan otomatis berdasarkan data terbaru dari dashboard.
        Anda dapat menyesuaikan konten sebelum disebarluaskan.
    </div>
    """, unsafe_allow_html=True)

with col2:
    if st.button("🔄 Perbarui Data", help="Generate ulang siaran pers dari data terkini", use_container_width=True):
        st.cache_data.clear()
        if 'press_release' in st.session_state:
            del st.session_state.press_release
        st.rerun()

with col3:
    if st.button("📋 Salin Teks", help="Salin teks siaran pers ke clipboard", use_container_width=True):
        st.session_state.copied = True
        st.toast("Teks siaran pers telah disalin ke clipboard!")

# Garis pemisah
st.divider()

# --- Tampilan Utama Siaran Pers ---
st.markdown("### Pratinjau Siaran Pers")
with st.container():
    st.markdown("""
    <div class="press-container">
        <div class="press-release">
            <div style="text-align: center; margin-bottom: 2rem;">
                <h2 style="border-bottom: none;">SIARAN PERS KINERJA APBN</h2>
                <p style="font-weight: bold;">KEMENTERIAN KEUANGAN RI</p>
                <p>Kantor Pelayanan Perbendaharaan Negara Lhokseumawe</p>
                <p style="color: #6c757d;">{tanggal}</p>
            </div>
            {content}
        </div>
    </div>
    """.format(
        tanggal=datetime.now().strftime("%d %B %Y"),
        content=st.session_state.press_release
    ), unsafe_allow_html=True)

# Tombol aksi bawah
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    st.download_button(
        label="⬇️ Unduh HTML",
        data=st.session_state.press_release,
        file_name=f"siaran_pers_apbn_{datetime.now().strftime('%Y%m%d')}.html",
        mime="text/html",
        use_container_width=True
    )

with col2:
    st.download_button(
        label="⬇️ Unduh TXT",
        data=st.session_state.press_release,
        file_name=f"siaran_pers_apbn_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain",
        use_container_width=True
    )

st.divider()

# --- Editor Siaran Pers ---
with st.expander("✏️ Editor Siaran Pers", expanded=False):
    edited_release = st.text_area(
        "Edit teks siaran pers di bawah ini:",
        value=st.session_state.press_release,
        height=400,
        key="editor_area",
        label_visibility="collapsed"
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("💾 Simpan Perubahan", use_container_width=True):
            st.session_state.press_release = edited_release
            st.success("Perubahan disimpan!")
            st.rerun()

    with col2:
        if st.button("↩️ Kembalikan ke Versi Asli", use_container_width=True):
            st.session_state.press_release = generate_press_release()
            st.success("Teks telah dikembalikan ke versi asli!")
            st.rerun()

# Tombol kembali ke home
st.markdown('<div class="back-button">', unsafe_allow_html=True)
if st.button("⬅ Kembali ke Menu Utama", use_container_width=True, type="primary"):
    st.switch_page("Home.py")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# Catatan kaki
st.caption("""
<div style="text-align: center; margin-top: 2rem; color: #6c757d; font-size: 0.85rem;">
    <p>Siaran pers ini dihasilkan otomatis oleh Sistem Pelaporan Kinerja APBN KPPN Lhokseumawe</p>
    <p>Update terakhir: {tanggal}</p>
</div>
""".format(tanggal=datetime.now().strftime("%d/%m/%Y %H:%M")), unsafe_allow_html=True)
