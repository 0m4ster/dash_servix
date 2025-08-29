#!/bin/bash

echo "🚀 Railway Startup Script - Dashboard SMS"
echo "=========================================="

# Log todas as variáveis de ambiente
echo "🔍 Variáveis de ambiente:"
env | sort

echo ""
echo "📡 PORT: $PORT"
echo "📡 STREAMLIT_SERVER_PORT: $STREAMLIT_SERVER_PORT"

# Definir porta padrão se não estiver definida
if [ -z "$PORT" ]; then
    echo "⚠️  PORT não definido, definindo como 8080"
    PORT=8080
fi

# Validar PORT
if ! [[ "$PORT" =~ ^[0-9]+$ ]]; then
    echo "❌ PORT inválido: '$PORT', usando 8080"
    PORT=8080
fi

echo "✅ Porta final: $PORT"

# Verificar arquivos
echo "📁 Verificando arquivos:"
ls -la

echo ""
echo "🚀 Iniciando Streamlit na porta $PORT..."

# Comando direto sem export
exec streamlit run dash_api.py --server.port $PORT --server.address 0.0.0.0
