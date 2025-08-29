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

# Iniciar Streamlit
exec streamlit run dash_api.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false
