import streamlit as st
import requests
from bs4 import BeautifulSoup
from docx import Document
import io

st.set_page_config(page_title="Estrattore Link per il mio amore grande", page_icon="💛")

st.title("📚 Estrattore Testo da Link")
st.subheader("per il mio amore grande 💛")
st.write("Incolla i link qui sotto (uno per riga), clicca il pulsante e scarica i file elaborati.")

# Area di testo dove lei incollerà i link
urls_input = st.text_area("Lista dei link:", height=150)

if st.button("🚀 Avvia Estrazione"):
    if not urls_input.strip():
        st.warning("Inserisci almeno un link prima di iniziare!")
    else:
        # Pulisce la lista dei link e rimuove righe vuote
        urls = [url.strip() for url in urls_input.split('\n') if url.strip()]
        
        doc = Document()
        report_errori = []
        
        # Barra di caricamento per darle un feedback visivo
        progress_bar = st.progress(0)
        
        for i, url in enumerate(urls):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                titolo = soup.title.string if soup.title else url
                doc.add_heading(titolo.strip(), level=1)
                
                paragrafi = soup.find_all('p')
                for p in paragrafi:
                    testo = p.get_text().strip()
                    if testo:  
                        doc.add_paragraph(testo)
                        
                doc.add_page_break()
                
            except Exception as e:
                report_errori.append(f"- {url}\n  Errore: {e}")
                
            # Aggiorna la barra di caricamento
            progress_bar.progress((i + 1) / len(urls))
            
        st.success("Estrazione completata!")

        # 1. Prepara il file Word per il download (in memoria)
        word_buffer = io.BytesIO()
        doc.save(word_buffer)
        word_buffer.seek(0)
        
        st.download_button(
            label="📄 Scarica il Documento Word",
            data=word_buffer,
            file_name="testo_estratto.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
        # 2. Prepara il Report (se ci sono errori o se vuoi confermare il successo)
        report_text = "REPORT ESTRAZIONE\n" + "="*20 + "\n\n"
        if report_errori:
            report_text += "Si sono verificati problemi con questi link:\n"
            report_text += "\n".join(report_errori)
        else:
            report_text += "Tutti i link sono stati estratti con successo!"
            
        st.download_button(
            label="📊 Scarica il Report",
            data=report_text,
            file_name="report_estrazione.txt",
            mime="text/plain"
        )