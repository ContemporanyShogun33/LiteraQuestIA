import streamlit as st
import pandas as pd

# 1. Configuração de Arquitetura de Games Executiva
st.set_page_config(
    page_title="LiteraQuest IA | Roblox Engine", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 UI/UX DE ANALISTA LÓGICO: MODO ESCURO E DETALHES AZUL NEON
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
    .canvas-container {
        border: 2px solid #58A6FF; border-radius: 12px;
        background-color: #161B22; padding: 10px; text-align: center;
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
        "correta": "O ensino de tua mãe", "xp": 50, "moedas": 10
    },
    {
        "id": 2,
        "titulo": "🛡️ QUEST 2: A Âncora do Pastor",
        "versiculo": '"O Senhor é o meu pastor, nada me faltará." (Salmo 23:1)',
        "pergunta": "Qual é a consequência lógica e direta descrita no Salmo?",
        "opcoes": ["Ficar muito cansado na escola", "Nada me faltará", "Ganhar muitos pontos de XP", "Vencer todas as intrigas"],
        "correta": "Nada me faltará", "xp": 60, "moedas": 15
    }
]

# --- ⚙️ INICIALIZAÇÃO DE VARIÁVEIS DE ESTADO (SESSION STATE) ---
if "xp_total" not in st.session_state: st.session_state.xp_total = 0
if "moedas_holding" not in st.session_state: st.session_state.moedas_holding = 0
if "tempo_gasto_tela" not in st.session_state: st.session_state.tempo_gasto_tela = 0.0
if "diario_leitura" not in st.session_state: st.session_state.diario_leitura = []
if "quest_atual_idx" not in st.session_state: st.session_state.quest_atual_idx = 0

# Estado estável de customização do avatar
if "item_chapeu" not in st.session_state: st.session_state.item_chapeu = "Boné Cyber"
if "item_traje" not in st.session_state: st.session_state.item_traje = "Camisa Floral"
if "item_mao" not in st.session_state: st.session_state.item_mao = "Notebook"

# --- 📐 BARRA LATERAL: CUSTOMIZAÇÃO DO AVATAR E STATUS ---
st.sidebar.title("LiteraQuest AI 🛡️")
st.sidebar.caption("Ecossistema de Inovação | Kaleb Machado")
st.sidebar.markdown("---")

menu_navegacao = st.sidebar.selectbox("Navegar pelo Painel:", ["⚔️ Quests Ativas", "💎 Loja de Recompensas"])
st.sidebar.markdown("---")

# 🦊 PAINEL ROBLOX: AL Altera o visual do boneco em tempo real
st.sidebar.subheader("🦊 Customizar Avatar")
st.session_state.item_chapeu = st.sidebar.selectbox("Acessório de Cabeça:", ["Nenhum", "Boné Cyber", "Coroa de Ouro", "Elmo de Ferro"], index=["Nenhum", "Boné Cyber", "Coroa de Ouro", "Elmo de Ferro"].index(st.session_state.item_chapeu))
st.session_state.item_traje = st.sidebar.selectbox("Camisa / Traje:", ["Padrão", "Camisa Floral", "Manto Branco", "Armadura Azul"], index=["Padrão", "Camisa Floral", "Manto Branco", "Armadura Azul"].index(st.session_state.item_traje))
st.session_state.item_mao = st.sidebar.selectbox("Equipar Item de Mão:", ["Nenhum", "Notebook", "Espada Laser", "Pergaminho"], index=["Nenhum", "Notebook", "Espada Laser", "Pergaminho"].index(st.session_state.item_mao))

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Status do Perfil")
st.sidebar.metric(label="Pontos de XP", value=f"{st.session_state.xp_total} XP")
st.sidebar.metric(label="Moedas da Holding", value=f"MH$ {st.session_state.moedas_holding}")

# Trava Antivício
limite_diario = 60.0
tempo_restante = limite_diario - st.session_state.tempo_gasto_tela
trava_bloqueio = tempo_restante <= 0

st.sidebar.markdown("---")
st.sidebar.info("**Salmo 23:1**\n\n\"O Senhor é o meu pastor, nada me faltará.\" 🙏")

# --- 🦾 MOTOR GRÁFICO ROBLOX ENGINE (HTML5 CANVAS INTERATIVO + LOOP DE ANIMAÇÃO) ---
# Cores dinâmicas injetadas via Python diretamente no esqueleto JavaScript do navegador
cor_tronco = "#0056B3" if st.session_state.item_traje == "Armadura Azul" else ("#D1E8FF" if st.session_state.item_traje == "Manto Branco" else ("#FF4136" if st.session_state.item_traje == "Camisa Floral" else "#333333"))
cor_chapeu = "#FFDC00" if st.session_state.item_chapeu == "Coroa de Ouro" else ("#AAAAAA" if st.session_state.item_chapeu == "Elmo de Ferro" else ("#0074D9" if st.session_state.item_chapeu == "Boné Cyber" else "rgba(0,0,0,0)"))

