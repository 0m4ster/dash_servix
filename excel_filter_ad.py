import streamlit as st
import pandas as pd
from datetime import datetime, timedelta # Importar timedelta
import plotly.graph_objects as go
from facta_token_manager import get_facta_token, is_facta_token_valid
from config import(
     FACTA_DEFAULT_TOKEN,
     FACTA_API_URLS
)

def render_excel_filter_ad_page():
    """Renderiza a página específica para filtrar clientes com utm source = 'ad'."""
    
    # Header da página
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #2c3e50; margin-bottom: 10px;">🎯 Filtro de Clientes UTM Source = "ad"</h1>
        <p style="color: #7f8c8d; font-size: 16px;">Upload e filtro automático de clientes com utm source = "ad"</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Seção de upload
    st.markdown("""
    <div style="background-color: #ffffff; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin: 20px 0;">
        <h3 style="color: #2c3e50; text-align: center; margin-bottom: 25px;">📁 Upload de Arquivo Excel</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Upload do arquivo (sidebar)
    uploaded_file = st.sidebar.file_uploader(
        "📂 Carregar arquivo Excel",
        type=['xlsx', 'xls'],
        help="Faça upload de um arquivo Excel contendo a coluna 'utm source'"
    )
    
    if uploaded_file is not None:
        try:
            # Ler o arquivo Excel
            df_excel = pd.read_excel(uploaded_file)
            
            # Forçar coluna CPF como string imediatamente após a leitura
            if 'CPF' in df_excel.columns:
                df_excel['CPF'] = df_excel['CPF'].astype(str)
            
            # Verificar se a coluna utm source existe
            if 'utm source' not in df_excel.columns:
                st.error("❌ Coluna 'utm source' não encontrada no arquivo.")
                st.info("📋 Colunas encontradas no arquivo:")
                for col in df_excel.columns:
                    st.markdown(f"- {col}")
                return
            
            # Processar dados
            df_processed = process_excel_data(df_excel)
            
            if df_processed is not None:
                # Seção de filtro de datas
                st.markdown("---")
                st.markdown("""
                <div style="background-color: #e3f2fd; padding: 20px; border-radius: 10px; border-left: 4px solid #2196f3; margin: 20px 0;">
                    <h4 style="color: #2c3e50; margin-bottom: 15px;">📅 Filtro de Datas - Data Criacao</h4>
                    <p style="color: #7f8c8d; margin: 0;">Filtre os clientes por período de criação</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Verificar se a coluna Data Criacao existe e tem dados válidos
                if 'Data Criacao' in df_processed.columns:
                    # Manter apenas datas válidas para o range de seleção
                    df_datas_validas_para_range = df_processed.dropna(subset=['Data Criacao'])
                    
                    if not df_datas_validas_para_range.empty:
                        # Obter min e max das datas válidas
                        data_min = df_datas_validas_para_range['Data Criacao'].min()
                        data_max = df_datas_validas_para_range['Data Criacao'].max()
                        
                        # Interface de filtro de datas
                        col_data1, col_data2 = st.columns(2)
                        
                        with col_data1:
                            data_inicio = st.date_input(
                                "📅 Data de Início",
                                value=data_min.date(),
                                min_value=data_min.date(),
                                max_value=data_max.date(),
                                help="Selecione a data de início do filtro"
                            )
                        
                        with col_data2:
                            data_fim = st.date_input(
                                "📅 Data de Fim",
                                value=data_max.date(),
                                min_value=data_min.date(),
                                max_value=data_max.date(),
                                help="Selecione a data de fim do filtro"
                            )
                        
                        # Converter para datetime para comparação
                        data_inicio_dt = pd.Timestamp(data_inicio)
                        # Ajustar data_fim_dt para incluir todo o dia selecionado
                        data_fim_dt = pd.Timestamp(data_fim) + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)
                        
                        # Aplicar filtro de datas de forma flexível
                        # Primeiro, filtrar por datas válidas
                        df_filtrado_datas_validas = df_processed[
                            (df_processed['Data Criacao'] >= data_inicio_dt) & 
                            (df_processed['Data Criacao'] <= data_fim_dt)
                        ].copy()
                        
                        # Depois, incluir registros com Data Criacao NaT (para não perder clientes)
                        df_datas_nat = df_processed[df_processed['Data Criacao'].isna()].copy()
                        
                        # Combinar ambos os DataFrames
                        df_filtrado_datas = pd.concat([df_filtrado_datas_validas, df_datas_nat], ignore_index=True)
                        
                        # Métricas do filtro de datas
                        col_metricas_data1, col_metricas_data2, col_metricas_data3 = st.columns(3)
                        
                        with col_metricas_data1:
                            st.markdown("""
                            <div style="text-align: center; padding: 15px; background-color: #2196f3; border-radius: 8px; color: white;">
                                <h5 style="margin: 0 0 5px 0;">📅 Clientes no Período</h5>
                                <p style="font-size: 20px; font-weight: bold; margin: 0;">{}</p>
                            </div>
                            """.format(f"{len(df_filtrado_datas):,}"), unsafe_allow_html=True)
                        
                        with col_metricas_data2:
                            percentual_periodo = (len(df_filtrado_datas) / len(df_processed) * 100) if len(df_processed) > 0 else 0
                            st.markdown("""
                            <div style="text-align: center; padding: 15px; background-color: #4caf50; border-radius: 8px; color: white;">
                                <h5 style="margin: 0 0 5px 0;">📊 % do Total</h5>
                                <p style="font-size: 20px; font-weight: bold; margin: 0;">{:.1f}%</p>
                            </div>
                            """.format(percentual_periodo), unsafe_allow_html=True)
                        
                        with col_metricas_data3:
                            st.markdown("""
                            <div style="text-align: center; padding: 15px; background-color: #ff9800; border-radius: 8px; color: white;">
                                <h5 style="margin: 0 0 5px 0;">📋 Total Original</h5>
                                <p style="font-size: 20px; font-weight: bold; margin: 0;">{}</p>
                            </div>
                            """.format(f"{len(df_processed):,}"), unsafe_allow_html=True)
                        
                        # Mostrar distribuição dos UTM sources
                        utm_distribution = df_filtrado_datas['utm source'].value_counts()
                        
                        # Permitir escolha do UTM source para filtrar
                        st.markdown("---")
                        st.markdown("""
                        <div style="background-color: #fff3e0; padding: 20px; border-radius: 10px; border-left: 4px solid #ff9800; margin: 20px 0;">
                            <h4 style="color: #2c3e50; margin-bottom: 15px;">🎯 Filtro por UTM Source (Opcional)</h4>
                            <p style="color: #7f8c8d; margin: 0;">Escolha se deseja filtrar por UTM source específico ou ver todos os clientes</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Opção para escolher UTM source
                        # Usar os UTMs disponíveis no df_filtrado_datas para a seleção
                        utm_sources_disponiveis = sorted(df_filtrado_datas['utm source'].unique())
                        utm_selecionado = st.selectbox(
                            "🔍 Selecione o UTM Source para filtrar (ou 'Todos' para ver todos):",
                            options=['Todos'] + list(utm_sources_disponiveis),
                            help="Escolha 'Todos' para ver todos os clientes do período ou selecione um UTM source específico"
                        )
                        
                        # Aplicar filtro baseado na seleção
                        if utm_selecionado == 'Todos':
                            df_filtered_ad_temp = df_filtrado_datas.copy()
                        else:
                            # O filtro já está normalizado para minúsculas em process_excel_data
                            df_filtered_ad_temp = df_filtrado_datas[df_filtrado_datas['utm source'] == utm_selecionado].copy()
                        
                        # Remover duplicatas baseado no CPF (se a coluna existir)
                        df_filtered_ad = handle_cpf_deduplication(df_filtered_ad_temp)
                        
                    else:
                        st.warning("⚠️ Nenhuma data válida encontrada na coluna 'Data Criacao' para definir o período.")
                        # Se não há datas válidas, não podemos aplicar filtro de data.
                        # Apenas aplicar o filtro de UTM 'ad' e deduplicar.
                        df_filtered_ad_temp = df_processed[df_processed['utm source'] == 'ad'].copy()
                        df_filtered_ad = handle_cpf_deduplication(df_filtered_ad_temp)
                        st.info(f"📊 Aplicando filtro apenas por UTM source = 'ad': {len(df_filtered_ad):,} clientes.")
                        # Definir df_filtrado_datas como df_processed para métricas posteriores
                        df_filtrado_datas = df_processed.copy()
                
                else:
                    st.warning("⚠️ Coluna 'Data Criacao' não encontrada no arquivo. Aplicando filtro apenas por UTM source = 'ad'.")
                    # Se não há coluna de data, aplicar filtro apenas por utm source
                    df_filtered_ad_temp = df_processed[df_processed['utm source'] == 'ad'].copy()
                    
                    # Remover duplicatas baseado no CPF (se a coluna existir)
                    df_filtered_ad = handle_cpf_deduplication(df_filtered_ad_temp)
                    # Definir df_filtrado_datas como df_processed para métricas posteriores
                    df_filtrado_datas = df_processed.copy()
                
                # Métricas do filtro aplicado (data + utm source)
                st.markdown("---")
                st.markdown("""
                <div style="background-color: #e8f5e9; padding: 20px; border-radius: 10px; border-left: 4px solid #4caf50; margin: 20px 0;">
                    <h4 style="color: #2c3e50; margin-bottom: 15px;">🎯 Resultado do Filtro Combinado</h4>
                    <p style="color: #7f8c8d; margin: 0;">Clientes com UTM Source = "ad" no período selecionado</p>
                </div>
                """, unsafe_allow_html=True)
                
                col_metrics1, col_metrics2, col_metrics3, col_metrics4 = st.columns(4)
                
                with col_metrics1:
                     st.markdown("""
                     <div style="text-align: center; padding: 20px; background-color: #4caf50; border-radius: 12px; color: white; min-height: 120px; display: flex; flex-direction: column; justify-content: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                         <h5 style="margin: 0 0 10px 0; font-size: 14px; opacity: 0.9;">✅ Clientes Filtrados</h5>
                         <p style="font-size: 24px; font-weight: bold; margin: 0;">{}</p>
                     </div>
                     """.format(f"{len(df_filtered_ad):,}"), unsafe_allow_html=True)
                 
                with col_metrics2:
                     total_original = len(df_processed)
                     percentual = (len(df_filtered_ad) / total_original * 100) if total_original > 0 else 0
                     st.markdown("""
                     <div style="text-align: center; padding: 20px; background-color: #2196f3; border-radius: 12px; color: white; min-height: 120px; display: flex; flex-direction: column; justify-content: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                         <h5 style="margin: 0 0 10px 0; font-size: 14px; opacity: 0.9;">📊 % do Total</h5>
                         <p style="font-size: 24px; font-weight: bold; margin: 0;">{:.1f}%</p>
                     </div>
                     """.format(percentual), unsafe_allow_html=True)
                 
                with col_metrics3:
                     # Usar len(df_filtrado_datas) que já foi definido acima
                     st.markdown("""
                     <div style="text-align: center; padding: 20px; background-color: #ff9800; border-radius: 12px; color: white; min-height: 120px; display: flex; flex-direction: column; justify-content: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                         <h5 style="margin: 0 0 10px 0; font-size: 14px; opacity: 0.9;">📅 No Período</h5>
                         <p style="font-size: 24px; font-weight: bold; margin: 0;">{}</p>
                     </div>
                     """.format(f"{len(df_filtrado_datas):,}"), unsafe_allow_html=True)
                 
                with col_metrics4:
                     st.markdown("""
                     <div style="text-align: center; padding: 20px; background-color: #f44336; border-radius: 12px; color: white; min-height: 120px; display: flex; flex-direction: column; justify-content: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                         <h5 style="margin: 0 0 10px 0; font-size: 14px; opacity: 0.9;">📋 Total Original</h5>
                         <p style="font-size: 24px; font-weight: bold; margin: 0;">{}</p>
                     </div>
                     """.format(f"{total_original:,}"), unsafe_allow_html=True)
                
                # Exibir dados filtrados
                st.markdown("---")
                st.markdown("""
                <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin: 20px 0;">
                    <h4 style="color: #2c3e50; margin-bottom: 15px;">📊 Clientes Filtrados - Período + UTM Source = "ad" ({})</h4>
                </div>
                """.format(f"{len(df_filtered_ad):,} registros"), unsafe_allow_html=True)
                
                st.dataframe(df_filtered_ad, use_container_width=True, hide_index=True)
                
                # Seção de CPFs dos clientes filtrados
                if 'CPF' in df_filtered_ad.columns:
                    st.markdown("---")
                    st.markdown("""
                    <div style="background-color: #e8f5e9; padding: 20px; border-radius: 10px; border-left: 4px solid #4caf50; margin: 20px 0;">
                        <h4 style="color: #2c3e50; margin-bottom: 15px;">🆔 CPFs Únicos dos Clientes Filtrados</h4>
                        <p style="color: #7f8c8d; margin: 0;">Lista de CPFs únicos dos clientes com utm source = "ad" no período selecionado (duplicatas removidas)</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Debug: mostrar informações detalhadas sobre CPFs
                    with st.expander("🔍 Debug - Informações dos CPFs"):
                        st.write("**Estatísticas dos CPFs:**")
                        st.write(f"- Total de registros: {len(df_filtered_ad):,}")
                        st.write(f"- CPFs únicos: {df_filtered_ad['CPF'].nunique():,}")
                        st.write(f"- CPFs nulos: {df_filtered_ad['CPF'].isna().sum():,}")
                        st.write(f"- CPFs vazios: {(df_filtered_ad['CPF'].astype(str).str.strip() == '').sum():,}")
                        
                        # Mostrar alguns exemplos de CPFs
                        st.write("**Exemplos de CPFs:**")
                        cpfs_exemplos = df_filtered_ad['CPF'].dropna().head(10).tolist()
                        for i, cpf in enumerate(cpfs_exemplos, 1):
                            st.write(f"{i}. {cpf}")
                
                    # Extrair CPFs únicos (já sem duplicatas devido ao filtro anterior)
                    cpfs_unicos = df_filtered_ad['CPF'].dropna().unique()
                    cpfs_limpos = [str(cpf).strip() for cpf in cpfs_unicos if str(cpf).strip() not in ['nan', 'None', '']]
                    
                    # Métricas dos CPFs
                    col_cpf1, col_cpf2, col_cpf3 = st.columns(3)
                    
                    with col_cpf1:
                         st.markdown("""
                         <div style="text-align: center; padding: 20px; background-color: #4caf50; border-radius: 12px; color: white; min-height: 120px; display: flex; flex-direction: column; justify-content: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                             <h5 style="margin: 0 0 10px 0; font-size: 14px; opacity: 0.9;">🆔 CPFs Únicos</h5>
                             <p style="font-size: 24px; font-weight: bold; margin: 0;">{}</p>
                         </div>
                         """.format(f"{len(cpfs_limpos):,}"), unsafe_allow_html=True)
                     
                    with col_cpf2:
                         st.markdown("""
                         <div style="text-align: center; padding: 20px; background-color: #2196f3; border-radius: 12px; color: white; min-height: 120px; display: flex; flex-direction: column; justify-content: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                             <h5 style="margin: 0 0 10px 0; font-size: 14px; opacity: 0.9;">📊 Total de Registros</h5>
                             <p style="font-size: 24px; font-weight: bold; margin: 0;">{}</p>
                         </div>
                         """.format(f"{len(df_filtered_ad):,}"), unsafe_allow_html=True)
                     
                    with col_cpf3:
                         # Como já removemos duplicatas, este valor deve ser 0
                         st.markdown("""
                         <div style="text-align: center; padding: 20px; background-color: #ff9800; border-radius: 12px; color: white; min-height: 120px; display: flex; flex-direction: column; justify-content: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                             <h5 style="margin: 0 0 10px 0; font-size: 14px; opacity: 0.9;">✅ Sem Duplicatas</h5>
                             <p style="font-size: 24px; font-weight: bold; margin: 0;">0</p>
                         </div>
                         """.format(f"{len(cpfs_limpos):,}"), unsafe_allow_html=True)
                    
                    # Exibir CPFs em formato de lista
                    st.markdown("---")
                    st.markdown("""
                    <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin: 20px 0;">
                        <h4 style="color: #2c3e50; margin-bottom: 15px;">📋 Lista de CPFs Únicos ({})</h4>
                        <p style="color: #7f8c8d; margin: 0;">Todos os CPFs são únicos - duplicatas removidas automaticamente</p>
                    </div>
                    """.format(f"{len(cpfs_limpos):,} CPFs únicos"), unsafe_allow_html=True)
                    
                    # Criar DataFrame apenas com CPFs
                    df_cpfs = pd.DataFrame({'CPF': cpfs_limpos})
                    st.dataframe(df_cpfs, use_container_width=True, hide_index=True)
                    
                    # Download dos CPFs
                    if cpfs_limpos:
                        st.markdown("---")
                        
                        # Download como CSV
                        csv_cpfs = df_cpfs.to_csv(index=False)
                        st.download_button(
                            label="📥 Download CSV - Lista de CPFs (Período + UTM Source = 'ad')",
                            data=csv_cpfs,
                            file_name=f"cpfs_utm_source_ad_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                         
                        # Consulta na API FACTA - Andamento de Propostas
                        st.markdown("---")
                        st.markdown("""
                        <div style="background-color: #e3f2fd; padding: 20px; border-radius: 10px; border-left: 4px solid #2196f3; margin: 20px 0;">
                            <h4 style="color: #2c3e50; margin-bottom: 15px;">🔍 Consulta na API FACTA - Andamento de Propostas</h4>
                            <p style="color: #7f8c8d; margin: 0;">Consulta todas as propostas no período (últimos 30 dias) e filtra pelos CPFs encontrados</p>
                        </div>
                        """, unsafe_allow_html=True)
                         
                        # Token FACTA - automático
                        token_facta = (
                            st.session_state.get('token_facta')
                            or get_facta_token()
                            or (FACTA_DEFAULT_TOKEN if FACTA_DEFAULT_TOKEN else None)
                        )
                        
                        if token_facta and (is_facta_token_valid() if callable(is_facta_token_valid) else True):
                            st.success("✅ Token FACTA carregado automaticamente")
                        else:
                            token_facta = None
                            st.warning("⚠️ Token FACTA não encontrado. Gere um token na aba '🔑 Geração de Token' primeiro.")
                            st.info("💡 Após gerar o token FACTA, volte para esta aba para consultar os CPFs.")
                        
                        if token_facta and cpfs_limpos:
                            if st.sidebar.button("🔍 Consultar Todas as Propostas na FACTA"):
                                with st.spinner("Consultando todas as propostas no período..."):
                                    try:
                                        # Consultar CPFs na FACTA
                                        resultados_facta = consultarandamento_propostas_facta(cpfs_limpos, token_facta)
                                        
                                        if resultados_facta is not None and not resultados_facta.empty:
                                            # Exibir resultados
                                            st.markdown("---")
                                            st.markdown("""
                                            <div style="background-color: #e8f5e9; padding: 20px; border-radius: 10px; border-left: 4px solid #4caf50; margin: 20px 0;">
                                                <h4 style="color: #2c3e50; margin-bottom: 15px;">✅ Resultados da Consulta FACTA</h4>
                                                <p style="color: #7f8c8d; margin: 0;">Todas as propostas no período filtradas pelos CPFs consultados</p>
                                            </div>
                                            """, unsafe_allow_html=True)
                                            
                                            # Métricas da consulta
                                            col_facta1, col_facta2, col_facta3, col_facta4, col_facta5, col_facta6 = st.columns(6)
                                             
                                            with col_facta1:
                                                 st.markdown("""
                                                 <div style="text-align: center; padding: 20px; background-color: #4caf50; border-radius: 12px; color: white; min-height: 120px; display: flex; flex-direction: column; justify-content: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                                                     <h5 style="margin: 0 0 10px 0; font-size: 14px; opacity: 0.9;">✅ Propostas</h5>
                                                     <p style="font-size: 24px; font-weight: bold; margin: 0;">{}</p>
                                                 </div>
                                                 """.format(f"{len(resultados_facta):,}"), unsafe_allow_html=True)
                                             
                                            with col_facta2:
                                                 st.markdown("""
                                                 <div style="text-align: center; padding: 20px; background-color: #2196f3; border-radius: 12px; color: white; min-height: 120px; display: flex; flex-direction: column; justify-content: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                                                     <h5 style="margin: 0 0 10px 0; font-size: 14px; opacity: 0.9;">📊 Leads</h5>
                                                     <p style="font-size: 24px; font-weight: bold; margin: 0;">{}</p>
                                                 </div>
                                                 """.format(f"{len(cpfs_limpos):,}"), unsafe_allow_html=True)
                                             
                                            with col_facta3:
                                                 percentual_encontrado = (len(resultados_facta) / len(cpfs_limpos) * 100) if cpfs_limpos else 0
                                                 st.markdown("""
                                                 <div style="text-align: center; padding: 20px; background-color: #ff9800; border-radius: 12px; color: white; min-height: 120px; display: flex; flex-direction: column; justify-content: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                                                     <h5 style="margin: 0 0 10px 0; font-size: 14px; opacity: 0.9;">📈 Contratos Gerados</h5>
                                                     <p style="font-size: 24px; font-weight: bold; margin: 0;">{:.1f}%</p>
                                                 </div>
                                                 """.format(percentual_encontrado), unsafe_allow_html=True)
                                             
                                            with col_facta4:
                                                 # Calcular total de valores AF das propostas encontradas
                                                 total_af_encontrado = resultados_facta['valor_af'].sum() if 'valor_af' in resultados_facta.columns else 0
                                                 st.markdown("""
                                                 <div style="text-align: center; padding: 20px; background-color: #e91e63; border-radius: 12px; color: white; min-height: 120px; display: flex; flex-direction: column; justify-content: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                                                     <h5 style="margin: 0 0 10px 0; font-size: 14px; opacity: 0.9;">💰 Total Valor AF</h5>
                                                     <p style="font-size: 24px; font-weight: bold; margin: 0;">R$ {}</p>
                                                 </div>
                                                 """.format(f"{total_af_encontrado:,.2f}"), unsafe_allow_html=True)
                                             
                                            with col_facta5:
                                                 # Contratos pagos (status que indica pagamento)
                                                 contratos_pagos = resultados_facta[
                                                     resultados_facta['status_proposta'].str.contains('PAGO|PAGAMENTO|EFETIVADO|CONCLUIDO', case=False, na=False)
                                                 ] if 'status_proposta' in resultados_facta.columns else pd.DataFrame()
                                                 
                                                 # Calcular total de valores AF dos contratos pagos
                                                 total_af_pagos = contratos_pagos['valor_af'].sum() if not contratos_pagos.empty and 'valor_af' in contratos_pagos.columns else 0
                                                 
                                                 st.markdown("""
                                                 <div style="text-align: center; padding: 20px; background-color: #8bc34a; border-radius: 12px; color: white; min-height: 120px; display: flex; flex-direction: column; justify-content: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                                                     <h5 style="margin: 0 0 10px 0; font-size: 14px; opacity: 0.9;">💳 Contratos Pagos</h5>
                                                     <p style="font-size: 24px; font-weight: bold; margin: 0;">R$ {}</p>
                                                     <small style="font-size: 12px; opacity: 0.8; margin-top: 5px;">{} contratos</small>
                                                 </div>
                                                 """.format(f"{total_af_pagos:,.2f}", f"{len(contratos_pagos):,}"), unsafe_allow_html=True)
                                             
                                            with col_facta6:
                                                 # Aguardando assinatura (status que indica pendência)
                                                 aguardando_assinatura = resultados_facta[
                                                     resultados_facta['status_proposta'].str.contains('AGUARDANDO|PENDENTE|ASSINATURA|ANALISE|CRIVO', case=False, na=False)
                                                 ] if 'status_proposta' in resultados_facta.columns else pd.DataFrame()
                                                 
                                                 # Calcular total de valores AF dos aguardando assinatura
                                                 total_af_aguardando = aguardando_assinatura['valor_af'].sum() if not aguardando_assinatura.empty and 'valor_af' in aguardando_assinatura.columns else 0
                                                 
                                                 st.markdown("""
                                                 <div style="text-align: center; padding: 20px; background-color: #f5f5f5; border-radius: 12px; color: #333; min-height: 120px; display: flex; flex-direction: column; justify-content: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border: 2px solid #e0e0e0;">
                                                     <h5 style="margin: 0 0 10px 0; font-size: 14px; opacity: 0.9;">⏳ Aguardando Assinatura</h5>
                                                     <p style="font-size: 24px; font-weight: bold; margin: 0;">R$ {}</p>
                                                     <small style="font-size: 12px; opacity: 0.8; margin-top: 5px;">{} contratos</small>
                                                 </div>
                                                 """.format(f"{total_af_aguardando:,.2f}", f"{len(aguardando_assinatura):,}"), unsafe_allow_html=True)
                                            
                                            # Exibir resultados em tabela
                                            st.markdown("---")
                                            st.markdown("""
                                            <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin: 20px 0;">
                                                <h4 style="color: #2c3e50; margin-bottom: 15px;">📊 Resultados da Consulta FACTA ({})</h4>
                                            </div>
                                            """.format(f"{len(resultados_facta):,} registros"), unsafe_allow_html=True)
                                            
                                            st.dataframe(resultados_facta, use_container_width=True, hide_index=True)
                                            
                                            # Download dos resultados FACTA
                                            if not resultados_facta.empty:
                                                st.markdown("---")
                                                csv_facta = resultados_facta.to_csv(index=False)
                                                st.download_button(
                                                    label="📥 Download CSV - Resultados FACTA",
                                                    data=csv_facta,
                                                    file_name=f"andamento_propostas_facta_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                                    mime="text/csv"
                                                )
                                        else:
                                            st.error("❌ Nenhum resultado encontrado na API FACTA.")
                                            
                                    except Exception as e:
                                        st.error(f"❌ Erro ao consultar API FACTA: {str(e)}")
                        elif not token_facta and cpfs_limpos:
                            st.info("🔑 Insira o token FACTA para consultar os CPFs na API.")
                        elif not cpfs_limpos:
                            st.warning("⚠️ Nenhum CPF válido encontrado para consulta.")
                        
                else:
                    st.warning("⚠️ Coluna 'CPF' não encontrada nos dados filtrados. Não foi possível extrair CPFs únicos ou consultar a API FACTA.")
                    
                    # Download dos dados filtrados
                    if not df_filtered_ad.empty:
                        st.markdown("---")
                        csv_data_ad = df_filtered_ad.to_csv(index=False)
                        st.download_button(
                            label="📥 Download CSV - Clientes Filtrados (Período + UTM Source = 'ad')",
                            data=csv_data_ad,
                            file_name=f"clientes_utm_source_ad_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                
        except Exception as e:
            st.error(f"❌ Erro ao processar arquivo Excel: {str(e)}")
            st.exception(e) # Mostra o traceback completo para depuração
    else:
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 30px; border-radius: 12px; text-align: center; margin: 50px 0;">
            <h3 style="color: #2c3e50; margin-bottom: 15px;">🎯 Filtro de Clientes UTM Source = "ad"</h3>
            <p style="color: #7f8c8d; font-size: 16px; margin-bottom: 20px;">
                Faça upload de um arquivo Excel contendo a coluna "utm source" para filtrar automaticamente apenas os clientes com utm source = "ad".
            </p>
            <div style="display: flex; justify-content: center; gap: 20px; margin-top: 20px; flex-wrap: wrap;">
                <div style="background-color: #e8f5e9; padding: 15px; border-radius: 8px; border-left: 4px solid #4caf50; min-width: 200px;">
                    <h4 style="color: #2c3e50; margin: 0 0 10px 0;">🎯 Filtro Automático</h4>
                    <p style="color: #7f8c8d; margin: 0;">Apenas clientes com utm source = "ad"</p>
                </div>
                <div style="background-color: #e3f2fd; padding: 15px; border-radius: 8px; border-left: 4px solid #2196f3; min-width: 200px;">
                    <h4 style="color: #2c3e50; margin: 0 0 10px 0;">🆔 Extração de CPFs</h4>
                    <p style="color: #7f8c8d; margin: 0;">Lista de CPFs dos clientes filtrados</p>
                </div>
                <div style="background-color: #fff3e0; padding: 15px; border-radius: 8px; border-left: 4px solid #ff9800; min-width: 200px;">
                    <h4 style="color: #2c3e50; margin: 0 0 10px 0;">📥 Download</h4>
                    <p style="color: #7f8c8d; margin: 0;">Exportação em CSV/TXT dos CPFs</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def process_excel_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Processa os dados do Excel para análise, incluindo a conversão e limpeza de datas e normalização de UTMs.
    """
    df_processed = df.copy()
    
    # Processar coluna CPF ANTES de qualquer outra operação para preservar zeros à esquerda
    if 'CPF' in df_processed.columns:
        df_processed['CPF'] = df_processed['CPF'].astype(str).str.strip()
        
        # Adicionar zeros à esquerda para CPFs com menos de 11 dígitos
        def padronizar_cpf(cpf):
            if pd.isna(cpf) or cpf == 'nan' or cpf == '':
                return cpf
            
            # Remover pontos, traços e espaços
            cpf_limpo = str(cpf).replace('.', '').replace('-', '').replace(' ', '')
            
            # Se tem exatamente 11 dígitos, retornar como está
            if len(cpf_limpo) == 11:
                return cpf_limpo
            
            # Se tem menos de 11 dígitos, adicionar zeros à esquerda
            if len(cpf_limpo) < 11:
                return cpf_limpo.zfill(11)
            
            # Se tem mais de 11 dígitos, truncar para 11
            if len(cpf_limpo) > 11:
                return cpf_limpo[:11]
            
            return cpf_limpo
        
        # Aplicar correção a todos os CPFs
        df_processed['CPF'] = df_processed['CPF'].apply(padronizar_cpf)
    
    # Processar coluna de data se existir
    if 'Data Criacao' in df_processed.columns:
        # Tentar converter para datetime, com tratamento de erros
        # 'coerce' transforma valores inválidos em NaT
        df_processed['Data Criacao'] = pd.to_datetime(df_processed['Data Criacao'], errors='coerce')
    
    # Limpar e normalizar dados UTM
    utm_columns = ['utm source', 'utm medium', 'utm campaign']
    for col in utm_columns:
        if col in df_processed.columns:
            # Converter para string, remover espaços e converter para minúsculas
            df_processed[col] = df_processed[col].astype(str).str.strip().str.lower()
            # Substituir valores nulos/vazios por 'n/a' (minúsculo para consistência)
            df_processed[col] = df_processed[col].replace(['nan', 'none', ''], 'n/a')
    
    return df_processed

def handle_cpf_deduplication(df_temp: pd.DataFrame) -> pd.DataFrame:
    """
    Função auxiliar para lidar com a deduplicação de CPFs.
    """
    if 'CPF' not in df_temp.columns:
        return df_temp.copy()
    
    total_antes = len(df_temp)
    
    # Remover CPFs nulos/vazios antes de deduplicar
    df_temp = df_temp.dropna(subset=['CPF'])
    df_temp = df_temp[df_temp['CPF'].astype(str).str.strip() != '']
    
    # Os CPFs já foram padronizados para 11 dígitos na função process_excel_data
    # Agora apenas limpar e verificar se estão corretos
    df_temp['CPF_limpo'] = df_temp['CPF'].astype(str).str.strip()
    
    # Remover duplicatas mantendo a primeira ocorrência
    df_filtered = df_temp.drop_duplicates(subset=['CPF_limpo'], keep='first').copy()
    
    # Remover coluna temporária
    df_filtered = df_filtered.drop('CPF_limpo', axis=1)
    
    return df_filtered

def consultarandamento_propostas_facta(cpfs: list, token: str) -> pd.DataFrame:
    """
    Consulta todas as propostas no período usando o endpoint 'Andamento de propostas'.
    Esta abordagem é mais eficiente pois retorna todas as propostas de uma vez,
    permitindo análise mais abrangente dos dados.
    """
    try:
        import requests
        
        # Configuração da API
        url = "https://webservice.facta.com.br/proposta/andamento-propostas"
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # Calcular período de consulta (últimos 30 dias)
        data_fim = datetime.now()
        data_inicio = data_fim - timedelta(days=30)
        data_ini_str = data_inicio.strftime('%d/%m/%Y')
        data_fim_str = data_fim.strftime('%d/%m/%Y')
        
        # Parâmetros para consulta
        params = {
            'convenio': 3,  # FACTA FINANCEIRA
            'quantidade': 5000,  # Máximo permitido por página
            'pagina': 1,
            'data_ini': data_ini_str,
            'data_fim': data_fim_str
        }
        
        # Consultar todas as páginas
        todas_propostas = []
        pagina_atual = 1
        
        while True:
            try:
                params['pagina'] = pagina_atual
                
                response = requests.get(
                    url, 
                    headers=headers, 
                    params=params, 
                    timeout=60,
                    allow_redirects=False
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if not data.get('erro', False):
                        propostas = data.get('propostas', [])
                        
                        if propostas:
                            # Adicionar informações de rastreamento
                            for proposta in propostas:
                                proposta['pagina_consulta'] = pagina_atual
                                proposta['data_consulta'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                            
                            todas_propostas.extend(propostas)
                            
                            # Verificar se há mais páginas
                            if len(propostas) < params['quantidade']:
                                break
                            else:
                                pagina_atual += 1
                                import time
                                time.sleep(0.5)  # Aguardar para evitar rate limiting
                        else:
                            break  # Nenhuma proposta na página, parar
                    else:
                        break
                        
                elif response.status_code == 401:
                    st.error(f"❌ Erro na página {pagina_atual}: Token inválido ou expirado. Por favor, gere um novo token.")
                    break
                elif response.status_code == 429:
                    import time
                    time.sleep(5)  # Aguardar mais tempo em caso de rate limit
                    continue
                else:
                    st.error(f"❌ Erro HTTP na página {pagina_atual}: {response.status_code} - {response.text}")
                    break
                    
            except requests.exceptions.Timeout:
                import time
                time.sleep(2)  # Pequena pausa antes de tentar novamente
                continue
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Página {pagina_atual}: Erro de requisição: {str(e)}")
                break
            except Exception as e:
                st.error(f"❌ Página {pagina_atual}: Erro inesperado durante a consulta: {str(e)}")
                break
        
        # Processar resultados
        if not todas_propostas:
            return pd.DataFrame()
        
        df_propostas = pd.DataFrame(todas_propostas)
        
        # Limpar CPFs para comparação
        cpfs_limpos_para_filtro = [str(cpf).replace('.', '').replace('-', '').strip() for cpf in cpfs]
        
        # Filtrar propostas que contenham os CPFs consultados
        df_propostas_filtrado = df_propostas[
            df_propostas['cpf'].isin(cpfs_limpos_para_filtro)
        ].copy()
        
        if df_propostas_filtrado.empty:
            return pd.DataFrame()
        
        # Reorganizar colunas para melhor visualização
        colunas_principais = [
            'cpf', 'cliente', 'status_proposta', 'status_crivo',
            'valor_bruto', 'valor_af', 'vlrprestacao', 'numeroprestacao', 'saldo_devedor',
            'data_movimento', 'data_digitacao', 'produto', 'convenio',
            'averbador', 'codigo_af', 'numero_contrato', 'tipo_operacao',
            'taxa', 'valor_iof', 'valor_seguro', 'corretor',
            'pagina_consulta', 'data_consulta'
        ]
        
        # Selecionar apenas colunas que existem no DataFrame
        colunas_disponiveis = [col for col in df_propostas_filtrado.columns if col in colunas_principais]
        outras_colunas = [col for col in df_propostas_filtrado.columns if col not in colunas_principais and col not in colunas_disponiveis]
        colunas_finais = colunas_disponiveis + outras_colunas
        
        # Reorganizar DataFrame
        df_final = df_propostas_filtrado[colunas_finais]
        
        return df_final
            
    except Exception as e:
        st.error(f"❌ Erro geral ao consultar API FACTA: {str(e)}")
        st.exception(e)
        return pd.DataFrame()

if __name__ == "__main__":
    render_excel_filter_ad_page()

