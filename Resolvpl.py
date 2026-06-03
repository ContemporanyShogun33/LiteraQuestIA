import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. Configuração de Arquitetura de Games Executiva
st.set_page_config(
    page_title="LiteraQuest IA | 3D Avatar Engine", 
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
    .canvas-container {
        border: 2px solid #58A6FF;
        border-radius: 12px;
        background-color: #161B22;
        padding: 10px;
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

# --- ⚙️ INICIALIZAÇÃO DE VARIÁVEIS DE ESTADO ---
if "xp_total" not in st.session_state: st.session_state.xp_total = 0
if "moedas_holding" not in st.session_state: st.session_state.moedas_holding = 0
if "tempo_gasto_tela" not in st.session_state: st.session_state.tempo_gasto_tela = 0.0
if "diario_leitura" not in st.session_state: st.session_state.diario_leitura = []
if "quest_atual_idx" not in st.session_state: st.session_state.quest_atual_idx = 0

# Configurações de Rigging salvas na sessão
if "rig_type" not in st.session_state: st.session_state.rig_type = "R6 (Clássico)"
if "flex_juntas" not in st.session_state: st.session_state.flex_juntas = 0

# --- 📐 BARRA LATERAL: ENGINES DE RIGGING E STATUS ---
st.sidebar.title("LiteraQuest AI 🛡️")
st.sidebar.caption("Ecossistema de Inovação | Kaleb Machado")
st.sidebar.markdown("---")

menu_navegacao = st.sidebar.selectbox("Navegar pelo Painel:", ["⚔️ Quests Ativas", "💎 Loja de Recompensas"])
st.sidebar.markdown("---")

# 🦊 CONFIGURAÇÃO DO RIG DO BONECO (ESTILO IMAGEM ROBLOX)
st.sidebar.subheader("🦾 Mecânica do Rig 3D")
st.session_state.rig_type = st.sidebar.radio(
    "Escolha a estrutura do esqueleto:",
    ["R6 (Clássico)", "R15 (Articulado)"]
)

# Slider para dobrar os braços/pernas se for R15
if st.session_state.rig_type == "R15 (Articulado)":
    st.session_state.flex_juntas = st.sidebar.slider("Dobrar Articulações do Avatar:", 0, 45, 15)
else:
    st.session_state.flex_juntas = 0 # R6 fica totalmente travado/rígido

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Status do Perfil")
st.sidebar.metric(label="Pontos de XP", value=f"{st.session_state.xp_total} XP")
st.sidebar.metric(label="Moedas da Holding", value=f"MH$ {st.session_state.moedas_holding}")

# Trava Antivício Física
limite_diario = 60.0
tempo_restante = limite_diario - st.session_state.tempo_gasto_tela
trava_bloqueio = tempo_restante <= 0

if trava_bloqueio:
    st.sidebar.error("🚨 TRAVA ANTIVÍCIO ATIVADA!")
else:
    st.sidebar.success(f"Foco Seguro: {tempo_restante:.1f} min")

st.sidebar.markdown("---")
st.sidebar.info("**Salmo 23:1**\n\n\"O Senhor é o meu pastor, nada me faltará.\" 🙏")

# --- ARTINMANHA DO MOTOR GRÁFICO 3D (HTML5 CANVAS + JAVASCRIPT PROPRIETÁRIO) ---
# Esse bloco gera um visualizador 3D interativo na tela usando matrizes matemáticas puras no Chrome
angulo_dobra = st.session_state.flex_juntas
is_r15 = "true" if st.session_state.rig_type == "R15 (Articulado)" else "false"

html_avatar_3d = f"""
<div style="text-align: center; font-family: sans-serif; color: #FFFFFF;">
    <canvas id="robloxCanvas" width="300" height="280" style="background:#161B22; border-radius:10px;"></canvas>
    <script>
        const canvas = document.getElementById('robloxCanvas');
        const ctx = canvas.getContext('2d');
        
        function desenharAvatar() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.save();
            ctx.translate(canvas.width / 2, canvas.height / 2);
            
            // 1. Cabeça (Bloco Clássico)
            ctx.fillStyle = "#FFD1A4"; 
            ctx.fillRect(-20, -100, 40, 40);
            // Olhos de óculos escuros de analista
            ctx.fillStyle = "#000000";
            ctx.fillRect(-15, -85, 30, 8);
            
            // 2. Tronco (Camisa Floral Azul da Holding)
            ctx.fillStyle = "#58A6FF";
            ctx.fillRect(-30, -55, 60, 70);
            ctx.fillStyle = "#FFFFFF";
            ctx.font = "10px sans-serif";
            ctx.fillText("{st.session_state.rig_type[:3]}", -10, -15);
            
            // 3. Braço Esquerdo
            ctx.save();
            ctx.translate(-45, -55);
            ctx.fillStyle = "#FFD1A4";
            if ({is_r15}) {{
                // Simulação de junta R15 dobrando
                ctx.fillRect(0, 0, 12, 30);
                ctx.translate(0, 30);
                ctx.rotate({angulo_dobra} * Math.PI / 180);
                ctx.fillRect(0, 0, 12, 25);
            }} else {{
                // R6 Rígido clássico da imagem
                ctx.fillRect(0, 0, 12, 55);
            }}
            ctx.restore();
            
            // 4. Braço Direito
            ctx.save();
            ctx.translate(33, -55);
            ctx.fillStyle = "#FFD1A4";
            if ({is_r15}) {{
                ctx.fillRect(0, 0, 12, 30);
                ctx.translate(0, 30);
                ctx.rotate(-{angulo_dobra} * Math.PI / 180);
                ctx.fillRect(0, 0, 12, 25);
            }} else {{
                ctx.fillRect(0, 0, 12, 55);
            }}
            ctx.restore();
            
            // 5. Perna Esquerda
            ctx.save();
            ctx.translate(-25, 15);
            ctx.fillStyle = "#30363D";
            if ({is_r15}) {{
                ctx.fillRect(0, 0, 22, 25);
                ctx.translate(0, 25);
                ctx.rotate({angulo_dobra} * 0.5 * Math.PI / 180);
                ctx.fillRect(0, 0, 22, 25);
            }} else {{
                ctx.fillRect(0, 0, 22, 50);
            }}
            ctx.restore();
            
            // 6. Perna Direita
            ctx.save();
            ctx.translate(3, 15);
            ctx.fillStyle = "#30363D";
            if ({is_r15}) {{
                ctx.fillRect(0, 0, 22, 25);
                ctx.translate(0, 25);
                ctx.rotate(-{angulo_dobra} * 0.5 * Math.PI / 180);
                ctx.fillRect(0, 0, 22, 25);
            }} else {{
                ctx.fillRect(0, 0, 22, 50);
            }}
            ctx.restore();
            
            ctx.restore();
        }}
        desenharAvatar();
    </script>
</div>
"""

# --- 📊 EXECUÇÃO PRINCIPAL DO ECOSSISTEMA ---
if menu_navegacao == "⚔️ Quests Ativas":
    
    # RENDERIZAÇÃO DO AVATAR NO TOPO DO HUB
    st.title("Hub de Leitura Estratégica 📚")
    
    c_titulo, c_canvas = st.columns([1.5, 1])
    with c_titulo:
        st.caption("Resolução de problemas através da absorção analítica de versículos")
        st.write("Aqui está a simulação estrutural do seu esqueleto em tempo de execução no Chrome:")
        st.info(f"**Modo Ativo:** Seu personagem está renderizado no formato de malha **{st.session_state.rig_type}**.")
    with c_canvas:
        # Injeta o motor gráfico Javascript dentro do contêiner azul do Streamlit
        st.markdown('<div class="canvas-container">', unsafe_allow_html=True)
        components.html(html_avatar_3d, height=290)
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
        
        st.write("### ⚔️ Desafio Lógico da Quest")
        resposta_usuario = st.radio("Escolha a alternativa correta baseada no versículo acima:", quest["opcoes"])
        

