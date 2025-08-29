#!/usr/bin/env python3
"""
Script de inicialização do Streamlit para Railway
Trata as variáveis de ambiente de forma mais robusta
"""

import os
import sys
import subprocess
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_port():
    """Obtém a porta da variável de ambiente PORT ou usa padrão"""
    port = os.environ.get('PORT')
    
    if port is None:
        logger.info("PORT não definido, usando porta padrão 8501")
        return 8501
    
    try:
        port_int = int(port)
        logger.info(f"Usando porta: {port_int}")
        return port_int
    except ValueError:
        logger.warning(f"PORT '{port}' não é um número válido, usando porta padrão 8501")
        return 8501

def create_dynamic_config(port):
    """Cria um arquivo de configuração dinâmico para o Streamlit"""
    config_content = f"""[server]
port = {port}
address = "0.0.0.0"
enableCORS = false
enableXsrfProtection = false
headless = true

[browser]
gatherUsageStats = false
"""
    
    # Criar diretório .streamlit se não existir
    os.makedirs('.streamlit', exist_ok=True)
    
    # Escrever configuração
    config_path = '.streamlit/config.toml'
    with open(config_path, 'w') as f:
        f.write(config_content)
    
    logger.info(f"✅ Configuração do Streamlit criada em {config_path}")
    return config_path

def main():
    """Função principal"""
    logger.info("🚀 Iniciando Dashboard SMS...")
    
    # Verificar se estamos em um ambiente Docker
    if os.path.exists('/.dockerenv'):
        logger.info("🐳 Executando em container Docker")
    else:
        logger.info("💻 Executando em ambiente local")
    
    # Verificar variáveis de ambiente
    logger.info("🔍 Variáveis de ambiente disponíveis:")
    for key, value in os.environ.items():
        if 'PORT' in key or 'STREAMLIT' in key:
            logger.info(f"  {key}: {value}")
    
    # Obter porta
    port = get_port()
    
    # Criar configuração dinâmica
    create_dynamic_config(port)
    
    # Verificar se o arquivo dash_api.py existe
    if not os.path.exists('dash_api.py'):
        logger.error("❌ ERRO: dash_api.py não encontrado!")
        logger.info("📁 Arquivos no diretório atual:")
        for file in os.listdir('.'):
            logger.info(f"  {file}")
        sys.exit(1)
    
    # Verificar se o streamlit está instalado
    try:
        import streamlit
        logger.info(f"✅ Streamlit {streamlit.__version__} encontrado")
    except ImportError:
        logger.error("❌ ERRO: streamlit não está instalado!")
        sys.exit(1)
    
    logger.info("✅ Verificações concluídas, iniciando Streamlit...")
    
    # Construir comando para iniciar Streamlit
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', 'dash_api.py',
        '--server.port', str(port),
        '--server.address', '0.0.0.0'
    ]
    
    logger.info(f"🚀 Comando: {' '.join(cmd)}")
    
    # Iniciar Streamlit
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Erro ao executar Streamlit: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("🛑 Streamlit interrompido pelo usuário")
        sys.exit(0)

if __name__ == '__main__':
    main()
