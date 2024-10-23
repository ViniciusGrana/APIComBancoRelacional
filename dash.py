

import streamlit as st
import pandas as pd
import plotly.express as px
from query import conexao
from streamlit_option_menu import option_menu 

# **PRIMEIRA CONSULTA / ATUALIZAÇÃO DE DADOS**
query = "SELECT * FROM tb_carros"

# Carregar os dados
df = conexao(query)

# botao para atualizar
if st.button("Atualizar dados"):
    df = conexao(query)

# ****** ESTRUTURA LATERAL DE FILTROS
st.sidebar.header("Selecione o Filtro")

marca = st.sidebar.multiselect("Marca Selecionada", #nome do seletor 
                               options=df["marca"].unique(), #opçoes disponiveis sao unicas
                               default=df["marca"].unique(), #e por padrão as opçoes serão essas
                               )

modelo = st.sidebar.multiselect("Modelo Selecionado", #nome do seletor 
                               options=df["modelo"].unique(), #opçoes disponiveis sao unicas
                               default=df["modelo"].unique(), #e por padrão as opçoes serão essas
                               )

ano = st.sidebar.multiselect("Ano Selecionado", #nome do seletor 
                               options=df["ano"].unique(), #opçoes disponiveis sao unicas
                               default=df["ano"].unique(), #e por padrão as opçoes serão essas
                               )

valor = st.sidebar.multiselect("Valor Selecionado", #nome do seletor 
                               options=df["valor"].unique(), #opçoes disponiveis sao unicas
                               default=df["valor"].unique(), #e por padrão as opçoes serão essas
                               )

cor = st.sidebar.multiselect("Cor Selecionada", #nome do seletor 
                               options=df["cor"].unique(), #opçoes disponiveis sao unicas
                               default=df["cor"].unique(), #e por padrão as opçoes serão essas
                               )

numero_vendas = st.sidebar.multiselect("Numero de vendas Selecionado", #nome do seletor 
                               options=df["numero_vendas"].unique(), #opçoes disponiveis sao unicas
                               default=df["numero_vendas"].unique(), #e por padrão as opçoes serão essas
                               )

# Aplicar os filtros selecionados
df_selecionado = df[
    (df["marca"].isin(marca)) &
    (df["modelo"].isin(modelo)) &
    (df["ano"].isin(ano)) &
    (df["valor"].isin(valor)) &
    (df["cor"].isin(cor)) &
    (df["numero_vendas"].isin(numero_vendas))
]

# ****Exibir valores medios - estatistica
def Home():
    with st.expander("Valores"): #Cria uma caixa expansivel com um titulo
     mostrarDados = st.multiselect('Filter',df_selecionado, default=[])

    # Verifica se o usuario selecionou colunas para exibir
     if mostrarDados:
    # Exibe os dados filtrados pelas colunas selecionadas
        st.write(df_selecionado[mostrarDados])
    
    if not df_selecionado.empty:
        venda_total = df_selecionado['numero_vendas'].sum()
        venda_media = df_selecionado['numero_vendas'].mean()
        venda_mediana = df_selecionado["numero_vendas"].median()
        
        total1,total2,total3 = st.columns(3,gap="large")
        
        with total1:
            st.info("Valor Total de Vendas dos Carros", icon ="📌")
            st.metric(label="Total", value =f"{venda_total:,.0f}")
            
        with total2:
            st.info("Valor Medio das Vendas", icon ="📌")
            st.metric(label="Media", value =f"{venda_media:,.0f}")
            
        with total3:
            st.info("Valor Mediano dos Carros", icon ="📌")
            st.metric(label="Mediana", value =f"{venda_mediana:,.0f}")
    else:
        st.warning("Nenhum dado disponivel com os filtros selecionados")
        
    st.markdown("""-------""")
    
#  DEFINIR ESTATISTICAS

