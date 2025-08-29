#!/bin/bash

# Script de inicialização para Railway
echo "🚀 Iniciando Dashboard SMS..."

# Usar a variável de ambiente PORT fornecida pela plataforma
echo "📡 Usando porta: $PORT"
echo "🌐 Endereço: 0.0.0.0"

# Configurar variáveis de ambiente para o Streamlit
export STREAMLIT_SERVER_PORT=$PORT
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_ENABLE_CORS=false
export STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

echo "🔧 Variáveis configuradas:"
echo "   PORT: $STREAMLIT_SERVER_PORT"
echo "   ADDRESS: $STREAMLIT_SERVER_ADDRESS"

# Iniciar Streamlit com a porta correta
exec streamlit run dash_api.py --server.port $PORT --server.address 0.0.0.0
