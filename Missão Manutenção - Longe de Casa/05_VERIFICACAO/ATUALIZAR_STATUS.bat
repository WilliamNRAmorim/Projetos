@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PYEXE=
python --version >nul 2>&1 && set PYEXE=python
if not defined PYEXE (py -3 --version >nul 2>&1 && set PYEXE=py -3)
if not defined PYEXE goto sempython
%PYEXE% -c "import openpyxl, PIL" >nul 2>&1 || goto semlib
%PYEXE% -X utf8 atualizar_status.py
goto fim
:sempython
echo.
echo Python nao foi encontrado neste computador.
echo Instale o Python 3 (python.org) e rode de novo.
echo O arquivo IDENTIFICADOR.html funciona sem Python: abra com dois cliques.
goto fim
:semlib
echo.
echo Faltam bibliotecas do Python. Rode uma vez, no Prompt de Comando:
echo     %PYEXE% -m pip install openpyxl pillow pymupdf
echo e depois dois cliques aqui de novo.
:fim
echo.
pause
