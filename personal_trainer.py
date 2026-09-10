import streamlit as st
from groq import Groq
from datetime import datetime
import json

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="PERSONAL TRAINER IA", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp { background-color:#F8F9FA; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }

    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }

    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#495057,#343A40) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#343A40,#212529) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

    .stApp h1, .stApp h2, .stApp h3 { color:#1A1A2E !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

    .card { background:linear-gradient(135deg,#F1F3F5,#E9ECEF); padding:20px; border-radius:14px; border:1px solid #CED4DA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color:#1A1A2E !important; }

    .card-dark { background:linear-gradient(135deg,#E9ECEF,#DEE2E6); padding:20px; border-radius:14px; border:1px solid #ADB5BD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#1A1A2E !important; }

    .card-green { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; white-space:normal; word-wrap:break-word; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #CED4DA; }
    .stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#1A1A2E !important; }
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#495057 !important; }

    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #CED4DA; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div, .stApp .hist-item small { color:#1A1A2E !important; }

    .badge { background:#495057; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-azul { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#CED4DA,transparent); margin:18px 0; }

    .chat-user { background:#FFFFFF; border:1px solid #CED4DA; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#1A1A2E !important; }

    .chat-persona { background:#F8F9FA; border:1px solid #CED4DA; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona span, .stApp .chat-persona div { color:#1A1A2E !important; }

    .questao-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:12px; padding:18px; margin-bottom:14px; }
    .stApp .questao-box, .stApp .questao-box p, .stApp .questao-box span, .stApp .questao-box div { color:#1A1A2E !important; }

    .avaliacao-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:14px; padding:18px; margin-bottom:12px; }
    .stApp .avaliacao-box, .stApp .avaliacao-box p, .stApp .avaliacao-box span, .stApp .avaliacao-box div { color:#1A1A2E !important; }

    .meta-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:12px; padding:16px; text-align:center; margin:10px 0; }
    .stApp .meta-box, .stApp .meta-box div, .stApp .meta-box span { color:#1A1A2E !important; }
    .stApp .meta-numero { font-size:2em; font-weight:700; color:#495057 !important; }

    .chat-scroll-container { max-height:40vh; overflow-y:auto; display:flex; flex-direction:column; scroll-behavior:smooth; padding-bottom:4px; }
    .chat-scroll-container > * { flex-shrink:0; }
    

    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CACHE
# ─────────────────────────────────────────────
@st.cache_resource
def get_cache_personal():
    return {"perfis": {}}

_cache = get_cache_personal()

# ─────────────────────────────────────────────
# PERSISTÊNCIA LOCAL (JSON)
# ─────────────────────────────────────────────
CHAVES_SALVAR = [
    'usuario', 'historico_treinos', 'treinos_salvos',
    'objetivo_treino', 'local_treino', 'nivel_treino',
    'dias_semana', 'limitacoes', 'tempo_treino',
    'peso', 'altura', 'treinos_realizados',
]

def gerar_json_sessao() -> str:
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados: dict):
    for k in CHAVES_SALVAR:
        if k in dados:
            st.session_state[k] = dados[k]

def salvar_perfil_cache(usuario: str):
    _cache["perfis"][usuario] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos() -> list:
    return list(_cache["perfis"].keys())

def carregar_perfil_cache(usuario: str) -> dict | None:
    return _cache["perfis"].get(usuario)

def salvar_treino(tipo: str, foco: str, conteudo: str):
    st.session_state.historico_treinos.append({
        'data':    datetime.now().strftime('%d/%m %H:%M'),
        'tipo':    tipo,
        'foco':    foco,
        'conteudo': conteudo,
    })

# --- INICIALIZAÇÃO DE ESTADO ---
defaults = {
    'etapa':            "Login",
    'usuario':          "",
    'api_key':          "",
    'pagina':           "Home",
    'historico_treinos':[],
    'treinos_salvos':   [],
    'objetivo_treino':  "Emagrecer",
    'local_treino':     "Academia",
    'nivel_treino':     "Iniciante",
    'dias_semana':      3,
    'limitacoes':       "",
    'tempo_treino':     "60 minutos",
    'peso':             "",
    'altura':           "",
    'treinos_realizados': 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- MOTOR DE IA ---
def personal_ia(prompt: str, system_extra: str = "") -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        system = f"""Você é um Personal Trainer profissional especialista em treinamento físico.
Usuário: {st.session_state.usuario}.
Objetivo: {st.session_state.objetivo_treino}.
Local de treino: {st.session_state.local_treino}.
Nível: {st.session_state.nivel_treino}.
Limitações físicas: {st.session_state.limitacoes or 'nenhuma'}.
Tempo disponível: {st.session_state.tempo_treino}.
{system_extra}
REGRAS:
- Sempre indique séries, repetições e tempo de descanso
- Adapte ao nível e limitações do usuário
- Explique brevemente como executar cada exercício
- Use emojis para deixar visual e motivador
- Escreva em português brasileiro"""
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system},
                {"role": "user",   "content": prompt},
            ],
            model="openai/gpt-oss-120b",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

# --- BARRA DE SALVAR ---
def barra_salvar():
    salvar_perfil_cache(st.session_state.usuario)
    nome_usuario = st.session_state.usuario.lower().replace(' ', '_') or 'minha_sessao'
    total  = len(st.session_state.historico_treinos)
    salvos = len(st.session_state.treinos_salvos)
    realizados = st.session_state.treinos_realizados

    col_info, col_btn = st.columns([4, 2])
    with col_info:
        st.markdown(
            f"<div style='background:#FFF1F2;border:1px solid #FDA4AF;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#1A1A2E;line-height:1.6;'>"
            f"💾 <strong>Antes de sair, salve seus dados no computador.</strong><br>"
            f"<span style='color:#888;font-size:0.88em;'>{total} treinos gerados · "
            f"{realizados} treinos concluídos · {salvos} salvos</span>"
            f"</div>",
            unsafe_allow_html=True
        )
    with col_btn:
        st.download_button(
            label="💾 SALVAR MEUS DADOS (.json)",
            data=gerar_json_sessao(),
            file_name=f"personal_trainer_{nome_usuario}.json",
            mime="application/json",
            use_container_width=True,
        )
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("""<style>
    .dica-nav{font-size:0.72em;color:#94A3B8;text-align:center;padding:2px 0 6px;}
    .dica-mobile{display:none;}
    .dica-desktop{display:block;}
    @media(max-width:768px){.dica-mobile{display:block;}.dica-desktop{display:none;}}
    </style>
    <div class='dica-nav dica-mobile'>👆 Deslize o dedo para navegar entre as abas</div>
    <div class='dica-nav dica-desktop'>📋 Clique no ícone acima para abrir o menu completo</div>
    """, unsafe_allow_html=True)

# ============================================================
# TELA: LOGIN
# ============================================================
if 'altura' not in st.session_state: st.session_state['altura'] = None
if 'dias_semana' not in st.session_state: st.session_state['dias_semana'] = 0
if 'historico_treinos' not in st.session_state: st.session_state['historico_treinos'] = []
if 'limitacoes' not in st.session_state: st.session_state['limitacoes'] = None
if 'local_treino' not in st.session_state: st.session_state['local_treino'] = None
if 'nivel_treino' not in st.session_state: st.session_state['nivel_treino'] = None
if 'objetivo_treino' not in st.session_state: st.session_state['objetivo_treino'] = None
if 'peso' not in st.session_state: st.session_state['peso'] = None
if 'tempo_treino' not in st.session_state: st.session_state['tempo_treino'] = None
if 'treinos_realizados' not in st.session_state: st.session_state['treinos_realizados'] = None
if 'treinos_salvos' not in st.session_state: st.session_state['treinos_salvos'] = None

if st.session_state.etapa == "Login":
    st.markdown("# 🤖 PERSONAL TRAINER IA")
    st.markdown("<div class=\'card\'><b>🔒 ACESSO RESTRITO A CLIENTES DO QUIZ COM PRÊMIOS</b><br>🔗 quizcompremios.com.br</div>", unsafe_allow_html=True)
    st.info("💻 **Dica:** Pela complexidade dos agentes, no computador a experiência é mais agradável.")
    with st.container():
        nome  = st.text_input("Seu Nome:", key="nome_login")
        chave = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_login")
        arq_j = st.file_uploader("📂 Carregar dados salvos (.json):", type=["json"], key="upload_login")
        dados_login = json.load(arq_j) if arq_j else None
        if st.button("✨ ENTRAR", key="btn_entrar_login"):
            if len(nome.strip()) < 2:
                st.warning("Digite um nome com pelo menos 2 caracteres.")
            elif chave.strip():
                st.session_state.usuario = nome.strip()
                st.session_state.api_key = chave
                if dados_login: carregar_json_sessao(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

elif st.session_state.etapa == "App":



    # TABS — navegação nativa
    (_tab_Home, _tab_TreinoDia, _tab_Semana, _tab_Casa, _tab_Evolucao, _tab_Alongamento, _tab_Salvos, _tab_Progresso, _tab_Anamnese, _tab_Suplementacao, _tab_Fadiga, _tab_Macros, _tab_Recuperacao, _tab_Mental, _tab_Biblioteca, _tab_Desafio) = st.tabs(['🏠 Painel', '💪 Treino do Dia', '📅 Semana', '🏡 Treino Casa', '📈 Progressão', '🧘 Alongamento', '❤️ Salvos', '📊 Progresso', '📋 Anamnese', '💊 Suplementação', '🔥 Energia', '🍽️ Macros', '😴 Recuperação', '🧠 Mentalidade', '📚 Biblioteca', '🏆 Desafio'])

    with _tab_Home:
        col_u, col_r = st.columns([3, 1])
        with col_u:
            st.title(f"Bora treinar, {st.session_state.usuario}! 💪")
            st.markdown("<span class='badge'>Modo Personal</span>", unsafe_allow_html=True)
        with col_r:
            if st.button("🚪 Sair", key="personal3"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

        # AVISO SE DADOS SUMIRAM
        if len(st.session_state.historico_treinos) == 0 and st.session_state.treinos_realizados == 0:
            st.markdown("""<div style="background:#FEF3C7;border:2px solid #F59E0B;border-radius:12px;
            padding:12px 18px;margin-bottom:4px;color:#000;font-size:0.9em;font-weight:600;">
            ⚠️ Seus dados não estão mais no servidor.
            </div>""", unsafe_allow_html=True)
            arq_home = st.file_uploader("Carregar meus dados salvos (.json):", type=["json"], key="upload_home")
            if arq_home is not None:
                try:
                    dados_home = json.load(arq_home)
                    carregar_json_sessao(dados_home)
                    salvar_perfil_cache(st.session_state.usuario)
                    st.success("✅ Dados recuperados!")
                    st.rerun()
                except Exception:
                    st.error("Arquivo inválido.")

        # PERFIL DO ATLETA
        st.markdown("#### ⚙️ Seu perfil de treino")
        col_a, col_b = st.columns(2)
        with col_a:
            st.session_state.objetivo_treino = st.selectbox(
                "Objetivo:", ["Emagrecer","Ganhar massa","Definir","Condicionamento físico","Saúde e bem-estar","Reabilitação"],
                index=["Emagrecer","Ganhar massa","Definir","Condicionamento físico","Saúde e bem-estar","Reabilitação"].index(
                    st.session_state.objetivo_treino) if st.session_state.objetivo_treino in
                    ["Emagrecer","Ganhar massa","Definir","Condicionamento físico","Saúde e bem-estar","Reabilitação"] else 0)
            st.session_state.local_treino = st.selectbox(
                "Onde treina:", ["Academia","Casa com equipamentos","Casa sem equipamentos","Ar livre","Misto"],
                index=["Academia","Casa com equipamentos","Casa sem equipamentos","Ar livre","Misto"].index(
                    st.session_state.local_treino) if st.session_state.local_treino in
                    ["Academia","Casa com equipamentos","Casa sem equipamentos","Ar livre","Misto"] else 0)
            st.session_state.nivel_treino = st.selectbox(
                "Nível:", ["Iniciante","Intermediário","Avançado"],
                index=["Iniciante","Intermediário","Avançado"].index(
                    st.session_state.nivel_treino) if st.session_state.nivel_treino in
                    ["Iniciante","Intermediário","Avançado"] else 0)
        with col_b:
            st.session_state.dias_semana  = st.slider("Dias por semana:", 1, 7, st.session_state.dias_semana, key="personal1")
            st.session_state.tempo_treino = st.selectbox(
                "Tempo por treino:", ["30 minutos","45 minutos","60 minutos","90 minutos","2 horas"],
                index=["30 minutos","45 minutos","60 minutos","90 minutos","2 horas"].index(
                    st.session_state.tempo_treino) if st.session_state.tempo_treino in
                    ["30 minutos","45 minutos","60 minutos","90 minutos","2 horas"] else 2)
            st.session_state.limitacoes   = st.text_input(
                "Limitações físicas:", value=st.session_state.limitacoes,
                placeholder="ex: dor no joelho, hérnia de disco, ombro operado...")
            col_p, col_a2 = st.columns(2)
            with col_p:
                st.session_state.peso   = st.text_input("Peso (kg):", value=st.session_state.peso, placeholder="ex: 75", key="personal4")
            with col_a2:
                st.session_state.altura = st.text_input("Altura (cm):", value=st.session_state.altura, placeholder="ex: 170", key="personal5")


        # IMC rápido
        try:
            peso_f   = float(st.session_state.peso.replace(',','.'))
            altura_f = float(st.session_state.altura.replace(',','.')) / 100
            imc      = round(peso_f / (altura_f ** 2), 1)
            if imc < 18.5:    cat_imc = "Abaixo do peso"
            elif imc < 25:    cat_imc = "Peso normal ✅"
            elif imc < 30:    cat_imc = "Sobrepeso"
            else:             cat_imc = "Obesidade"
        except:
            imc, cat_imc = None, None

        # MÉTRICAS
        total      = len(st.session_state.historico_treinos)
        realizados = st.session_state.treinos_realizados
        salvos     = len(st.session_state.treinos_salvos)

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{total}</div><div>Treinos gerados</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{realizados}</div><div>Treinos concluídos</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{salvos}</div><div>Treinos salvos</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.dias_semana}x</div><div>Dias/semana</div></div>", unsafe_allow_html=True)
        c5.markdown(f"<div class='stat-box'><div class='stat-numero'>{imc or '--'}</div><div>IMC {('· ' + cat_imc) if cat_imc else ''}</div></div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>💡 <em>'O melhor treino é o que você consegue fazer com consistência. Não o mais difícil — o mais regular.'</em></div>", unsafe_allow_html=True)

        st.markdown("### 🗺️ O que cada aba faz")
        guia = {
            "💪 Treino do Dia":        "Gera o treino completo do dia com exercícios, séries, repetições e descanso",
            "📅 Planilha da Semana":   "Planilha completa de treinos para a semana — cada dia com foco diferente",
            "🏠 Treino em Casa":       "Treinos sem equipamento — só com o peso do corpo, em qualquer espaço",
            "📈 Progressão de Cargas": "Como aumentar a intensidade semana a semana para continuar evoluindo",
            "🧘 Aquecimento/Alongamento": "Aquecimento antes e alongamento depois — específico para cada treino",
            "❤️ Treinos Salvos":       "Seus treinos favoritos organizados e prontos para usar",
            "📊 Progresso":            "Histórico completo de todos os treinos gerados",
        }
        for aba, desc in guia.items():
            st.markdown(f"**{aba}** — {desc}")

        if st.session_state.historico_treinos:
            st.markdown("### 🕐 Últimos Treinos")
            for item in reversed(st.session_state.historico_treinos[-4:]):
                st.markdown(
                    f"<div class='hist-item'>"
                    f"<span class='badge'>{item['tipo']}</span> "
                    f"<span class='badge-laranja'>{item.get('foco', '')}</span> "
                    f"<small style='color:#888'>{item['data']}</small></div>",
                    unsafe_allow_html=True
                )

        # ========================
        # TREINO DO DIA
        # ========================

    with _tab_TreinoDia:
        st.header("💪 Treino do Dia")
        st.markdown("Treino completo personalizado — exercícios, séries, repetições e como executar.")

        col1, col2 = st.columns(2)
        with col1:
            foco_dia   = st.selectbox("🎯 Foco de hoje:", [
                "Peito e Tríceps", "Costas e Bíceps", "Pernas e Glúteos",
                "Ombros e Trapézio", "Abdômen e Core", "Corpo inteiro (Full Body)",
                "Cardio e Queima de Gordura", "Funcional", "Livre (IA decide pelo objetivo)",
            ])
            local_d    = st.selectbox("📍 Local:", ["Academia","Casa com equipamentos","Casa sem equipamentos","Ar livre"],
                index=["Academia","Casa com equipamentos","Casa sem equipamentos","Ar livre"].index(
                    st.session_state.local_treino) if st.session_state.local_treino in
                    ["Academia","Casa com equipamentos","Casa sem equipamentos","Ar livre"] else 0)
        with col2:
            nivel_d    = st.selectbox("📊 Nível:", ["Iniciante","Intermediário","Avançado"],
                index=["Iniciante","Intermediário","Avançado"].index(
                    st.session_state.nivel_treino) if st.session_state.nivel_treino in
                    ["Iniciante","Intermediário","Avançado"] else 0)
            tempo_d    = st.selectbox("⏱️ Tempo:", ["30 minutos","45 minutos","60 minutos","90 minutos"],
                index=["30 minutos","45 minutos","60 minutos","90 minutos"].index(
                    st.session_state.tempo_treino) if st.session_state.tempo_treino in
                    ["30 minutos","45 minutos","60 minutos","90 minutos"] else 2)
            limitacoes_d = st.text_input("⚠️ Limitações:", value=st.session_state.limitacoes,
                placeholder="ex: joelho, lombar...")

        if st.button("💪 GERAR TREINO DO DIA", key="personal6"):
            with st.spinner("Seu personal montando o treino..."):
                prompt = (
                    f"Monte um treino completo do dia.\n"
                    f"Foco: {foco_dia}. Local: {local_d}. Nível: {nivel_d}.\n"
                    f"Tempo: {tempo_d}. Objetivo: {st.session_state.objetivo_treino}.\n"
                    f"Limitações: {limitacoes_d or 'nenhuma'}.\n\n"
                    f"FORMATO OBRIGATÓRIO:\n\n"
                    f"💪 TREINO DE {foco_dia.upper()}\n"
                    f"Nível: {nivel_d} | Local: {local_d} | Tempo: {tempo_d}\n\n"
                    f"🔥 AQUECIMENTO (5-10 min):\n"
                    f"[3-4 exercícios de aquecimento específicos para esse foco]\n\n"
                    f"📋 TREINO PRINCIPAL:\n\n"
                    f"Para cada exercício use este formato:\n"
                    f"[NÚMERO]. [NOME DO EXERCÍCIO] 💪\n"
                    f"   • Séries: [X] | Repetições: [X] | Descanso: [X] segundos\n"
                    f"   • Como executar: [instrução clara em 2 linhas]\n"
                    f"   • Dica: [erro mais comum e como evitar]\n\n"
                    f"[Mínimo 6 exercícios para o foco principal]\n\n"
                    f"🧘 VOLTA À CALMA (5 min):\n"
                    f"[3-4 alongamentos específicos para os músculos trabalhados]\n\n"
                    f"📊 RESUMO DO TREINO:\n"
                    f"Total de exercícios: [X]\n"
                    f"Volume total (séries x rep): [X]\n"
                    f"Calorias estimadas: [X] cal\n"
                    f"Músculos trabalhados: [lista]\n\n"
                    f"💡 DICA DO PERSONAL:\n"
                    f"[1 dica específica para maximizar esse treino]\n\n"
                    f"⚡ PRÓXIMO TREINO SUGERIDO:\n"
                    f"[O que trabalhar na próxima sessão para equilíbrio muscular]"
                )
                res = personal_ia(prompt)
                salvar_treino("Treino do Dia", foco_dia, res)
                st.session_state['treino_dia_temp'] = res
                st.markdown(f"<div class='card'>{res}</div>", unsafe_allow_html=True)

        if st.session_state.get('treino_dia_temp'):
            col_dl, col_sv, col_ok = st.columns(3)
            with col_dl:
                st.download_button("📋 Baixar treino (.txt)",
                    data=st.session_state['treino_dia_temp'],
                    file_name=f"treino_{foco_dia.replace(' ','_') if 'foco_dia' in dir() else 'dia'}.txt",
                    mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar treino", use_container_width=True, key="personal7"):
                    st.session_state.treinos_salvos.append({
                        'tipo': 'Treino do Dia', 'foco': foco_dia if 'foco_dia' in dir() else '',
                        'conteudo': st.session_state['treino_dia_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("❤️ Salvo!")
            with col_ok:
                if st.button("✅ Treino concluído!", use_container_width=True, key="personal8"):
                    st.session_state.treinos_realizados += 1
                    st.success(f"🎉 Parabéns! {st.session_state.treinos_realizados} treinos no total!")
                    st.rerun()

        # ========================
        # PLANILHA DA SEMANA
        # ========================

    with _tab_Semana:
        st.header("📅 Planilha de Treino Semanal")
        st.markdown("Planilha completa para a semana — cada dia com foco e objetivo diferentes.")

        col1, col2 = st.columns(2)
        with col1:
            dias_s   = st.slider("Dias de treino na semana:", 2, 6, st.session_state.dias_semana, key="personal2")
            local_s  = st.selectbox("Local:", ["Academia","Casa com equipamentos","Casa sem equipamentos","Misto"],
                index=0)
            nivel_s  = st.selectbox("Nível:", ["Iniciante","Intermediário","Avançado"],
                index=["Iniciante","Intermediário","Avançado"].index(
                    st.session_state.nivel_treino) if st.session_state.nivel_treino in
                    ["Iniciante","Intermediário","Avançado"] else 0)
        with col2:
            objetivo_s   = st.selectbox("Objetivo principal:", [
                "Emagrecer","Ganhar massa","Definir","Condicionamento","Saúde geral"],
                index=["Emagrecer","Ganhar massa","Definir","Condicionamento","Saúde geral"].index(
                    st.session_state.objetivo_treino) if st.session_state.objetivo_treino in
                    ["Emagrecer","Ganhar massa","Definir","Condicionamento","Saúde geral"] else 0)
            tempo_s      = st.selectbox("Tempo por treino:", ["30 minutos","45 minutos","60 minutos","90 minutos"],
                index=2)
            limitacoes_s = st.text_input("Limitações:", value=st.session_state.limitacoes, key="personal9")

        if st.button("📅 GERAR PLANILHA DA SEMANA", key="personal10"):
            with st.spinner("Montando sua planilha semanal..."):
                prompt = (
                    f"Monte uma planilha de treino para {dias_s} dias na semana.\n"
                    f"Objetivo: {objetivo_s}. Local: {local_s}. Nível: {nivel_s}.\n"
                    f"Tempo por sessão: {tempo_s}. Limitações: {limitacoes_s or 'nenhuma'}.\n\n"
                    f"ESTRUTURA:\n\n"
                    f"📅 PLANILHA SEMANAL — {objetivo_s.upper()}\n"
                    f"{dias_s} dias de treino · {tempo_s} por sessão · {nivel_s}\n\n"
                    f"Para cada dia de treino use:\n\n"
                    f"━━━━━━━━━━━━━━━━━━━━━\n"
                    f"💪 DIA [N] — [GRUPO MUSCULAR / FOCO]\n"
                    f"━━━━━━━━━━━━━━━━━━━━━\n"
                    f"Exercício 1: [nome] — [X] séries x [X] rep — descanso [X]s\n"
                    f"Exercício 2: [nome] — [X] séries x [X] rep — descanso [X]s\n"
                    f"Exercício 3: [nome] — [X] séries x [X] rep — descanso [X]s\n"
                    f"Exercício 4: [nome] — [X] séries x [X] rep — descanso [X]s\n"
                    f"Exercício 5: [nome] — [X] séries x [X] rep — descanso [X]s\n"
                    f"🔥 Finalizador: [exercício cardio/metabólico]\n\n"
                    f"[Para os dias de descanso: indique recuperação ativa]\n\n"
                    f"📊 VISÃO GERAL DA SEMANA:\n"
                    f"[Tabela resumida: Dia | Foco | Volume | Intensidade]\n\n"
                    f"📈 PROGRESSÃO NAS PRÓXIMAS SEMANAS:\n"
                    f"Semana 2: [como aumentar]\n"
                    f"Semana 3: [como aumentar]\n"
                    f"Semana 4: [deload — semana de recuperação]\n\n"
                    f"💡 DICA DA SEMANA:\n"
                    f"[1 estratégia para maximizar os resultados dessa divisão]"
                )
                res = personal_ia(prompt)
                salvar_treino("Planilha Semanal", f"{dias_s} dias", res)
                st.session_state['semana_temp'] = res
                st.markdown(f"<div class='card-dark'>{res}</div>", unsafe_allow_html=True)

        if st.session_state.get('semana_temp'):
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar planilha (.txt)",
                    data=st.session_state['semana_temp'],
                    file_name="planilha_semanal.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar planilha", key="sv_sem", use_container_width=True):
                    st.session_state.treinos_salvos.append({
                        'tipo': 'Planilha Semanal',
                        'foco': f"{dias_s} dias — {objetivo_s}",
                        'conteudo': st.session_state['semana_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("❤️ Salvo!")

        # ========================
        # TREINO EM CASA
        # ========================

    with _tab_Casa:
        st.header("🏠 Treino em Casa")
        st.markdown("Sem academia, sem desculpa — treinos com o peso do corpo em qualquer espaço.")

        col1, col2 = st.columns(2)
        with col1:
            foco_casa    = st.selectbox("Foco:", [
                "Corpo inteiro (Full Body)","Pernas e Glúteos","Abdômen e Core",
                "Peito e Braços","Cardio e Queima de Gordura","Funcional","Yoga e Mobilidade",
            ])
            espaco       = st.selectbox("Espaço disponível:", [
                "Sala/quarto pequeno (2x2m)","Sala maior (3x3m+)","Quintal/área externa","Qualquer espaço",
            ])
        with col2:
            equipamentos = st.multiselect("Equipamentos que tem em casa:", [
                "Nenhum (só peso do corpo)","Halteres","Elásticos/faixas","Barra fixa",
                "Corda de pular","Banco/cadeira","Garrafa d'água como peso",
            ], default=["Nenhum (só peso do corpo)"])
            nivel_c      = st.selectbox("Nível:", ["Iniciante","Intermediário","Avançado"],
                index=["Iniciante","Intermediário","Avançado"].index(
                    st.session_state.nivel_treino) if st.session_state.nivel_treino in
                    ["Iniciante","Intermediário","Avançado"] else 0)
            tempo_c      = st.selectbox("Tempo:", ["20 minutos","30 minutos","45 minutos","60 minutos"], key="personal11")

        if st.button("🏠 GERAR TREINO EM CASA", key="personal12"):
            with st.spinner("Montando treino em casa..."):
                equip = ", ".join(equipamentos) if equipamentos else "só peso do corpo"
                prompt = (
                    f"Monte um treino em casa completo.\n"
                    f"Foco: {foco_casa}. Espaço: {espaco}. Equipamentos: {equip}.\n"
                    f"Nível: {nivel_c}. Tempo: {tempo_c}. Objetivo: {st.session_state.objetivo_treino}.\n"
                    f"Limitações: {st.session_state.limitacoes or 'nenhuma'}.\n\n"
                    f"FORMATO:\n\n"
                    f"🏠 TREINO EM CASA — {foco_casa.upper()}\n"
                    f"Sem academia · {equip} · {tempo_c}\n\n"
                    f"🔥 AQUECIMENTO (3-5 min):\n"
                    f"[Aquecimento sem equipamento, em espaço pequeno]\n\n"
                    f"💪 CIRCUITO PRINCIPAL:\n"
                    f"[Organize em blocos/circuitos de 3-4 exercícios]\n\n"
                    f"BLOCO 1 — [nome do bloco]:\n"
                    f"• [Exercício 1]: [X] séries x [X] rep (ou [X] segundos)\n"
                    f"  Como fazer: [instrução simples]\n"
                    f"• [Exercício 2]: ...\n"
                    f"• [Exercício 3]: ...\n"
                    f"Descanso entre blocos: [X] segundos\n\n"
                    f"[Repita para todos os blocos]\n\n"
                    f"🧘 ALONGAMENTO FINAL (5 min):\n"
                    f"[Alongamentos no chão/em pé]\n\n"
                    f"📊 RESUMO:\n"
                    f"Calorias estimadas: [X] cal\n"
                    f"Músculos trabalhados: [lista]\n\n"
                    f"💡 VERSÃO MAIS DIFÍCIL:\n"
                    f"[Como tornar esse treino mais intenso quando ficar fácil]\n\n"
                    f"📱 TIMER SUGERIDO:\n"
                    f"[Como usar o cronômetro para esse treino — Tabata, EMOM, AMRAP...]"
                )
                res = personal_ia(prompt)
                salvar_treino("Treino em Casa", foco_casa, res)
                st.session_state['casa_temp'] = res
                st.markdown(f"<div class='card-green'>{res}</div>", unsafe_allow_html=True)

        if st.session_state.get('casa_temp'):
            col_dl, col_sv, col_ok = st.columns(3)
            with col_dl:
                st.download_button("📋 Baixar treino (.txt)",
                    data=st.session_state['casa_temp'],
                    file_name="treino_casa.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_casa", use_container_width=True):
                    st.session_state.treinos_salvos.append({
                        'tipo': 'Treino em Casa', 'foco': foco_casa,
                        'conteudo': st.session_state['casa_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("❤️ Salvo!")
            with col_ok:
                if st.button("✅ Concluído!", key="ok_casa", use_container_width=True):
                    st.session_state.treinos_realizados += 1
                    st.success(f"🎉 Treino {st.session_state.treinos_realizados} concluído!")
                    st.rerun()

        # ========================
        # PROGRESSÃO DE CARGAS
        # ========================

    with _tab_Evolucao:
        st.header("📈 Progressão de Cargas e Evolução")
        st.markdown("Como aumentar a intensidade semana a semana para nunca parar de evoluir.")

        col1, col2 = st.columns(2)
        with col1:
            semanas_atual= st.number_input("Há quantas semanas está treinando:", min_value=1, max_value=104, value=4, key="personal13")
            treino_atual = st.text_area("Seu treino atual (exercícios e cargas):", height=120,
                placeholder="ex: Supino reto: 3x10 com 30kg\nAgachamento: 4x12 com 40kg\nRosca direta: 3x12 com 10kg...")
        with col2:
            objetivo_e   = st.selectbox("Objetivo da progressão:", [
                "Ganhar força (menos rep, mais carga)",
                "Ganhar massa (hipertrofia)",
                "Resistência (mais rep, menos carga)",
                "Misto equilibrado",
            ])
            nivel_e      = st.selectbox("Nível:", ["Iniciante","Intermediário","Avançado"],
                index=["Iniciante","Intermediário","Avançado"].index(
                    st.session_state.nivel_treino) if st.session_state.nivel_treino in
                    ["Iniciante","Intermediário","Avançado"] else 0)

        if st.button("📈 GERAR PLANO DE PROGRESSÃO", key="personal14"):
            if treino_atual.strip():
                with st.spinner("Calculando sua progressão..."):
                    prompt = (
                        f"Crie um plano de progressão de cargas para 8 semanas.\n"
                        f"Semanas treinando: {semanas_atual}. Nível: {nivel_e}.\n"
                        f"Objetivo: {objetivo_e}.\n"
                        f"Treino atual:\n{treino_atual}\n\n"
                        f"ESTRUTURA:\n\n"
                        f"📈 PLANO DE PROGRESSÃO — 8 SEMANAS\n"
                        f"Objetivo: {objetivo_e}\n\n"
                        f"📊 ANÁLISE DO TREINO ATUAL:\n"
                        f"[Avaliação honesta do volume e intensidade atual]\n\n"
                        f"🗓️ PROGRESSÃO SEMANA A SEMANA:\n\n"
                        f"Para cada semana:\n"
                        f"Semana [N]:\n"
                        f"• [Exercício]: [séries]x[rep] com [carga] kg\n"
                        f"  Mudança: [o que aumentou e por quê]\n\n"
                        f"[Semana 4: deload — redução de 40% do volume]\n"
                        f"[Semana 8: teste de força máxima]\n\n"
                        f"📏 REGRAS DE PROGRESSÃO:\n"
                        f"[Quando aumentar carga, quando manter, quando recuar]\n\n"
                        f"🚨 SINAIS DE ALERTA:\n"
                        f"[Quando parar de progredir significa que algo está errado]\n\n"
                        f"💡 PERIODIZAÇÃO:\n"
                        f"[Como organizar os ciclos após as 8 semanas]"
                    )
                    res = personal_ia(prompt)
                    salvar_treino("Progressão de Cargas", objetivo_e, res)
                    st.session_state['evolucao_temp'] = res
                    st.markdown(f"<div class='card-blue'>{res}</div>", unsafe_allow_html=True)
            else:
                st.warning("Informe seu treino atual com as cargas.")

        if st.session_state.get('evolucao_temp'):
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar plano (.txt)",
                    data=st.session_state['evolucao_temp'],
                    file_name="progressao_cargas.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_ev", use_container_width=True):
                    st.session_state.treinos_salvos.append({
                        'tipo': 'Progressão', 'foco': objetivo_e,
                        'conteudo': st.session_state['evolucao_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("❤️ Salvo!")

        # ========================
        # AQUECIMENTO E ALONGAMENTO
        # ========================

    with _tab_Alongamento:
        st.header("🧘 Aquecimento e Alongamento")
        st.markdown("Prepare o corpo antes e recupere depois — para treinar sem lesões.")

        tab1, tab2 = st.tabs(["🔥 Aquecimento", "🧘 Alongamento"])

        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                musculo_aq = st.selectbox("Grupo muscular do treino:", [
                    "Peito e Tríceps","Costas e Bíceps","Pernas e Glúteos",
                    "Ombros","Abdômen","Corpo inteiro",
                ])
                tempo_aq   = st.selectbox("Tempo para aquecimento:", ["5 minutos","8 minutos","10 minutos","15 minutos"], key="personal15")
            with col2:
                local_aq   = st.selectbox("Local:", ["Academia","Casa","Ar livre"], key="personal16")
                nivel_aq   = st.selectbox("Nível:", ["Iniciante","Intermediário","Avançado"],
                    index=["Iniciante","Intermediário","Avançado"].index(
                        st.session_state.nivel_treino) if st.session_state.nivel_treino in
                        ["Iniciante","Intermediário","Avançado"] else 0)

            if st.button("🔥 GERAR AQUECIMENTO", key="personal17"):
                with st.spinner("Preparando aquecimento..."):
                    prompt = (
                        f"Crie um protocolo de aquecimento completo para treino de {musculo_aq}.\n"
                        f"Tempo: {tempo_aq}. Local: {local_aq}. Nível: {nivel_aq}.\n\n"
                        f"FORMATO:\n\n"
                        f"🔥 AQUECIMENTO — {musculo_aq.upper()}\n"
                        f"Duração: {tempo_aq}\n\n"
                        f"FASE 1 — Ativação geral (2-3 min):\n"
                        f"[Exercícios para elevar temperatura corporal]\n\n"
                        f"FASE 2 — Mobilização articular (2-3 min):\n"
                        f"[Movimentos para as articulações envolvidas no treino]\n\n"
                        f"FASE 3 — Ativação específica (2-3 min):\n"
                        f"[Exercícios leves dos músculos que vão ser treinados]\n\n"
                        f"Para cada exercício:\n"
                        f"• [Nome]: [X] repetições ou [X] segundos\n"
                        f"  Como fazer: [instrução rápida]\n\n"
                        f"✅ VOCÊ ESTÁ PRONTO PARA TREINAR QUANDO:\n"
                        f"[Sinais de que o corpo está aquecido corretamente]"
                    )
                    res = personal_ia(prompt)
                    salvar_treino("Aquecimento", musculo_aq, res)
                    st.session_state['aquec_temp'] = res
                    st.markdown(f"<div class='card-orange'>{res}</div>", unsafe_allow_html=True)

            if st.session_state.get('aquec_temp'):
                st.download_button("📋 Baixar aquecimento (.txt)",
                    data=st.session_state['aquec_temp'],
                    file_name="aquecimento.txt", mime="text/plain")

        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                musculo_al = st.selectbox("Músculo trabalhado no treino:", [
                    "Peito e Tríceps","Costas e Bíceps","Pernas e Glúteos",
                    "Ombros","Abdômen","Corpo inteiro",
                ], key="musc_al")
                tempo_al   = st.selectbox("Tempo para alongamento:", ["5 minutos","10 minutos","15 minutos","20 minutos"], key="tempo_al")
            with col2:
                objetivo_al= st.radio("Objetivo:", ["Recuperação pós-treino","Flexibilidade","Relaxamento"], horizontal=True, key="personal18")
                limitacoes_al = st.text_input("Limitações:", value=st.session_state.limitacoes, key="lim_al")

            if st.button("🧘 GERAR ALONGAMENTO", key="personal19"):
                with st.spinner("Preparando alongamento..."):
                    prompt = (
                        f"Crie um protocolo de alongamento após treino de {musculo_al}.\n"
                        f"Tempo: {tempo_al}. Objetivo: {objetivo_al}.\n"
                        f"Limitações: {limitacoes_al or 'nenhuma'}.\n\n"
                        f"FORMATO:\n\n"
                        f"🧘 ALONGAMENTO — {musculo_al.upper()}\n"
                        f"Duração: {tempo_al} | Foco: {objetivo_al}\n\n"
                        f"Para cada alongamento:\n"
                        f"[NÚMERO]. [NOME DO ALONGAMENTO]\n"
                        f"   • Duração: [X] segundos por lado\n"
                        f"   • Como fazer: [instrução clara]\n"
                        f"   • Músculo alongado: [qual músculo]\n"
                        f"   • Respiração: [como respirar durante]\n\n"
                        f"[Mínimo 6 alongamentos]\n\n"
                        f"💡 DICA DE RECUPERAÇÃO:\n"
                        f"[O que mais fazer para recuperar bem após esse treino]\n\n"
                        f"🥤 NUTRIÇÃO PÓS-TREINO:\n"
                        f"[O que comer/beber nas próximas 2 horas para maximizar a recuperação]"
                    )
                    res = personal_ia(prompt)
                    salvar_treino("Alongamento", musculo_al, res)
                    st.session_state['along_temp'] = res
                    st.markdown(f"<div class='card-purple'>{res}</div>", unsafe_allow_html=True)

            if st.session_state.get('along_temp'):
                st.download_button("📋 Baixar alongamento (.txt)",
                    data=st.session_state['along_temp'],
                    file_name="alongamento.txt", mime="text/plain")

        # ========================
        # TREINOS SALVOS
        # ========================

    with _tab_Salvos:
        st.header("❤️ Treinos Salvos")
        st.markdown("Seus treinos favoritos — organizados e prontos para usar a qualquer hora.")

        if not st.session_state.treinos_salvos:
            st.info("Nenhum treino salvo ainda. Gere treinos e salve os favoritos!")
        else:
            tipos_s = list(set(t['tipo'] for t in st.session_state.treinos_salvos))
            filtro  = st.selectbox("Filtrar por tipo:", ["Todos"] + tipos_s, key="personal20")

            treinos_f = [
                t for t in st.session_state.treinos_salvos
                if filtro == "Todos" or t['tipo'] == filtro
            ]

            st.markdown(f"**{len(treinos_f)} treino(s) encontrado(s)**")

            for i, item in enumerate(reversed(treinos_f)):
                idx_real = len(st.session_state.treinos_salvos) - 1 - i
                with st.expander(f"❤️ [{item['tipo']}] {item.get('foco', '')} — {item['data']}"):
                    st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                    col_dl, col_ok, col_del = st.columns([2, 2, 1])
                    with col_dl:
                        st.download_button("📋 Baixar", data=item['conteudo'],
                            file_name=f"{item['tipo'].lower().replace(' ','_')}.txt",
                            mime="text/plain", key=f"dl_salvo_{i}")
                    with col_ok:
                        if st.button("✅ Marcar como feito", key=f"ok_salvo_{i}"):
                            st.session_state.treinos_realizados += 1
                            st.success(f"🎉 +1 treino! Total: {st.session_state.treinos_realizados}")
                            st.rerun()
                    with col_del:
                        if st.button("🗑️", key=f"del_salvo_{i}"):
                            st.session_state.treinos_salvos.pop(idx_real)
                            st.rerun()

        # ========================
        # PROGRESSO
        # ========================

    with _tab_Progresso:
        st.header("📊 Meu Progresso")

        total      = len(st.session_state.historico_treinos)
        realizados = st.session_state.treinos_realizados
        salvos     = len(st.session_state.treinos_salvos)
        tipos = {}
        for t in st.session_state.historico_treinos:
            tipos[t['tipo']] = tipos.get(t['tipo'], 0) + 1

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{total}</div><div>Treinos gerados</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{realizados}</div><div>Treinos concluídos 🏆</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{salvos}</div><div>Treinos salvos</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{tipos.get('Treino do Dia',0)}</div><div>Treinos do dia</div></div>", unsafe_allow_html=True)
        c5.markdown(f"<div class='stat-box'><div class='stat-numero'>{tipos.get('Planilha Semanal',0)}</div><div>Planilhas</div></div>", unsafe_allow_html=True)

        # Ajuste manual de treinos realizados
        with st.expander("✏️ Ajustar treinos concluídos"):
            novo_r = st.number_input("Total de treinos concluídos:", min_value=0, value=realizados, key="personal21")
            if st.button("Salvar", key="personal22"):
                st.session_state.treinos_realizados = novo_r
                st.success("✅ Atualizado!")
                st.rerun()

        if st.session_state.historico_treinos:
            col_f, col_ex = st.columns([3, 1])
            with col_f:
                filtro = st.selectbox("Filtrar:", ["Todos"] + list(tipos.keys()), key="personal23")
            with col_ex:
                hist_txt = "\n\n".join(
                    f"[{t['data']}] {t['tipo']} — {t['foco']}\n{t['conteudo']}\n{'─'*40}"
                    for t in st.session_state.historico_treinos
                )
                st.download_button("⬇️ Exportar TXT", data=hist_txt,
                    file_name="historico_treinos.txt", mime="text/plain")

            for i, item in enumerate(reversed(st.session_state.historico_treinos)):
                if filtro != "Todos" and item['tipo'] != filtro:
                    continue

        # ========================
        # ANAMNESE
        # ========================

    with _tab_Anamnese:
        st.header("📋 Minha Anamnese Completa")
        st.markdown("Preencha uma vez — a IA usa tudo isso em todos os módulos para personalizar cada resposta.")

        with st.form("form_anamnese"):
            st.markdown("#### 👤 Dados Básicos")
            col1, col2, col3 = st.columns(3)
            with col1:
                an_idade = st.number_input("Idade:", min_value=12, max_value=90, value=st.session_state.get('an_idade', 30), key="personal24")
                an_peso = st.number_input("Peso atual (kg):", min_value=30.0, max_value=250.0, value=st.session_state.get('an_peso', 70.0), step=0.5, key="personal25")
            with col2:
                an_altura = st.number_input("Altura (cm):", min_value=120, max_value=220, value=st.session_state.get('an_altura', 170), key="personal26")
                an_sexo = st.selectbox("Sexo biológico:", ["Masculino","Feminino"], index=0 if st.session_state.get('an_sexo','Masculino')=='Masculino' else 1, key="personal27")
            with col3:
                an_objetivo = st.selectbox("Objetivo principal:", ["Perder gordura","Ganhar massa muscular","Manutenção","Condicionamento físico","Saúde geral","Desempenho esportivo"],
                    index=["Perder gordura","Ganhar massa muscular","Manutenção","Condicionamento físico","Saúde geral","Desempenho esportivo"].index(st.session_state.get('an_objetivo','Perder gordura')))
                an_nivel = st.selectbox("Nível de experiência:", ["Iniciante (menos de 6 meses)","Intermediário (6m-2 anos)","Avançado (2+ anos)","Atleta"],
                    index=["Iniciante (menos de 6 meses)","Intermediário (6m-2 anos)","Avançado (2+ anos)","Atleta"].index(st.session_state.get('an_nivel','Iniciante (menos de 6 meses)')))

            st.markdown("#### 🏋️ Treino")
            col4, col5 = st.columns(2)
            with col4:
                an_dias = st.slider("Dias disponíveis por semana:", 1, 7, st.session_state.get('an_dias', 3), key="personal3_x2")
                an_duracao = st.selectbox("Duração por sessão:", ["30 min","45 min","60 min","75 min","90 min+"],
                    index=["30 min","45 min","60 min","75 min","90 min+"].index(st.session_state.get('an_duracao','60 min')))
            with col5:
                an_local = st.selectbox("Local de treino:", ["Academia completa","Academia básica","Em casa com equipamentos","Em casa sem equipamentos","Ao ar livre","Híbrido"],
                    index=["Academia completa","Academia básica","Em casa com equipamentos","Em casa sem equipamentos","Ao ar livre","Híbrido"].index(st.session_state.get('an_local','Academia completa')))
                an_equipamentos = st.text_input("Equipamentos disponíveis:", value=st.session_state.get('an_equipamentos',''), placeholder="ex: halteres, barra, elásticos...", key="personal28")

            st.markdown("#### 🩺 Saúde e Limitações")
            col6, col7 = st.columns(2)
            with col6:
                an_lesoes = st.text_area("Lesões ou limitações físicas:", height=80, value=st.session_state.get('an_lesoes',''), placeholder="ex: dor lombar, joelho operado, tendinite no ombro...", key="personal29")
                an_doencas = st.text_area("Condições de saúde relevantes:", height=80, value=st.session_state.get('an_doencas',''), placeholder="ex: hipertensão, diabetes, hipotireoidismo...", key="personal30")
            with col7:
                an_medicamentos = st.text_input("Medicamentos em uso:", value=st.session_state.get('an_medicamentos',''), placeholder="ex: metformina, losartana...", key="personal31")
                an_historico = st.text_area("Histórico de atividade física:", height=80, value=st.session_state.get('an_historico',''), placeholder="ex: pratiquei musculação por 2 anos, parei há 6 meses...", key="personal32")

            st.markdown("#### 🍽️ Alimentação e Rotina")
            col8, col9 = st.columns(2)
            with col8:
                an_dieta = st.selectbox("Tipo de alimentação:", ["Onívoro","Vegetariano","Vegano","Low carb","Cetogênica","Sem restrições"],
                    index=["Onívoro","Vegetariano","Vegano","Low carb","Cetogênica","Sem restrições"].index(st.session_state.get('an_dieta','Onívoro')))
                an_sono = st.selectbox("Horas de sono por noite:", ["Menos de 5h","5-6h","6-7h","7-8h","8h+"],
                    index=["Menos de 5h","5-6h","6-7h","7-8h","8h+"].index(st.session_state.get('an_sono','7-8h')))
            with col9:
                an_trabalho = st.selectbox("Nível de atividade no trabalho:", ["Sedentário (escritório)","Levemente ativo","Moderadamente ativo","Muito ativo (trabalho físico)"],
                    index=["Sedentário (escritório)","Levemente ativo","Moderadamente ativo","Muito ativo (trabalho físico)"].index(st.session_state.get('an_trabalho','Sedentário (escritório)')))
                an_estresse = st.selectbox("Nível de estresse geral:", ["Baixo","Moderado","Alto","Muito alto"],
                    index=["Baixo","Moderado","Alto","Muito alto"].index(st.session_state.get('an_estresse','Moderado')))

            an_obs = st.text_area("Outras informações importantes:", height=80, value=st.session_state.get('an_obs',''),
                placeholder="qualquer coisa que seu personal precisaria saber...")

            submitted = st.form_submit_button("💾 SALVAR ANAMNESE COMPLETA", key="personalfsb501")
            if submitted:
                for k, v in [('an_idade',an_idade),('an_peso',an_peso),('an_altura',an_altura),
                              ('an_sexo',an_sexo),('an_objetivo',an_objetivo),('an_nivel',an_nivel),
                              ('an_dias',an_dias),('an_duracao',an_duracao),('an_local',an_local),
                              ('an_equipamentos',an_equipamentos),('an_lesoes',an_lesoes),
                              ('an_doencas',an_doencas),('an_medicamentos',an_medicamentos),
                              ('an_historico',an_historico),('an_dieta',an_dieta),('an_sono',an_sono),
                              ('an_trabalho',an_trabalho),('an_estresse',an_estresse),('an_obs',an_obs)]:
                    st.session_state[k] = v
                st.success("✅ Anamnese salva! Todos os módulos agora usarão essas informações.")

        if st.session_state.get('an_objetivo'):
            imc = st.session_state.get('an_peso',70) / ((st.session_state.get('an_altura',170)/100)**2)
            c1,c2,c3 = st.columns(3)
            c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{imc:.1f}</div><div>IMC</div></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.get('an_objetivo','—')}</div><div>Objetivo</div></div>", unsafe_allow_html=True)
            c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.get('an_nivel','—').split(' ')[0]}</div><div>Nível</div></div>", unsafe_allow_html=True)

        # ========================
        # SUPLEMENTAÇÃO
        # ========================

    with _tab_Suplementacao:
        st.header("💊 Suplementação Inteligente")

        def contexto_anamnese():
            if st.session_state.get('an_objetivo'):
                return (f"Perfil do aluno: {st.session_state.get('an_sexo','')}, {st.session_state.get('an_idade','')} anos, "
                        f"{st.session_state.get('an_peso','')}kg, objetivo: {st.session_state.get('an_objetivo','')}, "
                        f"nível: {st.session_state.get('an_nivel','')}, dieta: {st.session_state.get('an_dieta','')}, "
                        f"lesões: {st.session_state.get('an_lesoes','nenhuma')}, "
                        f"doenças: {st.session_state.get('an_doencas','nenhuma')}.")
            return "Perfil não preenchido — responda de forma geral."

        tab_s1, tab_s2, tab_s3 = st.tabs(["🎯 Recomendação Personalizada","📚 Guia de Suplementos","⚠️ O que EVITAR"])

        with tab_s1:
            col1, col2 = st.columns(2)
            with col1:
                orcamento_sup = st.selectbox("💰 Orçamento mensal:", ["Sem orçamento (só o essencial)","Até R$100","R$100-300","R$300-600","Acima de R$600"], key="personal33")
                fase_sup = st.selectbox("📊 Fase atual:", ["Perda de gordura","Ganho de massa","Manutenção","Cutting","Bulking"], key="personal34")
            with col2:
                restricoes_sup = st.multiselect("🚫 Restrições:", ["Vegano","Intolerante à lactose","Sem glúten","Alergia a soja","Sem cafeína"], key="personal4_x2")
                experiencia_sup = st.selectbox("🎓 Experiência com suplementos:", ["Nunca usei","Uso básico (só proteína)","Uso intermediário","Uso avançado"], key="personal35")

            if st.button("💊 GERAR RECOMENDAÇÃO PERSONALIZADA", key="personal36"):
                with st.spinner("Analisando seu perfil..."):
                    prompt = (
                        f"Crie uma recomendação completa e honesta de suplementação.\n"
                        f"{contexto_anamnese()}\n"
                        f"Orçamento: {orcamento_sup}. Fase: {fase_sup}. Restrições: {', '.join(restricoes_sup) or 'nenhuma'}. "
                        f"Experiência: {experiencia_sup}.\n\n"
                        f"FORMATO:\n\n"
                        f"💊 SUPLEMENTAÇÃO RECOMENDADA\n\n"
                        f"⭐ ESSENCIAIS (maior evidência científica para seu objetivo):\n"
                        f"[Para cada: nome, dose, momento ideal, por que para ESTE perfil, custo estimado]\n\n"
                        f"➕ OPCIONAIS (benefício real mas secundário):\n[mesma estrutura]\n\n"
                        f"❌ NÃO NECESSÁRIOS PARA VOCÊ AGORA:\n[o que o marketing vende mas não faz sentido para esse perfil]\n\n"
                        f"📅 PROTOCOLO DIÁRIO:\n[como encaixar cada suplemento na rotina do dia]\n\n"
                        f"⚠️ IMPORTANTE:\n[interações com medicamentos se houver, contraindicações pelo perfil de saúde]"
                    )
                    res = personal_ia(prompt, "Seja honesto sobre evidências científicas. Não exagere benefícios. Sempre considere as condições de saúde reportadas.")
                    salvar_treino("Suplementacao", "Recomendação personalizada", res)
                    st.session_state['sup_rec_temp'] = res

            if st.session_state.get('sup_rec_temp'):
                st.markdown(f"<div class='card-green'>{st.session_state['sup_rec_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['sup_rec_temp'], file_name="suplementacao.txt", mime="text/plain", key="personal37")

        with tab_s2:
            supl_escolhido = st.selectbox("Escolha um suplemento:", [
                "Whey Protein","Creatina","BCAA","Glutamina","Cafeína/Pré-treino",
                "Ômega-3","Vitamina D","ZMA","Beta-Alanina","Albumina",
                "Proteína Vegetal (pea, arroz)","Colágeno","Multivitamínico","HMB","Ashwagandha"
            ])
            if st.button("📚 GUIA COMPLETO DESTE SUPLEMENTO", key="personal38"):
                with st.spinner("Preparando guia..."):
                    prompt = (
                        f"Crie um guia completo e científicamente embasado sobre: {supl_escolhido}.\n\n"
                        f"FORMATO:\n\n"
                        f"📚 {supl_escolhido.upper()}\n\n"
                        f"🔬 O QUE É E COMO FUNCIONA:\n[mecanismo real no corpo]\n\n"
                        f"✅ PARA QUEM FAZ SENTIDO:\n[perfis que mais se beneficiam]\n\n"
                        f"📊 DOSAGEM BASEADA EM EVIDÊNCIA:\n[dose, timing, forma de uso]\n\n"
                        f"⚡ O QUE A CIÊNCIA DIZ:\n[nível de evidência — forte, moderada ou fraca]\n\n"
                        f"💰 CUSTO-BENEFÍCIO:\n[vale o investimento para a maioria das pessoas?]\n\n"
                        f"⚠️ CUIDADOS E CONTRAINDICAÇÕES:\n[quem deve evitar ou consultar médico antes]"
                    )
                    res = personal_ia(prompt)
                    st.session_state['sup_guia_temp'] = res

            if st.session_state.get('sup_guia_temp'):
                st.markdown(f"<div class='card-blue'>{st.session_state['sup_guia_temp']}</div>", unsafe_allow_html=True)

        with tab_s3:
            if st.button("⚠️ O QUE EVITAR E POR QUÊ", key="personal39"):
                with st.spinner("Preparando lista crítica..."):
                    prompt = (
                        f"Liste suplementos e produtos que devem ser evitados ou têm evidência fraca.\n\n"
                        f"FORMATO:\n\n"
                        f"⚠️ SUPLEMENTOS QUE NÃO VALEM O DINHEIRO\n\n"
                        f"[Para cada: nome, por que é vendido, o que a ciência realmente diz, veredicto]\n\n"
                        f"🚨 PRODUTOS PERIGOSOS OU SUSPEITOS:\n[substâncias que oferecem risco real]\n\n"
                        f"💡 REGRA DE OURO:\n[como avaliar qualquer novo suplemento antes de comprar]"
                    )
                    res = personal_ia(prompt)
                    st.session_state['sup_evitar_temp'] = res

            if st.session_state.get('sup_evitar_temp'):
                st.markdown(f"<div class='card-orange'>{st.session_state['sup_evitar_temp']}</div>", unsafe_allow_html=True)

        # ========================
        # TREINO POR FADIGA
        # ========================

    with _tab_Fadiga:
        st.header("🔥 Treino por Nível de Energia")
        st.markdown("A IA adapta o treino de hoje ao seu nível real de disposição.")

        col1, col2 = st.columns(2)
        with col1:
            energia_pct = st.slider("⚡ Seu nível de energia hoje (%):", 10, 100, 70, step=10, key="personal5_x2")
            sono_noite = st.selectbox("😴 Como foi o sono ontem:", ["Ótimo (7h+)","Razoável (5-6h)","Ruim (menos de 5h)","Não dormi bem"], key="personal40")
        with col2:
            dores_hoje = st.multiselect("💢 Dores ou desconforto hoje:", ["Sem dores","Lombar","Pernas cansadas","Ombros","Braços","Dor de cabeça","Mal-estar geral"], key="personal6_x2")
            ultimo_treino = st.selectbox("📅 Último treino foi:", ["Hoje cedo","Ontem","2 dias atrás","3+ dias atrás","Não lembro"], key="personal41")

        foco_fadiga = st.text_input("🎯 Qual grupo muscular você gostaria de treinar (opcional):", placeholder="ex: pernas, costas, peito...", key="personal42")

        if st.button("🔥 GERAR TREINO ADAPTADO", key="personal43"):
            with st.spinner("Calibrando para seu nível de hoje..."):
                nivel_txt = "BAIXO" if energia_pct <= 30 else ("MÉDIO" if energia_pct <= 60 else "ALTO")
                perfil = (f"Perfil: {st.session_state.get('an_sexo','')}, {st.session_state.get('an_nivel','intermediário')}, "
                         f"objetivo: {st.session_state.get('an_objetivo','melhora geral')}, "
                         f"local: {st.session_state.get('an_local','academia')}, "
                         f"lesões: {st.session_state.get('an_lesoes','nenhuma')}." if st.session_state.get('an_objetivo') else "")
                prompt = (
                    f"Crie um treino adaptado ao nível de energia atual.\n"
                    f"{perfil}\n"
                    f"Energia: {energia_pct}% (nível {nivel_txt}). Sono: {sono_noite}. "
                    f"Dores: {', '.join(dores_hoje) or 'nenhuma'}. Último treino: {ultimo_treino}. "
                    f"Foco desejado: {foco_fadiga or 'livre'}.\n\n"
                    f"FORMATO:\n\n"
                    f"🔥 TREINO DE HOJE — NÍVEL {nivel_txt} ({energia_pct}%)\n\n"
                    f"🎯 ESTRATÉGIA DO DIA:\n[por que esse tipo de treino faz sentido hoje com essa energia]\n\n"
                    f"⚡ AQUECIMENTO ({5 if energia_pct < 50 else 10} min):\n[adaptado ao nível de energia]\n\n"
                    f"💪 TREINO PRINCIPAL:\n[exercícios com séries, repetições e descanso — "
                    f"mais leve e menos volume se energia baixa, normal/intenso se alta]\n\n"
                    f"🔄 ADAPTAÇÕES PARA AS DORES REPORTADAS:\n[como modificar exercícios]\n\n"
                    f"🧘 FINALIZAÇÃO:\n[volta à calma adequada ao estado de hoje]\n\n"
                    f"💡 CONSELHO DO DIA:\n[1 orientação sobre treinar com esse nível de energia]"
                )
                res = personal_ia(prompt)
                salvar_treino("Fadiga", f"Energia {energia_pct}%", res)
                st.session_state['fadiga_temp'] = res

        if st.session_state.get('fadiga_temp'):
            cor = "card-red" if energia_pct <= 30 else ("card-orange" if energia_pct <= 60 else "card-green")
            st.markdown(f"<div class='{cor}'>{st.session_state['fadiga_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['fadiga_temp'], file_name="treino_fadiga.txt", mime="text/plain", use_container_width=True, key="personal44")
            with col_sv:
                if st.button("✅ Treino Concluído!", key="concluir_fadiga", use_container_width=True):
                    st.session_state.treinos_realizados += 1
                    st.success("🏆 +1 treino concluído!")

        # ========================
        # CALCULADORA DE MACROS
        # ========================

    with _tab_Macros:
        st.header("🍽️ Calculadora de Macros")

        col1, col2, col3 = st.columns(3)
        with col1:
            peso_mac = st.number_input("Peso (kg):", min_value=30.0, max_value=250.0,
                value=float(st.session_state.get('an_peso', 70)), step=0.5)
            altura_mac = st.number_input("Altura (cm):", min_value=120, max_value=220,
                value=int(st.session_state.get('an_altura', 170)))
            idade_mac = st.number_input("Idade:", min_value=12, max_value=90,
                value=int(st.session_state.get('an_idade', 30)))
        with col2:
            sexo_mac = st.selectbox("Sexo biológico:", ["Masculino","Feminino"],
                index=0 if st.session_state.get('an_sexo','Masculino')=='Masculino' else 1)
            atividade_mac = st.selectbox("Nível de atividade:", [
                "Sedentário (sem exercício)","Levemente ativo (1-2x/sem)",
                "Moderadamente ativo (3-4x/sem)","Muito ativo (5-6x/sem)","Extremamente ativo (2x/dia)"])
        with col3:
            objetivo_mac = st.selectbox("Objetivo:", ["Perder gordura","Manutenção","Ganhar massa"], key="personal45")
            dieta_mac = st.selectbox("Preferência alimentar:", ["Onívoro","Vegetariano","Vegano","Low carb","Cetogênica"], key="personal46")

        if st.button("🍽️ CALCULAR MEUS MACROS", key="personal47"):
            with st.spinner("Calculando..."):
                # TMB pelo método Harris-Benedict
                if sexo_mac == "Masculino":
                    tmb = 88.36 + (13.4 * peso_mac) + (4.8 * altura_mac) - (5.7 * idade_mac)
                else:
                    tmb = 447.6 + (9.2 * peso_mac) + (3.1 * altura_mac) - (4.3 * idade_mac)

                fat = {"Sedentário (sem exercício)":1.2,"Levemente ativo (1-2x/sem)":1.375,
                       "Moderadamente ativo (3-4x/sem)":1.55,"Muito ativo (5-6x/sem)":1.725,
                       "Extremamente ativo (2x/dia)":1.9}
                tdee = tmb * fat.get(atividade_mac, 1.55)
                cal_alvo = tdee - 400 if objetivo_mac == "Perder gordura" else (tdee + 300 if objetivo_mac == "Ganhar massa" else tdee)

                prompt = (
                    f"Crie um plano completo de macros para esta pessoa.\n"
                    f"TMB calculada: {tmb:.0f} kcal. TDEE: {tdee:.0f} kcal. Calorias alvo: {cal_alvo:.0f} kcal.\n"
                    f"Perfil: {sexo_mac}, {idade_mac} anos, {peso_mac}kg, {altura_mac}cm, "
                    f"objetivo: {objetivo_mac}, dieta: {dieta_mac}.\n\n"
                    f"FORMATO:\n\n"
                    f"🍽️ SEU PLANO DE MACROS\n\n"
                    f"📊 CALORIAS DIÁRIAS: {cal_alvo:.0f} kcal\n"
                    f"(TMB: {tmb:.0f} | TDEE: {tdee:.0f})\n\n"
                    f"🥩 PROTEÍNA: [X]g/dia ([X] kcal)\n[justificativa e fontes recomendadas para {dieta_mac}]\n\n"
                    f"🍞 CARBOIDRATO: [X]g/dia ([X] kcal)\n[timing e melhores fontes]\n\n"
                    f"🥑 GORDURA: [X]g/dia ([X] kcal)\n[melhores fontes]\n\n"
                    f"📅 DISTRIBUIÇÃO NAS REFEIÇÕES:\n[como dividir os macros ao longo do dia — 4-6 refeições]\n\n"
                    f"🍱 EXEMPLOS DE REFEIÇÕES:\n[3 exemplos práticos que batem os macros do dia, respeitando {dieta_mac}]\n\n"
                    f"💡 DICA PRINCIPAL:\n[1 ajuste que mais impacta o resultado para esse objetivo]"
                )
                res = personal_ia(prompt)
                salvar_treino("Macros", f"{objetivo_mac} — {cal_alvo:.0f}kcal", res)
                st.session_state['macros_temp'] = res

        if st.session_state.get('macros_temp'):
            st.markdown(f"<div class='card-green'>{st.session_state['macros_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['macros_temp'], file_name="plano_macros.txt", mime="text/plain", use_container_width=True, key="personal48")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_macros", use_container_width=True):
                    st.session_state.treinos_salvos.append({'tipo':'Macros','foco':f"{objetivo_mac}",'conteudo':st.session_state['macros_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # RECUPERAÇÃO E SONO
        # ========================

    with _tab_Recuperacao:
        st.header("😴 Recuperação e Sono")

        tab_r1, tab_r2, tab_r3 = st.tabs(["😴 Sono e Recuperação","🧊 Recuperação Ativa","🚨 Overtraining"])

        with tab_r1:
            horas_sono = st.selectbox("Quantas horas você dorme por noite:", ["Menos de 5h","5-6h","6-7h","7-8h","8h+"], key="personal49")
            qualidade_sono = st.selectbox("Qualidade do sono:", ["Ótima (acordo descansado)","Boa","Regular","Ruim (acordo cansado)","Péssima (insônia)"], key="personal50")

            if st.button("😴 ANALISAR MEU SONO E RECUPERAÇÃO", key="personal51"):
                with st.spinner("Analisando..."):
                    prompt = (
                        f"Analise o padrão de sono e crie um guia de recuperação personalizado.\n"
                        f"Sono: {horas_sono} por noite. Qualidade: {qualidade_sono}.\n"
                        f"Objetivo: {st.session_state.get('an_objetivo','melhora geral')}. "
                        f"Nível: {st.session_state.get('an_nivel','intermediário')}. "
                        f"Estresse: {st.session_state.get('an_estresse','moderado')}.\n\n"
                        f"FORMATO:\n\n"
                        f"😴 ANÁLISE DO SEU SONO\n\n"
                        f"📊 O IMPACTO NO SEU TREINO:\n[como esse padrão de sono afeta seus resultados especificamente]\n\n"
                        f"🧠 POR QUE O SONO É O SUPLEMENTO MAIS PODEROSO:\n[mecanismos fisiológicos — GH, testosterona, recuperação muscular]\n\n"
                        f"✅ PROTOCOLO DE HIGIENE DO SONO:\n[ações específicas para melhorar, em ordem de impacto]\n\n"
                        f"⏰ ROTINA IDEAL PRÉ-SONO:\n[o que fazer nas 2 horas antes de dormir]\n\n"
                        f"💊 SUPLEMENTOS QUE PODEM AJUDAR:\n[com base em evidência — melatonina, magnésio, etc]\n\n"
                        f"🎯 META DESTA SEMANA:\n[1 mudança concreta para começar hoje]"
                    )
                    res = personal_ia(prompt)
                    st.session_state['sono_temp'] = res

            if st.session_state.get('sono_temp'):
                st.markdown(f"<div class='card-purple'>{st.session_state['sono_temp']}</div>", unsafe_allow_html=True)

        with tab_r2:
            dias_sem_treino = st.number_input("Dias seguidos treinando sem descanso:", min_value=0, max_value=30, value=3, key="personal52")
            tipo_dor = st.multiselect("Onde você sente dor muscular agora:", ["Sem dores","Pernas","Costas","Peito","Ombros","Braços","Abdômen"], key="personal7_x2")

            if st.button("🧊 PROTOCOLO DE RECUPERAÇÃO ATIVA", key="personal53"):
                with st.spinner("Preparando protocolo..."):
                    prompt = (
                        f"Crie um protocolo de recuperação ativa.\n"
                        f"Dias consecutivos treinando: {dias_sem_treino}. Dores: {', '.join(tipo_dor) or 'nenhuma'}.\n\n"
                        f"FORMATO:\n\n"
                        f"🧊 PROTOCOLO DE RECUPERAÇÃO ATIVA\n\n"
                        f"🎯 DIAGNÓSTICO:\n[avaliação do estado de recuperação]\n\n"
                        f"✅ ATIVIDADES DE RECUPERAÇÃO RECOMENDADAS HOJE:\n[o que fazer — caminhada leve, mobilidade, natação leve, etc]\n\n"
                        f"🧊 TÉCNICAS DE RECUPERAÇÃO FÍSICA:\n[banho frio, contraste, foam roller, compressão — o que ajuda e como]\n\n"
                        f"🍽️ NUTRIÇÃO PARA RECUPERAÇÃO:\n[o que comer para acelerar a recuperação muscular]\n\n"
                        f"⏳ QUANDO VOLTAR AO TREINO INTENSO:\n[guia de timing baseado no estado atual]"
                    )
                    res = personal_ia(prompt)
                    st.session_state['rec_ativa_temp'] = res

            if st.session_state.get('rec_ativa_temp'):
                st.markdown(f"<div class='card-blue'>{st.session_state['rec_ativa_temp']}</div>", unsafe_allow_html=True)

        with tab_r3:
            sintomas_over = st.multiselect("Você está sentindo:", [
                "Queda de desempenho nos treinos","Fadiga persistente mesmo com descanso",
                "Irritabilidade e mudanças de humor","Insônia ou sono ruim",
                "Dores articulares frequentes","Perda de motivação para treinar",
                "Infecções frequentes (gripes, resfriados)","Frequência cardíaca em repouso elevada"])

            if st.button("🚨 AVALIAR RISCO DE OVERTRAINING", key="personal54"):
                if sintomas_over:
                    with st.spinner("Analisando..."):
                        prompt = (
                            f"Avalie o risco de overtraining com base nos sintomas.\n"
                            f"Sintomas: {', '.join(sintomas_over)}.\n"
                            f"Frequência de treino: {st.session_state.get('an_dias',3)} dias/semana. "
                            f"Nível: {st.session_state.get('an_nivel','intermediário')}.\n\n"
                            f"FORMATO:\n\n"
                            f"🚨 AVALIAÇÃO DE OVERTRAINING\n\n"
                            f"📊 NÍVEL DE RISCO: [Baixo/Moderado/Alto/Crítico]\n[justificativa]\n\n"
                            f"🔬 O QUE ESTÁ ACONTECENDO NO SEU CORPO:\n[fisiologia do overtraining]\n\n"
                            f"🛑 O QUE FAZER AGORA:\n[protocolo de ação baseado no nível de risco]\n\n"
                            f"📅 PLANO DE DELOAD:\n[como estruturar a semana de recuperação]\n\n"
                            f"✅ COMO PREVENIR NO FUTURO:\n[periodização e sinais de alerta precoces]"
                        )
                        res = personal_ia(prompt, "Seja conservador nas recomendações de saúde. Se os sintomas forem graves, recomende avaliação médica.")
                        st.session_state['over_temp'] = res
                else:
                    st.info("Selecione os sintomas que está sentindo.")

            if st.session_state.get('over_temp'):
                st.markdown(f"<div class='card-orange'>{st.session_state['over_temp']}</div>", unsafe_allow_html=True)

        # ========================
        # MÓDULO MENTAL
        # ========================

    with _tab_Mental:
        st.header("🧠 Mentalidade e Consistência")

        tema_mental = st.selectbox("O que você está enfrentando:", [
            "Falta de motivação para treinar","Procrastinação — fico adiando o treino",
            "Abandonei os treinos e quero recomeçar","Sabotagem — começo bem e travejo no meio",
            "Como criar um hábito de treino duradouro","Ansiedade com resultados lentos",
            "Como lidar com a semana que fugiu do plano","Mentalidade de atleta para vida real",
        ])
        contexto_mental = st.text_area("Conte mais sobre o que está acontecendo:", height=100,
            placeholder="ex: Sei que devo treinar mas quando chega a hora invento desculpas...")

        if st.button("🧠 ORIENTAÇÃO MENTAL", key="personal55"):
            with st.spinner("Preparando orientação..."):
                prompt = (
                    f"Ofereça orientação sobre mentalidade e consistência no treino.\n"
                    f"Tema: {tema_mental}. Contexto: {contexto_mental or 'não detalhado'}.\n"
                    f"Perfil: objetivo {st.session_state.get('an_objetivo','melhora geral')}, "
                    f"nível {st.session_state.get('an_nivel','iniciante')}.\n\n"
                    f"FORMATO:\n\n"
                    f"🧠 {tema_mental.upper()}\n\n"
                    f"🎯 O QUE REALMENTE ESTÁ ACONTECENDO:\n[a raiz psicológica do problema, sem julgamento]\n\n"
                    f"🔬 A CIÊNCIA POR TRÁS:\n[o que a psicologia do comportamento e neurociência diz sobre isso]\n\n"
                    f"⚙️ ESTRATÉGIAS PRÁTICAS:\n[3-5 ações concretas e replicáveis]\n\n"
                    f"📅 O QUE FAZER HOJE:\n[1 ação imediata para quebrar o padrão]\n\n"
                    f"💪 REFRAME:\n[uma perspectiva diferente que muda como você vê a situação]"
                )
                res = personal_ia(prompt, "Seja direto, empático e prático. Evite clichês motivacionais vazios. Fale de igual para igual.")
                salvar_treino("Mental", tema_mental, res)
                st.session_state['mental_temp'] = res

        if st.session_state.get('mental_temp'):
            st.markdown(f"<div class='card-dark'>{st.session_state['mental_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['mental_temp'], file_name="mentalidade.txt", mime="text/plain", use_container_width=True, key="personal56")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_mental", use_container_width=True):
                    st.session_state.treinos_salvos.append({'tipo':'Mental','foco':tema_mental,'conteudo':st.session_state['mental_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # BIBLIOTECA DE EXERCÍCIOS
        # ========================

    with _tab_Biblioteca:
        st.header("📚 Biblioteca de Exercícios")

        tab_b1, tab_b2, tab_b3 = st.tabs(["🔄 Substituições","📖 Guia do Exercício","💢 Adaptações para Lesão"])

        with tab_b1:
            col1, col2 = st.columns(2)
            with col1:
                exercicio_orig = st.text_input("Exercício que você NÃO pode fazer:", placeholder="ex: agachamento, supino, barra fixa...", key="personal57")
            with col2:
                motivo_subst = st.selectbox("Motivo:", ["Não tenho o equipamento","Lesão ou dor","Iniciante — muito difícil","Prefiro variar"], key="personal58")

            if st.button("🔄 ENCONTRAR SUBSTITUIÇÕES", key="personal59"):
                if exercicio_orig.strip():
                    with st.spinner("Buscando alternativas..."):
                        prompt = (
                            f"Sugira substituições para o exercício: {exercicio_orig}.\n"
                            f"Motivo: {motivo_subst}.\n"
                            f"Equipamentos disponíveis: {st.session_state.get('an_equipamentos','não informado')}. "
                            f"Local: {st.session_state.get('an_local','academia')}. "
                            f"Lesões: {st.session_state.get('an_lesoes','nenhuma')}.\n\n"
                            f"FORMATO:\n\n"
                            f"🔄 SUBSTITUIÇÕES PARA: {exercicio_orig.upper()}\n\n"
                            f"✅ SUBSTITUTO PRINCIPAL (mais similar em recrutamento muscular):\n[nome, como fazer, por que é equivalente]\n\n"
                            f"✅ SUBSTITUTO ALTERNATIVO 1:\n[nome, como fazer]\n\n"
                            f"✅ SUBSTITUTO ALTERNATIVO 2:\n[nome, como fazer]\n\n"
                            f"💡 DICA DE TRANSIÇÃO:\n[como adaptar a carga/série ao mudar de exercício]"
                        )
                        res = personal_ia(prompt)
                        st.session_state['subst_temp'] = res

            if st.session_state.get('subst_temp'):
                st.markdown(f"<div class='card-green'>{st.session_state['subst_temp']}</div>", unsafe_allow_html=True)

        with tab_b2:
            exercicio_guia = st.text_input("Exercício para estudar:", placeholder="ex: levantamento terra, elevação lateral...", key="personal60")

            if st.button("📖 GUIA COMPLETO", key="personal61"):
                if exercicio_guia.strip():
                    with st.spinner("Preparando guia..."):
                        prompt = (
                            f"Crie um guia completo e técnico sobre o exercício: {exercicio_guia}.\n\n"
                            f"FORMATO:\n\n"
                            f"📖 {exercicio_guia.upper()}\n\n"
                            f"🏋️ MÚSCULOS TRABALHADOS:\n[principal e secundários]\n\n"
                            f"⚙️ EXECUÇÃO CORRETA (passo a passo):\n[técnica detalhada]\n\n"
                            f"❌ ERROS MAIS COMUNS:\n[e como corrigir cada um]\n\n"
                            f"📊 VARIAÇÕES:\n[versões mais fáceis, mais difíceis e alternativas]\n\n"
                            f"💡 DICAS DE PERFORMANCE:\n[o que muda para iniciantes vs avançados]\n\n"
                            f"⚠️ CUIDADOS E CONTRAINDICAÇÕES:\n[quando evitar ou ter cuidado especial]"
                        )
                        res = personal_ia(prompt)
                        st.session_state['guia_ex_temp'] = res

            if st.session_state.get('guia_ex_temp'):
                st.markdown(f"<div class='card-blue'>{st.session_state['guia_ex_temp']}</div>", unsafe_allow_html=True)

        with tab_b3:
            lesao_adapt = st.text_input("Sua lesão ou limitação:", placeholder="ex: dor no joelho, tendinite no ombro, hérnia lombar...", key="personal62")
            grupo_adapt = st.selectbox("Grupo muscular que quer treinar:", ["Pernas","Costas","Peito","Ombros","Bíceps","Tríceps","Abdômen","Full body"], key="personal63")

            if st.button("💢 TREINO ADAPTADO PARA MINHA LESÃO", key="personal64"):
                if lesao_adapt.strip():
                    with st.spinner("Adaptando treino..."):
                        prompt = (
                            f"Crie um protocolo de treino adaptado para treinar {grupo_adapt} com a limitação: {lesao_adapt}.\n\n"
                            f"FORMATO:\n\n"
                            f"💢 TREINO DE {grupo_adapt.upper()} COM {lesao_adapt.upper()}\n\n"
                            f"⚠️ EXERCÍCIOS A EVITAR COMPLETAMENTE:\n[e por que causam risco]\n\n"
                            f"✅ EXERCÍCIOS SEGUROS:\n[lista com séries, repetições e cuidados específicos]\n\n"
                            f"🔧 ADAPTAÇÕES TÉCNICAS:\n[modificações na execução para proteger a lesão]\n\n"
                            f"🩺 QUANDO CONSULTAR UM PROFISSIONAL:\n[sinais de alerta que indicam necessidade de avaliação médica]"
                        )
                        res = personal_ia(prompt, "IMPORTANTE: sempre recomende avaliação médica ou fisioterapêutica antes de treinar com lesões. Não faça diagnóstico — apenas oriente sobre adaptações gerais.")
                        st.session_state['adapt_lesao_temp'] = res

            if st.session_state.get('adapt_lesao_temp'):
                st.markdown(f"<div class='card-orange'>{st.session_state['adapt_lesao_temp']}</div>", unsafe_allow_html=True)
                st.markdown("<div class='disclaimer' style='background:#FFF7ED;border:1px solid #FDE68A;border-radius:10px;padding:12px;font-size:0.82em;color:#92400E;margin-top:8px;'>⚠️ Este conteúdo é educativo. Sempre consulte um médico ou fisioterapeuta antes de treinar com lesões.</div>", unsafe_allow_html=True)

        # ========================
        # DESAFIO 30/60/90 DIAS
        # ========================

    with _tab_Desafio:
        st.header("🏆 Desafio 30/60/90 Dias")

        if 'desafio_ativo' not in st.session_state:
            st.session_state.desafio_ativo = None
        if 'desafio_checkins' not in st.session_state:
            st.session_state.desafio_checkins = []
        if 'desafio_pontos' not in st.session_state:
            st.session_state.desafio_pontos = 0

        if st.session_state.desafio_ativo is None:
            st.markdown("### 🎯 Crie seu Desafio")
            col1, col2 = st.columns(2)
            with col1:
                duracao_des = st.selectbox("Duração:", ["30 dias","60 dias","90 dias"], key="personal65")
                objetivo_des = st.selectbox("Objetivo do desafio:", [
                    "Perder gordura","Ganhar massa","Criar hábito de treino",
                    "Melhorar condicionamento","Definição muscular","Força"])
            with col2:
                dias_semana_des = st.slider("Dias de treino por semana:", 2, 6, 3, key="personal8_x2")
                nivel_des = st.selectbox("Intensidade:", ["Leve (foco no hábito)","Moderada","Intensa"], key="personal66")

            if st.button("🏆 CRIAR MEU DESAFIO", key="personal67"):
                with st.spinner("Montando seu desafio..."):
                    prompt = (
                        f"Crie um programa de desafio completo.\n"
                        f"Duração: {duracao_des}. Objetivo: {objetivo_des}. "
                        f"Treinos/semana: {dias_semana_des}. Intensidade: {nivel_des}.\n"
                        f"Perfil: {st.session_state.get('an_nivel','iniciante')}, "
                        f"local: {st.session_state.get('an_local','academia')}.\n\n"
                        f"FORMATO:\n\n"
                        f"🏆 DESAFIO {duracao_des.upper()} — {objetivo_des.upper()}\n\n"
                        f"🎯 O QUE VOCÊ VAI CONQUISTAR:\n[resultados esperados realistas]\n\n"
                        f"📅 ESTRUTURA DO PROGRAMA:\n[como as semanas se organizam — progressão]\n\n"
                        f"💪 TREINOS DA SEMANA 1:\n[treinos completos para começar]\n\n"
                        f"📊 COMO MEDIR SEU PROGRESSO:\n[métricas semanais para acompanhar]\n\n"
                        f"🔥 REGRAS DO DESAFIO:\n[compromissos claros e não-negociáveis]\n\n"
                        f"💡 MISSÃO DO DIA 1:\n[o que fazer hoje para começar com força]"
                    )
                    res = personal_ia(prompt)
                    st.session_state.desafio_ativo = {
                        'duracao': duracao_des, 'objetivo': objetivo_des,
                        'inicio': datetime.now().strftime('%d/%m/%Y'),
                        'programa': res, 'dias_semana': dias_semana_des
                    }
                    st.session_state.desafio_pontos = 0
                    st.session_state.desafio_checkins = []
                    st.rerun()
        else:
            des = st.session_state.desafio_ativo
            dias_passados = len(st.session_state.desafio_checkins)
            total_dias = int(des['duracao'].split()[0])
            pct = min(int(dias_passados / total_dias * 100), 100)

            col1, col2, col3, col4 = st.columns(4)
            col1.markdown(f"<div class='stat-box'><div class='stat-numero'>{dias_passados}</div><div>Dias concluídos</div></div>", unsafe_allow_html=True)
            col2.markdown(f"<div class='stat-box'><div class='stat-numero'>{total_dias - dias_passados}</div><div>Dias restantes</div></div>", unsafe_allow_html=True)
            col3.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.desafio_pontos}</div><div>Pontos</div></div>", unsafe_allow_html=True)
            col4.markdown(f"<div class='stat-box'><div class='stat-numero'>{pct}%</div><div>Concluído</div></div>", unsafe_allow_html=True)

            st.progress(pct / 100)
            st.markdown(f"<br>**🏆 {des['duracao']} de {des['objetivo']}** — iniciado em {des['inicio']}", unsafe_allow_html=True)

            with st.expander("📋 Ver programa completo"):
                st.markdown(f"<div class='card'>{des['programa']}</div>", unsafe_allow_html=True)

            st.markdown("### ✅ Check-in do Dia")
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                treinou_hoje = st.radio("Você treinou hoje?", ["✅ Sim, treinei!","❌ Não treinei"], key="treinou_radio")
                nota_treino = st.slider("Como foi o treino (1-10):", 1, 10, 7, key="personal9_x2") if "Sim" in treinou_hoje else None
            with col_c2:
                comeu_bem = st.radio("Seguiu a alimentação?", ["✅ Sim","Parcialmente","❌ Não"], key="personal68")
                obs_dia = st.text_input("Observação do dia:", placeholder="ex: Senti evolução no supino...", key="personal69")

            if st.button("📝 FAZER CHECK-IN DE HOJE", key="personal70"):
                checkin = {
                    'data': datetime.now().strftime('%d/%m/%Y'),
                    'treinou': "Sim" in treinou_hoje,
                    'nota': nota_treino,
                    'alimentacao': comeu_bem,
                    'obs': obs_dia
                }
                st.session_state.desafio_checkins.append(checkin)
                pontos = 10 if "Sim" in treinou_hoje else 2
                pontos += 5 if comeu_bem == "✅ Sim" else (2 if comeu_bem == "Parcialmente" else 0)
                st.session_state.desafio_pontos += pontos
                st.success(f"✅ Check-in registrado! +{pontos} pontos 🔥")
                st.rerun()

            if st.session_state.desafio_checkins:
                with st.expander(f"📊 Histórico de check-ins ({len(st.session_state.desafio_checkins)} dias)"):
                    for c in reversed(st.session_state.desafio_checkins[-10:]):
                        status = "✅" if c['treinou'] else "❌"
                        st.markdown(f"**{c['data']}** — {status} Treino | Alimentação: {c['alimentacao']} {('| Nota: ' + str(c['nota'])) if c['nota'] else ''} {('| ' + c['obs']) if c['obs'] else ''}")

            st.markdown("<hr>", unsafe_allow_html=True)
            if st.button("🔄 Encerrar e criar novo desafio", key="encerrar_desafio"):
                st.session_state.desafio_ativo = None
                st.rerun()


        # --- RODAPÉ ---
        st.markdown(
        "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
        "© 2026 Personal Trainer IA — Treinos Personalizados com IA · Quiz Com Prêmios"
        "</div>", unsafe_allow_html=True
        )

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "© 2026 Personal Trainer IA — Treinos Personalizados com IA · Quiz Com Prêmios"
    "</div>", unsafe_allow_html=True
)
