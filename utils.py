import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re
from urllib.parse import quote
from urllib.error import URLError
from datetime import datetime
import streamlit as st
import base64
from pathlib import Path

# --- FUNGSI-FUNGSI HELPER ---

def parse_value(value):
    """
    PERBAIKAN: Menggunakan versi yang lebih andal untuk membaca berbagai format angka.
    """
    if isinstance(value, (int, float)):
        return float(value)
    try:
        s = str(value).strip()
        if not s: return 0.0
        if '%' in s:
            s = s.replace(',', '.'); s = re.sub(r'[^\d.-]', '', s)
            return float(s) if s else 0.0
        # Menghapus titik ribuan, lalu mengganti koma desimal
        s = s.replace('.', '').replace(',', '.')
        return float(s) if s else 0.0
    except (ValueError, TypeError):
        return 0.0

def format_otomatis(n, prefix="Rp"):
    """
    PERBAIKAN: Definisi fungsi diperbarui untuk menerima argumen 'prefix'.
    """
    if not isinstance(n, (int, float)):
        return f"{prefix} 0".strip()
    abs_n = abs(n)
    if abs_n >= 1_000_000_000_000:
        val, satuan = n / 1_000_000_000_000, "T"
    elif abs_n >= 1_000_000_000:
        val, satuan = n / 1_000_000_000, "M"
    elif abs_n >= 1_000_000:
        val, satuan = n / 1_000_000, "Jt"
    else:
        # Menambahkan spasi hanya jika prefix ada
        return f"{prefix} {n:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".").strip()

    # Menambahkan spasi hanya jika prefix ada
    formatted_val = f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{prefix} {formatted_val} {satuan}".strip()


# --- FUNGSI MEMUAT DATA ---
@st.cache_data(ttl=1200)
def get_data(sheet_name):
    SHEET_ID = "1MHvPog5TFyIx8lnUVV3mYJP0BZKCTHjkGe1zJ7Js8Ek"
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={quote(sheet_name)}'
    try:
        df = pd.read_csv(url, header=0); df.columns = df.columns.str.strip()
        return df.dropna(how='all')
    except Exception as e:
        st.error(f"Gagal memuat sheet '{sheet_name}'. Pastikan nama sheet benar dan file dapat diakses publik.")
        return pd.DataFrame()

def img_to_base64(img_path):
    """Mengubah file gambar menjadi string base64."""
    path = Path(img_path)
    if not path.is_file():
        # Jika file tidak ditemukan, kembalikan None agar tidak error
        st.error(f"File logo tidak ditemukan di: {img_path}")
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def tampilkan_header(lebar_logo_kiri=255, lebar_intress=130, lebar_djpb=60, margin_atas='4rem', margin_bawah='4rem'):
    """
    Menampilkan header yang disesuaikan dengan logo yang sejajar dan presisi.
    - Logo kanan rata penuh ke kanan tanpa margin.
    - Lebar logo kanan bisa diatur satu per satu.
    """
    # CSS untuk perataan vertikal dan kontrol padding
    st.markdown(
        f"""
        <style>
            /* Mengatur padding atas dan bawah dari blok utama Streamlit */
            div.block-container {{
                padding-top: {margin_atas};
                padding-bottom: {margin_bawah};
                padding-left: 2rem;
                padding-right: 2rem;
            }}
            /* CSS untuk menyejajarkan item di dalam kolom secara vertikal */
            [data-testid="stHorizontalBlock"] {{
                align-items: flex-end;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Mengatur kolom utama untuk tata letak header
    col_logo_kiri, col_kosong, col_logo_kanan = st.columns([2, 5, 2.5])

    with col_logo_kiri:
        # Logo Kementerian Keuangan di sisi kiri
        st.image("logo/KEMENKEU.png", width=lebar_logo_kiri)

    with col_logo_kanan:
        # Path logo
        intress_path = "logo/INTRESS.png"
        djpb_path = "logo/DJPb.png"

        # Encode gambar ke base64
        intress_b64 = img_to_base64(intress_path)
        djpb_b64 = img_to_base64(djpb_path)

        # Hanya tampilkan jika gambar berhasil di-load
        if intress_b64 and djpb_b64:
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-end; align-items: center; gap: 8px;">
                <img src="data:image/png;base64,{intress_b64}" width="{lebar_intress}">
                <img src="data:image/png;base64,{djpb_b64}" width="{lebar_djpb}">
            </div>
            """, unsafe_allow_html=True)

# --- FUNGSI-FUNGSI VISUALISASI LENGKAP ---

