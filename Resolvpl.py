import streamlit as st
import pandas as pd
import random

# 1. Configuração de Arquitetura de Games Executiva
st.set_page_config(
    page_title="LiteraQuest IA | Advanced Evolution", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 UI/UX REALISTA: TEMA ESCURO E PALETA DE ANALISTA LÓGICO
st.markdown("""
<style>
    .stApp { background-color: #0D1117 !important; color: #FFFFFF !important; }
    h1, h2, h3, h4, p, label, .stMarkdown { color: #FFFFFF !important; }
    .stTextInput input, .stTextArea textarea, .stSelectbox div {
        background-color: #161B22 !important; color: #FFFFFF !important;
        border: 1px solid #30363D !important; border-radius: 6px !important;
    }
    .quest-card {
        background-color: #161B22; border: 2px solid #58A6FF;
        padding: 20px; border-radius: 12px; margin-bottom: 20px;
    }
    .avatar-preview {
        background-color: #161B22; border: 1px dashed #58A6FF;
        padding: 10px; border-radius: 8px; text-align: center; margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 📚 BANCO DE DADOS DE QUESTS BÍBLICAS ---
QUESTS_BANCO = [
    {
        "id": 1,
        "titulo": "📜 QUEST 1: A Sabedoria de Salomão",
        "versiculo": '"Filho meu, ouve a instrução de teu pai e não deixes o ensino de tua mãe..." (Provérbios 1:8)',
        "pergunta": "O que Provérbios 1:8 dita para o filho não abandonar?",
        "opcoes": ["A fofoca da sala de aula", "O ensino de tua mãe", "Os jogos de computador", "A busca por status da manada"],
        "correta": "O ensino de tua mãe",
        "xp": 50, "moedas": 10
    },
    {
        "id": 2,
        "titulo": "🛡️ QUEST 2: A Âncora do Pastor",
        "versiculo": '"O Senhor é o meu pastor, nada me faltará." (Salmo 23:1)',
        "pergunta": "Qual é a consequência lógica e direta descrita no Salmo?",
        "opcoes": ["Ficar muito cansado na escola", "Nada me faltará", "Ganhar muitos pontos de XP", "Vencer todas as intrigas"],
        "correta": "Nada me faltará",
        "xp": 60, "moedas": 15
    },
    {
        "id": 3,
        "titulo": "⚔️ QUEST 3: A Armadura do Coração",
        "versiculo": '"Sobre tudo o que se deve guardar, guarda o teu coração, porque dele procedem as fontes da vida." (Provérbios 4:23)',
        "pergunta": "Por que o coração deve ser blindado e guardado acima de tudo?",
        "opcoes": ["Porque dele procedem as fontes da vida", "Para tirar notas altas na prova", "Para impressionar o playboy da sala", "Para programar sem interrupções"],
        "correta": "Porque dele procedem as fontes da vida",
        "xp": 70, "moedas": 20
    }
]

# --- ⚙️ INICIALIZAÇÃO DE VARIÁVEIS DE ESTADO (SESSION STATE) ---
if "xp_total" not in st.session_state: st.session_state.xp_total = 0
if "moedas_holding" not in st.session_state: st.session_state.moedas_holding = 0
if "tempo_gasto_tela" not in st.session_state: st.session_state.tempo_gasto_tela = 0.0
if "diario_leitura" not in st.session_state: st.session_state.diario_leitura = []
if "quest_atual_idx" not in st.session_state: st.session_state.quest_atual_idx = 0

# Customização estilo Roblox salvas no estado
if "avatar_chapeu" not in st.session_state: st.session_state.avatar_chapeu = "Nenhum"
if "avatar_armadura" not in st.session_state: st.session_state.avatar_armadura = "Traje Inicial"
if "avatar_item" not in st.session_state: st.session_state.avatar_item = "Nenhum"

# --- 📐 BARRA LATERAL: CUSTOMIZAÇÃO DE AVATAR (ESTILO ROBLOX) E STATUS ---
st.sidebar.title("LiteraQuest IA 🛡️")
st.sidebar.caption("Ecossistema de Inovação | Kaleb Machado")
st.sidebar.markdown("---")

menu_navegacao = st.sidebar.selectbox("Navegar pelo Painel:", ["⚔️ Quests Ativas", "💎 Loja de Recompensas"])
st.sidebar.markdown("---")

# 👤 CENTRAL DE CUSTOMIZAÇÃO DO PERSONAGEM (ROBLOX STYLE)
st.sidebar.subheader("🦊 Customizar seu Avatar")
st.session_state.avatar_chapeu = st.sidebar.selectbox(
    "Chapéu / Elmo:", 
    ["Nenhum", "Capacete de Cavaleiro", "Coroa de Salomão", "Boné Cyberpunk"],
    index=["Nenhum", "Capacete de Cavaleiro", "Coroa de Salomão", "Boné Cyberpunk"].index(st.session_state.avatar_chapeu)
)
st.session_state.avatar_armadura = st.sidebar.selectbox(
    "Armadura / Traje:", 
    ["Traje Inicial", "Cota de Malha Medieval", "Manto de Profeta", "Armadura de Kevlar"],
    index=["Traje Inicial", "Cota de Malha Medieval", "Manto de Profeta", "Armadura de Kevlar"].index(st.session_state.avatar_armadura)
)
st.session_state.avatar_item = st.sidebar.selectbox(
    "Item de Mão / Arma:", 
    ["Nenhum", "Espada da Verdade", "Pergaminho Antigo", "Notebook da Holding"],
    index=["Nenhum", "Espada da Verdade", "Pergaminho Antigo", "Notebook da Holding"].index(st.session_state.avatar_item)
)

# Bloco Visual do Equipamento do Player
st.sidebar.markdown('<div class="avatar-preview"><b>EQUIPAMENTO ATUAL</b><br>'
                   f'🎩 {st.session_state.avatar_chapeu}<br>'
                   f'🛡️ {st.session_state.avatar_armadura}<br>'
                   f'⚔️ {st.session_state.avatar_item}</div>', unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Status do Perfil")
st.sidebar.metric(label="Pontos de XP", value=f"{st.session_state.xp_total} XP")
st.sidebar.metric(label="Moedas da Holding", value=f"MH$ {st.session_state.moedas_holding}")

# Trava Antivício Física
limite_diario = 60.0
tempo_restante = limite_diario - st.session_state.tempo_gasto_tela
if tempo_restante <= 0:
    st.sidebar.error("🚨 TRAVA ANTIVÍCIO ATIVADA!")
    trava_bloqueio = True
else:
    st.sidebar.success(f"Foco Seguro: {tempo_restante:.1f} min")
    trava_bloqueio = False

# --- 📊 EXECUÇÃO PRINCIPAL DO ECOSSISTEMA ---
if menu_navegacao == "⚔️ Quests Ativas":
    st.title("Hub de Leitura Estratégica 📚")
    st.caption("Resolução de problemas através da absorção analítica de versículos")
    st.markdown("---")
    
    if trava_bloqueio:
        st.error("🔒 **ACESSO BLOQUEADO PELO SISTEMA ANTIVÍCIO**")
        st.markdown("Seu tempo limite de tela expirou por diretrizes de saúde. Vá descansar a mente.")
    else:
        # Puxa a quest atual baseada no índice do banco de dados
        q_idx = st.session_state.quest_atual_idx % len(QUESTS_BANCO)
        quest = QUESTS_BANCO[q_idx]
        
        # Renderização do Card de Quest Dinâmico
        st.markdown(f"""
        <div class="quest-card">
            <h3 style="color:#58A6FF; margin:0;">{quest['titulo']}</h3>
            <p style="color:#8B949E; font-size:13px; margin:5px 0;">Recompensa: +{quest['xp']} XP | +{quest['moedas']} Moedas</p>
            <p style="color:#FFFFFF; font-size:15px; margin-top:10px;">{quest['versiculo']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # ARTÍMANHA COGNITIVA: Sistema de 4 Escolhas Prontas
        st.write("### ⚔️ Desafio Lógico da Quest")
        resposta_usuario = st.radio("Escolha a alternativa correta baseada no versículo acima:", quest["opcoes"])
        
        col_input, col_cronometro = st.columns(2)
        with col_input:
            insight = st.text_area("Insira o seu relatório analítico de absorção (mínimo 10 caracteres):")
        with col_time:
            minutos_leitura = st.number_input("Minutos de foco real dedicados:", min_value=1.0, value=15.0, step=5.0)
            
        if st.button("Submeter Resposta e Atualizar Ledger", type="primary", use_container_width=True):
            if not insight or len(insight) < 10:
                st.warning("Relatório de leitura inválido ou muito curto para análise.")
            else:
                if resposta_usuario == quest["correta"]:
                    st.session_state.xp_total += quest["xp"]
                    st.session_state.moedas_holding += quest["moedas"]
                    st.session_state.tempo_gasto_tela += minutos_leitura
                    
                    st.session_state.diario_leitura.append({
                        "Quest": quest["titulo"],
                        "Resultado": "✅ Acertou",
                        "Tempo": f"{minutos_leitura} min",
                        "Equipamento": st.session_state.avatar_item
                    })
                    st.success(f"🔥 Resposta Correta! +{quest['xp']} XP injetados.")
                    st.session_state.quest_atual_idx += 1
                    st.rerun()
                else:
                    st.error("❌ Resposta Incorreta! A lógica do versículo foi violada. Releia com atenção.")

    # Tabela de logs de auditoria
    st.markdown("---")
    st.write("### 📜 Histórico de Desempenho Tático")
    if st.session_state.diario_leitura:
        st.dataframe(pd.DataFrame(st.session_state.diario_leitura), use_container_width=True)
    else:
        st.caption("Nenhum bloco de dados processado.")

elif menu_navegacao == "💎 Loja de Recompensas":
    st.title("💎 Loja de Recompensas e Valuation Real")
    st.write("Troque suas Moedas da Holding por prêmios reais e vantagens de tempo.")
    st.markdown("---")
    
    lp1, lp2, lp3 = st.columns(3)
    with lp1:
        st.write("### 🥉 Item Comum: Elmo Lendário")
        st.caption("Custo: 30 Moedas")
        if st.button("Adquirir na Loja", key="up1", use_container_width=True):
            if st.session_state.moedas_holding >= 30:
                st.session_state.moedas_holding -= 30
                st.success("Item comprado! Vá no menu lateral para equipar.")
                st.rerun()
            else:
                st.error("Fundos insuficientes.")
            
    with lp2:
        st.write("### 🥈 Licença Tempo Extra")
        st.caption("Custo: 100 Moedas")
        if st.button("Comprar Licença", key="up2", type="primary", use_container_width=True):
            if st.session_state.moedas_holding >= 100:
                st.session_state.moedas_holding -= 100
                st.session_state.tempo_gasto_tela = max(0.0, st.session_state.tempo_gasto_tela - 20.0)
                st.success("Trava Antivício expandida em +20 minutos!")


