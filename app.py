import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np # Ses üretimi için gerekli

# --- YARDIMCI FONKSİYONLAR ---
def _safe_rerun():
    if hasattr(st, "rerun"): st.rerun()
    else: st.experimental_rerun()

def _build_graph():
    # k=4 yaptık, Watts-Strogatz için çift sayı şart!
    G = nx.watts_strogatz_graph(15, 4, 0.3, seed=42)
    cc = nx.closeness_centrality(G)
    # En merkezi düğümü seç
    true_zero = sorted(cc.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
    return G, true_zero

def run():
    st.title("🕵️‍♂️ Vaka 1: Hayalet Protokol (Ağlar)")

    # State Init
    if "math_mode" not in st.session_state: st.session_state["math_mode"] = False
    if "G" not in st.session_state:
        G, true_zero = _build_graph()
        st.session_state["G"] = G
        st.session_state["true_zero"] = true_zero

    # Hikaye / Matematik Geçişi
    if not st.session_state["math_mode"]:
        st.markdown("**Görev:** Virüsün kaynağı olan 'Ana Sunucuyu' bul. Yanlış sunucuyu kapatırsan hastane sistemi çöker!")
        st.info("💡 İpucu: Hangi nokta diğerlerine en hızlı ulaşır (En Merkezi)?")
    else:
        st.markdown(r"### 📐 MATEMATİKSEL YÜZLEŞME: Closeness Centrality$$ C(x) = \frac{1}{\sum_{y} d(x, y)} $$")

    col1, col2 = st.columns([2, 1])

    with col1:
        G = st.session_state["G"]
        pos = nx.spring_layout(G, seed=42)
        fig, ax = plt.subplots(figsize=(6, 4))
        nx.draw(G, pos, with_labels=True, node_color="skyblue", edge_color="gray", node_size=500, ax=ax)
        st.pyplot(fig)

    with col2:
        st.subheader("📡 Sunucu Analizi")
        guess = st.number_input("Şüpheli ID:", min_value=0, max_value=14, step=1)

        if st.button("Sistemi Tara"):
            if int(guess) == int(st.session_state["true_zero"]):
                # --- BAŞARI BLOĞU ---
                st.success("BAŞARILI! Kaynak İzole Edildi.")
                st.balloons()
                st.caption("✅ **Gerçek Dünya:** Bot hesapları bulmak için de bu algoritma kullanılır.")
                
                # Envanter
                st.session_state["inventory_audio_file"] = "Project_Moriarty_Log.wav"
                st.toast("🎒 Envanter: Ses Dosyası")

                # Ses Efekti (White Noise + 42Hz)
                sample_rate = 44100
                t = np.linspace(0, 2, 2 * sample_rate, endpoint=False)
                audio_data = np.sin(2 * np.pi * 42 * t) * 0.1 + np.random.normal(0, 0.5, t.shape)
                st.audio(audio_data, sample_rate=sample_rate)
                st.caption("🔊 Ele Geçirilen Dosya (Çok Cızırtılı!)")

            else:
                # --- HATA/ETİK BLOĞU ---
                st.error("KRİTİK HATA: Yanlış Sunucuyu Kapattınız!")
                st.warning("""
                **Saha Raporu:** Kapattığınız sunucu **Londra Şehir Hastanesi** veri tabanıydı. 
                Sistem çöktü. Ağ analizinde 'False Positive' (Yanlış Alarm) hayati risk taşır.
                """)

    st.divider()
    if st.button("🔴 Kırmızı Hap: Analojiyi Kır"):
        st.session_state["math_mode"] = not st.session_state["math_mode"]
        _safe_rerun()

    with st.expander("🛠️ Reality Check"):
        st.write("**Soru:** `p=0.0` olursa ağ neye benzer?")
        ans = st.radio("Cevap:", ["Kaos", "Düzenli Çember", "Yıldız"])
        if ans == "Düzenli Çember": st.success("Doğru!"); 
        elif ans: st.error("Yanlış.")


def main():
    run()


if __name__ == "__main__":
    main()
