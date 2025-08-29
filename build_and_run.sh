#!/bin/bash

echo "========================================"
echo "    Build e Execucao do Dashboard"
echo "========================================"
echo

echo "1. Parando containers existentes..."
docker stop dash-dashboard 2>/dev/null
docker rm dash-dashboard 2>/dev/null

echo
echo "2. Removendo imagem antiga..."
docker rmi dash-dashboard 2>/dev/null

echo
echo "3. Fazendo build da nova imagem..."
docker build -t dash-dashboard .

if [ $? -ne 0 ]; then
    echo
    echo "ERRO: Falha no build da imagem Docker!"
    exit 1
fi

echo
echo "4. Executando o container..."
docker run -d --name dash-dashboard -p 8501:8501 dash-dashboard

if [ $? -ne 0 ]; then
    echo
    echo "ERRO: Falha ao executar o container!"
    exit 1
fi

echo
echo "========================================"
echo "    Dashboard executando com sucesso!"
echo "========================================"
echo
echo "URL: http://localhost:8501"
echo
echo "Para parar o container: docker stop dash-dashboard"
echo "Para ver logs: docker logs dash-dashboard"
echo
