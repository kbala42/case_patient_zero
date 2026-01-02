import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

# Sayfa Ayarları
st.set_page_config(page_title="Vaka: Sıfırıncı Hasta", layout="wide")

st.title("🕵️‍♂️ Vaka: Görünmez Ağ (Sıfırıncı Hasta)")
st.markdown("""
**Sherlock'un Notu:** "Bir hastalığı (veya bilgiyi) durdurmak istiyorsan, nereden başladığını bulmalısın. 
Gözlerinle bakarsan karmaşa görürsün, matrislerle bakarsan yolu görürsün."
""")

# --- SOL PANEL: AYARLAR (LABORATUVAR) ---
with st.sidebar:
    st.header("🔬 Laboratuvar Ayarları")
    num_nodes = st.slider("İnsan Sayısı (Düğüm)", 10, 50, 20)
    infection_prob = st.slider("Bulaşma İhtimali", 0.1, 1.0, 0.5)
    steps = st.slider("Zaman Adımı (Gün)", 1, 5, 2)
    
    if st.button("Simülasyonu Başlat / Sıfırla"):
        st.session_state['network'] = None
        st.session_state['zero_patient'] = None

# --- FONKSİYONLAR ---

def create_social_network(n):
    # Rastgele bir sosyal ağ oluştur (Watts-Strogatz modeli - "Küçük Dünya" teorisi)
    # Bu model gerçek insan ilişkilerini en iyi simüle eden modeldir.
    G = nx.watts_strogatz_graph(n, k=4, p=0.1)
    return G

def spread_virus(G, source, steps, prob):
    # Virüsü yayma simülasyonu
    infected = {source}
    current_spreaders = {source}
    
    history = [list(infected)] # Her adımda kimler hasta oldu kaydet
    
    for _ in range(steps):
        new_infected = set()
        for person in current_spreaders:
            # Komşularına bak
            neighbors = list(G.neighbors(person))
            for neighbor in neighbors:
                if neighbor not in infected:
                    if random.random() < prob:
                        new_infected.add(neighbor)
        
        infected.update(new_infected)
        current_spreaders = new_infected # Sadece yeni hastalar bulaştırır (basit model)
        history.append(list(infected))
    
    return list(infected), history

# --- ANA AKIŞ ---

# 1. Ağı Oluştur (Eğer yoksa)
if 'network' not in st.session_state or st.session_state['network'] is None:
    G = create_social_network(num_nodes)
    zero_patient = random.choice(list(G.nodes()))
    
    st.session_state['network'] = G
    st.session_state['zero_patient'] = zero_patient

G = st.session_state['network']
true_zero = st.session_state['zero_patient']

# 2. Virüsü Yay
infected_list, history = spread_virus(G, true_zero, steps, infection_prob)

# --- GÖRSELLEŞTİRME ---

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🏙️ Şehrin Kuşbakışı Görünümü")
    
    fig, ax = plt.subplots(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42) # Sabit düzen
    
    # Sağlıklıları Çiz
    healthy = [n for n in G.nodes() if n not in infected_list]
    nx.draw_networkx_nodes(G, pos, nodelist=healthy, node_color='lightblue', node_size=300, label="Sağlıklı")
    
    # Hastaları Çiz (Kırmızı)
    nx.draw_networkx_nodes(G, pos, nodelist=infected_list, node_color='red', node_size=300, label="Enfekte")
    
    # Bağlantıları Çiz
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    
    # Etiketleri Çiz
    nx.draw_networkx_labels(G, pos, font_size=10)
    
    plt.legend(["Sağlıklı", "Enfekte"])
    st.pyplot(fig)

with col2:
    st.subheader("🕵️‍♂️ Dedektif Paneli")
    st.write(f"Toplam Nüfus: {num_nodes}")
    st.write(f"Enfekte Olanlar: {len(infected_list)}")
    
    st.info("Kırmızı düğümlere bak. Sence bu salgın HANGİSİNDEN başladı?")
    
    guess = st.selectbox("Tahminini Seç (Düğüm Numarası):", sorted(infected_list))
    
    if st.button("Tahmini Kontrol Et"):
        if guess == true_zero:
            st.success(f"TEBRİKLER! Sherlock gibi düşündün. Kaynak: {true_zero}")
            st.balloons()
        else:
            st.error(f"Yanlış. Gerçek kaynak {true_zero} idi. Ama pes etme Watson!")
            
    # --- İPUCU KUTUSU (Sezgiselden Matematiğe Geçiş) ---
    with st.expander("💡 İpucu: Mühendis Gibi Düşün (Matematiksel Analiz)"):
        st.write("""
        Gözle bulmak zor değil mi? Bilgisayarlar bunu nasıl yapar?
        **'Merkezilik' (Centrality)** ölçeriz.
        
        Enfekte grubun tam ortasında kim var? Enfekte olan arkadaşlarına en yakın olan kişi kim?
        """)
        
        # Basit bir matematiksel ipucu hesaplama
        # Sadece enfekte olanlardan oluşan bir alt-grafik (subgraph) oluştur
        sub_G = G.subgraph(infected_list)
        # Closeness Centrality (Yakınlık Merkeziliği) hesapla
        centrality = nx.closeness_centrality(sub_G)
        likely_suspect = max(centrality, key=centrality.get)
        
        st.write(f"📊 Matematiksel Analiz (Algoritma) diyor ki:")
        st.code(f"En Olası Şüpheli: {likely_suspect}")
        st.write("(Not: Bu algoritma her zaman %100 bilmez, ama en iyi tahmini yapar.)")