html_motor_roblox = f"""
<div style="text-align: center;">
    <canvas id="robloxStage" width="400" height="260" style="background:#161B22; border-radius:10px;"></canvas>
    <script>
        const canvas = document.getElementById('robloxStage');
        const ctx = canvas.getContext('2d');
        let tick = 0;

        function renderLoop() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            tick += 0.15; // Velocidade da caminhada

            // Lógica matemática do balanço das pernas e braços (Efeito Andando do Roblox)
            let balanco_bracos = Math.sin(tick) * 20;
            let balanco_pernas = Math.cos(tick) * 25;

            ctx.save();
            ctx.translate(canvas.width / 2, canvas.height / 2 + 10);

            // 1. PERNA ESQUERDA (Bloquinhos característicos do Roblox)
            ctx.save();
            ctx.translate(-14, 25);
            ctx.rotate(balanco_pernas * Math.PI / 180);
            ctx.fillStyle = "#111111";
            ctx.fillRect(-10, 0, 18, 45);
            ctx.restore();

            // 2. PERNA DIREITA
            ctx.save();
            ctx.translate(14, 25);
            ctx.rotate(-balanco_pernas * Math.PI / 180);
            ctx.fillStyle = "#111111";
            ctx.fillRect(-8, 0, 18, 45);
            ctx.restore();

            // 3. TRONCO QUADRADÃO ESTILO ROBLOX
            ctx.fillStyle = "{cor_tronco}";
            ctx.fillRect(-24, -40, 48, 65);

            // 4. CABEÇA ROBLOX CLÁSSICA (Amarela e quadrada com juntas de pescoço)
            ctx.fillStyle = "#FFD1A4";
            ctx.fillRect(-16, -76, 32, 32);
            
            // Rostinho sorridente clássico do Roblox
            ctx.fillStyle = "#000000";
            ctx.fillRect(-10, -64, 4, 4); // Olho esquerdo
            ctx.fillRect(6, -64, 4, 4);  // Olho direito
            ctx.beginPath();
            ctx.arc(0, -52, 6, 0, Math.PI); // Sorriso
            ctx.stroke();

            // CUSTOMIZAÇÃO DO CHAPÉU
            if ("{st.session_state.item_chapeu}" !== "Nenhum") {{
                ctx.fillStyle = "{cor_chapeu}";
                ctx.fillRect(-20, -84, 40, 10); // Base do chapéu
                ctx.fillRect(-12, -96, 24, 14); // Topo do chapéu
            }}

            // 5. BRAÇO ESQUERDO (Balançando)
            ctx.save();
            ctx.translate(-34, -40);
            ctx.rotate(-balanco_bracos * Math.PI / 180);
            ctx.fillStyle = "#FFD1A4";
            ctx.fillRect(-10, 0, 16, 50);
            ctx.restore();

            // 6. BRAÇO DIREITO E EQUIPAMENTO DE MÃO
            ctx.save();
            ctx.translate(34, -40);
            ctx.rotate(balanco_bracos * Math.PI / 180);
            ctx.fillStyle = "#FFD1A4";
            ctx.fillRect(-6, 0, 16, 50);

            // Item de Mão renderizado exatamente na ponta do braço
            if ("{st.session_state.item_mao}" === "Notebook") {{
                ctx.fillStyle = "#58A6FF";
                ctx.fillRect(2, 35, 20, 15);
            }} else if ("{st.session_state.item_mao}" === "Espada Laser") {{
                ctx.fillStyle = "#FF4136";
                ctx.fillRect(4, 20, 6, 40);
            }} else if ("{st.session_state.item_mao}" === "Pergaminho") {{
                ctx.fillStyle = "#FFDC00";
                ctx.fillRect(2, 30, 12, 22);
            }}
            ctx.restore();

            ctx.restore();
            requestAnimationFrame(renderLoop);
        }}
        renderLoop();
    </script>
</div>
"""

# --- 📊 EXECUÇÃO PRINCIPAL DO ECOSSISTEMA ---
if menu_navegacao == "⚔️ Quests Ativas":
    st.title("Hub de Leitura Estratégica 📚")
    
    c_titulo, c_canvas = st.columns([1.3, 1])
    with c_titulo:
        st.caption("Resolução de problemas através da absorção analítica de versículos")
        st.write("### 🤖 Seu Personagem Roblox")
        st.info("O motor gráfico detectou o seu avatar em movimento contínuo na tela. Altere os trajes e itens no painel do lado para ver a atualização instantânea!")
    with c_canvas:
        # Contêiner robusto do Motor do Avatar
        st.markdown('<div class="canvas-container">', unsafe_allow_html=True)
        st.components.v1.html(html_motor_roblox, height=270)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown("---")
    
    if trava_bloqueio:
        st.error("🔒 **ACESSO BLOQUEADO PELO SISTEMA ANTIVÍCIO**")
    else:
        q_idx = st.session_state.quest_atual_idx % len(QUESTS_BANCO)
        quest = QUESTS_BANCO[q_idx]
        
        st.markdown(f"""
        <div class="quest-card">
            <h3 style="color:#58A6FF; margin:0;">{quest['titulo']}</h3>
            <p style="color:#8B949E; font-size:13px; margin:5px 0;">Recompensa: +{quest['xp']} XP | +{quest['moedas']} Moedas</p>
            <p style="color:#FFFFFF; font-size:15px; margin-top:10px;">{quest['versiculo']}</p>
        </div>
        """, unsafe_allow_html=True)
        
