#!/usr/bin/env python3
"""
Script de teste para verificar o tratamento da variável de ambiente PORT
"""

import os
import sys

def test_port_handling():
    """Testa o tratamento da variável de ambiente PORT"""
    
    print("🔍 Testando tratamento da variável PORT...")
    print("=" * 50)
    
    # Verificar variáveis de ambiente
    port_env = os.environ.get('PORT')
    streamlit_port = os.environ.get('STREAMLIT_SERVER_PORT')
    
    print(f"📡 PORT: {port_env}")
    print(f"🔧 STREAMLIT_SERVER_PORT: {streamlit_port}")
    
    # Simular o comando streamlit
    if port_env:
        try:
            port_int = int(port_env)
            print(f"✅ PORT convertido para inteiro: {port_int}")
            print(f"✅ Comando seria: streamlit run dash_api.py --server.port {port_int} --server.address 0.0.0.0")
        except ValueError:
            print(f"❌ ERRO: PORT '{port_env}' não é um número válido!")
            print("💡 Solução: Verifique se a variável PORT está sendo definida corretamente")
            return False
    else:
        print("⚠️  PORT não definido, usando porta padrão 8501")
        print("✅ Comando seria: streamlit run dash_api.py --server.port 8501 --server.address 0.0.0.0")
    
    print("\n" + "=" * 50)
    print("🎯 Teste concluído!")
    
    return True

if __name__ == "__main__":
    success = test_port_handling()
    sys.exit(0 if success else 1)
