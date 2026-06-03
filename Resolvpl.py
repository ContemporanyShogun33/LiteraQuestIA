import streamlit as st
import pandas as pd

# 1. Configuração de Arquitetura de Games Executiva
st.set_page_config(
    page_title="LiteraQuest IA | Clash Edition", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 UI/UX CLASH OF CLANS METÁLICO E ESCURO
st.markdown("""
<style>
    .stApp { background-color: #0B0E14 !important; color: #FFFFFF !important; }
    h1, h2, h3, h4, p, label, .stMarkdown { color: #FFFFFF !important; }
    .stTextInput input, .stTextArea textarea, .stSelectbox div {
        background-color: #121824 !important; color: #FFFFFF !important;
        border: 2px solid #58A6FF !important; border-radius: 8px !important;
    }
    .quest-card {
        background-color: #121824; border: 2px solid #FFCC00;
        padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(255,204,0,0.1);
        margin-bottom: 20px;
    }
    .canvas-container {
        border: 3px solid #FFCC00; border-radius: 12px;
        background-color: #0F1622; padding: 5px; text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- 📚 BANCO DE DADOS DE QUESTS BÍBLICAS ---
QUESTS_BANCO = [
    {
        "id": 1,
        "titulo": "⚔️ CLAN QUEST 1: A Sabedoria do Rei Salomão",
        "versiculo": '"Filho meu, ouve a instrução de teu pai e não deixes o ensino de tua mãe..." (Provérbios 1:8)',
        "opcoes": ["A fofoca da sala de aula", "O ensino de tua mãe", "Os jogos de computador", "A busca por status da manada"],
        "correta": "O ensino de tua mãe", "xp": 50, "moedas": 10
    },
    {
        "id": 2,
        "titulo": "🛡️ CLAN QUEST 2: A Fortaleza do Pastor",
        "versiculo": '"O Senhor é o meu pastor, nada me faltará." (Salmo 23:1)',
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

# Variáveis de Nível do Vilarejo Clash Style
if "nivel_heroi" not in st.session_state: st.session_state.nivel_heroi = 1
if "tipo_heroi" not in st.session_state: st.session_state.tipo_heroi = "Rei Bárbaro"
if "nivel_centro" not in st.session_state: st.session_state.nivel_centro = 1

# --- 📐 BARRA LATERAL: QUARTEL DE UPGRADES DA VILA ---
st.sidebar.title("LiteraQuest: Clash IA 🏰")
st.sidebar.caption("Centro de Vila da Holding | Kaleb Machado")
st.sidebar.markdown("---")

menu_navegacao = st.sidebar.selectbox("Navegar pelo Vilarejo:", ["⚔️ Atacar Quests", "🛡️ Quartel de Upgrades"])
st.sidebar.markdown("---")

# 🏰 STATUS DO CENTRO DE VILA DO INTROVERTIDO ANALISTA
st.sidebar.subheader("👑 Seus Heróis e Defesas")
st.sidebar.write(f"🏰 Centro de Vila: **Nível {st.session_state.nivel_centro}**")
st.sidebar.write(f"🦸‍♂️ Herói Ativo: **{st.session_state.tipo_heroi} (Nv. {st.session_state.nivel_heroi})**")
st.sidebar.markdown("---")

st.sidebar.subheader("💰 Recursos do Clã")
st.sidebar.metric(label="Elixir de XP Acumulado", value=f"{st.session_state.xp_total} XP")
st.sidebar.metric(label="Ouro da Holding 🟡", value=f"MH$ {st.session_state.moedas_holding}")

# Monitor Antivício (Trava de Escudo de Proteção do Clã)
limite_diario = 60.0
tempo_restante = limite_diario - st.session_state.tempo_gasto_tela
trava_bloqueio = tempo_restante <= 0

st.sidebar.markdown("---")
if trava_bloqueio:
    st.sidebar.error("🚨 ESCUDO QUEBRADO! Sistema antivício ativado. Vá descansar.")
else:
    st.sidebar.success(f"🛡️ Escudo do Clã Ativo: {tempo_restante:.1f} min")

st.sidebar.info("**Salmo 23:1**\n\n\"O Senhor é o meu pastor, nada me faltará.\" 🙏")

# --- 🦾 CLASH ISOMETRIC GRAPHICS ENGINE (HTML5 CANVAS ISOMÉTRICO 2.5D) ---
tipo_h = st.session_state.tipo_heroi
nv_h = st.session_state.nivel_heroi
nv_c = st.session_state.nivel_centro

html_motor_clash = f"""
<div style="text-align: center;">
    <canvas id="clashStage" width="400" height="260" style="background:#1B2616; border-radius:10px;"></canvas>
    <script>
        const canvas = document.getElementById('clashStage');
        const ctx = canvas.getContext('2d');
        let frame = 0;

        function desenharVilaIsometria() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            frame += 0.05;

            ctx.save();
            ctx.translate(canvas.width / 2, 60);
            
            ctx.strokeStyle = "#24341E";
            ctx.lineWidth = 1;
            for(let i = -4; i <= 4; i++) {{
                ctx.beginPath();
                ctx.moveTo(i * 40 - 160, 100 + i * 20);
                ctx.lineTo(i * 40 + 160, 200 + i * 20);
                ctx.stroke();
            }}

            // 1. DESENHAR CENTRO DE VILA
            ctx.fillStyle = "#4A525A";
            ctx.beginPath();
            ctx.moveTo(0, 40);
            ctx.lineTo(50, 65);
            ctx.lineTo(0, 90);
            ctx.lineTo(-50, 65);
            ctx.fill();
            
            ctx.fillStyle = "#2B303A";
            ctx.beginPath();
            ctx.moveTo(-50, 65);
            ctx.lineTo(0, 90);
            ctx.lineTo(0, 130);
            ctx.lineTo(-50, 105);
            ctx.fill();
            
            ctx.fillStyle = "#3F444E";
            ctx.beginPath();
            ctx.moveTo(0, 90);
            ctx.lineTo(50, 65);
            ctx.lineTo(50, 105);
            ctx.lineTo(0, 130);
            ctx.fill();
            
            ctx.fillStyle = "#A62626";
            ctx.beginPath();
            ctx.moveTo(0, 20);
            ctx.lineTo(40, 45);
            ctx.lineTo(0, 65);
            ctx.lineTo(-40, 45);
            ctx.fill();

            ctx.fillStyle = "#FFFFFF";
            ctx.font = "bold 10px sans-serif";
            ctx.fillText("CV {nv_c}", -12, 100);

            // 2. DESENHAR O HERÓI
            let respiracao = Math.sin(frame) * 5;
            ctx.translate(0, 140 + respiracao);

            ctx.fillStyle = "#5E6571";
            ctx.beginPath();
            ctx.ellipse(0, 20, 25, 12, 0, 0, 2 * Math.PI);
            ctx.fill();

            if ("{tipo_h}" === "Rei Bárbaro") {{
                ctx.fillStyle = "#FFCC00"; 
                ctx.fillRect(-10, -35, 20, 15);
                ctx.fillStyle = "#8C4F2B"; 
                ctx.fillRect(-12, -20, 24, 30);
                ctx.fillStyle = "#FFCC00";
                ctx.fillRect(14, -30, 6, 40);
            }} else {{
                ctx.fillStyle = "#7F3FBF"; 
                ctx.fillRect(-12, -25, 24, 35);
                ctx.fillStyle = "#FFD1A4"; 
                ctx.fillRect(-8, -40, 16, 16);
                ctx.fillStyle = "#E5A93C";
                ctx.fillRect(14, -45, 4, 55);
                ctx.fillStyle = "#58A6FF"; 
                ctx.fillRect(12, -53, 8, 8);
            }}

            ctx.fillStyle = "#FFCC00";
            ctx.fillRect(-22, 25, 44, 14);
            ctx.fillStyle = "#000000";
            ctx.font = "bold 9px sans-serif";
            ctx.fillText("LV {nv_h}", -11, 36);

            ctx.restore();
            requestAnimationFrame(desenharVilaIsometria);
        }}
        desenharVilaIsometria();
    </script>
