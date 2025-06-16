import streamlit as st
from SPARQLWrapper import SPARQLWrapper, JSON

SPARQL_ENDPOINT = "http://localhost:7200/repositories/1rv"  

# Enhanced styling with better design
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500;600&display=swap');

/* Main background */
[data-testid="stMain"] {
    background-image: url("https://img.freepik.com/free-vector/dark-luxury-mandala-background_1055-3152.jpg?semt=ais_items_boosted&w=740");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
    background-attachment: fixed;
    min-height: 100vh;
    position: relative;
}

[data-testid="stMain"]::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.7);
    z-index: 0;
    pointer-events: none;
}

/* Sidebar styling */
.css-1d391kg, [data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(52, 31, 19, 0.95) 0%, rgba(35, 20, 12, 0.95) 100%);
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}

.css-1d391kg .css-17eq0hr, [data-testid="stSidebar"] .css-17eq0hr {
    color: #ffffff;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Playfair Display', serif;
    color: #ffffff;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

h1 {
    font-size: 2.5rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 2rem;
    text-align: center;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

h2 {
    font-size: 1.8rem;
    color: #ffffff;
    border-bottom: 2px solid rgba(255, 255, 255, 0.3);
    padding-bottom: 0.5rem;
    margin-bottom: 1.5rem;
}

h3 {
    font-size: 1.4rem;
    color: #87ceeb;
}

p, div, span {
    font-family: 'Inter', sans-serif;
    color: #e8e8e8;
    line-height: 1.6;
}

/* Cards and containers */
.stExpander {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    backdrop-filter: blur(10px);
    margin-bottom: 1rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.stExpander > div > div {
    background: transparent;
}

.stExpander[data-testid="stExpander"] {
    border: 1px solid rgba(255, 215, 0, 0.2);
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 24px;
    background: rgba(255, 255, 255, 0.05);
    padding: 8px;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.stTabs [data-baseweb="tab"] {
    height: 50px;
    padding: 0 24px;
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: #e8e8e8;
    font-weight: 500;
    transition: all 0.3s ease;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(135, 206, 235, 0.2), rgba(135, 206, 235, 0.1));
    border-color: rgba(135, 206, 235, 0.5);
    color: #87ceeb;
}

.stTabs [data-baseweb="tab"]:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.3);
}

/* Input styling */
.stTextInput > div > div > input {
    background: rgba(255, 255, 255, 0.1);
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    color: #ffffff;
    font-size: 16px;
    padding: 12px 16px;
    backdrop-filter: blur(5px);
    transition: all 0.3s ease;
}

.stTextInput > div > div > input:focus {
    border-color: #87ceeb;
    box-shadow: 0 0 0 2px rgba(135, 206, 235, 0.2);
    background: rgba(255, 255, 255, 0.15);
}

/* Custom content cards */
.content-card {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.03));
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 24px;
    margin: 16px 0;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
}

.content-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
    border-color: rgba(135, 206, 235, 0.3);
}

.uri-text {
    color: #87ceeb;
    font-size: 0.9rem;
    font-family: monospace;
    background: rgba(135, 206, 235, 0.1);
    padding: 4px 8px;
    border-radius: 6px;
    border: 1px solid rgba(135, 206, 235, 0.2);
    margin-bottom: 12px;
    display: inline-block;
}

.transliteration {
    color: #87ceeb;
    font-weight: 500;
    margin: 12px 0;
    padding: 12px;
    background: rgba(135, 206, 235, 0.05);
    border-left: 4px solid #87ceeb;
    border-radius: 0 8px 8px 0;
}

.translation {
    color: #98fb98;
    margin: 12px 0;
    padding: 12px;
    background: rgba(152, 251, 152, 0.05);
    border-left: 4px solid #98fb98;
    border-radius: 0 8px 8px 0;
}

.stTabs [data-baseweb="tab-list"] {
    overflow-x: auto !important;
    white-space: nowrap !important;
    display: flex;
    flex-wrap: nowrap !important;
    scrollbar-width: thin;
}

/* Tambahan: styling scrollbar horizontal */
.stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
    height: 6px;
}

.stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-thumb {
    background: rgba(135, 206, 235, 0.4);
    border-radius: 3px;
}