def display_pendapatan_infographic():
    SHEET_NAME = 'KINERJA PENDAPATAN APBN'
    df = get_data(SHEET_NAME)
    if df is None or df.empty: return

    st.markdown("""
    <style>
        .pend-row { display: flex; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 15px 5px; }
        .pend-row:last-child { border-bottom: none; }
        .pend-icon { font-size: 2.5em; width: 60px; text-align: center; }
        .pend-details { flex-grow: 1; padding-left: 15px; }
        .pend-details-sub { padding-left: 85px; }
        .pend-category { font-size: 1.05em; color: #333; font-weight: 600; }
        .pend-amount { font-size: 1.2em; color: #003366; font-weight: 700; }
        .pend-yoy { display: inline-block; padding: 4px 10px; border-radius: 20px; font-weight: 600; font-size: 0.95em; margin-left: 10px; }
        .pend-yoy-positive { background-color: #e6f7ec; color: #008744; }
        .pend-yoy-negative { background-color: #fdecea; color: #d93025; }
    </style>
    """, unsafe_allow_html=True)
    try:
        df['anggaran_num'] = df['anggaran (Rp)'].apply(parse_value)
        df['yoy_num'] = df['% yoy'].apply(parse_value)
        perpajakan = df[df['kategori'] == 'Penerimaan Perpajakan'].iloc[0]
        pajak_dn = df[df['kategori'] == 'Pajak Dalam Negeri'].iloc[0]
        pajak_pi = df[df['kategori'] == 'Pajak Perdagangan Internasional'].iloc[0]
        pnbp = df[df['kategori'] == 'Penerimaan Negara Bukan Pajak'].iloc[0]
        pnbp_lain = df[df['kategori'] == 'PNBP Lainnya'].iloc[0]
        pnbp_blu = df[df['kategori'] == 'Pendapatan BLU'].iloc[0]
        penerimaan_dn = df[df['kategori'] == 'Penerimaan Dalam Negeri'].iloc[0]

        display_data = [
            {'level': 1, 'icon': '💰', 'cat': '1. Penerimaan Perpajakan', 'amount': perpajakan['anggaran_num'], 'yoy': perpajakan['yoy_num']},
            {'level': 2, 'icon': '', 'cat': 'a) Pajak Dalam Negeri', 'amount': pajak_dn['anggaran_num'], 'yoy': pajak_dn['yoy_num']},
            {'level': 2, 'icon': '', 'cat': 'b) Pajak Perdagangan Internasional', 'amount': pajak_pi['anggaran_num'], 'yoy': pajak_pi['yoy_num']},
            {'level': 1, 'icon': '🏦', 'cat': '2. Penerimaan Negara Bukan Pajak', 'amount': pnbp['anggaran_num'], 'yoy': pnbp['yoy_num']},
            {'level': 2, 'icon': '', 'cat': 'a) PNBP Lainnya', 'amount': pnbp_lain['anggaran_num'], 'yoy': pnbp_lain['yoy_num']},
            {'level': 2, 'icon': '', 'cat': 'b) Pendapatan BLU', 'amount': pnbp_blu['anggaran_num'], 'yoy': pnbp_blu['yoy_num']},
            {'level': 1, 'icon': '🧾', 'cat': '3. Penerimaan Dalam Negeri', 'amount': penerimaan_dn['anggaran_num'], 'yoy': penerimaan_dn['yoy_num']},
        ]

        for item in display_data:
            details_class = "pend-details-sub" if item['level'] == 2 else "pend-details"
            if item['yoy'] > 0: yoy_class, yoy_symbol = "pend-yoy-positive", "▲"
            elif item['yoy'] < 0: yoy_class, yoy_symbol = "pend-yoy-negative", "▼"
            else: yoy_class, yoy_symbol = "pend-yoy-zero", "▬"
            st.markdown(f"""
            <div class="pend-row"><div class="pend-icon">{item['icon']}</div><div class="{details_class}">
            <div class="pend-category">{item['cat']}</div><div><span class="pend-amount">{format_otomatis(item['amount'])}</span>
            <span class="pend-yoy {yoy_class}">{yoy_symbol} {item['yoy']:.2f}% yoy</span></div></div></div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Gagal memproses visualisasi Pendapatan: {e}")

def display_belanja_kl_chart():
    SHEET_NAME = 'REALISASI BELANJA KL'
    df = get_data(SHEET_NAME)
    if df is None or df.empty: return

    st.markdown("""
    <style>
        .bkl-summary-box { background-color: #FFFBEA; border: 1px solid #FFECB3; border-radius: 10px; padding: 15px; text-align: center; width: 250px; height: fit-content; margin: 30px auto 0 auto; }
        .bkl-summary-title { font-size: 1.1em; font-weight: 600; }
        .bkl-summary-percent { font-size: 2.5em; font-weight: 700; color: #003366; margin: 5px 0; }
        .bkl-summary-pagu { font-size: 0.9em; }
        .bkl-item { display: flex; align-items: center; margin-bottom: 25px; }
        .bkl-cat-label { width: 120px; font-weight: 600; text-align: right; padding-right: 15px; }
        .bkl-bars-container { flex-grow: 1; }
        .bkl-bar-wrapper { margin-bottom: 4px; position: relative; }
        .bkl-bar { height: 20px; border-radius: 4px; }
        .bkl-bar-realisasi { background-color: #FFC107; }
        .bkl-bar-pagu { background-color: #0D47A1; }
        .bkl-bar-label { position: absolute; left: 8px; top: 50%; transform: translateY(-50%); color: white; font-size: 0.8em; font-weight: 600; text-shadow: 1px 1px 2px rgba(0,0,0,0.5); }
        .bkl-stats { width: 180px; text-align: left; padding-left: 15px; font-size: 0.95em; }
        .bkl-yoy-pos { color: #2E7D32; font-weight: 600; }
        .bkl-yoy-neg { color: #C62828; font-weight: 600; }
        .bkl-legend { display: flex; justify-content: center; gap: 20px; margin-top: 20px; font-size: 0.9em; }
        .bkl-legend-item { display: flex; align-items: center; gap: 5px; }
        .bkl-legend-color { width: 15px; height: 15px; border-radius: 3px; }
    </style>
    """, unsafe_allow_html=True)
    try:
        df['pagu_num'] = df['Pagu (Rp)'].apply(parse_value)
        df['realisasi_num'] = df['Realisasi (Rp)'].apply(parse_value)
        df['yoy_num'] = df['%yoy'].apply(parse_value)
        df['persen_realisasi'] = (df['realisasi_num'] / df['pagu_num'].replace(0, np.nan) * 100).fillna(0)
        total_pagu = df['pagu_num'].sum()
        total_realisasi = df['realisasi_num'].sum()
        total_persen_realisasi = (total_realisasi / total_pagu) * 100 if total_pagu > 0 else 0
        max_val = df['pagu_num'].max()

        for _, row in df.sort_values('pagu_num', ascending=False).iterrows():
            width_realisasi = (row['realisasi_num'] / max_val) * 100 if max_val > 0 else 0
            width_pagu = (row['pagu_num'] / max_val) * 100 if max_val > 0 else 0
            if row['yoy_num'] > 0: yoy_class, yoy_symbol = "bkl-yoy-pos", "▲"
            elif row['yoy_num'] < 0: yoy_class, yoy_symbol = "bkl-yoy-neg", "▼"
            else: yoy_class, yoy_symbol = "bkl-yoy-zero", "▬"
            st.markdown(f"""
            <div class="bkl-item">
                <div class="bkl-cat-label">{row['Jenis Belanja']}</div>
                <div class="bkl-bars-container">
                    <div class="bkl-bar-wrapper"><div class="bkl-bar bkl-bar-realisasi" style="width: {width_realisasi}%;"><span class="bkl-bar-label">{format_otomatis(row['realisasi_num'])}</span></div></div>
                    <div class="bkl-bar-wrapper"><div class="bkl-bar bkl-bar-pagu" style="width: {width_pagu}%;"><span class="bkl-bar-label">{format_otomatis(row['pagu_num'])}</span></div></div>
                </div>
                <div class="bkl-stats"><div><b>{row['persen_realisasi']:.2f}%</b></div><div class="{yoy_class}">{yoy_symbol} {row['yoy_num']:.2f}% yoy</div></div>
            </div>""", unsafe_allow_html=True)
        st.markdown("""<div class="bkl-legend"><div class="bkl-legend-item"><div class="bkl-legend-color" style="background-color: #FFC107;"></div> Realisasi</div><div class="bkl-legend-item"><div class="bkl-legend-color" style="background-color: #0D47A1;"></div> Pagu</div></div>""", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="bkl-summary-box">
            <div class="bkl-summary-title">Realisasi Total</div>
            <div class="bkl-summary-percent">{total_persen_realisasi:.2f}%</div>
            <div class="bkl-summary-pagu">dari pagu <b>{format_otomatis(total_pagu)}</b></div>
        </div>""", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Gagal memproses visualisasi Belanja K/L: {e}")

def display_tkd_chart():
    SHEET_NAME = 'CAPAIAN PENYALURAN TKD'
    df = get_data(SHEET_NAME)
    if df is None or df.empty: return

    try:
        df['pagu_num'] = df['Pagu (Rp)'].apply(parse_value)
        df['realisasi_num'] = df['Realisasi (Rp)'].apply(parse_value)
        df['persentase'] = (df['realisasi_num'] / df['pagu_num'].replace(0, np.nan) * 100).fillna(0)

        max_val = df['pagu_num'].max()
        if max_val >= 1_000_000_000:
            divisor, unit, yaxis_title = 1_000_000_000, "M", "dalam Miliar Rupiah"
        else:
            divisor, unit, yaxis_title = 1_000_000, "Jt", "dalam Juta Rupiah"
        df['pagu_display'] = df['pagu_num'] / divisor
        df['realisasi_display'] = df['realisasi_num'] / divisor

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(go.Bar(
            x=df['Jenis Dana'], y=df['pagu_display'], name='Pagu', marker_color='#0056b3',
            text=df['pagu_display'].apply(lambda x: f"<b>{x:,.2f}</b>"),
            textposition='outside',
            textfont=dict(color='black', size=11, family="Arial")
        ), secondary_y=False)

        fig.add_trace(go.Bar(
            x=df['Jenis Dana'], y=df['realisasi_display'], name='Realisasi', marker_color='#ffc107',
            text=df['realisasi_display'].apply(lambda x: f"<b>{x:,.2f}</b>"),
            textposition='outside',
            textfont=dict(color='black', size=11, family="Arial")
        ), secondary_y=False)

        fig.add_trace(go.Scatter(
            x=df['Jenis Dana'], y=df['persentase'], name='Persentase',
            mode='lines+markers+text',
            line=dict(color='black', width=3),
            marker=dict(color='black', size=8),
            text=df['persentase'].apply(lambda x: f'<b>{x:.2f}%</b>'),
            textposition="top center",
            textfont=dict(color='black', size=12, family="Arial")
        ), secondary_y=True)

        # PERUBAHAN: Mengatur warna sumbu, tick, dan judul menjadi hitam
        fig.update_layout(
            barmode='group',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            uniformtext_minsize=8,
            uniformtext_mode='hide',
            margin=dict(t=50),
            xaxis=dict(
                tickfont=dict(color='black', size=12),
                linecolor='black'
            ),
            yaxis=dict(
                title=yaxis_title,
                title_font=dict(color='black', size=12),
                tickfont=dict(color='black', size=12),
                linecolor='black'
            ),
            yaxis2=dict(
                title='Persentase (%)',
                title_font=dict(color='black', size=12),
                tickfont=dict(color='black', size=12),
                linecolor='black'
            )
        )

        st.plotly_chart(fig, use_container_width=True)

        total_pagu = df['pagu_num'].sum()
        total_realisasi = df['realisasi_num'].sum()
        total_persen_realisasi = (total_realisasi / total_pagu) * 100 if total_pagu > 0 else 0
        summary_html = f"""
        <div style="background-color: #f8f9fa; border-radius: 10px; padding: 20px; text-align: center; margin-top: -20px; position: relative; z-index: 1; border: 1px solid #dee2e6;">
            <div style="font-size: 1.1em; color: #000000; margin-bottom: 8px; font-weight: 600;">Total Dana Transfer ke Daerah (TKD) disalurkan sebesar</div>
            <div style="font-size: 2em; font-weight: 700; color: #ffc107; line-height: 1.2;">{format_otomatis(total_realisasi)}</div>
            <div style="font-size: 1em; color: #6c757d;">dari total pagu {format_otomatis(total_pagu)}</div>
            <div style="border-top: 1px solid #dee2e6; padding-top: 15px; margin-top: 15px; display: flex; align-items: center; justify-content: center; gap: 15px;">
                <span style="font-size: 1.2em; color: #000000; font-weight: 600;">Tingkat Realisasi</span>
                <span style="font-size: 2em; font-weight: 700; color: #0056b3; background-color: #e7f1ff; padding: 5px 12px; border-radius: 8px;">{total_persen_realisasi:.2f}%</span>
            </div>
        </div>
        """
        st.markdown(summary_html, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Gagal memproses data untuk visualisasi TKD: {e}")

def display_belanja_negara_chart():
    SHEET_NAME = 'REALISASI BELANJA NEGARA'
    df = get_data(SHEET_NAME)
    if df is None or df.empty: return

    try:
        df['pagu_num'] = df['Pagu (Rp)'].apply(parse_value)
        df['realisasi_num'] = df['Realisasi (Rp)'].apply(parse_value)
        df['persentase'] = (df['realisasi_num'] / df['pagu_num'].replace(0, np.nan) * 100).fillna(0)

        max_val = df['pagu_num'].max()
        if max_val >= 1_000_000_000_000:
            divisor, unit, yaxis_title = 1_000_000_000_000, "T", "dalam Triliun Rupiah"
        else:
            divisor, unit, yaxis_title = 1_000_000_000, "M", "dalam Miliar Rupiah"
        df['pagu_display'] = df['pagu_num'] / divisor
        df['realisasi_display'] = df['realisasi_num'] / divisor

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(go.Bar(
            x=df['Kategori'], y=df['pagu_display'], name='Pagu', marker_color='#2962FF',
            text=df['pagu_display'].apply(lambda x: f"<b>{x:,.2f}</b>"),
            textposition='outside',
            textfont=dict(color='black', size=11, family="Arial")
        ), secondary_y=False)

        fig.add_trace(go.Bar(
            x=df['Kategori'], y=df['realisasi_display'], name='Realisasi', marker_color='#FFC107',
            text=df['realisasi_display'].apply(lambda x: f"<b>{x:,.2f}</b>"),
            textposition='outside',
            textfont=dict(color='black', size=11, family="Arial")
        ), secondary_y=False)

        fig.add_trace(go.Scatter(
            x=df['Kategori'], y=df['persentase'], name='Persentase',
            mode='lines+markers',
            line=dict(color='black', width=3),
            marker=dict(color='black', size=8)
        ), secondary_y=True)

        for i, row in df.iterrows():
            fig.add_annotation(
                x=row['Kategori'], y=row['persentase'], text=f"<b>{row['persentase']:.2f}%</b>",
                font=dict(color="black", size=12, family="Arial"),
                showarrow=False, yshift=15, yref="y2"
            )

        # PERUBAHAN: Mengatur warna sumbu, tick, dan judul menjadi hitam
        fig.update_layout(
            barmode='group',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=50),
            xaxis=dict(
                tickfont=dict(color='black', size=12),
                linecolor='black'
            ),
            yaxis=dict(
                title=yaxis_title,
                titlefont=dict(color='black', size=12),
                tickfont=dict(color='black', size=12),
                linecolor='black'
            ),
            yaxis2=dict(
                title='Persentase (%)',
                title_font=dict(color='black', size=12),
                tickfont=dict(color='black', size=12),
                linecolor='black'
            )
        )

        st.plotly_chart(fig, use_container_width=True)

        total_data = df[df['Kategori'] == 'Belanja Negara'].iloc[0]
        summary_text = (f"Belanja yang dikelola ➔ Realisasi <b>{format_otomatis(total_data['realisasi_num'])}</b> dari Pagu <b>{format_otomatis(total_data['pagu_num'])}</b> ({total_data['persentase']:.2f}%)")
        st.markdown(f'<div style="background-color: #E8F5E9; border-radius: 10px; padding: 15px; text-align: center; margin-top: -20px; position: relative; z-index: 1; border: 1px solid #A5D6A7;"><p style="font-size: 1.1em; color: #1B5E20;">{summary_text}</p></div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Gagal memproses data untuk visualisasi Belanja Negara: {e}")

def display_umi_kur_chart():
    SHEET_NAME = "PENYALURAN PEMBIAYAAN UMi & KUR"
    df = get_data(SHEET_NAME)
    if df is None or df.empty: return

    st.markdown("""
    <style>
        /* Kartu Ringkasan */
        .summary-card { padding: 18px; border-radius: 10px; text-align: center; margin-bottom: 20px; }
        .umi-card { background-color: #E7F5FF; border: 1px solid #B3E5FC; }
        .kur-card { background-color: #FFF8E1; border: 1px solid #FFECB3; }
        .summary-title { font-size: 1.1em; font-weight: 600; color: #333; }
        .summary-amount { font-size: 2em; font-weight: 700; color: #0D47A1; margin: 5px 0; }
        .kur-card .summary-amount { color: #FF6F00; }
        .summary-debitur { font-size: 1em; color: #555; }

        /* Visualisasi UMi */
        .umi-item { display: flex; align-items: center; margin-bottom: 15px; }
        .umi-label { width: 120px; text-align: right; padding-right: 15px; font-weight: 600; }
        .umi-bar-container { flex-grow: 1; }
        .umi-bar {
            height: 30px; border-radius: 5px; color: white; display: flex;
            align-items: center; justify-content: center; font-weight: 600;
            text-shadow: 1px 1px 1px rgba(0,0,0,0.4); margin: 0 auto;
        }
        .umi-bar-0 { background-color: #ffc107; }
        .umi-bar-1 { background-color: #007bff; }
        .umi-bar-2 { background-color: #28a745; }

        /* <-- PERUBAHAN: Menambahkan CSS untuk detail debitur UMi --> */
        .umi-debitur-details {
            width: 140px; /* Memberi ruang untuk teks */
            text-align: left;
            padding-left: 15px;
            font-size: 1.05em;
            font-weight: 600;
            color: #333;
        }

        /* Visualisasi KUR */
        .kur-item { display: flex; align-items: center; font-size: 1.1em; margin-bottom: 15px; }
        .kur-label { width: 120px; text-align: right; padding-right: 15px; font-weight: 600; }
        .kur-amount { color: #d9534f; font-weight: 700; }
        .kur-arrow { font-size: 1.5em; color: #007bff; margin: 0 15px; }
        .kur-debitur { font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)
    try:
        df['pembiayaan_num'] = df['Jumlah Pembiayaan (Rp)'].apply(parse_value)
        df['debitur_num'] = df['Jumlah Debitur'].apply(parse_value)

        umi_df = df[df['Jenis Pembiayaan'] == 'UMi'].copy()
        kur_df = df[df['Jenis Pembiayaan'] == 'KUR'].copy()

        total_umi_val = umi_df['pembiayaan_num'].sum()
        total_umi_debitur = umi_df['debitur_num'].sum()
        total_kur_val = kur_df['pembiayaan_num'].sum()
        total_kur_debitur = kur_df['debitur_num'].sum()
        max_umi_val = umi_df['pembiayaan_num'].max() if not umi_df.empty else 0

        st.subheader("Penyaluran Pembiayaan UMi")
        st.markdown(f"""
        <div class="summary-card umi-card">
            <div class="summary-title">Total Penyaluran UMi</div>
            <div class="summary-amount">{format_otomatis(total_umi_val)}</div>
            <div class="summary-debitur">untuk <b>{int(total_umi_debitur):,}</b> debitur</div>
        </div>
        """, unsafe_allow_html=True)
        for i, row in umi_df.iterrows():
            bar_width = (row['pembiayaan_num'] / max_umi_val) * 60 if max_umi_val > 0 else 0 # <-- PERUBAHAN: Mengurangi lebar bar agar ada ruang
            st.markdown(f"""
            <div class="umi-item">
                <div class="umi-label">{row['Wilayah']}</div>
                <div class="umi-bar-container">
                    <div class="umi-bar umi-bar-{i % 3}" style="width: {bar_width}%; min-width: 110px;">{format_otomatis(row['pembiayaan_num'])}</div>
                </div>
                <div class="umi-debitur-details">
                    ➔ <b>{int(row['debitur_num']):,}</b> Debitur
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        st.subheader("Penyaluran Pembiayaan KUR")
        st.markdown(f"""
        <div class="summary-card kur-card">
            <div class="summary-title">Total Penyaluran KUR</div>
            <div class="summary-amount">{format_otomatis(total_kur_val)}</div>
            <div class="summary-debitur">untuk <b>{int(total_kur_debitur):,}</b> debitur</div>
        </div>
        """, unsafe_allow_html=True)

        for i, row in kur_df.iterrows():
            st.markdown(f"""
            <div class="kur-item">
                <div class="kur-label">{row['Wilayah']}</div>
                <div class="kur-amount">{format_otomatis(row['pembiayaan_num'])}</div>
                <div class="kur-arrow">➔</div>
                <div class="kur-debitur">{int(row['debitur_num']):,} Debitur</div>
            </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Gagal memproses data untuk visualisasi UMi & KUR: {e}")

def display_digitalisasi_chart():
    SHEET_NAME = "CAPAIAN DIGITALISASI PEMBAYARAN"
    df = get_data(SHEET_NAME)
    if df is None or df.empty: return

    st.markdown("""
    <style>
        .digi-card { background-color: #ffffff; border-radius: 12px; padding: 20px; border-left: 5px solid; box-shadow: 0 4px 12px rgba(0,0,0,0.08); border: 1px solid #e9ecef; height: 100%; margin-bottom: 20px; }
        .digi-header { display: flex; align-items: center; margin-bottom: 18px; }
        .digi-icon { font-size: 2rem; margin-right: 15px; width: 45px; text-align: center; }
        .digi-title { font-size: 1.5rem; font-weight: 600; }
        .digi-metrics-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        .digi-metric-item { background-color: #f8f9fa; padding: 12px; border-radius: 8px; text-align: center; border: 1px solid #e9ecef; }
        .digi-metric-label { font-size: 0.85rem; color: #6c757d; margin-bottom: 8px; }
        .digi-value-container { display: flex; justify-content: center; align-items: baseline; gap: 8px; flex-wrap: wrap; }
        .digi-metric-value { font-size: 1.4rem; font-weight: 700; color: #212529; line-height: 1.2; }
        .digi-yoy { font-size: 0.8rem; font-weight: 600; }
        .digi-yoy-pos { color: #198754; }
        .digi-yoy-neg { color: #dc3545; }
        .digi-yoy-zero { color: #6c757d; }
    </style>
    """, unsafe_allow_html=True)

    def get_yoy_html(yoy_value):
        if yoy_value is None or str(yoy_value).strip().lower() == 'none':
            return ""

        yoy_val = parse_value(yoy_value)
        if yoy_val > 0:
            return f'<div class="digi-yoy digi-yoy-pos">▲ {abs(yoy_val):.2f}%</div>'
        elif yoy_val < 0:
            return f'<div class="digi-yoy digi-yoy-neg">▼ {abs(yoy_val):.2f}%</div>'
        else:
            return f'<div class="digi-yoy digi-yoy-zero">▬ {abs(yoy_val):.2f}%</div>'

    try:
        df['nilai_transaksi_num'] = df['Nilai Transaksi (Rp)'].apply(parse_value)
        df['jumlah_transaksi_num'] = df['Jumlah Transaksi'].apply(parse_value)

        platforms = {
            'digipay': {'name': 'DigiPay', 'color': '#ffc107', 'icon': '💳'},
            'KKP': {'name': 'Kartu Kredit Pemerintah', 'color': '#0d6efd', 'icon': '💲'},
            'CMS': {'name': 'Cash Management System', 'color': '#198754', 'icon': '🖥️'}
        }

        for platform_key, data in platforms.items():
            platform_df = df[df['Platform'] == platform_key]

            if not platform_df.empty:
                row = platform_df.iloc[0]
                metrik_values = re.findall(r'\d+', str(row['Metrik Utama']))
                yoy_nilai_html = get_yoy_html(row['Pertumbuhan YoY (%)'])

                card_html = f'<div class="digi-card" style="border-left-color: {data["color"]};">'
                card_html += f'<div class="digi-header"><div class="digi-icon">{data["icon"]}</div><div class="digi-title">{data["name"]}</div></div>'
                card_html += '<div class="digi-metrics-grid">'

                if platform_key == 'digipay' and len(metrik_values) >= 2:
                    card_html += f"""
                        <div class="digi-metric-item"><div class="digi-metric-label">Satker</div><div class="digi-metric-value">{metrik_values[0]}</div></div>
                        <div class="digi-metric-item"><div class="digi-metric-label">Vendor</div><div class="digi-metric-value">{metrik_values[1]}</div></div>
                        <div class="digi-metric-item"><div class="digi-metric-label">Transaksi</div><div class="digi-metric-value">{int(row['jumlah_transaksi_num']):,}</div></div>
                        <div class="digi-metric-item">
                            <div class="digi-metric-label">Nilai Transaksi</div>
                            <div class="digi-value-container">
                                <div class="digi-metric-value">{format_otomatis(row['nilai_transaksi_num'])}</div>
                                {yoy_nilai_html}
                            </div>
                        </div>
                    """
                elif len(metrik_values) >= 2: # Untuk KKP dan CMS
                    card_html += f"""
                        <div class="digi-metric-item"><div class="digi-metric-label">Satker Pengguna</div><div class="digi-metric-value">{metrik_values[0]} dari {metrik_values[1]}</div></div>
                        <div class="digi-metric-item">
                            <div class="digi-metric-label">Nilai Transaksi</div>
                            <div class="digi-value-container">
                                <div class="digi-metric-value">{format_otomatis(row['nilai_transaksi_num'])}</div>
                                {yoy_nilai_html}
                            </div>
                        </div>
                    """
                card_html += '</div></div>'
                st.markdown(card_html, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Gagal memproses data digitalisasi: {str(e)}")

def generate_press_release():
    """
    FUNGSI YANG DIPERBARUI:
    Menghasilkan siaran pers detail dengan mengadopsi logika terstruktur
    dari class APBNSheetWisePressRelease.
    """
    press_sections = []
    today = datetime.now().strftime("%d %B %Y")

    # --- 1. BAGIAN PENDAPATAN ---
    pendapatan_df = get_data('KINERJA PENDAPATAN APBN')
    if not pendapatan_df.empty:
        try:
            pendapatan_df['anggaran_num'] = pendapatan_df['anggaran (Rp)'].apply(parse_value)
            pendapatan_df['yoy_num'] = pendapatan_df['% yoy'].apply(parse_value)

            narasi = ["### 1. Kinerja Pendapatan Negara"]

            # Kategori utama
            total = pendapatan_df[pendapatan_df['kategori'].str.strip() == 'Penerimaan Dalam Negeri'].iloc[0]
            pajak = pendapatan_df[pendapatan_df['kategori'].str.strip() == 'Penerimaan Perpajakan'].iloc[0]
            pnbp = pendapatan_df[pendapatan_df['kategori'].str.strip() == 'Penerimaan Negara Bukan Pajak'].iloc[0]

            narasi.append(f"📌 **Total Pendapatan Negara** mencapai **{format_otomatis(total['anggaran_num'])}**, tumbuh sebesar **{total['yoy_num']:.2f}%** (YoY).")

            # Detail Perpajakan
            narasi.append(f"\n🔍 **Penerimaan Perpajakan** memberikan kontribusi **{format_otomatis(pajak['anggaran_num'])}** ({pajak['yoy_num']:.2f}% YoY), dengan rincian:")
            sub_pajak = ['Pajak Dalam Negeri', 'Pajak Perdagangan Internasional']
            for kat in sub_pajak:
                data = pendapatan_df[pendapatan_df['kategori'].str.strip() == kat].iloc[0]
                narasi.append(f"- **{kat}**: {format_otomatis(data['anggaran_num'])} ({data['yoy_num']:.2f}% YoY)")

            # Detail PNBP
            narasi.append(f"\n🔍 **PNBP** menyumbang **{format_otomatis(pnbp['anggaran_num'])}** ({pnbp['yoy_num']:.2f}% YoY), terdiri dari:")
            sub_pnbp = ['PNBP Lainnya', 'Pendapatan BLU']
            for kat in sub_pnbp:
                data = pendapatan_df[pendapatan_df['kategori'].str.strip() == kat].iloc[0]
                narasi.append(f"- **{kat}**: {format_otomatis(data['anggaran_num'])} ({data['yoy_num']:.2f}% YoY)")

            press_sections.append("\n".join(narasi))
        except Exception as e:
            press_sections.append(f"### 1. Kinerja Pendapatan Negara\n_Gagal memproses data: {e}_")

    # --- 2. BAGIAN BELANJA ---
    belanja_df = get_data('REALISASI BELANJA NEGARA')
    if not belanja_df.empty:
        try:
            belanja_df['pagu_num'] = belanja_df['Pagu (Rp)'].apply(parse_value)
            belanja_df['realisasi_num'] = belanja_df['Realisasi (Rp)'].apply(parse_value)
            belanja_df['persentase'] = (belanja_df['realisasi_num'] / belanja_df['pagu_num'].replace(0, np.nan) * 100).fillna(0)

            narasi = ["### 2. Realisasi Belanja Negara"]

            total = belanja_df[belanja_df['Kategori'].str.strip() == 'Belanja Negara'].iloc[0]
            narasi.append(f"📊 **Total Belanja Negara** telah terealisasi sebesar **{format_otomatis(total['realisasi_num'])}**, atau **{total['persentase']:.2f}%** dari total pagu.")

            narasi.append("\n**Rincian realisasi per jenis belanja**:")
            sub_belanja = ['Belanja K/L', 'Transfer ke Daerah', 'Belanja Negara']
            for kat in sub_belanja:
                data = belanja_df[belanja_df['Kategori'].str.strip() == kat].iloc[0]
                narasi.append(f"- **{kat}**: {format_otomatis(data['realisasi_num'])} ({data['persentase']:.2f}% dari pagu)")

            press_sections.append("\n".join(narasi))
        except Exception as e:
            press_sections.append(f"### 2. Realisasi Belanja Negara\n_Gagal memproses data: {e}_")

    # --- 3. BAGIAN TRANSFER KE DAERAH ---
    tkd_df = get_data('CAPAIAN PENYALURAN TKD')
    if not tkd_df.empty:
        try:
            tkd_df['pagu_num'] = tkd_df['Pagu (Rp)'].apply(parse_value)
            tkd_df['realisasi_num'] = tkd_df['Realisasi (Rp)'].apply(parse_value)
            tkd_df['persentase'] = (tkd_df['realisasi_num'] / tkd_df['pagu_num'].replace(0, np.nan) * 100).fillna(0)

            narasi = ["### 3. Penyaluran Transfer ke Daerah (TKD)"]

            total_pagu = tkd_df['pagu_num'].sum()
            total_realisasi = tkd_df['realisasi_num'].sum()
            total_persen = (total_realisasi / total_pagu * 100) if total_pagu > 0 else 0

            narasi.append(f"🏛️ **Total TKD** yang telah disalurkan mencapai **{format_otomatis(total_realisasi)}**, atau **{total_persen:.2f}%** dari alokasi.")

            narasi.append("\n**Detail penyaluran per jenis dana**:")
            for _, row in tkd_df.iterrows():
                narasi.append(f"- **{row['Jenis Dana']}**: {format_otomatis(row['realisasi_num'])} ({row['persentase']:.2f}% dari pagu)")

            press_sections.append("\n".join(narasi))
        except Exception as e:
            press_sections.append(f"### 3. Penyaluran TKD\n_Gagal memproses data: {e}_")

    # --- 4. BAGIAN PEMBIAYAAN ---
    pembiayaan_df = get_data('PENYALURAN PEMBIAYAAN UMi & KUR')
    if not pembiayaan_df.empty:
        try:
            pembiayaan_df['pembiayaan_num'] = pembiayaan_df['Jumlah Pembiayaan (Rp)'].apply(parse_value)
            pembiayaan_df['debitur_num'] = pembiayaan_df['Jumlah Debitur'].apply(parse_value)

            narasi = ["### 4. Dukungan Pembiayaan UMKM"]

            # Proses UMi
            umi_data = pembiayaan_df[pembiayaan_df['Jenis Pembiayaan'] == 'UMi']
            if not umi_data.empty:
                total_umi = umi_data['pembiayaan_num'].sum()
                total_debitur_umi = umi_data['debitur_num'].sum()
                narasi.append(f"\n**Pembiayaan Ultra Mikro (UMi)** telah disalurkan sebesar **{format_otomatis(total_umi)}** kepada **{int(total_debitur_umi):,} debitur**.")

            # Proses KUR
            kur_data = pembiayaan_df[pembiayaan_df['Jenis Pembiayaan'] == 'KUR']
            if not kur_data.empty:
                total_kur = kur_data['pembiayaan_num'].sum()
                total_debitur_kur = kur_data['debitur_num'].sum()
                narasi.append(f"**Kredit Usaha Rakyat (KUR)** tersalurkan sebesar **{format_otomatis(total_kur)}** kepada **{int(total_debitur_kur):,} debitur**.")

            press_sections.append("\n".join(narasi))
        except Exception as e:
            press_sections.append(f"### 4. Dukungan Pembiayaan UMKM\n_Gagal memproses data: {e}_")

    # --- GABUNGKAN SEMUA BAGIAN ---
    if press_sections:
        header = []
        header.append("\n### ANALISIS DETAIL")

        final_report = header + press_sections
        return "\n\n".join(final_report)
    else:
        return "## Tidak dapat menghasilkan laporan\nData tidak tersedia atau format tidak sesuai."
