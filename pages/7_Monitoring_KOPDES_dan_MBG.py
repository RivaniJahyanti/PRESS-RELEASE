import streamlit as st
from utils import get_data, display_kopdes_mbg_chart, tampilkan_header
from datetime import datetime

# Konfigurasi Halaman
st.set_page_config(
    layout="wide",
    page_title="Monitoring KOPDES & MBG",
    page_icon="📊"
)

tampilkan_header()

# Custom CSS untuk perbaikan tampilan
st.markdown("""
<style>
    /* Gaya untuk header utama */
    .main-title {
        text-align: center;
        color: #2b5876;
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(to right, #2b5876, #4e4376);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Gaya untuk subheader */
    .sub-header {
        text-align: center;
        color: #4a6fa5;
        font-size: 1.8rem;
        margin-top: 0 !important;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }

    /* Gaya untuk periode */
    .period {
        text-align: center;
        color: #6b7280;
        font-size: 2rem;
        margin-bottom: 1.5rem;
    }

    /* Container untuk data */
    .data-container {
        display: flex;
        gap: 30px;
        margin-bottom: 30px;
        flex-wrap: wrap;
    }

    .data-section {
        flex: 1;
        min-width: 300px;
        background: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    .data-title {
        font-size: 1.3em;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid #f1f1f1;
        text-align: center;
    }

    .data-row {
        display: flex;
        justify-content: space-between;
        padding: 12px 0;
        border-bottom: 1px solid #f5f5f5;
    }

    .data-row:last-child {
        border-bottom: none;
    }

    .pemda-name {
        font-weight: 600;
        color: #34495e;
        width: 45%;
    }

    .data-value {
        font-weight: 500;
        color: #2c3e50;
        text-align: right;
        width: 25%;
    }

    .percentage {
        font-weight: 700;
        width: 30%;
        text-align: right;
    }

    .percentage-100 {
        color: #27ae60;
    }

    .percentage-low {
        color: #e74c3c;
    }

    .percentage-mid {
        color: #f39c12;
    }

    .percentage-high {
        color: #27ae60;
    }

    .total-row {
        background-color: #f8f9fa;
        border-radius: 6px;
        padding: 12px;
        margin-top: 10px;
        font-weight: 700;
    }

    /* Progress bar styling */
    .progress-container {
        width: 100%;
        background-color: #e0e0e0;
        border-radius: 10px;
        margin: 10px 0;
    }

    .progress-bar {
        height: 10px;
        border-radius: 10px;
        background: linear-gradient(90deg, #4b6cb7, #182848);
    }

    /* Card styling for summary */
    .summary-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        text-align: center;
    }

    .summary-value {
        font-size: 2rem;
        font-weight: 700;
        color: #2b5876;
        margin: 10px 0;
    }

    .summary-label {
        font-size: 1rem;
        color: #6b7280;
    }

    /* Divider */
    .divider {
        margin: 1.5rem 0;
        border: 0;
        height: 1px;
        background-image: linear-gradient(to right, rgba(0,0,0,0), rgba(75, 85, 99, 0.5), rgba(0,0,0,0));
    }
</style>
""", unsafe_allow_html=True)

# Pesan di Sidebar
with st.sidebar:
    st.info("Anda sedang melihat laman **Monitoring KOPDES & MBG**.", icon="📊")
    st.markdown("- KPPN Lhokseumawe")

# Header
st.markdown("<h1 class='main-title'>MONITORING KOPDES & MBG</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='sub-header'>Lingkup KPPN Lhokseumawe</h3>", unsafe_allow_html=True)
st.markdown(f"<p class='period'>Periode: Januari - Juni {datetime.now().year}</p>", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# Display the chart
display_kopdes_mbg_chart()

# Tombol kembali ke home
st.markdown('<div style="text-align: center; margin-top: 30px;">', unsafe_allow_html=True)
if st.button("⬅ Kembali ke Menu Utama", use_container_width=True, type="primary"):
    st.switch_page("Home.py")
st.markdown('</div>', unsafe_allow_html=True)


# Catatan kaki
st.caption("""
**Keterangan:**
- **Sumber:**
""")
