#!/usr/bin/env python3
"""
Healthcheck endpoint para Railway
Este arquivo é usado pelo Railway para verificar se a aplicação está funcionando
"""

import os
import sys
import requests
from datetime import datetime

def check_health():
    """Verifica se a aplicação está saudável"""
    try:
        # Verificar se estamos rodando
        port = os.environ.get('PORT', '8501')
        base_url = f"http://localhost:{port}"
        
        # Tentar fazer uma requisição para a aplicação
        response = requests.get(f"{base_url}/", timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Healthcheck OK - Status: {response.status_code}")
            return True
        else:
            print(f"⚠️  Healthcheck Warning - Status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Healthcheck Failed - Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Healthcheck Error - {e}")
        return False

if __name__ == "__main__":
    success = check_health()
    sys.exit(0 if success else 1)
