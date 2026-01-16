import streamlit as st
import plotly.express as px
from queries import get_startups_by_sector, get_scores_by_sector

st.set_page_config(page_title="Análise de Startups IoT", layout="wide")

st.title("📊 Análise de Startups IoT")
st.subheader("Ranking por Pontuação Técnica (Tech Score)")

# Filtros
setor = st.selectbox(
    "Selecione o setor",
    ["Todos", "Agri-IoT", "SmartCity", "Water-Ops", "Enviro-Tech", "Power-Grid"]
)

top_n = st.slider("Quantidade de startups no ranking", 5, 45, 10)

# Dados filtrados
df = get_startups_by_sector(setor).head(top_n)

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Tabela de Startups")
    st.dataframe(df, use_container_width=True)

with col2:
    st.subheader("📈 Tech Score por Startup")

    fig_bar = px.bar(
        df,
        x="startup_name",
        y="tech_score",
        color="setor",
        title="Top Startups por Tech Score",
        labels={
            "startup_name": "Startup",
            "tech_score": "Pontuação Técnica"
        }
    )

    st.plotly_chart(fig_bar, use_container_width=True)

# -------------------------
# BOXPLOT POR SETOR
# -------------------------
st.subheader("📦 Distribuição de Tech Score por Setor")

df_box = get_scores_by_sector()

fig_box = px.box(
    df_box,
    x="setor",
    y="tech_score",
    color="setor",
    title="Variabilidade do Tech Score por Setor",
    labels={
        "setor": "Setor",
        "tech_score": "Pontuação Técnica"
    }
)

st.plotly_chart(fig_box, use_container_width=True)

# -------------------------
# Radar Técnica da Startup"
# -------------------------
from queries import get_startup_radar

st.subheader("🕸 Maturidade Técnica da Startup")

startup_list = df["startup_name"].unique().tolist()

selected_startup = st.selectbox(
    "Escolha uma startup para análise detalhada",
    startup_list
)

radar_df = get_startup_radar(selected_startup)

radar_df = radar_df.T.reset_index()
radar_df.columns = ["Dimensão", "Score"]

fig_radar = px.line_polar(
    radar_df,
    r="Score",
    theta="Dimensão",
    line_close=True,
    title=f"Maturidade Técnica – {selected_startup}"
)

st.plotly_chart(fig_radar, use_container_width=True)
