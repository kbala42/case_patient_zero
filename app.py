import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random

def run():
    st.title("🕵️‍♂️ Vaka 1: Hayalet Protokol (Ağlar)")
    
    # --- HİKAYE MODU ---
    if 'math_mode' not in st.session_state:
        st.session_state['math_mode'] = False

    if not st.session_state['math_mode']:
        st.markdown("""
        **Görev:** Londra sunucularına bir virüs bulaştı. Virüsün yayıldığı "Ana Sunucuyu" (Patient Zero) bulmalısın.
        **Ödül:** Eğer ana sunucuyu bulursan, virüsün kaynak kodundaki **Gizli Ses Kaydını (.wav)** ele geçireceğiz.
        """)
        st.info("💡 İpucu: Hangi nokta diğerlerine en çok hükmediyor?")
    else:
        st.markdown("""
        ### 📐 MATEMATİKSEL YÜZLEŞME
        **Konu:** Çizge Teorisi (Graph Theory) - Merkezilik (Centrality)
        
        Mennan Usta'nın "Çeşme Başı" dediği şey, matematikte **Closeness Centrality** formülüdür:
        
        $$ C(x) = \\frac{1}{\\sum_{y} d(x, y)} $$
        
        * $d(x, y)$: $x$ düğümü ile $y$ düğümü arasındaki en kısa yol.
        * Bir düğüm diğerlerine ne kadar "yakınsa", bilgi (veya virüs) o kadar hızlı yayılır.
        """)

    # --- SİMÜLASYON ---
    col1, col2 = st.columns([2, 1])

    with col1:
        # Ağ Oluşturma
        if 'G' not in st.session_state:
            st.session_state['G'] = nx.watts_strogatz_graph(15, 3, 0.3, seed=42)
            # Rastgele bir düğümü "Hasta Sıfır" yap ama söyleme
            st.session_state['true_zero'] = 4 # Sabitliyoruz ki senaryo çalışsın

        G = st.session_state['G']
        pos = nx.spring_layout(G, seed=42)
        
        # Çizim
        fig, ax = plt.subplots(figsize=(6, 4))
        nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=500)
        # Gerçek hastayı kırmızı yap (Sadece analizden sonra veya hileyle görünür normalde)
        # Eğitim amaçlı gizli tutuyoruz.
        st.pyplot(fig)

    with col2:
        st.subheader("📡 Sunucu Analizi")
        guess = st.number_input("Şüpheli Sunucu ID'si:", min_value=0, max_value=14, step=1)
        
        if st.button("Sistemi Tara"):
            if guess == st.session_state['true_zero']:
                st.success("BAŞARILI! Kaynak Sunucu Tespit Edildi.")
                st.balloons()
                
                # --- ENVANTER GÜNCELLEME (HİKAYE BAĞLANTISI) ---
                st.session_state['inventory_audio_file'] = "Project_Moriarty_Log.wav"
                st.toast("🎒 Envantere Eklendi: Project_Moriarty_Log.wav")
                st.write("📂 **Bulunan Dosya:** Bu ses kaydı çok gürültülü. Vaka 2'de bunu temizlemen gerekecek.")
                
            else:
                st.error("HATA: Bu sunucu temiz. Virüs buradan yayılmamış.")

    st.divider()

    # --- ANALOJİYİ KIR BUTONU ---
    if st.button("🔴 Kırmızı Hap: Analojiyi Kır (Matematiği Göster/Gizle)"):
        st.session_state['math_mode'] = not st.session_state['math_mode']
        st.rerun()
        
    # --- REALITY CHECK (KOD SORGUSU) ---
    with st.expander("🛠️ Kod Müdahalesi (Reality Check)"):
        st.write("**Soru:** Eğer `nx.watts_strogatz_graph` fonksiyonundaki `p=0.3` değerini `p=0.0` yaparsan ağın şekli neye döner?")
        answer = st.radio("Cevabını Seç:", ["Tamamen Rastgele (Kaos)", "Kusursuz Bir Çember (Düzen)", "Yıldız Şekli"])
        
        if answer == "Kusursuz Bir Çember (Düzen)":
            st.success("Doğru! p=0 olasılığı, hiç rastgele bağ olmadığını, herkesin sadece yanındakiyle konuştuğunu gösterir.")
        elif answer:
            st.error("Yanlış. Watts-Strogatz modelinde p, rastgelelik katsayısıdır. 0 demek, sıfır rastgelelik demektir.")

if __name__ == "__main__":
    run()
