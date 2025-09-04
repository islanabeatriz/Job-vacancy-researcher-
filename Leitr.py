import pandas as pd
import streamlit as st
import datetime
import webbrowser

st.set_page_config(page_title="📋 Dashboard de Vagas QA", layout="wide")
st.title("📋 Dashboard de Vagas de Testador de QA - LinkedIn")

# --------------------------
# Função para carregar CSV de forma segura
# --------------------------
def load_csv():
    df = pd.read_csv("linkedin_jobs.csv")
    # Garantir que a coluna 'Data' exista
    if 'Data' not in df.columns:
        df['Data'] = pd.NaT  # datetime nulo
    else:
        df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
    return df

# --------------------------
# Carregar CSV inicial
# --------------------------
df = load_csv()

# --------------------------
# Botão atualizar CSV
# --------------------------
if st.button("🔄 Atualizar CSV"):
    df = load_csv()  # recarrega o CSV
    st.success("CSV atualizado!")

# --------------------------
# Filtros
# --------------------------
st.sidebar.header("Filtros")
keyword = st.sidebar.text_input("Palavra-chave no título:")
empresas = df['Empresa'].unique().tolist()
empresa_filter = st.sidebar.multiselect("Filtrar por empresa:", empresas)

if 'Localização' in df.columns:
    localizacoes = df['Localização'].unique().tolist()
    local_filter = st.sidebar.multiselect("Filtrar por localização:", localizacoes)
else:
    local_filter = []

filtered_df = df.copy()
if keyword:
    filtered_df = filtered_df[filtered_df['Título'].str.contains(keyword, case=False, na=False)]
if empresa_filter:
    filtered_df = filtered_df[filtered_df['Empresa'].isin(empresa_filter)]
if local_filter:
    filtered_df = filtered_df[filtered_df['Localização'].isin(local_filter)]

# --------------------------
# Destaque visual seguro
# --------------------------
def highlight_new(row):
    if 'Data' in row.index and pd.notnull(row['Data']):
        days_diff = (datetime.datetime.now() - row['Data']).days
        if days_diff <= 7:
            return ['background-color:  #A9A9A9']*len(row)  # amarelo pastel
    return ['background-color: #C0C0C0']*len(row)  # cinza claro

st.subheader("🆕 Tabela de Vagas")
st.dataframe(filtered_df.style.apply(highlight_new, axis=1)
 .set_properties(**{'color': "#000000", 'font-size': '14px'}))

# --------------------------
# Contadores e métricas
# --------------------------
st.subheader("📊 Métricas")
col1, col2, col3 = st.columns(3)
col1.metric("Vagas totais", len(filtered_df))
num_new = (filtered_df['Data'] >= pd.Timestamp.now() - pd.Timedelta(days=7)).sum()
col2.metric("Vagas novas (últimos 7 dias)", num_new)
col3.metric("Empresas distintas", filtered_df['Empresa'].nunique())

# --------------------------
# Gráficos
# --------------------------
st.subheader("📈 Gráficos")
col1, col2 = st.columns(2)

with col1:
    st.write("Vagas por empresa")
    st.bar_chart(filtered_df['Empresa'].value_counts(), use_container_width=True)

with col2:
    if 'Localização' in filtered_df.columns:
        st.write("Vagas por localização")
        st.bar_chart(filtered_df['Localização'].value_counts(), use_container_width=True)

# --------------------------
# Abrir vaga no navegador
# --------------------------
st.subheader("🔗 Abrir vaga no LinkedIn")
job_index = st.number_input(
    "Digite o número da vaga (da tabela acima):",
    min_value=1,
    max_value=len(filtered_df),
    step=1
)
if st.button("Abrir vaga"):
    link = filtered_df.iloc[job_index-1]['Link']
    webbrowser.open(link)

# --------------------------
# Download CSV filtrado
# --------------------------
st.download_button(
    label="📥 Baixar CSV filtrado",
    data=filtered_df.to_csv(index=False, encoding='utf-8-sig'),
    file_name="vagas_filtradas.csv",
    mime="text/csv"
)
