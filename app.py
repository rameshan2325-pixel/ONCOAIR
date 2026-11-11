import streamlit as st
import requests

st.set_page_config(
    page_title="ONCOAI",
    page_icon="🧬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.block-container {max-width: 760px; padding-top: 1.2rem; padding-bottom: 2rem;}
.hero {
    background: linear-gradient(135deg, #102D48, #176B78);
    padding: 1.35rem; border-radius: 18px; color: white; margin-bottom: 1rem;
}
.hero h1 {color: white; margin: 0; font-size: 2.1rem;}
.hero p {color: #D9EDF3; margin: .35rem 0 0 0;}
.small-note {color: #667085; font-size: .85rem;}
</style>
<div class="hero">
  <h1>🧬 ONCOAI</h1>
  <p>Your personal cancer biology research assistant</p>
</div>
""", unsafe_allow_html=True)

st.subheader("Gene Explorer")
st.write("Search the NCBI Gene database for a human gene.")

gene = st.text_input("Enter a gene symbol", value="TP53", placeholder="Example: TP53, EGFR, BRCA1")
search = st.button("Search NCBI", type="primary", use_container_width=True)

def ncbi_gene_search(symbol):
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    params = {
        "db": "gene",
        "term": f"{symbol}[Gene Name] AND Homo sapiens[Organism]",
        "retmode": "json",
        "retmax": 5
    }
    r = requests.get(base + "esearch.fcgi", params=params, timeout=25)
    r.raise_for_status()
    ids = r.json().get("esearchresult", {}).get("idlist", [])
    if not ids:
        return None
    gene_id = ids[0]
    summary_params = {"db": "gene", "id": gene_id, "retmode": "json"}
    s = requests.get(base + "esummary.fcgi", params=summary_params, timeout=25)
    s.raise_for_status()
    record = s.json()["result"][gene_id]
    return gene_id, record

if search:
    symbol = gene.strip().upper()
    if not symbol:
        st.warning("Please enter a gene symbol.")
    else:
        with st.spinner("Searching NCBI..."):
            try:
                result = ncbi_gene_search(symbol)
                if result is None:
                    st.error("No matching human gene was found. Check the gene symbol and try again.")
                else:
                    gene_id, record = result
                    st.success("NCBI search completed.")
                    st.metric("NCBI Gene ID", gene_id)
                    st.write("**Gene symbol:**", record.get("name", "Not available"))
                    st.write("**Full name:**", record.get("description", "Not available"))
                    st.write("**Organism:**", record.get("organism", {}).get("scientificname", "Not available"))
                    st.write("**Chromosome:**", record.get("chromosome", "Not available"))
                    st.write("**Map location:**", record.get("maplocation", "Not available"))
                    st.write("**NCBI summary:**")
                    st.write(record.get("summary") or "No summary supplied by NCBI.")
                    st.link_button("Open NCBI gene record", f"https://www.ncbi.nlm.nih.gov/gene/{gene_id}", use_container_width=True)
            except requests.RequestException as e:
                st.error("Could not connect to NCBI. Check your internet connection and try again.")
                st.caption(str(e))
            except (KeyError, ValueError) as e:
                st.error("NCBI returned data that the app could not read.")
                st.caption(str(e))

st.divider()
st.subheader("Research tools")
st.info("Coming next: DNA sequence analysis, GC percentage, protein information and a research-paper assistant.")

with st.expander("About this app"):
    st.write(
        "ONCOAI is an educational and research-support prototype. "
        "It retrieves public gene records from NCBI. It does not diagnose cancer, "
        "estimate an individual's cancer risk, or recommend treatment."
    )

st.markdown('<p class="small-note">Data source: NCBI Gene / NCBI E-utilities. Use scientific sources to verify research conclusions.</p>', unsafe_allow_html=True)
