import streamlit as st
import pandas as pd
import time

# 1. Configuração de Arquitetura de Games Executiva
st.set_page_config(
    page_title="LiteraQuest IA | Gamified Reading Platform", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS Premium para o Hub de Leitura
st.markdown("""
<style>
    .stApp { background-color: #0D1117 !important; color: #FFFFFF !important; }
    h1, h2, h3, h4, p, label { color: #FFFFFF !important; }
    .quest-card {
        background-color: #161B22;
        border: 2px solid #58A6FF;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- ESTRUTURA DE DADOS DO JOGADOR (SESSION STATE) ---
if "xp_total" not in st.session_state:
    st.session_state.xp_total = 0
if "moedas_holding" not in st.session_state:
    st.session_state.moedas_holding = 0
if "tempo_gasto_tela" not in st.session_state:
    st.session_state.tempo_gasto_tela = 0.0
if "diario_leitura" not in st.session_state:
    st.session_state.diario_leitura = []

# --- 📐 PAINEL LATERAL: STATUS DO AVATAR ---
st.sidebar.title("LiteraQuest AI 🛡️")
st.sidebar.caption("Ecossistema de Inovação | Desenvolvido por Kaleb Machado")
st.sidebar.markdown("---")

st.sidebar.subheader("👤 Status do Player")
st.sidebar.metric(label="Pontos de XP Acumulados", value=f"{st.session_state.xp_total} XP")
st.sidebar.metric(label="Moedas da Holding 💰", value=f"MH$ {st.session_state.moedas_holding}")

# Trava Antivício Visível na Barra Lateral
limite_diario = 60.0 # 60 minutos limite
tempo_restante = limite_diario - st.session_state.tempo_gasto_tela
st.sidebar.markdown("---")
st.sidebar.subheader("⏳ Monitor Antivício Temporal")
st.sidebar.write(f"Tempo Consumido de Tela: **{st.session_state.tempo_gasto_tela:.1f} min** / {limite_diario} min")

if tempo_restante <= 0:
    st.sidebar.error("🚨 TRAVA ANTIVÍCIO ATIVADA! Limite de tela atingido. Vá descansar a mente.")
    trava_bloqueio = True
else:
    st.sidebar.success(f"Janela de Leitura Segura: **{tempo_restante:.1f} min restantes**")
    trava_bloqueio = False

st.sidebar.markdown("---")
st.sidebar.info("**Salmo 23:1**\n\n\"O Senhor é o meu pastor, nada me faltará.\" 🙏")

# --- 📊 CONTROLADORA E INTERFACE PRINCIPAL ---
tab_missoes, tab_loja = st.tabs(["⚔️ Quests Ativas", "💎 Loja de Recompensas Bíblicas"])

with tab_missoes:
    st.title("Hub de Leitura Estratégica")
    st.subheader("Suba o nível do seu intelecto e proteja sua mente do vício digital")
    st.markdown("---")
    
    if trava_bloqueio:
        st.error("🔒 **ACESSO BLOQUEADO PELO SISTEMA ANTIVÍCIO**")
        st.markdown("""
        Seu tempo de leitura e exposição digital para este bloco foi esgotado por diretrizes de saúde mental da holding. 
        O painel de quests será reaberto na próxima janela de foco. Vá meditar nas escrituras offline!
        """)
    else:
        # QUEST DO DIA
        st.markdown("""
        <div class="quest-card">
            <h3 style="color:#58A6FF; margin:0;">📜 QUEST PRINCIPAL: A Sabedoria do Rei Salomão</h3>
            <p style="color:#8B949E; font-size:13px; margin:5px 0;">Livro de Provérbios | Recompensa: +50 XP | +10 Moedas da Holding</p>
            <p style="color:#FFFFFF; font-size:14px;">"Filho meu, ouve a instrução de teu pai e não deixes o ensino de tua mãe. Porque serão como diadema de graça para a tua cabeça e colares para o teu pescoço." (Provérbios 1:8-9)</p>
        </div>
        """, unsafe_allow_html=True)
        
        # INPUT DE LEITURA
        col_text, col_time = st.columns([2, 1])
        with col_text:
            insight = st.text_area("O que você entendeu desse ensinamento? Deixe seu relatório de leitura analítico:")
        with col_time:
            minutos_leitura = st.number_input("Quantos minutos você passou focado lendo esta quest?", min_value=1.0, value=15.0, step=5.0)
            
        if st.button("Concluir Quest e Injetar Recompensas", type="primary"):
            if not insight or len(insight) < 10:
                st.warning("Seu relatório de leitura está muito curto. Seja mais descritivo e profundo na lógica!")
            else:
                # Atualiza os dados matemáticos do jogo
                st.session_state.xp_total += 50
                st.session_state.moedas_holding += 10
                st.session_state.tempo_gasto_tela += minutos_leitura
                
                # Guarda na planilha de histórico
                st.session_state.diario_leitura.append({
                    "Quest": "A Sabedoria de Salomão",
                    "Tempo Alocado": f"{minutos_leitura} min",
                    "Status": "✅ Concluída",
                    "Insight Gerado": insight[:50] + "..."
                })
                st.success("🔥 Quest arquivada com sucesso! Recompensas computadas no seu perfil da holding.")
                st.rerun()

    # --- HISTÓRICO DE LEITURA DO AVATAR ---
    st.markdown("---")
    st.write("### 📜 Linha do Tempo de Quests Concluídas")
    if st.session_state.diario_leitura:
        df_leitura = pd.DataFrame(st.session_state.diario_leitura)
        st.dataframe(df_leitura, use_container_width=True)
    else:
        st.caption("Nenhuma leitura documentada no registro atual.")

with tab_loja:
    st.title("💎 Loja de Recompensas e Valuation Real")
    st.write("Troque suas Moedas da Holding por prêmios reais e desbloqueios de sabedoria.")
    st.markdown("---")
    
    lp1, lp2, lp3 = st.columns(3)
    
    with lp1:
        st.markdown("""
        ### 🥉 Desbloqueio Tático
        **Cost: 50 Moedas**
        * Acesso a provérbios ocultos
        * Título de 'Estudioso Júnior' no perfil
        """)
        if st.button("Comprar Upgrade 1", key="up1"):
            if st.session_state.moedas_holding >= 50:
                st.session_state.moedas_holding -= 50
                st.success("Upgrade comprado! Seu Valuation de Conhecimento subiu.")
                st.rerun()
            else:
                st.error("Moedas insuficientes na carteira.")
                
    with lp2:
        st.markdown("""
        ### 🥈 Licença Tempo Extra
        **Cost: 120 Moedas**
        * **+15 minutos de leitura segura** na Trava Antivício
        * Desbloqueio do painel de Salmos Complexos
        """)
        if st.button("Comprar Upgrade 2", key="up2", type="primary"):
            if st.session_state.moedas_holding >= 120:
                st.session_state.moedas_holding -= 120
                st.success("Licença concedida! Janela antivício expandida.")
                st.rerun()
            else:
                st.error("Moedas insuficientes na carteira.")
                
    with lp3:
        st.markdown("""
        ### 🥇 Prêmio Master Real
        **Cost: 500 Moedas**
        * **PIX Real de R$ 20,00** pago pela holding (enviado para o Pix da Mãe)
        * Certificado de Mestre da Sabedoria Bíblica
        """)
        if st.button("Falar com Kaleb Machado", key="up3"):
            if st.session_state.moedas_holding >= 500:
                st.success("Parabéns! Requisição enviada ao Corporate Desk do Kaleb.")
            else:
                st.error("Você precisa focar mais nas leituras para gerar esse lucro.")

# Botão Executivo de Reset de Cache
st.markdown("---")
if st.button("Resetar Plataforma e Zerar Cronômetro"):
    st.session_state.xp_total = 0
    st.session_state.moedas_holding = 0
    st.session_state.tempo_gasto_tela = 0.0
    st.session_state.diario_leitura = []
    st.rerun()
