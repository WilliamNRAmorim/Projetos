@echo off
rem Atualiza a pasta GMS com o que foi gravado no GitHub (branch ccr-c1b378db-6ximsp).
rem Coloque este arquivo na raiz da pasta clonada (a que contem a pasta GMS) ou use o atalho abaixo.
cd /d "%~dp0"
if exist ".git" (cd /d "%~dp0") else (cd /d "%~dp0..")
git fetch origin ccr-c1b378db-6ximsp
git checkout ccr-c1b378db-6ximsp
git pull origin ccr-c1b378db-6ximsp
echo.
echo Pronto. Arquivos em: %cd%\GMS\Telas
pause
