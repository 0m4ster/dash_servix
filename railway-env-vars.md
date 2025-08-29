# Variáveis de Ambiente para Railway

## 🔧 **Variáveis Obrigatórias**

Configure estas variáveis no dashboard do Railway (seção "Variables"):

### **PORT** (Obrigatória)
- **Valor:** `8501`
- **Descrição:** Porta onde a aplicação será executada
- **Obrigatória:** ✅ Sim

### **STREAMLIT_SERVER_PORT** (Obrigatória)
- **Valor:** `8501`
- **Descrição:** Porta do servidor Streamlit
- **Obrigatória:** ✅ Sim

### **STREAMLIT_SERVER_ADDRESS** (Obrigatória)
- **Valor:** `0.0.0.0`
- **Descrição:** Endereço de binding do servidor
- **Obrigatória:** ✅ Sim

## 🌐 **Variáveis Opcionais (se necessário)**

### **STREAMLIT_SERVER_HEADLESS**
- **Valor:** `true`
- **Descrição:** Executar sem interface gráfica
- **Obrigatória:** ❌ Não

### **STREAMLIT_SERVER_ENABLE_CORS**
- **Valor:** `false`
- **Descrição:** Habilitar CORS
- **Obrigatória:** ❌ Não

## 📋 **Como Configurar no Railway:**

1. Acesse o dashboard do Railway
2. Vá para a seção "Variables"
3. Clique em "+ Variable"
4. Adicione cada variável com o nome e valor correspondente
5. Clique em "Save"

## 🚀 **Após Configurar:**

1. Faça commit das alterações no código
2. Push para o repositório
3. O Railway deve fazer deploy automaticamente
4. Verifique os logs para confirmar que está funcionando
5. A URL será gerada automaticamente
