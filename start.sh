#!/bin/bash

# Script de inicialização para Railway
echo "🚀 Iniciando Dashboard SMS..."

# Verificar variável PORT
if [ -z "$PORT" ]; then
    echo "⚠️ Variável PORT não definida, usando porta padrão 8501"
    export PORT=8501
fi

echo "📡 Porta configurada: $PORT"
echo "🌐 Endereço: 0.0.0.0"

# Configurar variável de ambiente para o Streamlit
export STREAMLIT_SERVER_PORT=${PORT:-8501}
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_ENABLE_CORS=false
export STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

echo "🔧 Variáveis configuradas:"
echo "   PORT: $STREAMLIT_SERVER_PORT"
echo "   ADDRESS: $STREAMLIT_SERVER_ADDRESS"

# Iniciar Streamlit
exec streamlit run dash_api.py