/* Statistics styling */
.stat-card {
    background: linear-gradient(135deg, rgba(135, 206, 235, 0.1), rgba(135, 206, 235, 0.05));
    border: 1px solid rgba(135, 206, 235, 0.3);
    border-radius: 12px;
    padding: 16px;
    margin: 8px 0;
    text-align: center;
}

.stat-number {
    font-size: 2rem;
    font-weight: 700;
    color: #87ceeb;
    display: block;
}

.stat-label {
    color: #e8e8e8;
    font-size: 0.9rem;
    margin-top: 4px;
}

/* Info message styling */
.stInfo {
    background: rgba(135, 206, 235, 0.1);
    border: 1px solid rgba(135, 206, 235, 0.3);
    border-radius: 12px;
    color: #87ceeb;
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: rgba(135, 206, 235, 0.3);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(135, 206, 235, 0.5);
}

/* Animation for loading */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.animate-fade-in {
    animation: fadeInUp 0.6s ease-out;
}

/* Responsive design */
@media (max-width: 768px) {
    h1 {
        font-size: 2rem;
    }
    
    .content-card {
        padding: 16px;
        margin: 12px 0;
    }
}
</style>
""", unsafe_allow_html=True)

# Fungsi SPARQL (tidak berubah)
def run_query(query):
    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def get_all_lines_grouped():
    query = """
    PREFIX ont: <http://contoh.org/ontology#>

    SELECT ?baris ?transliterasi ?terjemahan WHERE {
      ?baris a ont:SisiHalaman ;
             ont:hasTransliteration ?tl ;
             ont:hasTranslation ?tr .
      ?tl ont:value ?transliterasi .
      ?tr ont:value ?terjemahan .
    }
    ORDER BY ?baris
    """
    result = run_query(query)
    recto = []
    verso = []
    for res in result["results"]["bindings"]:
        uri = res["baris"]["value"]
        entry = {
            "id": uri,
            "transliterasi": res["transliterasi"]["value"],
            "terjemahan": res["terjemahan"]["value"]
        }
        if "recto" in uri:
            recto.append(entry)
        elif "verso" in uri:
            verso.append(entry)
    return recto, verso

def search_lines_grouped(keyword):
    query = f"""
    PREFIX ont: <http://contoh.org/ontology#>

    SELECT ?baris ?transliterasi ?terjemahan WHERE {{
        ?baris a ont:SisiHalaman ;
                ont:hasTransliteration ?tl ;
                ont:hasTranslation ?tr .
        ?tl ont:value ?transliterasi .
        ?tr ont:value ?terjemahan .

        FILTER (
            CONTAINS(LCASE(STR(?transliterasi)), LCASE("{keyword}")) ||
            CONTAINS(LCASE(STR(?terjemahan)), LCASE("{keyword}"))
        )
    }}
    ORDER BY ?baris
    """
    result = run_query(query)
    recto = []
    verso = []
    for res in result["results"]["bindings"]:
        uri = res["baris"]["value"]
        entry = {
            "id": uri,
            "transliterasi": res["transliterasi"]["value"],
            "terjemahan": res["terjemahan"]["value"]
        }
        if "recto" in uri:
            recto.append(entry)
        elif "verso" in uri:
            verso.append(entry)
    return recto, verso

def get_total_triples():
    query = "SELECT (COUNT(*) AS ?total) WHERE { ?s ?p ?o }"
    result = run_query(query)
    return int(result["results"]["bindings"][0]["total"]["value"])

def get_organized_lines():
    """Get lines organized by page (recto/verso pairs)"""
    query = """
    PREFIX ont: <http://contoh.org/ontology#>

    SELECT ?baris ?transliterasi ?terjemahan WHERE {
      ?baris a ont:SisiHalaman ;
             ont:hasTransliteration ?tl ;
             ont:hasTranslation ?tr .
      ?tl ont:value ?transliterasi .
      ?tr ont:value ?terjemahan .
    }
    ORDER BY ?baris
    """
    result = run_query(query)
    
    # Organize by page numbers
    pages = {}
    for res in result["results"]["bindings"]:
        uri = res["baris"]["value"]
        entry = {
            "id": uri,
            "transliterasi": res["transliterasi"]["value"],
            "terjemahan": res["terjemahan"]["value"]
        }
        
        # Extract page number from URI
        if "recto" in uri:
            # Extract number from URI like "...recto_1" or "...recto1"
            import re
            page_match = re.search(r'recto[_-]?(\d+)', uri)
            if page_match:
                page_num = int(page_match.group(1))
                if page_num not in pages:
                    pages[page_num] = {}
                pages[page_num]['recto'] = entry
        elif "verso" in uri:
            # Extract number from URI like "...verso_1" or "...verso1"
            import re
            page_match = re.search(r'verso[_-]?(\d+)', uri)
            if page_match:
                page_num = int(page_match.group(1))
                if page_num not in pages:
                    pages[page_num] = {}
                pages[page_num]['verso'] = entry
    
    return pages
    query = f"""
    PREFIX ont: <http://contoh.org/ontology#>
    SELECT (COUNT(?baris) AS ?jumlah) WHERE {{
      ?baris a ont:BarisNaskah ;
             ont:hasPosisi "{posisi}" .
    }}
    """
    result = run_query(query)
    return int(result["results"]["bindings"][0]["jumlah"]["value"])

# Helper function to render content cards
def render_content_card(entry):
    st.markdown(f"""
    <div class="content-card animate-fade-in">
        <div class="uri-text">📍 {entry['id']}</div>
        <div class="transliteration">
            <strong>📝 Transliterasi:</strong><br>
            {entry['transliterasi']}
        </div>
        <div class="translation">
            <strong>📚 Terjemahan:</strong><br>
            {entry['terjemahan']}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Sidebar dengan styling yang ditingkatkan
