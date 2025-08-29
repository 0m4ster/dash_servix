# 🔧 Guia de Solução de Problemas

## 🚨 Erro: "Invalid value for '--server.port' (env var: 'STREAMLIT_SERVER_PORT'): '$PORT' is not a valid integer"

### 📋 Descrição do Problema
Este erro ocorre quando a variável de ambiente `$PORT` não está sendo interpretada corretamente pelo shell, resultando no Streamlit recebendo literalmente a string "$PORT" em vez de um número.

### 🔍 Causas Comuns

1. **Variável PORT não definida** - A plataforma de deploy não está definindo a variável
2. **Shell não expandindo a variável** - Problemas na interpretação do shell
3. **Aspas incorretas** - Uso de aspas simples que impedem a expansão
4. **Script de inicialização incorreto** - Problemas no script de startup

### ✅ Soluções Aplicadas

#### 1. **Render.yaml** ✅
```yaml
startCommand: streamlit run dash_api.py --server.port $PORT --server.address 0.0.0.0
```
- ✅ Sem aspas ao redor de $PORT
- ✅ Comando direto no startCommand

#### 2. **Procfile (Heroku)** ✅
```
web: streamlit run dash_api.py --server.port $PORT --server.address 0.0.0.0
```
- ✅ Sem aspas ao redor de $PORT
- ✅ Formato correto para Heroku

#### 3. **start.sh (Railway/Docker)** ✅
```bash
#!/bin/bash
export STREAMLIT_SERVER_PORT=$PORT
exec streamlit run dash_api.py --server.port $PORT --server.address 0.0.0.0
```
- ✅ Exportação da variável antes do comando
- ✅ Uso direto de $PORT no comando

#### 4. **railway.json** ✅
```json
{
  "deploy": {
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```
- ✅ Removido startCommand duplicado
- ✅ Usa o script start.sh

### 🧪 Teste Local

Para testar se a correção está funcionando:

```bash
# Definir variável PORT
export PORT=8080

# Executar o script de teste
python test_port.py

# Ou executar diretamente
streamlit run dash_api.py --server.port $PORT --server.address 0.0.0.0
```

### 🔧 Verificações Adicionais

#### **Verificar se a variável está definida:**
```bash
echo $PORT
env | grep PORT
```

#### **Verificar se o shell está expandindo:**
```bash
# Deve mostrar o valor da variável, não "$PORT"
echo "Porta: $PORT"
```

#### **Testar com valor fixo:**
```bash
# Teste temporário para isolar o problema
streamlit run dash_api.py --server.port 8080 --server.address 0.0.0.0
```

### 🚀 Plataformas Suportadas

| Plataforma | Status | Arquivo de Configuração |
|------------|--------|-------------------------|
| **Render** | ✅ Funcionando | `render.yaml` |
| **Railway** | ✅ Funcionando | `railway.json` + `start.sh` |
| **Heroku** | ✅ Funcionando | `Procfile` |
| **Docker** | ✅ Funcionando | `Dockerfile` + `start.sh` |
| **Local** | ✅ Funcionando | `build_and_run.*` |

### 📝 Logs de Debug

Para debug adicional, adicione logs no script de inicialização:

```bash
#!/bin/bash
echo "🔍 Debug: PORT=$PORT"
echo "🔍 Debug: STREAMLIT_SERVER_PORT=$STREAMLIT_SERVER_PORT"
echo "🔍 Debug: Comando: streamlit run dash_api.py --server.port $PORT --server.address 0.0.0.0"
```

### 🎯 Comandos de Verificação

```bash
# Verificar se o arquivo está sendo executado
ps aux | grep streamlit

# Verificar portas em uso
netstat -tlnp | grep :8080

# Verificar logs do Streamlit
tail -f ~/.streamlit/logs/streamlit.log
```

### 📞 Suporte

Se o problema persistir:

1. **Verifique os logs** da plataforma de deploy
2. **Teste localmente** com `python test_port.py`
3. **Compare configurações** com os arquivos corrigidos
4. **Abra uma issue** no GitHub com os logs de erro

---

**Última atualização:** $(date)
**Status:** ✅ Problema resolvido
**Versão:** 1.0.0
