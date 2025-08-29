FROM python:3.10-slim

# Instalar dependências do sistema necessárias e configurar fuso horário
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Configurar fuso horário para Brasil
ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o resto do código
COPY . .

# Configurar Streamlit para Railway
RUN mkdir -p .streamlit
COPY railway-streamlit.toml .streamlit/config.toml

# Tornar o script executável
RUN chmod +x start_streamlit.py

# Usar ENTRYPOINT para garantir que o script seja executado corretamente
ENTRYPOINT ["python", "start_streamlit.py"]