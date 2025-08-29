@echo off
echo ========================================
echo    Build e Execucao do Dashboard
echo ========================================
echo.

echo 1. Parando containers existentes...
docker stop dash-dashboard 2>nul
docker rm dash-dashboard 2>nul

echo.
echo 2. Removendo imagem antiga...
docker rmi dash-dashboard 2>nul

echo.
echo 3. Fazendo build da nova imagem...
docker build -t dash-dashboard .

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERRO: Falha no build da imagem Docker!
    pause
    exit /b 1
)

echo.
echo 4. Executando o container...
docker run -d --name dash-dashboard -p 8501:8501 dash-dashboard

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERRO: Falha ao executar o container!
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Dashboard executando com sucesso!
echo ========================================
echo.
echo URL: http://localhost:8501
echo.
echo Para parar o container: docker stop dash-dashboard
echo Para ver logs: docker logs dash-dashboard
echo.
pause