def graficos(df_selecionado):
   if df_selecionado.empty:
      st.warning("Nenhum dado disponivel para gerar gráficos")
      return 
   


   graf1, graf2, graf3, graf4, graf5 = st.tabs(["Gráfico de Barras", "Gráfico de Linhas","Gráfico de Pizza", "Gráfico de Dispersão", "Grafico de Altura"])


   with graf1:
      st.write("Gráfico de Barras") # Titulo

      investimento = df_selecionado.groupby("marca").count()[["valor"]].sort_values(by="valor", ascending=False)

      fig_valores = px.bar(investimento,
                           y="valor",
                           orientation="h",
                           title="Valores de Carros</b>",
                           color_discrete_sequence=["#0083b3"] )
                #EXIBE A FIGURA  E AJUSTE NA TELA PARA OCUPAR TODA A LARGURA DISPONIVEL    
      st.plotly_chart(fig_valores, use_container_width=True)
                                 
   with graf2:
        st.write("Grafico de Linhas")                          
        dados = df_selecionado.groupby("marca").count()[["valor"]]
    
        fig_valores2 = px.line(dados,
                           x=dados.index,
                           y="valor",
                           title="<b>Valores por Marca</b>",
                           color_discrete_sequence=["#0083b8"])
    
        st.plotly_chart(fig_valores2,use_container_width=True)
    
    
    
        with graf3:
            st.write("Grafico de Pizza")
            dados2 = df_selecionado.groupby("marca").sum()[["valor"]]
        
            fig_valores3 =px.pie(dados2,
                             values="valor", #Valores que serão representados 
                             names=dados2.index, #Os nomes (marcas) que irão rotular
                             title="<b>Distribuição de valores por marca</b>"
                             )
        
            st.plotly_chart(fig_valores3,use_container_width=True)
        
        with graf4:
            st.write("Grafico de disperção")
            dados3 = df_selecionado.melt(id_vars=["marca"], value_vars=["valor"])
        
            fig_valores4 = px.scatter(dados3,
                                  x="marca",
                                  y="value",
                                  color='variable',
                                  title="<b>Dispersão de valores por marca</b>"
                                  )
        
            st.plotly_chart(fig_valores4,use_container_width=True)
            
        with graf5:
            st.write("Total de Carros Vendidos por Ano de Fabricação")

    # Agrupar os dados pelo ano de fabricação e somar o número de vendas
            dados_ano_vendas = df_selecionado.groupby('ano')['numero_vendas'].sum().reset_index()

    # Criar o gráfico de barras
            fig_valores5 = px.bar(
                dados_ano_vendas,
                x="ano",
                y="numero_vendas",
                title="<b>Total de Carros Vendidos por Ano de Fabricação</b>",
                labels={'numero_vendas': 'Total de Carros Vendidos', 'ano': 'Ano de Fabricação'}
    )

    # Exibir o gráfico no Streamlit
            st.plotly_chart(fig_valores5, use_container_width=True)
              
        
def barraprogresso():
    valorAtual = df_selecionado["numero_vendas"].sum()
    percentual = round((valorAtual / objetivo * 100))
    objetivo = 200000
    
    if percentual > 100:
        st.subheader("Valores Atingidos!!!")
        
    else:
        st.write(f"Voce tem {percentual}% de {objetivo}, Corra atras filhão!")
        mybar = st.progress(0)
        for percentualCompleto in range(percentual):
            mybar.progress(percentualCompleto + 1, text="Alvo %")

# MENU LATERAL
def menuLateral():
    with st.sidebar:
        selecionado = option_menu(menu_title="Menu", options=["Home",
                                  "Progresso"], icons=["house", "eye"], menu_icon="cast",
                                  default_index=0)
        
        if selecionado == "Home":
            st.subheader(f"Página:{selecionado}")
            Home()
            graficos(df_selecionado)

        if selecionado == "Progresso":
            st.subheader(f"Página:{selecionado}")
            barraprogresso()
            graficos(df_selecionado)

menuLateral()

   
