import streamlit as st
import re
from datetime import datetime
import io
import csv
import math

# ------------------------------
# FUNÇÕES AUXILIARES
# ------------------------------

def validar_email(email):
    """Valida o formato de um e-mail."""
    regex = r"[^@]+@[^@]+\.[^@]+"
    return re.match(regex, email)

def get_icon(interest):
    """Retorna um emoji consoante o interesse."""
    i = interest.lower()
    if "cinema" in i:
        return "🎬"
    elif "música" in i:
        return "🎵"
    elif "fotografia" in i:
        return "📷"
    elif any(x in i for x in ["arte", "design", "ilustração", "pintura", "escultura", "moda", "animação", "publicidade", "comunicação visual", "arquitetura"]):
        return "🎨"
    elif any(x in i for x in ["programação", "software", "jogos", "robótica", "inteligência artificial", "cibersegurança", "hardware", "redes"]):
        return "💻"
    elif any(x in i for x in ["empreendedorismo", "negócios", "finanças", "investimentos", "marketing", "planeamento", "gestão"]):
        return "💼"
    elif any(x in i for x in ["psicologia", "comportamento", "neuro", "bem-estar", "autoconhecimento", "sociologia", "antropologia"]):
        return "🧠"
    elif any(x in i for x in ["serviço social", "direitos", "comunitário", "voluntariado", "sustentabilidade", "cidadania", "educação", "políticas"]):
        return "🤝"
    elif any(x in i for x in ["comunicação empresarial", "relações públicas", "mídias sociais", "eventos", "branding", "networking", "liderança"]):
        return "📢"
    elif any(x in i for x in ["reportagem", "investigação", "jornalismo", "redação", "telejornalismo", "entrevistas"]):
        return "📰"
    else:
        return "⭐"

def toggle_interest(interest):
    """Adiciona ou remove um interesse da lista."""
    if interest in st.session_state.selected_interesses:
        st.session_state.selected_interesses.remove(interest)
    else:
        st.session_state.selected_interesses.append(interest)

def obter_cursos_recomendados(selecionados):
    """Calcula os cursos recomendados com base numa lógica de pontuação ponderada."""
    recomendados = {}
    for curso, keywords in course_keywords.items():
        score = 0
        for inter in selecionados:
            inter_clean = inter.lower().strip()
            for kw in keywords:
                kw_clean = kw.lower().strip()
                if inter_clean == kw_clean:
                    score += 2  # correspondência exata
                elif kw_clean in inter_clean:
                    score += 1  # correspondência parcial
        if score > 0:
            recomendados[curso] = score
    return recomendados

# ------------------------------
# CONFIGURAÇÃO INICIAL
# ------------------------------
st.set_page_config(page_title="Orientação Vocacional", layout="wide")

# Inicialização das variáveis de sessão
if "page" not in st.session_state:
    st.session_state.page = "inicio"
if "selected_interesses" not in st.session_state:
    st.session_state.selected_interesses = []
if "verInteressesDev" not in st.session_state:
    st.session_state.verInteressesDev = False
if "dados_utilizadores" not in st.session_state:
    st.session_state.dados_utilizadores = []
if "mostrar_download" not in st.session_state:
    st.session_state.mostrar_download = False

# Lista de interesses reduzida (20 cartões)
interesses = [
    "Arte Digital",
    "Design Gráfico",
    "Fotografia",
    "Cinema",
    "Música",
    "Programação",
    "Desenvolvimento de Software",
    "Jogos Digitais",
    "Empreendedorismo",
    "Marketing Digital",
    "Psicologia",
    "Serviço Social",
    "Comunicação Empresarial",
    "Jornalismo",
    "Realidade Virtual",
    "Robótica",
    "Arquitetura",
    "Moda",
    "Publicidade",
    "Redes de Computadores"
]

# Lista de cursos disponíveis
cursos = [
    "Design de Comunicação",
    "Multimédia",
    "Jornalismo",
    "Comunicação Empresarial",
    "Empreendedorismo",
    "Gestão",
    "Gestão de Recursos Humanos",
    "Psicologia",
    "Serviço Social",
    "Informática"
]

