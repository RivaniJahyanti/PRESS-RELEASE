import streamlit as st
from utils import tampilkan_header

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Layanan Tanpa Biaya",
    page_icon="🚫",
    layout="wide"
)

tampilkan_header()

# --- CSS Kustom untuk Styling ---
st.markdown("""
<style>
/* Kontainer utama */
.main-container {
    text-align: center;
    font-family: 'Poppins', sans-serif;
    padding: 1rem 1rem;
    max-width: 300px;
    margin: 0 auto;
}

/* BAGIAN INI MEMBUAT JUDUL JADI SANGAT BESAR */
.header-text {
    font-size: 4.5rem; 
    font-weight: 800;
    color: #0056b3;
    margin-bottom: 0.5rem;
    line-height: 1.2;
    text-align: center;
}

.subheader-text {
    font-size: 5.0rem;
    font-weight: 800;
    color: #e63946;
    margin-top: 0;
    margin-bottom: 1.5rem;
    text-align: center;
}

.emoji-container {
    font-size: 7.0rem;
    margin: 1rem 0;
    line-height: 1;
    text-align: center;
}

.cta-text {
    font-size: 4.0rem;
    font-weight: 800;
    color: #e63946;
    margin: 1.5rem 0;
    line-height: 1.2;
    padding: 1rem;
    background: rgba(230, 57, 70, 0.05);
    border-radius: 10px;
    text-align: center;
}

.section-title {
    font-size: 3.0rem;
    font-weight: 800;
    color: #0056b3;
    margin: 2rem 0 1rem;
    line-height: 1.2;
    text-align: center;
}

/* BAGIAN INI MEMBUAT INFO KONTAK JADI KECIL */
.contact-info {
    font-size: 1.3rem;
    font-weight: 600;
    color: #333;
    line-height: 1.8;
    margin: 0 auto;
    max-width: 700px;
    background: rgba(0, 86, 179, 0.05);
    padding: 1.5rem;
    border-radius: 10px;
    border-left: 4px solid #0056b3;
    text-align: center;
}

.contact-info b {
    color: #0056b3;
}

.hashtags {
    font-size: 1.2rem;
    font-weight: 600;
    color: #0056b3;
    margin: 2rem 0;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 15px;
}

.hashtags span {
    background: rgba(0, 86, 179, 0.1);
    padding: 8px 16px;
    border-radius: 50px;
}

.footer-text {
    text-align: center;
    color: #666;
    font-size: 1.0rem;
    margin-top: 1.5rem;
}

/* Responsive design */
@media (max-width: 768px) {
    .header-text { font-size: 3.5rem; }
    .subheader-text { font-size: 3.8rem; }
    .cta-text { font-size: 3.0rem; }
    .section-title { font-size: 2.5rem; }
    .contact-info { font-size: 1.1rem; padding: 1rem; }
}
</style>
""", unsafe_allow_html=True)

# --- Layout Aplikasi ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# --- HEADER (Menggunakan class .header-text dan .subheader-text) ---
st.markdown('<h1 class="header-text">SELURUH LAYANAN KAMI</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="subheader-text">TANPA BIAYA (GRATIS)</h2>', unsafe_allow_html=True)

# --- EMOJI BESAR ---
st.markdown('<div class="emoji-container">🚫💰</div>', unsafe_allow_html=True)

# --- AJAKAN UTAMA ---
st.markdown('<h2 class="cta-text">TOLAK DAN LAPOR GRATIFIKASI !!!</h2>', unsafe_allow_html=True)

# --- SALURAN PENGADUAN ---
st.markdown('<h3 class="section-title">SALURAN PENGADUAN</h3>', unsafe_allow_html=True)

# --- INFO KONTAK (Menggunakan class .contact-info) ---
st.markdown("""
<div class="contact-info">
    <span>📱</span> WHATSAPP <b>0811 6840 089</b><br>
    <span>📞</span> TELEPON <b>(0645) 42258</b><br>
    <span>✉️</span> E-MAIL <b>ukip.kppn089@gmail.com</b><br>
    <span>🌐</span> SIPANDU <b>pengaduandjpb.kemenkeu.go.id</b><br>
    <span>🔒</span> WHISTLEBLOWING SYSTEM <b>www.wise.kemenkeu.go.id</b>
</div>
""", unsafe_allow_html=True)

# --- HASHTAGS ---
st.markdown("""
<div class="hashtags">
    <span>#LayananKPPNGratis</span>
    <span>#TolakGratifikasi</span>
    <span>#WISEKemenkeu</span>
    <span>#SIPANDU</span>
</div>
""", unsafe_allow_html=True)

# --- DIVIDER ---
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div class="footer-text">
    Kantor Pelayanan Perbendaharaan Negara Lhokseumawe<br>
    <b>djpb.kemenkeu.go.id</b>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Tombol kembali ke home
st.markdown('<div class="back-button">', unsafe_allow_html=True)
if st.button("⬅ Kembali ke Menu Utama", use_container_width=True, type="primary"):
    st.switch_page("Home.py")
st.markdown('</div>', unsafe_allow_html=True)
