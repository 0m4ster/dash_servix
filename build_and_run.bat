@echo off
echo 🚀 Iniciando Dashboard SMS...

REM Definir porta padrão para desenvolvimento local
set PORT=8501

REM Verificar se a porta foi definida como variável de ambiente
if defined PORT (
    echo 📡 Usando porta: %PORT%
) else (
    echo 📡 Usando porta padrão: %PORT%
)

REM Configurar variáveis de ambiente para o Streamlit
set STREAMLIT_SERVER_PORT=%PORT%
set STREAMLIT_SERVER_ADDRESS=0.0.0.0
set STREAMLIT_SERVER_HEADLESS=true
set STREAMLIT_SERVER_ENABLE_CORS=false
set STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

echo 🔧 Variáveis configuradas:
echo    PORT: %STREAMLIT_SERVER_PORT%
echo    ADDRESS: %STREAMLIT_SERVER_ADDRESS%

REM Iniciar Streamlit com a porta correta
echo 🌐 Iniciando Streamlit...
streamlit run dash_api.py --server.port %PORT% --server.address 0.0.0.0

pause