# Dicionário de palavras-chave para cada curso
course_keywords = {
    "Design de Comunicação": ["arte", "design", "fotografia", "ilustração", "pintura", "escultura", "moda", "publicidade", "comunicação visual"],
    "Multimédia": ["animação", "cinema", "música", "edição de vídeo", "multimédia", "design gráfico", "fotografia"],
    "Jornalismo": ["reportagem", "investigação", "redação", "entrevistas", "mídia digital", "telejornalismo"],
    "Comunicação Empresarial": ["comunicação empresarial", "marketing", "branding", "relações públicas", "mídias sociais", "eventos", "networking"],
    "Empreendedorismo": ["empreendedorismo", "startups", "inovação", "negócios", "planeamento estratégico"],
    "Gestão": ["gestão", "planeamento", "liderança", "gestão de projectos", "negócios", "finanças", "investimentos", "economia"],
    "Gestão de Recursos Humanos": ["recursos humanos", "formação", "desenvolvimento de talentos", "cultura organizacional", "diversidade", "inclusão"],
    "Psicologia": ["psicologia", "comportamento humano", "neurociência", "bem-estar", "autoconhecimento"],
    "Serviço Social": ["serviço social", "direitos humanos", "engajamento comunitário", "voluntariado", "sustentabilidade", "cidadania"],
    "Informática": ["programação", "desenvolvimento de software", "jogos digitais", "realidade virtual", "robótica", "inteligência artificial", "ciência de dados", "cibersegurança", "hardware", "redes de computadores"]
}

# Dicionário de ícones para os cursos
course_icons = {
    "Design de Comunicação": "🎨",
    "Multimédia": "🖥️",
    "Jornalismo": "📰",
    "Comunicação Empresarial": "📢",
    "Empreendedorismo": "💼",
    "Gestão": "📊",
    "Gestão de Recursos Humanos": "🤝",
    "Psicologia": "🧠",
    "Serviço Social": "🤝",
    "Informática": "💻"
}

# ------------------------------
# PÁGINAS
# ------------------------------