st.sidebar.markdown("# 🏛️ Website Translasi")
st.sidebar.markdown("## Sanghyang Tatwa Ajnyana")
st.sidebar.markdown("""
<div style="background: rgba(255, 255, 255, 0.05); padding: 16px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1);">
<p style="margin: 0;">Aplikasi ini dirancang untuk membantu dalam memahami naskah Sanghyang Tatwa Ajnyana</p>
<br>
<a href="https://www.academia.edu/5937886/_With_Tien_Wartini_et_al_2011_Sanghyang_Tatwa_Ajnyana_Teks_dan_Terjemahan#loswp-work-container" 
   style="color: #87ceeb; text-decoration: underline;">
   📖 Dokumen Sanghyang Tatwa Ajnyana
</a>
</div>
""", unsafe_allow_html=True)

# Informasi dataset dengan styling yang lebih baik
total_triples = get_total_triples()

st.sidebar.markdown("---")
st.sidebar.markdown("## 🗏 Panduan Halaman")
st.sidebar.markdown("""
<div style="background: rgba(135, 206, 235, 0.05); padding: 16px; border-radius: 12px; border: 1px solid rgba(135, 206, 235, 0.2);">
Sanghyang Tatwa Ajnyana disusun dalam bentuk <strong>lempir (lembar daun)</strong> yang ditulis bolak-balik. Setiap lempir terdiri dari 2 sisi:
<br>
• Recto (r): sisi depan lempir
<br>
• Verso (v): sisi belakang lempir
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("## 🔍 Panduan Pencarian")
st.sidebar.markdown("""
<div style="background: rgba(135, 206, 235, 0.05); padding: 16px; border-radius: 12px; border: 1px solid rgba(135, 206, 235, 0.2);">
• Masukkan kata atau frasa dari transliterasi atau terjemahan<br>
• Pencarian tidak peka huruf kapital<br>
• <strong>Contoh:</strong> dewa, mulia, hyang, sang
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("## 📊 Statistik Dataset")
st.sidebar.markdown(f"""
<div class="stat-card">
    <span class="stat-number">{total_triples}</span>
    <div class="stat-label">Total Triples</div>
</div>
""", unsafe_allow_html=True)

# Tampilan utama dengan header yang lebih menarik
st.markdown("# 📜 Naskah Digital: Transliterasi & Terjemahan")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["📚 Urutan Halaman", "📖 Per Recto Verso", "🔍 Pencarian Teks", "ℹ️ Informasi"])

