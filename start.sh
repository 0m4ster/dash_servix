#!/bin/bash

# Script de inicialização para Railway
echo "🚀 Iniciando Dashboard SMS..."
echo "🔍 Debug: Iniciando script start.sh"

# Verificar se estamos em um ambiente Docker
if [ -f /.dockerenv ]; then
    echo "🐳 Executando em container Docker"
else
    echo "💻 Executando em ambiente local"
fi

# Verificar variáveis de ambiente
echo "🔍 Variáveis de ambiente disponíveis:"
env | grep -E "(PORT|STREAMLIT)" || echo "⚠️  Nenhuma variável PORT encontrada"

# Usar a variável de ambiente PORT fornecida pela plataforma
if [ -z "$PORT" ]; then
    echo "⚠️  PORT não definido, usando porta padrão 8501"
    export PORT=8501
else
    echo "📡 Usando porta: $PORT"
fi

# Validar se PORT é um número
if ! [[ "$PORT" =~ ^[0-9]+$ ]]; then
    echo "❌ ERRO: PORT '$PORT' não é um número válido!"
    echo "💡 Usando porta padrão 8501"
    export PORT=8501
fi

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

# Verificar se o arquivo dash_api.py existe
if [ ! -f "dash_api.py" ]; then
    echo "❌ ERRO: dash_api.py não encontrado!"
    echo "📁 Arquivos no diretório atual:"
    ls -la
    exit 1
fi

# Verificar se o streamlit está instalado
if ! command -v streamlit &> /dev/null; then
    echo "❌ ERRO: streamlit não está instalado!"
    echo "📦 Pacotes Python instalados:"
    pip list | grep streamlit || echo "⚠️  Streamlit não encontrado"
    exit 1
fi

echo "✅ Verificações concluídas, iniciando Streamlit..."

# Iniciar Streamlit com a porta correta
echo "🚀 Comando: streamlit run dash_api.py --server.port $PORT --server.address 0.0.0.0"
exec streamlit run dash_api.py --server.port $PORT --server.address 0.0.0.0