# Página 0: Ecrã de Boas-Vindas
if st.session_state.page == "inicio":
    # Banner de boas-vindas (full width)
    st.markdown(
        """
        <div style="background-color:#4a90e2; padding:50px; border-radius:10px; text-align:center; color:white;">
            <h1 style="font-size:3em;">Descobre o teu Futuro no ISMT</h1>
            <p style="font-size:1.5em; max-width:800px; margin:0 auto;">
                Bem-vindo(a) ao nosso espaço de Orientação Vocacional! 
                Vem descobrir qual dos nossos cursos combina melhor com os teus interesses 
                e inicia uma jornada que pode mudar o teu futuro. 
                Prepara-te para explorar um mundo de possibilidades e encontrar a formação 
                que mais se adequa a ti!
            </p>
            <img src="https://ismt.pt/ismt/img/logo-ismt.png" alt="Boas-vindas" style="max-width:70%; margin-top:20px;">
            <br><br>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # CSS para estilo do botão principal e do botão de administração
    st.markdown(
        """
        <style>
        /* Botão principal (call-to-action) */
        .main-button .stButton button {
            background-color: #ff7f50;
            color: white;
            font-size: 1.5em;
            font-weight: bold;
            padding: 1em 3em;
            border-radius: 10px;
            border: none;
            box-shadow: 0px 6px 8px rgba(0,0,0,0.3);
            transition: background-color 0.3s ease, transform 0.3s ease;
        }
        .main-button .stButton button:hover {
            background-color: #ff9068;
            transform: scale(1.05);
            cursor: pointer;
        }

        /* Botão discreto (admin) */
        .admin-button .stButton button {
            background-color: transparent;
            color: #aaa;
            font-size: 0.8em;
            text-decoration: underline;
            border: none;
        }
        .admin-button .stButton button:hover {
            color: #888;
            cursor: pointer;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Botão principal de ação, centralizado
    with st.container():
        st.markdown('<div class="main-button" style="text-align:center; margin-top:30px;">', unsafe_allow_html=True)
        if st.button("📝 Indicar os meus Interesses 📝", key="main_button"):
            st.session_state.page = "selecao_interesses"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Espaçamento extra
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Botão discreto para administração (Descarregar Dados)
    with st.container():
        st.markdown('<div class="admin-button" style="text-align:center;">', unsafe_allow_html=True)
        if st.button("Descarregar Dados (Admin)", key="download_data_button"):
            st.session_state.mostrar_download = True
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Se a opção de download foi acionada, solicitar password
    if st.session_state.mostrar_download:
        admin_password = st.text_input("Insira a password de administração", type="password")
        if admin_password == "ismt#2526":
            st.markdown("#### Dados Recolhidos")
            buffer = io.StringIO()
            writer = csv.writer(buffer)
            writer.writerow(["Nome", "Email", "Interesses", "Cursos_Recomendados"])
            for entry in st.session_state.dados_utilizadores:
                writer.writerow([
                    entry["nome"], 
                    entry["email"], 
                    entry["interesses"], 
                    entry["cursos_recomendados"]
                ])
            now = datetime.now()
            date_str = now.strftime("%d%m%Y")
            time_str = now.strftime("%H%M%S")
            filename = f"dados_recolhidos_feira_{date_str}_{time_str}.csv"
            st.download_button("Descarregar Dados", data=buffer.getvalue(), file_name=filename, mime="text/csv")

# Página 1: Seleção de Interesses
elif st.session_state.page == "selecao_interesses":
    st.markdown(
        '<div class="main-header"><h1>Seleciona os Teus Interesses</h1><p>Clica nos cartões para indicar os teus hobbies!</p></div>',
        unsafe_allow_html=True
    )
    total_interesses = len(interesses)
    colunas_por_linha = 5  # Reduzido para 5 botões por linha
    linhas = math.ceil(total_interesses / colunas_por_linha)

    for i in range(linhas):
        cols = st.columns(colunas_por_linha)
        for j in range(colunas_por_linha):
            index = i * colunas_por_linha + j
            if index < total_interesses:
                inter = interesses[index]
                icon = get_icon(inter)
                label = f"{icon} {inter}"
                if inter in st.session_state.selected_interesses:
                    label = f"✅ {label}"
                cols[j].button(label, key=f"card_{index}", on_click=lambda i=inter: toggle_interest(i))

    if st.session_state.verInteressesDev:
        st.markdown("### Interesses Selecionados:")
        st.write(st.session_state.selected_interesses)
    
    if st.button("Ver cursos compatíveis com os meus interesses"):
        st.session_state.page = "resultado_cursos"
        st.rerun()

# Página 2: Resultados e Contacto
elif st.session_state.page == "resultado_cursos":
    st.markdown(
        '<div class="main-header"><h1>Cursos Compatíveis no ISMT</h1><p>Estes cursos combinam com os teus interesses!</p></div>',
        unsafe_allow_html=True
    )

    # Botão para voltar à seleção de interesses
    if st.button("Voltar à seleção de interesses"):
        st.session_state.page = "selecao_interesses"
        st.rerun()
    
    recomendados = obter_cursos_recomendados(st.session_state.selected_interesses)
    max_score = max(recomendados.values()) if recomendados else 0
    threshold = 0.5 * max_score

    for curso in cursos:
        if curso in recomendados:
            score = recomendados[curso]
            icon = course_icons.get(curso, "⭐")
            if score >= threshold:
                st.markdown(f"**:star: {icon} {curso} (compatibilidade: {score})**")
            else:
                st.markdown(f"{icon} {curso} (compatibilidade: {score})")
        else:
            st.markdown(curso)

    st.markdown("---")
    st.markdown("Para mais informações, indica o teu nome e e-mail:")
    nome = st.text_input("Nome")
    email = st.text_input("E-mail")

    if st.button("Enviar"):
        if nome and email:
            if not validar_email(email):
                st.error("Por favor, introduz um e-mail válido.")
            else:
                cursos_recomendados = ", ".join([
                    f"{curso} ({score})" 
                    for curso, score in sorted(recomendados.items(), key=lambda item: item[1], reverse=True)
                ])
                interesses_selecionados = ", ".join(st.session_state.selected_interesses)
                st.session_state.dados_utilizadores.append({
                    "nome": nome,
                    "email": email,
                    "interesses": interesses_selecionados,
                    "cursos_recomendados": cursos_recomendados
                })
                st.success("Obrigado! Em breve entraremos em contacto.")
        else:
            st.error("Por favor, preenche ambos os campos: nome e e-mail.")

    if st.button("Começar de Novo"):
        st.session_state.selected_interesses = []
        st.session_state.page = "inicio"
        st.session_state.verInteressesDev = False
        st.rerun()
