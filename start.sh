#!/bin/bash

# Script de inicialização para Railway
echo "🚀 Iniciando Dashboard SMS..."

# Verificar se estamos em um ambiente Docker
if [ -f /.dockerenv ]; then
    echo "🐳 Executando em container Docker"
else
    echo "💻 Executando em ambiente local"
fi

# Verificar variáveis de ambiente
echo "🔍 Variáveis de ambiente disponíveis:"
env | grep -E "(PORT|STREAMLIT|RAILWAY)" || echo "⚠️  Nenhuma variável relevante encontrada"

# Usar a variável de ambiente PORT fornecida pela plataforma
if [ -z "$PORT" ]; then
    echo "⚠️  PORT não definido, usando porta padrão 8501"
    export PORT=8501
else
    echo "📡 Usando porta: $PORT"
fi

# Validar se PORT é um número válido
if ! [[ "$PORT" =~ ^[0-9]+$ ]]; then
    echo "❌ ERRO: PORT '$PORT' não é um número válido!"
    echo "💡 Usando porta padrão 8501"
    export PORT=8501
fi

echo "🌐 Endereço: 0.0.0.0"

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

# Criar configuração dinâmica do Streamlit
mkdir -p .streamlit
cat > .streamlit/config.toml << EOF
[server]
port = $PORT
address = "0.0.0.0"
enableCORS = false
enableXsrfProtection = false
headless = true
maxUploadSize = 200

[browser]
gatherUsageStats = false

[logger]
level = "info"
EOF

echo "🔧 Configuração do Streamlit criada com porta $PORT"
echo "📋 Conteúdo do config.toml:"
cat .streamlit/config.toml

# Iniciar Streamlit com a porta correta
echo "🚀 Comando: streamlit run dash_api.py --server.port $PORT --server.address 0.0.0.0"
echo "🌐 URL será: http://0.0.0.0:$PORT"
exec streamlit run dash_api.py --server.port $PORT --server.address 0.0.0.0