</div>
"""

# --- 📊 EXECUÇÃO PRINCIPAL DO ECOSSISTEMA ---
if menu_navegacao == "⚔️ Atacar Quests":
    st.title("Hub de Ataques de Leitura ⚔️")
    
    c_titulo, c_canvas = st.columns([1.3, 1])
    with c_titulo:
        st.caption("Destrua o vício digital coletando recursos reais com a palavra")
        st.write("### 🏰 Seu Vilarejo em Tempo Real")
        st.info("Sua vila tática está gerando recursos. Conclua os relatórios analíticos abaixo para pilhar Ouro e Elixir para o seu clã!")
    with c_canvas:
        st.markdown('<div class="canvas-container">', unsafe_allow_html=True)
        st.components.v1.html(html_motor_clash, height=270)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown("---")
    
    if trava_bloqueio:
        st.error("🔒 **PROTEÇÃO DO ESCUDO ESGOTADA PELO MONITOR ANTIVÍCIO**")
    else:
        q_idx = st.session_state.quest_atual_idx % len(QUESTS_BANCO)
        quest = QUESTS_BANCO[q_idx]
        
        st.markdown(f"""
        <div class="quest-card">
            <h3 style="color:#FFCC00; margin:0;">{quest['titulo']}</h3>
            <p style="color:#8B949E; font-size:13px; margin:5px 0;">Pilhagem Esperada: +{quest['xp']} Elixir | +{quest['moedas']} Ouro da Holding</p>
            <p style="color:#FFFFFF; font-size:15px; margin-top:10px;">{quest['versiculo']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("### 🎯 Alvo do Ataque: Escolha a alternativa correta:")
        resposta_usuario = st.radio("Selecione a verdade baseada nas escrituras:", quest["opcoes"])
        
        col_text, col_cronometro = st.columns(2)
        with col_text:
            insight = st.text_area("Digite o seu pergaminho de insights analíticos (mínimo 10 caracteres):")
        with col_cronometro:
            minutos_leitura = st.number_input("Tempo de expedição alocado (minutos):", min_value=1.0, value=15.0, step=5.0)
            
        if st.button("Lançar Ataque e Coletar Recursos", type="primary", use_container_width=True):
            if not insight or len(insight) < 10:
                st.warning("Seu pergaminho de insight está muito curto para ser validado pelos magos do clã.")
            else:
                if resposta_usuario == quest["correta"]:
                    st.session_state.xp_total += quest["xp"]
                    st.session_state.moedas_holding += quest["moedas"]
        
