#!/bin/bash

#!/bin/bash

# Script de inicialização para Railway
echo "🚀 Iniciando Dashboard SMS..."

# Railway usa porta 8080 por padrão
echo "📡 Usando porta padrão do Railway: 8080"
echo "🌐 Endereço: 0.0.0.0"

# Configurar variáveis de ambiente para o Streamlit
export STREAMLIT_SERVER_PORT=8080
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_ENABLE_CORS=false
export STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

echo "🔧 Variáveis configuradas:"
echo "   PORT: $STREAMLIT_SERVER_PORT"
echo "   ADDRESS: $STREAMLIT_SERVER_ADDRESS"

# Iniciar Streamlit
exec streamlit run dash_api.py
