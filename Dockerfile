FROM python:3.10-slim

# Instalar dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o resto do código
COPY . .

# Tornar o script executável
RUN chmod +x start.sh

# Criar diretório .streamlit se não existir
RUN mkdir -p .streamlit

# Expor a porta padrão (será sobrescrita pela variável PORT)
EXPOSE 8501

# Usar ENTRYPOINT para garantir que o script seja executado corretamente
ENTRYPOINT ["./start.sh"]