with tab1:
    st.markdown("## 📚 Urutan Halaman Naskah")
    st.markdown("Jelajahi seluruh isi naskah Sanghyang Tatwa Ajnyana dengan transliterasi dan terjemahannya.")
    
    pages = get_organized_lines()
    
    if pages:
        st.markdown(f"**📄 Total Halaman:** 138 halaman")
        
        for page_num in sorted(pages.keys()):
            page_data = pages[page_num]
            
            # Display Recto
            if 'recto' in page_data:
                st.markdown(f"**📄 Recto {page_num}**")
                render_content_card(page_data['recto'])
            else:
                st.markdown(f"**📄 Recto {page_num}** - *Tidak tersedia*")
            
            # Display Verso
            if 'verso' in page_data:
                st.markdown(f"**📄 Verso {page_num}**")
                render_content_card(page_data['verso'])
            else:
                st.markdown(f"**📄 Verso {page_num}** - *Tidak tersedia*")
            
            st.markdown("---")
    else:
        st.info("Tidak ada data halaman yang tersedia.")

with tab2:
    st.markdown("## 📚 Koleksi Lengkap Naskah")
    st.markdown("Naskah ditampilkan dalam kelompok Recto dan Verso.")
    
    recto, verso = get_all_lines_grouped()

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**📄 Recto** ({len(recto)} entri)")
    with col2:
        st.markdown(f"**📄 Verso** ({len(verso)} entri)")

    with st.expander("📄 Recto", expanded=False):
        if recto:
            for res in recto:
                render_content_card(res)
        else:
            st.info("Tidak ada data recto yang tersedia.")

    with st.expander("📄 Verso", expanded=False):
        if verso:
            for res in verso:
                render_content_card(res)
        else:
            st.info("Tidak ada data verso yang tersedia.")

with tab3:
    st.markdown("## 🔍 Pencarian Transliterasi & Terjemahan")
    st.markdown("Temukan bagian spesifik dari naskah berdasarkan kata kunci.")
    
    keyword = st.text_input("🔍 Masukkan kata kunci pencarian:", placeholder="Contoh: dewa, mulia, hyang...")
    
    if keyword:
        with st.spinner("🔍 Mencari dalam database..."):
            recto, verso = search_lines_grouped(keyword)

        if not recto and not verso:
            st.markdown("""
            <div style="background: rgba(255, 193, 7, 0.1); border: 1px solid rgba(255, 193, 7, 0.3); 
                        border-radius: 12px; padding: 20px; text-align: center; margin: 20px 0;">
                <h3 style="color: #87ceeb; margin: 0;">🔍 Tidak ditemukan hasil</h3>
                <p style="margin: 10px 0 0 0;">Coba gunakan kata kunci yang berbeda atau periksa ejaan.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"### 🎯 Ditemukan {len(recto) + len(verso)} hasil untuk '{keyword}'")
            
            if recto:
                with st.expander(f"📄 Recto ({len(recto)} hasil)", expanded=True):
                    for res in recto:
                        render_content_card(res)

            if verso:
                with st.expander(f"📄 Verso ({len(verso)} hasil)", expanded=True):
                    for res in verso:
                        render_content_card(res)

with tab4:
    st.markdown("Sistem halaman dalam naskah Sanghyang Tatwa Ajnyana menggunakan sistem penomoran khas naskah Sunda Kuna berbahan daun gebang, dan disusun dalam bentuk lempir (lembar daun) yang ditulis bolak-balik. Setiap lempir diberi nomor dalam aksara Buda dan terdiri dari dua sisi:")
    st.markdown("• Recto (r): sisi depan lempir")
    st.markdown("• Verso (v): sisi belakang lempir")
    st.markdown("Masing-masing sisi memiliki empat baris teks. Penomoran menggunakan sistem angka asli aksara Buda yang ditulis di tepi kiri pada halaman verso. Penulisan konten mengikuti sistem transliterasi diplomatik yang menjaga susunan asli naskah tanpa menyisipkan koreksi eksplisit.")
    st.markdown("Nama dokumen atau istilah untuk menyebut jenis naskah ini adalah kropak. Dalam konteks naskah Sanghyang Tatwa Ajnyana, naskah ini dikenal sebagai Kropak 1099, yaitu nama katalog dari Perpustakaan Nasional Republik Indonesia (PNRI) untuk koleksi tersebut. Kropak merujuk pada kotak kayu penyimpanan naskah yang biasanya diberi nomor inventaris.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; background: rgba(255, 255, 255, 0.05); 
            border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1); margin-top: 40px;">
    <p style="margin: 0; color: #87ceeb;">
        🏛️ Website Translasi Sanghyang Tatwa Ajnyana | 
        Dibuat untuk melestarikan warisan budaya Indonesia
    </p>
</div>
""", unsafe_allow_html=True)